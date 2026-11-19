"""
数据库模块 - 外卖系统数据库管理
负责数据库连接、表创建、数据增删改查操作
"""
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "food_delivery.db")


def get_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """初始化数据库，创建所有表"""
    conn = get_connection()
    cursor = conn.cursor()

    # 用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'customer' CHECK(role IN ('customer', 'admin', 'delivery')),
            phone TEXT,
            address TEXT,
            avatar TEXT DEFAULT 'default.png',
            balance REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1
        )
    ''')

    # 商家/餐厅表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            address TEXT,
            phone TEXT,
            rating REAL DEFAULT 5.0,
            monthly_sales INTEGER DEFAULT 0,
            delivery_fee REAL DEFAULT 3.0,
            min_order REAL DEFAULT 15.0,
            image TEXT DEFAULT 'default_rest.png',
            description TEXT,
            is_open INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 菜品表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL,
            original_price REAL,
            description TEXT,
            image TEXT DEFAULT 'default_dish.png',
            sales_count INTEGER DEFAULT 0,
            rating REAL DEFAULT 5.0,
            is_available INTEGER DEFAULT 1,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
        )
    ''')

    # 订单表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_no TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            restaurant_id INTEGER NOT NULL,
            total_price REAL NOT NULL,
            delivery_fee REAL DEFAULT 3.0,
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'confirmed', 'preparing', 'delivering', 'completed', 'cancelled')),
            address TEXT NOT NULL,
            phone TEXT,
            remark TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            delivery_time TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
        )
    ''')

    # 订单详情表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            dish_id INTEGER NOT NULL,
            dish_name TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (dish_id) REFERENCES dishes(id)
        )
    ''')

    # 购物车表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            dish_id INTEGER NOT NULL,
            restaurant_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (dish_id) REFERENCES dishes(id),
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
        )
    ''')

    # 评价表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            restaurant_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
        )
    ''')

    # 配送员表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS delivery_staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            phone TEXT,
            status TEXT DEFAULT 'available' CHECK(status IN ('available', 'busy', 'offline')),
            current_orders INTEGER DEFAULT 0,
            total_deliveries INTEGER DEFAULT 0,
            rating REAL DEFAULT 5.0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ 数据库初始化完成")


