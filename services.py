"""
服务层 - 业务逻辑处理
封装所有业务操作，实现数据访问与界面展示的分离
"""
import sqlite3
import random
import string
from datetime import datetime
from typing import List, Optional, Tuple
from database import get_connection
from models import (User, Customer, Admin, DeliveryStaff, Restaurant,
                    Dish, Order, OrderItem, CartItem, Review)


class UserService:
    """用户服务类 - 处理用户相关的业务逻辑"""

    @staticmethod
    def register(username: str, password: str, phone: str = "", address: str = "") -> Tuple[bool, str]:
        """
        用户注册
        返回: (成功与否, 消息)
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # 检查用户名是否已存在
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                conn.close()
                return False, "用户名已存在"

            # 验证用户名长度
            if len(username) < 3 or len(username) > 20:
                return False, "用户名长度需在3-20个字符之间"

            # 验证密码长度
            if len(password) < 6:
                return False, "密码长度不能少于6位"

            # 插入新用户
            cursor.execute(
                "INSERT INTO users (username, password, phone, address, role) VALUES (?, ?, ?, ?, 'customer')",
                (username, password, phone, address)
            )
            conn.commit()
            conn.close()
            return True, "注册成功"

        except sqlite3.IntegrityError:
            return False, "用户名已存在"
        except Exception as e:
            return False, f"注册失败: {str(e)}"

    @staticmethod
    def login(username: str, password: str) -> Optional[User]:
        """
        用户登录
        返回: User对象或None
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = ? AND password = ? AND is_active = 1",
                (username, password)
            )
            row = cursor.fetchone()
            conn.close()

            if row:
                user_data = dict(row)
                user_data['user_id'] = user_data.pop('id')
                user_data.pop('avatar', None)
                role = user_data['role']
                if role == 'customer':
                    return Customer(**user_data)
                elif role == 'admin':
                    return Admin(**user_data)
                elif role == 'delivery':
                    return DeliveryStaff(**user_data)
            return None
        except Exception as e:
            print(f"登录错误: {e}")
            return None

    @staticmethod
    def update_profile(user_id: int, phone: str = None, address: str = None) -> bool:
        """更新用户资料"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            if phone:
                cursor.execute("UPDATE users SET phone = ? WHERE id = ?", (phone, user_id))
            if address:
                cursor.execute("UPDATE users SET address = ? WHERE id = ?", (address, user_id))
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

    @staticmethod
    def get_all_users() -> List[dict]:
        """获取所有用户（管理员用）"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role, phone, address, balance, created_at FROM users WHERE role != 'admin'")
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return users


class RestaurantService:
    """餐厅服务类"""

    @staticmethod
    def get_all_restaurants(category: str = None, keyword: str = None) -> List[Restaurant]:
        """获取所有餐厅，支持分类筛选和关键词搜索"""
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM restaurants WHERE is_open = 1"
        params = []

        if category and category != "全部":
            query += " AND category = ?"
            params.append(category)

        if keyword:
            query += " AND (name LIKE ? OR description LIKE ?)"
            params.extend([f"%{keyword}%", f"%{keyword}%"])

        query += " ORDER BY rating DESC, monthly_sales DESC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        restaurants = []
        for row in rows:
            r = dict(row)
            restaurant = Restaurant(
                restaurant_id=r['id'], name=r['name'], category=r['category'],
                address=r['address'], phone=r['phone'], rating=r['rating'],
                monthly_sales=r['monthly_sales'], delivery_fee=r['delivery_fee'],
                min_order=r['min_order'], description=r['description'],
                is_open=bool(r['is_open'])
            )
            restaurants.append(restaurant)
        return restaurants

    @staticmethod
    def get_restaurant_by_id(restaurant_id: int) -> Optional[Restaurant]:
        """根据ID获取餐厅"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM restaurants WHERE id = ?", (restaurant_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            r = dict(row)
            return Restaurant(
                restaurant_id=r['id'], name=r['name'], category=r['category'],
                address=r['address'], phone=r['phone'], rating=r['rating'],
                monthly_sales=r['monthly_sales'], delivery_fee=r['delivery_fee'],
                min_order=r['min_order'], description=r['description'],
                is_open=bool(r['is_open'])
            )
        return None

    @staticmethod
    def get_categories() -> List[str]:
        """获取所有餐厅分类"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM restaurants WHERE is_open = 1 ORDER BY category")
        categories = [row['category'] for row in cursor.fetchall()]
        conn.close()
        return ["全部"] + categories


