"""
模型模块 - 面向对象的核心数据模型
定义系统中所有实体的类，体现面向对象编程思想
"""
from datetime import datetime
from typing import List, Optional


class User:
    """用户基类"""

    def __init__(self, user_id: int = 0, username: str = "", password: str = "",
                 role: str = "customer", phone: str = "", address: str = "",
                 balance: float = 0.0, created_at: str = "", is_active: bool = True):
        self._id = user_id
        self._username = username
        self._password = password
        self._role = role
        self._phone = phone
        self._address = address
        self._balance = balance
        self._created_at = created_at
        self._is_active = is_active

    @property
    def id(self) -> int:
        return self._id

    @property
    def username(self) -> str:
        return self._username

    @property
    def role(self) -> str:
        return self._role

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str):
        self._phone = value

    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, value: str):
        self._address = value

    @property
    def balance(self) -> float:
        return self._balance

    def check_password(self, password: str) -> bool:
        """验证密码"""
        return self._password == password

    def deduct_balance(self, amount: float) -> bool:
        """扣减余额"""
        if self._balance >= amount:
            self._balance -= amount
            return True
        return False

    def __str__(self) -> str:
        return f"User(id={self._id}, username='{self._username}', role='{self._role}')"


class Customer(User):
    """顾客类 - 继承自User"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._order_history: List[int] = []
        self._cart: dict = {}

    def add_to_cart(self, dish_id: int, restaurant_id: int, quantity: int = 1):
        """添加菜品到购物车"""
        key = (dish_id, restaurant_id)
        if key in self._cart:
            self._cart[key] += quantity
        else:
            self._cart[key] = quantity

    def remove_from_cart(self, dish_id: int, restaurant_id: int):
        """从购物车移除菜品"""
        key = (dish_id, restaurant_id)
        if key in self._cart:
            del self._cart[key]

    def get_cart_items(self) -> dict:
        """获取购物车内容"""
        return self._cart.copy()

    def clear_cart(self):
        """清空购物车"""
        self._cart.clear()

    def __str__(self) -> str:
        return f"Customer(id={self._id}, name='{self._username}', orders={len(self._order_history)})"


class Admin(User):
    """管理员类 - 继承自User"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._permissions = ['manage_users', 'manage_restaurants', 'manage_orders', 'view_stats']

    def has_permission(self, permission: str) -> bool:
        """检查权限"""
        return permission in self._permissions

    def __str__(self) -> str:
        return f"Admin(id={self._id}, name='{self._username}')"


class DeliveryStaff(User):
    """配送员类 - 继承自User"""

    def __init__(self, staff_id: int = 0, **kwargs):
        super().__init__(**kwargs)
        self._staff_id = staff_id
        self._status = "available"
        self._current_orders: List[int] = []
        self._total_deliveries = 0
        self._rating = 5.0

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        self._status = value

    def accept_order(self, order_id: int):
        """接受配送订单"""
        self._current_orders.append(order_id)
        self._status = "busy"

    def complete_delivery(self, order_id: int):
        """完成配送"""
        if order_id in self._current_orders:
            self._current_orders.remove(order_id)
            self._total_deliveries += 1
        if not self._current_orders:
            self._status = "available"

    def __str__(self) -> str:
        return f"DeliveryStaff(id={self._staff_id}, status='{self._status}', deliveries={self._total_deliveries})"


class Restaurant:
    """餐厅类"""

    def __init__(self, restaurant_id: int = 0, name: str = "", category: str = "",
                 address: str = "", phone: str = "", rating: float = 5.0,
                 monthly_sales: int = 0, delivery_fee: float = 3.0,
                 min_order: float = 15.0, description: str = "",
                 is_open: bool = True):
        self._id = restaurant_id
        self._name = name
        self._category = category
        self._address = address
        self._phone = phone
        self._rating = rating
        self._monthly_sales = monthly_sales
        self._delivery_fee = delivery_fee
        self._min_order = min_order
        self._description = description
        self._is_open = is_open
        self._menu: List['Dish'] = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def category(self) -> str:
        return self._category

    @property
    def rating(self) -> float:
        return self._rating

    @property
    def delivery_fee(self) -> float:
        return self._delivery_fee

    @property
    def min_order(self) -> float:
        return self._min_order

    @property
    def monthly_sales(self) -> int:
        return self._monthly_sales

    @property
    def description(self) -> str:
        return self._description

    @property
    def is_open(self) -> bool:
        return self._is_open

    def add_dish(self, dish: 'Dish'):
        """添加菜品到菜单"""
        self._menu.append(dish)

    def get_menu(self) -> List['Dish']:
        """获取菜单"""
        return self._menu.copy()

    def __str__(self) -> str:
        return f"Restaurant(id={self._id}, name='{self._name}', rating={self._rating})"