def insert_sample_data():
    """插入示例数据"""
    conn = get_connection()
    cursor = conn.cursor()

    # 检查是否已有数据
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    # 插入管理员
    cursor.execute(
        "INSERT INTO users (username, password, role, phone, address) VALUES (?, ?, ?, ?, ?)",
        ("admin", "admin123", "admin", "13800000000", "系统管理")
    )

    # 插入示例用户
    users = [
        ("zhangsan", "123456", "customer", "13811111111", "北京市海淀区中关村大街1号"),
        ("lisi", "123456", "customer", "13822222222", "北京市朝阳区望京SOHO T1"),
        ("wangwu", "123456", "customer", "13833333333", "北京市西城区西单北大街"),
        ("delivery1", "123456", "delivery", "13844444444", "配送区域A"),
        ("delivery2", "123456", "delivery", "13855555555", "配送区域B"),
    ]
    cursor.executemany(
        "INSERT INTO users (username, password, role, phone, address) VALUES (?, ?, ?, ?, ?)",
        users
    )

    # 插入配送员
    delivery_staff = [
        (5, "张飞", "13844444444"),
        (6, "李逵", "13855555555"),
    ]
    cursor.executemany(
        "INSERT INTO delivery_staff (user_id, name, phone) VALUES (?, ?, ?)",
        delivery_staff
    )

    # 插入餐厅
    restaurants = [
        ("川味坊", "中餐", "北京市海淀区知春路100号", "010-82001001", 4.8, 1580, 3.0, 15.0, "正宗川菜，麻辣鲜香"),
        ("寿司の屋", "日料", "北京市朝阳区建国路88号", "010-82001002", 4.9, 980, 5.0, 20.0, "新鲜刺身，匠心手握"),
        ("披萨工厂", "西餐", "北京市西城区金融街甲1号", "010-82001003", 4.6, 2100, 4.0, 25.0, "意式手工披萨，现烤现送"),
        ("黄焖鸡米饭", "快餐", "北京市丰台区南四环西路", "010-82001004", 4.5, 3200, 2.0, 10.0, "黄焖鸡，米饭管够"),
        ("星巴克", "饮品", "北京市东城区东单北大街", "010-82001005", 4.7, 4500, 6.0, 30.0, "咖啡与轻食"),
        ("麦当劳", "快餐", "北京市通州区万达广场", "010-82001006", 4.4, 5600, 3.0, 12.0, "全球连锁快餐"),
        ("海底捞火锅", "火锅", "北京市昌平区回龙观", "010-82001007", 4.9, 1200, 8.0, 50.0, "服务至上，火锅首选"),
        ("沙县小吃", "快餐", "北京市大兴区黄村", "010-82001008", 4.2, 6800, 2.0, 8.0, "经济实惠，品种丰富"),
    ]
    cursor.executemany(
        "INSERT INTO restaurants (name, category, address, phone, rating, monthly_sales, delivery_fee, min_order, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        restaurants
    )

    # 插入菜品
    dishes = [
        # 川味坊
        (1, "麻婆豆腐", "热菜", 28.0, 32.0, "麻辣鲜香，下饭神器", 856),
        (1, "宫保鸡丁", "热菜", 32.0, 38.0, "花生酥脆，鸡丁嫩滑", 723),
        (1, "水煮鱼", "热菜", 58.0, 68.0, "鲜嫩鱼片，麻辣汤底", 534),
        (1, "回锅肉", "热菜", 35.0, None, "肥而不腻，蒜苗飘香", 612),
        (1, "担担面", "主食", 18.0, None, "麻辣鲜香，面条劲道", 445),
        # 寿司の屋
        (2, "三文鱼刺身", "刺身", 68.0, 78.0, "挪威进口三文鱼", 321),
        (2, "鳗鱼饭", "饭类", 52.0, None, "蒲烧鳗鱼，酱汁浓郁", 287),
        (2, "加州卷", "寿司", 38.0, None, "经典口味，新鲜食材", 456),
        (2, "味噌汤", "汤类", 15.0, None, "传统日式味噌", 234),
        # 披萨工厂
        (3, "玛格丽特披萨", "披萨", 48.0, 58.0, "番茄罗勒，经典口味", 567),
        (3, "夏威夷披萨", "披萨", 52.0, None, "菠萝火腿，酸甜可口", 432),
        (3, "意面肉酱面", "意面", 38.0, None, "意式肉酱，手工面条", 345),
        (3, "凯撒沙拉", "沙拉", 28.0, None, "新鲜蔬菜，经典酱汁", 234),
        # 黄焖鸡米饭
        (4, "黄焖鸡米饭(大)", "套餐", 22.0, 25.0, "大份黄焖鸡+米饭", 1234),
        (4, "黄焖鸡米饭(小)", "套餐", 16.0, None, "小份黄焖鸡+米饭", 987),
        (4, "黄焖排骨米饭", "套餐", 26.0, 30.0, "排骨黄焖+米饭", 654),
        (4, "加卤蛋", "加料", 2.0, None, "卤蛋一个", 876),
        # 星巴克
        (5, "拿铁", "咖啡", 32.0, None, "经典拿铁，中杯", 2345),
        (5, "美式咖啡", "咖啡", 28.0, None, "纯正美式，提神醒脑", 1876),
        (5, "焦糖玛奇朵", "咖啡", 36.0, None, "焦糖甜蜜，奶泡绵密", 1567),
        (5, "蓝莓麦芬", "甜点", 22.0, None, "蓝莓果粒，松软可口", 987),
        # 麦当劳
        (6, "巨无霸", "汉堡", 24.0, None, "双层牛肉，经典口味", 3456),
        (6, "麦辣鸡腿堡", "汉堡", 20.0, None, "香辣鸡腿，生菜爽口", 2987),
        (6, "薯条(大)", "小食", 13.0, None, "金黄酥脆，大份薯条", 4567),
        (6, "麦旋风", "甜品", 15.0, None, "奥利奥麦旋风", 2345),
        # 海底捞火锅
        (7, "鸳鸯锅底", "锅底", 68.0, None, "麻辣+清汤，一锅两味", 876),
        (7, "肥牛卷", "肉类", 48.0, None, "精选肥牛，纹理清晰", 654),
        (7, "虾滑", "丸滑", 38.0, None, "鲜虾手打，Q弹爽口", 543),
        (7, "蔬菜拼盘", "蔬菜", 28.0, None, "时令蔬菜，新鲜搭配", 432),
        # 沙县小吃
        (8, "蒸饺", "主食", 10.0, None, "皮薄馅大，鲜香可口", 2345),
        (8, "拌面", "主食", 8.0, None, "花生酱拌面，经典味道", 1987),
        (8, "扁肉", "汤类", 10.0, None, "皮薄馅嫩，汤鲜味美", 1876),
        (8, "炖罐", "汤类", 15.0, None, "滋补炖罐，营养丰富", 1234),
    ]
    cursor.executemany(
        "INSERT INTO dishes (restaurant_id, name, category, price, original_price, description, sales_count) VALUES (?, ?, ?, ?, ?, ?, ?)",
        dishes
    )

    # 插入一些示例订单
    import random
    import string

    for i in range(20):
        order_no = 'ORD' + datetime.now().strftime('%Y%m%d') + ''.join(random.choices(string.digits, k=6))
        user_id = random.choice([2, 3, 4])
        restaurant_id = random.randint(1, 8)
        total_price = round(random.uniform(20, 150), 2)
        status = random.choice(['pending', 'confirmed', 'preparing', 'delivering', 'completed', 'completed', 'completed'])
        address = f"北京市测试地址{i+1}号"

        cursor.execute(
            "INSERT INTO orders (order_no, user_id, restaurant_id, total_price, delivery_fee, status, address) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (order_no, user_id, restaurant_id, total_price, 3.0, status, address)
        )

        order_id = cursor.lastrowid
        num_items = random.randint(1, 4)
        for j in range(num_items):
            dish_id = random.randint(1, 33)
            quantity = random.randint(1, 3)
            cursor.execute(
                "INSERT INTO order_items (order_id, dish_id, dish_name, quantity, price) VALUES (?, ?, ?, ?, ?)",
                (order_id, dish_id, f"菜品{dish_id}", quantity, round(random.uniform(10, 50), 2))
            )

    conn.commit()
    conn.close()
    print("✅ 示例数据插入完成")


if __name__ == "__main__":
    init_db()
    insert_sample_data()