class DishService:
    """菜品服务类"""

    @staticmethod
    def get_dishes_by_restaurant(restaurant_id: int) -> List[Dish]:
        """获取餐厅的所有菜品"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM dishes WHERE restaurant_id = ? AND is_available = 1 ORDER BY sales_count DESC",
            (restaurant_id,)
        )
        rows = cursor.fetchall()
        conn.close()

        dishes = []
        for row in rows:
            d = dict(row)
            dish = Dish(
                dish_id=d['id'], restaurant_id=d['restaurant_id'],
                name=d['name'], category=d['category'], price=d['price'],
                original_price=d['original_price'], description=d['description'],
                sales_count=d['sales_count'], rating=d['rating'],
                is_available=bool(d['is_available'])
            )
            dishes.append(dish)
        return dishes

    @staticmethod
    def get_hot_dishes(limit: int = 10) -> List[dict]:
        """获取热门菜品"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT d.*, r.name as restaurant_name
            FROM dishes d
            JOIN restaurants r ON d.restaurant_id = r.id
            WHERE d.is_available = 1
            ORDER BY d.sales_count DESC
            LIMIT ?
        ''', (limit,))
        dishes = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return dishes

    @staticmethod
    def search_dishes(keyword: str) -> List[dict]:
        """搜索菜品"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT d.*, r.name as restaurant_name
            FROM dishes d
            JOIN restaurants r ON d.restaurant_id = r.id
            WHERE d.is_available = 1 AND (d.name LIKE ? OR d.description LIKE ?)
            ORDER BY d.sales_count DESC
        ''', (f"%{keyword}%", f"%{keyword}%"))
        dishes = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return dishes