class Dish:
    """菜品类"""

    def __init__(self, dish_id: int = 0, restaurant_id: int = 0, name: str = "",
                 category: str = "", price: float = 0.0, original_price: float = None,
                 description: str = "", sales_count: int = 0, rating: float = 5.0,
                 is_available: bool = True):
        self._id = dish_id
        self._restaurant_id = restaurant_id
        self._name = name
        self._category = category
        self._price = price
        self._original_price = original_price
        self._description = description
        self._sales_count = sales_count
        self._rating = rating
        self._is_available = is_available

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def category(self) -> str:
        return self._category

    @property
    def price(self) -> float:
        return self._price

    @property
    def original_price(self) -> Optional[float]:
        return self._original_price

    @property
    def description(self) -> str:
        return self._description

    @property
    def sales_count(self) -> int:
        return self._sales_count

    @property
    def rating(self) -> float:
        return self._rating

    @property
    def is_available(self) -> bool:
        return self._is_available

    def has_discount(self) -> bool:
        """是否有折扣"""
        return self._original_price is not None and self._original_price > self._price

    def get_discount_rate(self) -> float:
        """获取折扣率"""
        if self.has_discount():
            return round(self._price / self._original_price * 10, 1)
        return 10.0

    def __str__(self) -> str:
        return f"Dish(id={self._id}, name='{self._name}', price={self._price})"


class Order:
    """订单类"""

    STATUS_MAP = {
        'pending': '待确认',
        'confirmed': '已确认',
        'preparing': '准备中',
        'delivering': '配送中',
        'completed': '已完成',
        'cancelled': '已取消'
    }

    def __init__(self, order_id: int = 0, order_no: str = "", user_id: int = 0,
                 restaurant_id: int = 0, total_price: float = 0.0,
                 delivery_fee: float = 3.0, status: str = "pending",
                 address: str = "", phone: str = "", remark: str = "",
                 created_at: str = ""):
        self._id = order_id
        self._order_no = order_no
        self._user_id = user_id
        self._restaurant_id = restaurant_id
        self._total_price = total_price
        self._delivery_fee = delivery_fee
        self._status = status
        self._address = address
        self._phone = phone
        self._remark = remark
        self._created_at = created_at
        self._items: List['OrderItem'] = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def order_no(self) -> str:
        return self._order_no

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        self._status = value

    @property
    def total_price(self) -> float:
        return self._total_price

    def add_item(self, item: 'OrderItem'):
        """添加订单项"""
        self._items.append(item)

    def get_items(self) -> List['OrderItem']:
        """获取订单项"""
        return self._items.copy()

    def get_status_text(self) -> str:
        """获取状态中文文本"""
        return self.STATUS_MAP.get(self._status, '未知')

    def get_total_with_delivery(self) -> float:
        """获取含配送费的总价"""
        return self._total_price + self._delivery_fee

    def __str__(self) -> str:
        return f"Order(no='{self._order_no}', status='{self.get_status_text()}', total={self._total_price})"


class OrderItem:
    """订单项类"""

    def __init__(self, item_id: int = 0, order_id: int = 0, dish_id: int = 0,
                 dish_name: str = "", quantity: int = 1, price: float = 0.0):
        self._id = item_id
        self._order_id = order_id
        self._dish_id = dish_id
        self._dish_name = dish_name
        self._quantity = quantity
        self._price = price

    @property
    def dish_name(self) -> str:
        return self._dish_name

    @property
    def quantity(self) -> int:
        return self._quantity

    @property
    def price(self) -> float:
        return self._price

    def get_subtotal(self) -> float:
        """获取小计"""
        return self._price * self._quantity

    def __str__(self) -> str:
        return f"OrderItem(name='{self._dish_name}', qty={self._quantity}, subtotal={self.get_subtotal()})"


class CartItem:
    """购物车项类"""

    def __init__(self, dish: Dish, restaurant: Restaurant, quantity: int = 1):
        self._dish = dish
        self._restaurant = restaurant
        self._quantity = quantity

    @property
    def dish(self) -> Dish:
        return self._dish

    @property
    def restaurant(self) -> Restaurant:
        return self._restaurant

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        self._quantity = value

    def get_subtotal(self) -> float:
        """获取小计"""
        return self._dish.price * self._quantity

    def __str__(self) -> str:
        return f"CartItem(dish='{self._dish.name}', qty={self._quantity}, subtotal={self.get_subtotal()})"


class Review:
    """评价类"""

    def __init__(self, review_id: int = 0, order_id: int = 0, user_id: int = 0,
                 restaurant_id: int = 0, rating: int = 5, content: str = "",
                 created_at: str = ""):
        self._id = review_id
        self._order_id = order_id
        self._user_id = user_id
        self._restaurant_id = restaurant_id
        self._rating = rating
        self._content = content
        self._created_at = created_at

    @property
    def rating(self) -> int:
        return self._rating

    @property
    def content(self) -> str:
        return self._content

    def get_stars(self) -> str:
        """获取星级显示"""
        return "★" * self._rating + "☆" * (5 - self._rating)

    def __str__(self) -> str:
        return f"Review(rating={self._rating}, content='{self._content[:20]}...')"