class CartService:
    """购物车服务类"""

    @staticmethod
    def add_to_cart(user_id: int, dish_id: int, restaurant_id: int, quantity: int = 1) -> bool:
        """添加到购物车"""
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # 检查购物车中是否已有该菜品
            cursor.execute(
                "SELECT id, quantity FROM cart WHERE user_id = ? AND dish_id = ?",
                (user_id, dish_id)
            )
            existing = cursor.fetchone()

            if existing:
                new_qty = existing['quantity'] + quantity
                cursor.execute("UPDATE cart SET quantity = ? WHERE id = ?", (new_qty, existing['id']))
            else:
                cursor.execute(
                    "INSERT INTO cart (user_id, dish_id, restaurant_id, quantity) VALUES (?, ?, ?, ?)",
                    (user_id, dish_id, restaurant_id, quantity)
                )

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"添加购物车失败: {e}")
            return False

    @staticmethod
    def get_cart_items(user_id: int) -> List[dict]:
        """获取购物车内容"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.id, c.quantity, c.restaurant_id,
                   d.id as dish_id, d.name as dish_name, d.price, d.image,
                   r.name as restaurant_name
            FROM cart c
            JOIN dishes d ON c.dish_id = d.id
            JOIN restaurants r ON c.restaurant_id = r.id
            WHERE c.user_id = ?
            ORDER BY c.restaurant_id, c.created_at
        ''', (user_id,))
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def update_quantity(cart_id: int, quantity: int) -> bool:
        """更新购物车数量"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            if quantity <= 0:
                cursor.execute("DELETE FROM cart WHERE id = ?", (cart_id,))
            else:
                cursor.execute("UPDATE cart SET quantity = ? WHERE id = ?", (quantity, cart_id))
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

    @staticmethod
    def clear_cart(user_id: int) -> bool:
        """清空购物车"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

    @staticmethod
    def get_cart_total(user_id: int) -> float:
        """获取购物车总价"""
        items = CartService.get_cart_items(user_id)
        return sum(item['price'] * item['quantity'] for item in items)


class OrderService:
    """订单服务类"""

    @staticmethod
    def create_order(user_id: int, address: str, phone: str, remark: str = "") -> Tuple[bool, str]:
        """
        从购物车创建订单
        使用多线程模拟异步处理
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # 获取购物车内容
            cart_items = CartService.get_cart_items(user_id)
            if not cart_items:
                conn.close()
                return False, "购物车为空"

            # 按餐厅分组
            restaurant_items = {}
            for item in cart_items:
                rid = item['restaurant_id']
                if rid not in restaurant_items:
                    restaurant_items[rid] = []
                restaurant_items[rid].append(item)

            # 为每个餐厅创建订单
            order_ids = []
            for restaurant_id, items in restaurant_items.items():
                # 生成订单号
                order_no = 'ORD' + datetime.now().strftime('%Y%m%d%H%M%S') + \
                           ''.join(random.choices(string.digits, k=6))

                # 计算总价
                total_price = sum(item['price'] * item['quantity'] for item in items)

                # 获取配送费
                cursor.execute("SELECT delivery_fee FROM restaurants WHERE id = ?", (restaurant_id,))
                delivery_fee = cursor.fetchone()['delivery_fee']

                # 创建订单
                cursor.execute('''
                    INSERT INTO orders (order_no, user_id, restaurant_id, total_price,
                                       delivery_fee, status, address, phone, remark)
                    VALUES (?, ?, ?, ?, ?, 'pending', ?, ?, ?)
                ''', (order_no, user_id, restaurant_id, total_price, delivery_fee,
                      address, phone, remark))

                order_id = cursor.lastrowid
                order_ids.append(order_id)

                # 创建订单项
                for item in items:
                    cursor.execute('''
                        INSERT INTO order_items (order_id, dish_id, dish_name, quantity, price)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (order_id, item['dish_id'], item['dish_name'],
                          item['quantity'], item['price']))

                    # 更新菜品销量
                    cursor.execute(
                        "UPDATE dishes SET sales_count = sales_count + ? WHERE id = ?",
                        (item['quantity'], item['dish_id'])
                    )

                # 更新餐厅月销量
                cursor.execute(
                    "UPDATE restaurants SET monthly_sales = monthly_sales + 1 WHERE id = ?",
                    (restaurant_id,)
                )

            # 清空购物车
            cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))

            conn.commit()
            conn.close()
            return True, f"下单成功！共{len(order_ids)}个订单"

        except Exception as e:
            conn.rollback()
            conn.close()
            return False, f"下单失败: {str(e)}"

    @staticmethod
    def get_user_orders(user_id: int, status: str = None) -> List[dict]:
        """获取用户订单"""
        conn = get_connection()
        cursor = conn.cursor()

        query = '''
            SELECT o.*, r.name as restaurant_name
            FROM orders o
            JOIN restaurants r ON o.restaurant_id = r.id
            WHERE o.user_id = ?
        '''
        params = [user_id]

        if status and status != "全部":
            query += " AND o.status = ?"
            params.append(status)

        query += " ORDER BY o.created_at DESC"
        cursor.execute(query, params)
        orders = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return orders

    @staticmethod
    def get_order_items(order_id: int) -> List[dict]:
        """获取订单详情"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @staticmethod
    def update_order_status(order_id: int, status: str) -> bool:
        """更新订单状态"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (status, order_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

    @staticmethod
    def get_all_orders(status: str = None) -> List[dict]:
        """获取所有订单（管理员用）"""
        conn = get_connection()
        cursor = conn.cursor()

        query = '''
            SELECT o.*, r.name as restaurant_name, u.username
            FROM orders o
            JOIN restaurants r ON o.restaurant_id = r.id
            JOIN users u ON o.user_id = u.id
        '''
        params = []

        if status and status != "全部":
            query += " WHERE o.status = ?"
            params.append(status)

        query += " ORDER BY o.created_at DESC"
        cursor.execute(query, params)
        orders = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return orders

    @staticmethod
    def cancel_order(order_id: int, user_id: int) -> Tuple[bool, str]:
        """取消订单"""
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT status FROM orders WHERE id = ? AND user_id = ?",
                (order_id, user_id)
            )
            order = cursor.fetchone()

            if not order:
                conn.close()
                return False, "订单不存在"

            if order['status'] not in ('pending', 'confirmed'):
                conn.close()
                return False, "当前状态无法取消订单"

            cursor.execute(
                "UPDATE orders SET status = 'cancelled', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (order_id,)
            )
            conn.commit()
            conn.close()
            return True, "订单已取消"
        except Exception as e:
            return False, f"取消失败: {str(e)}"


class ReviewService:
    """评价服务类"""

    @staticmethod
    def add_review(order_id: int, user_id: int, restaurant_id: int,
                   rating: int, content: str) -> bool:
        """添加评价"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO reviews (order_id, user_id, restaurant_id, rating, content)
                VALUES (?, ?, ?, ?, ?)
            ''', (order_id, user_id, restaurant_id, rating, content))

            # 更新餐厅评分
            cursor.execute('''
                UPDATE restaurants SET rating = (
                    SELECT ROUND(AVG(rating), 1) FROM reviews WHERE restaurant_id = ?
                ) WHERE id = ?
            ''', (restaurant_id, restaurant_id))

            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

    @staticmethod
    def get_restaurant_reviews(restaurant_id: int) -> List[dict]:
        """获取餐厅评价"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.*, u.username
            FROM reviews r
            JOIN users u ON r.user_id = u.id
            WHERE r.restaurant_id = ?
            ORDER BY r.created_at DESC
        ''', (restaurant_id,))
        reviews = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return reviews


class StatsService:
    """统计服务类 - 用于生成报表和可视化数据"""

    @staticmethod
    def get_order_stats() -> dict:
        """获取订单统计"""
        conn = get_connection()
        cursor = conn.cursor()

        stats = {}

        # 各状态订单数量
        cursor.execute('''
            SELECT status, COUNT(*) as count
            FROM orders
            GROUP BY status
        ''')
        stats['status_counts'] = {row['status']: row['count'] for row in cursor.fetchall()}

        # 总订单数和总金额
        cursor.execute('''
            SELECT COUNT(*) as total_orders, 
                   COALESCE(SUM(total_price), 0) as total_amount,
                   COALESCE(AVG(total_price), 0) as avg_amount
            FROM orders
            WHERE status != 'cancelled'
        ''')
        row = cursor.fetchone()
        stats['total_orders'] = row['total_orders']
        stats['total_amount'] = round(row['total_amount'], 2)
        stats['avg_amount'] = round(row['avg_amount'], 2)

        conn.close()
        return stats

    @staticmethod
    def get_restaurant_stats() -> List[dict]:
        """获取餐厅销售统计"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.name, r.monthly_sales, r.rating, r.category,
                   COUNT(o.id) as order_count,
                   COALESCE(SUM(o.total_price), 0) as total_revenue
            FROM restaurants r
            LEFT JOIN orders o ON r.id = o.restaurant_id AND o.status != 'cancelled'
            GROUP BY r.id
            ORDER BY total_revenue DESC
        ''')
        stats = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return stats

    @staticmethod
    def get_popular_dishes(limit: int = 10) -> List[dict]:
        """获取热门菜品统计"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT d.name, d.sales_count, d.price, r.name as restaurant_name
            FROM dishes d
            JOIN restaurants r ON d.restaurant_id = r.id
            ORDER BY d.sales_count DESC
            LIMIT ?
        ''', (limit,))
        dishes = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return dishes

    @staticmethod
    def get_user_stats() -> dict:
        """获取用户统计"""
        conn = get_connection()
        cursor = conn.cursor()

        stats = {}
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE role = 'customer'")
        stats['total_customers'] = cursor.fetchone()['count']

        cursor.execute('''
            SELECT u.username, COUNT(o.id) as order_count,
                   COALESCE(SUM(o.total_price), 0) as total_spent
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id AND o.status != 'cancelled'
            WHERE u.role = 'customer'
            GROUP BY u.id
            ORDER BY total_spent DESC
        ''')
        stats['user_ranking'] = [dict(row) for row in cursor.fetchall()]

        conn.close()
        return stats
