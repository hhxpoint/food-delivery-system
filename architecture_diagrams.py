"""
系统架构图生成模块
生成UML类图、系统架构图、数据库ER图、用例图等
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm

# 设置中文字体
font_path = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def draw_box(ax, x, y, w, h, title, attrs=None, methods=None, color='#4A90D9'):
    """绘制UML类图的类框"""
    # 标题栏
    ax.add_patch(plt.Rectangle((x, y + h - 0.4), w, 0.4, facecolor=color, edgecolor='black', linewidth=1.5))
    ax.text(x + w / 2, y + h - 0.2, title, ha='center', va='center',
            fontsize=10, fontweight='bold', color='white')

    # 属性区
    attr_h = 0
    if attrs:
        attr_h = len(attrs) * 0.25 + 0.1
        ax.add_patch(plt.Rectangle((x, y + h - 0.4 - attr_h), w, attr_h,
                                    facecolor='#F0F4F8', edgecolor='black', linewidth=1))
        for i, attr in enumerate(attrs):
            ax.text(x + 0.1, y + h - 0.55 - i * 0.25, attr, fontsize=7, va='center', family='monospace')

    # 方法区
    method_h = 0
    if methods:
        method_h = len(methods) * 0.25 + 0.1
        ax.add_patch(plt.Rectangle((x, y + h - 0.4 - attr_h - method_h), w, method_h,
                                    facecolor='#FFFFFF', edgecolor='black', linewidth=1))
        for i, method in enumerate(methods):
            ax.text(x + 0.1, y + h - 0.55 - attr_h - i * 0.25, method, fontsize=7, va='center', family='monospace')


def plot_system_architecture():
    """系统架构图"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('外卖系统整体架构图', fontsize=20, fontweight='bold', pad=20)

    # 表示层
    ax.add_patch(plt.Rectangle((0.5, 7.5), 13, 2, facecolor='#E8F4FD', edgecolor='#4A90D9',
                                linewidth=2, linestyle='--'))
    ax.text(7, 9.1, '表示层 (Presentation Layer) - Tkinter GUI', ha='center', va='center',
            fontsize=13, fontweight='bold', color='#4A90D9')

    gui_modules = ['登录/注册页面', '主页面/餐厅列表', '餐厅详情/菜单', '购物车页面',
                   '订单管理页面', '个人中心', '管理员后台', '数据统计页面']
    for i, mod in enumerate(gui_modules):
        x = 1 + (i % 4) * 3.2
        y = 8.2 if i < 4 else 7.7
        ax.add_patch(plt.Rectangle((x, y), 2.8, 0.4, facecolor='#4A90D9', edgecolor='#2C5F8A',
                                    linewidth=1))
        ax.text(x + 1.4, y + 0.2, mod, ha='center', va='center', fontsize=8, color='white', fontweight='bold')

    # 业务逻辑层
    ax.add_patch(plt.Rectangle((0.5, 4.5), 13, 2.5, facecolor='#E8F8E8', edgecolor='#27AE60',
                                linewidth=2, linestyle='--'))
    ax.text(7, 6.6, '业务逻辑层 (Business Logic Layer) - Service', ha='center', va='center',
            fontsize=13, fontweight='bold', color='#27AE60')

    services = ['UserService\n用户服务', 'RestaurantService\n餐厅服务', 'DishService\n菜品服务',
                'CartService\n购物车服务', 'OrderService\n订单服务', 'ReviewService\n评价服务',
                'StatsService\n统计服务']
    for i, svc in enumerate(services):
        x = 1 + (i % 4) * 3.2
        y = 5.5 if i < 4 else 4.8
        ax.add_patch(plt.Rectangle((x, y), 2.8, 0.6, facecolor='#27AE60', edgecolor='#1E8449',
                                    linewidth=1))
        ax.text(x + 1.4, y + 0.3, svc, ha='center', va='center', fontsize=8, color='white', fontweight='bold')

    # 数据访问层
    ax.add_patch(plt.Rectangle((0.5, 2), 13, 2, facecolor='#FFF3E0', edgecolor='#E67E22',
                                linewidth=2, linestyle='--'))
    ax.text(7, 3.6, '数据访问层 (Data Access Layer) - Database', ha='center', va='center',
            fontsize=13, fontweight='bold', color='#E67E22')

    db_items = ['SQLite数据库', 'users表', 'restaurants表', 'dishes表',
                'orders表', 'order_items表', 'cart表', 'reviews表']
    for i, item in enumerate(db_items):
        x = 1 + (i % 4) * 3.2
        y = 2.8 if i < 4 else 2.3
        ax.add_patch(plt.Rectangle((x, y), 2.8, 0.4, facecolor='#E67E22', edgecolor='#C0631A',
                                    linewidth=1))
        ax.text(x + 1.4, y + 0.2, item, ha='center', va='center', fontsize=8, color='white', fontweight='bold')

    # 模型层
    ax.add_patch(plt.Rectangle((0.5, 0.3), 13, 1.3, facecolor='#F5E6FF', edgecolor='#8E44AD',
                                linewidth=2, linestyle='--'))
    ax.text(7, 1.3, '模型层 (Model Layer) - OOP', ha='center', va='center',
            fontsize=13, fontweight='bold', color='#8E44AD')

    models = ['User/Customer/Admin/DeliveryStaff', 'Restaurant', 'Dish',
              'Order/OrderItem', 'CartItem', 'Review']
    for i, mod in enumerate(models):
        x = 1 + i * 2.1
        ax.add_patch(plt.Rectangle((x, 0.4), 1.9, 0.5, facecolor='#8E44AD', edgecolor='#6C3483',
                                    linewidth=1))
        ax.text(x + 0.95, 0.65, mod, ha='center', va='center', fontsize=7, color='white', fontweight='bold')

    # 层间箭头
    arrow_style = dict(arrowstyle='->', color='#555555', lw=2)
    for x_pos in [3, 7, 11]:
        ax.annotate('', xy=(x_pos, 7.5), xytext=(x_pos, 7.0),
                     arrowprops=arrow_style)
        ax.annotate('', xy=(x_pos, 4.5), xytext=(x_pos, 4.0),
                     arrowprops=arrow_style)
        ax.annotate('', xy=(x_pos, 2.0), xytext=(x_pos, 1.6),
                     arrowprops=arrow_style)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'system_architecture.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ 系统架构图已生成")


def plot_class_diagram():
    """UML类图"""
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    ax.set_title('UML类图 - 核心类设计', fontsize=20, fontweight='bold', pad=20)

    # User基类
    draw_box(ax, 0.5, 7, 3.5, 3.5, 'User', 
             ['- _id: int', '- _username: str', '- _password: str', '- _role: str', '- _phone: str', '- _balance: float'],
             ['+ login()', '+ check_password()', '+ deduct_balance()'], '#4A90D9')

    # Customer子类
    draw_box(ax, 0.5, 3, 3.5, 3, 'Customer (继承User)',
             ['- _order_history: list', '- _cart: dict'],
             ['+ add_to_cart()', '+ remove_from_cart()', '+ clear_cart()'], '#3498DB')

    # Admin子类
    draw_box(ax, 5, 3, 3, 2.5, 'Admin (继承User)',
             ['- _permissions: list'],
             ['+ has_permission()'], '#E74C3C')

    # DeliveryStaff子类
    draw_box(ax, 5, 6.5, 3, 2.5, 'DeliveryStaff (继承User)',
             ['- _status: str', '- _current_orders: list'],
             ['+ accept_order()', '+ complete_delivery()'], '#F39C12')

    # Restaurant
    draw_box(ax, 9, 7, 3.5, 3.5, 'Restaurant',
             ['- _id: int', '- _name: str', '- _category: str', '- _rating: float', '- _delivery_fee: float'],
             ['+ add_dish()', '+ get_menu()'], '#27AE60')

    # Dish
    draw_box(ax, 13, 7, 2.5, 2.5, 'Dish',
             ['- _id: int', '- _name: str', '- _price: float', '- _sales_count: int'],
             ['+ has_discount()', '+ get_discount_rate()'], '#2ECC71')

    # Order
    draw_box(ax, 9, 3, 3.5, 3, 'Order',
             ['- _id: int', '- _order_no: str', '- _total_price: float', '- _status: str'],
             ['+ add_item()', '+ get_items()', '+ get_status_text()'], '#9B59B6')

    # OrderItem
    draw_box(ax, 13, 4.5, 2.5, 2, 'OrderItem',
             ['- _dish_name: str', '- _quantity: int', '- _price: float'],
             ['+ get_subtotal()'], '#8E44AD')

    # CartItem
    draw_box(ax, 13, 2, 2.5, 2, 'CartItem',
             ['- _dish: Dish', '- _quantity: int'],
             ['+ get_subtotal()'], '#E67E22')

    # 继承箭头
    arrow_inherit = dict(arrowstyle='-|>', color='#2C3E50', lw=2)
    ax.annotate('', xy=(2.25, 7), xytext=(2.25, 6.0), arrowprops=arrow_inherit)
    ax.annotate('', xy=(2.25, 7), xytext=(2.25, 6.0), arrowprops=arrow_inherit)
    ax.plot([2.25, 2.25], [6.0, 7.0], 'k-', lw=2)
    ax.plot([2.25, 6.5], [6.0, 6.0], 'k-', lw=2)
    ax.annotate('', xy=(6.5, 5.5), xytext=(6.5, 6.0), arrowprops=arrow_inherit)

    # 关联箭头
    arrow_assoc = dict(arrowstyle='->', color='#7F8C8D', lw=1.5)
    ax.annotate('', xy=(9, 8.5), xytext=(7.5, 8.5), arrowprops=arrow_assoc)
    ax.text(8.2, 8.7, '1..*', fontsize=8, color='#7F8C8D')

    ax.annotate('', xy=(13, 8.5), xytext=(12.5, 8.5), arrowprops=arrow_assoc)
    ax.text(12.7, 8.7, '*', fontsize=8, color='#7F8C8D')

    ax.annotate('', xy=(10.75, 6), xytext=(10.75, 7), arrowprops=arrow_assoc)
    ax.text(11, 6.5, '1..*', fontsize=8, color='#7F8C8D')

    # 图例
    legend_elements = [
        mpatches.Patch(facecolor='#4A90D9', label='用户相关类'),
        mpatches.Patch(facecolor='#27AE60', label='餐厅/菜品类'),
        mpatches.Patch(facecolor='#9B59B6', label='订单相关类'),
        mpatches.Patch(facecolor='#E67E22', label='购物车类'),
    ]
    ax.legend(handles=legend_elements, loc='lower left', fontsize=10)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'class_diagram.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ UML类图已生成")


def plot_er_diagram():
    """数据库ER图"""
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('数据库ER图 (实体关系图)', fontsize=20, fontweight='bold', pad=20)

    def draw_entity(ax, x, y, w, h, name, fields, color='#3498DB'):
        ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=color, edgecolor='#2C3E50', linewidth=2))
        ax.add_patch(plt.Rectangle((x, y + h - 0.5), w, 0.5, facecolor='#2C3E50', edgecolor='#2C3E50'))
        ax.text(x + w / 2, y + h - 0.25, name, ha='center', va='center',
                fontsize=11, fontweight='bold', color='white')
        for i, field in enumerate(fields):
            ax.text(x + 0.15, y + h - 0.8 - i * 0.3, field, fontsize=8, va='center', family='monospace')

    # Users表
    draw_entity(ax, 0.3, 6, 3, 3.2, 'users',
                ['* id (PK)', 'username (UNIQUE)', 'password', 'role', 'phone', 'address', 'balance', 'created_at', 'is_active'], '#3498DB')

    # Restaurants表
    draw_entity(ax, 6, 6, 3.2, 3.2, 'restaurants',
                ['* id (PK)', 'name', 'category', 'address', 'phone', 'rating', 'monthly_sales', 'delivery_fee', 'min_order'], '#27AE60')

    # Dishes表
    draw_entity(ax, 12, 6, 3.2, 3.2, 'dishes',
                ['* id (PK)', '* restaurant_id (FK)', 'name', 'category', 'price', 'original_price', 'sales_count', 'rating', 'is_available'], '#2ECC71')

    # Orders表
    draw_entity(ax, 0.3, 1.5, 3.5, 3.5, 'orders',
                ['* id (PK)', 'order_no (UNIQUE)', '* user_id (FK)', '* restaurant_id (FK)', 'total_price', 'delivery_fee', 'status', 'address', 'phone', 'remark', 'created_at'], '#9B59B6')

    # OrderItems表
    draw_entity(ax, 5.5, 1.5, 3.2, 2.5, 'order_items',
                ['* id (PK)', '* order_id (FK)', '* dish_id (FK)', 'dish_name', 'quantity', 'price'], '#8E44AD')

    # Cart表
    draw_entity(ax, 10.5, 1.5, 2.8, 2.5, 'cart',
                ['* id (PK)', '* user_id (FK)', '* dish_id (FK)', '* restaurant_id (FK)', 'quantity'], '#E67E22')

    # Reviews表
    draw_entity(ax, 10.5, 4.8, 2.8, 2.2, 'reviews',
                ['* id (PK)', '* order_id (FK)', '* user_id (FK)', '* restaurant_id (FK)', 'rating', 'content'], '#E74C3C')

    # 关系线
    line_style = dict(arrowstyle='-', color='#555', lw=1.5)
    # users -> orders (1:N)
    ax.annotate('', xy=(0.3, 5.0), xytext=(2, 6), arrowprops=dict(arrowstyle='->', color='#555', lw=1.5))
    ax.text(0.8, 5.3, '1:N', fontsize=9, color='#E74C3C', fontweight='bold')

    # restaurants -> dishes (1:N)
    ax.annotate('', xy=(12, 8.5), xytext=(9.2, 7.5), arrowprops=dict(arrowstyle='->', color='#555', lw=1.5))
    ax.text(10.2, 8.2, '1:N', fontsize=9, color='#E74C3C', fontweight='bold')

    # restaurants -> orders (1:N)
    ax.annotate('', xy=(3.8, 5.0), xytext=(6, 6), arrowprops=dict(arrowstyle='->', color='#555', lw=1.5))
    ax.text(4.5, 5.3, '1:N', fontsize=9, color='#E74C3C', fontweight='bold')

    # orders -> order_items (1:N)
    ax.annotate('', xy=(5.5, 3.5), xytext=(3.8, 3.0), arrowprops=dict(arrowstyle='->', color='#555', lw=1.5))
    ax.text(4.3, 3.5, '1:N', fontsize=9, color='#E74C3C', fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'er_diagram.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ ER图已生成")


def plot_use_case_diagram():
    """用例图"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('系统用例图', fontsize=20, fontweight='bold', pad=20)

    # 系统边界
    ax.add_patch(plt.Rectangle((2, 0.5), 10, 9, facecolor='#FAFAFA', edgecolor='#2C3E50',
                                linewidth=2, linestyle='--', fill=True))
    ax.text(7, 9.2, '外卖订餐系统', ha='center', va='center', fontsize=16, fontweight='bold', color='#2C3E50')

    # 参与者 - 顾客
    ax.plot(1.2, 6, 'o', markersize=25, color='#3498DB')
    ax.plot([1.2, 1.2], [5.5, 4.5], 'b-', lw=2)
    ax.plot([0.8, 1.6], [5.0, 5.0], 'b-', lw=2)
    ax.plot([1.2, 0.8], [4.5, 3.5], 'b-', lw=2)
    ax.plot([1.2, 1.6], [4.5, 3.5], 'b-', lw=2)
    ax.text(1.2, 3.0, '顾客', ha='center', fontsize=12, fontweight='bold', color='#3498DB')

    # 参与者 - 管理员
    ax.plot(13, 6, 'o', markersize=25, color='#E74C3C')
    ax.plot([13, 13], [5.5, 4.5], 'r-', lw=2)
    ax.plot([12.6, 13.4], [5.0, 5.0], 'r-', lw=2)
    ax.plot([13, 12.6], [4.5, 3.5], 'r-', lw=2)
    ax.plot([13, 13.4], [4.5, 3.5], 'r-', lw=2)
    ax.text(13, 3.0, '管理员', ha='center', fontsize=12, fontweight='bold', color='#E74C3C')

    # 用例椭圆函数
    def draw_usecase(ax, x, y, text, color='#3498DB'):
        ellipse = matplotlib.patches.Ellipse((x, y), 2.5, 0.8, facecolor='#E8F4FD',
                                               edgecolor=color, linewidth=1.5)
        ax.add_patch(ellipse)
        ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold')

    # 顾客用例
    customer_cases = [
        (4, 8.5, '用户注册'), (4, 7.2, '用户登录'), (4, 5.9, '浏览餐厅'),
        (4, 4.6, '查看菜单'), (4, 3.3, '加入购物车'), (4, 2.0, '提交订单'),
        (4, 0.7, '查看订单')
    ]
    for x, y, text in customer_cases:
        draw_usecase(ax, x, y, text, '#3498DB')
        ax.annotate('', xy=(2.5, y), xytext=(1.5, 6), arrowprops=dict(arrowstyle='->', color='#3498DB', lw=1, alpha=0.5))

    # 管理员用例
    admin_cases = [
        (10, 8.5, '用户管理'), (10, 7.2, '餐厅管理'), (10, 5.9, '订单管理'),
        (10, 4.6, '数据统计'), (10, 3.3, '系统配置')
    ]
    for x, y, text in admin_cases:
        draw_usecase(ax, x, y, text, '#E74C3C')
        ax.annotate('', xy=(11.5, y), xytext=(12.5, 6), arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=1, alpha=0.5))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'use_case_diagram.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ 用例图已生成")


def plot_flowchart():
    """系统流程图"""
    fig, ax = plt.subplots(figsize=(10, 14))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis('off')
    ax.set_title('用户下单流程图', fontsize=20, fontweight='bold', pad=20)

    def draw_rounded_rect(ax, x, y, w, h, text, color='#3498DB', text_color='white'):
        ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=color, edgecolor='#2C3E50',
                                    linewidth=1.5, joinstyle='round'))
        ax.text(x + w / 2, y + h / 2, text, ha='center', va='center',
                fontsize=10, fontweight='bold', color=text_color)

    def draw_diamond(ax, x, y, w, h, text, color='#F39C12'):
        diamond = plt.Polygon([(x, y + h / 2), (x + w / 2, y + h), (x + w, y + h / 2), (x + w / 2, y)],
                               facecolor=color, edgecolor='#2C3E50', linewidth=1.5)
        ax.add_patch(diamond)
        ax.text(x + w / 2, y + h / 2, text, ha='center', va='center', fontsize=8, fontweight='bold')

    # 开始
    ax.add_patch(matplotlib.patches.FancyBboxPatch((3.5, 13), 3, 0.6, boxstyle="round,pad=0.1",
                                                     facecolor='#2ECC71', edgecolor='#27AE60'))
    ax.text(5, 13.3, '开始', ha='center', va='center', fontsize=12, fontweight='bold', color='white')

    # 流程步骤
    steps = [
        (3, 12, 4, 0.6, '用户登录/注册', '#3498DB'),
        (3, 11, 4, 0.6, '浏览餐厅列表', '#3498DB'),
        (3, 10, 4, 0.6, '选择餐厅', '#3498DB'),
        (3, 9, 4, 0.6, '浏览菜单/选菜', '#3498DB'),
        (3, 8, 4, 0.6, '加入购物车', '#3498DB'),
        (3, 6.5, 4, 0.6, '确认订单信息', '#3498DB'),
        (3, 5, 4, 0.6, '提交订单', '#3498DB'),
        (3, 3.5, 4, 0.6, '订单生成成功', '#2ECC71'),
        (3, 2.5, 4, 0.6, '等待餐厅确认', '#F39C12'),
        (3, 1.5, 4, 0.6, '配送员配送', '#9B59B6'),
        (3, 0.5, 4, 0.6, '订单完成', '#2ECC71'),
    ]

    for x, y, w, h, text, color in steps:
        draw_rounded_rect(ax, x, y, w, h, text, color)

    # 判断节点
    draw_diamond(ax, 3, 7, 4, 0.8, '购物车是否为空?', '#E74C3C')

    # 箭头连接
    arrow = dict(arrowstyle='->', color='#2C3E50', lw=2)
    positions = [13, 12, 11, 10, 9, 8, 7, 6.5, 5, 3.5, 2.5, 1.5]
    for i in range(len(positions) - 1):
        if i == 5:  # 从判断节点出来
            ax.annotate('', xy=(5, positions[i + 1]), xytext=(5, positions[i]),
                        arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=2))
            ax.text(5.3, 7.3, '否 → 去选购', fontsize=8, color='#E74C3C')
            ax.annotate('', xy=(5, 6.5), xytext=(5, 7),
                        arrowprops=dict(arrowstyle='->', color='#27AE60', lw=2))
            ax.text(5.3, 6.7, '是', fontsize=8, color='#27AE60')
        else:
            ax.annotate('', xy=(5, positions[i + 1]), xytext=(5, positions[i]),
                        arrowprops=arrow)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'flowchart.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ 流程图已生成")


def plot_module_dependency():
    """模块依赖图"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('模块依赖关系图', fontsize=20, fontweight='bold', pad=20)

    modules = {
        'main.py': (6, 7, '#2ECC71'),
        'app.py\n(GUI)': (6, 5.5, '#3498DB'),
        'services.py\n(业务逻辑)': (3, 3.5, '#E67E22'),
        'database.py\n(数据库)': (3, 1.5, '#9B59B6'),
        'models.py\n(数据模型)': (9, 3.5, '#E74C3C'),
        'visualization.py\n(可视化)': (9, 1.5, '#1ABC9C'),
    }

    for name, (x, y, color) in modules.items():
        ax.add_patch(mpatches.FancyBboxPatch((x - 1.2, y - 0.4), 2.4, 0.8,
                                             boxstyle="round,pad=0.1",
                                             facecolor=color, edgecolor='#2C3E50', linewidth=2))
        ax.text(x, y, name, ha='center', va='center', fontsize=10, fontweight='bold', color='white')

    # 依赖箭头
    deps = [
        ('main.py', 'app.py\n(GUI)'),
        ('main.py', 'database.py\n(数据库)'),
        ('main.py', 'visualization.py\n(可视化)'),
        ('app.py\n(GUI)', 'services.py\n(业务逻辑)'),
        ('app.py\n(GUI)', 'models.py\n(数据模型)'),
        ('services.py\n(业务逻辑)', 'database.py\n(数据库)'),
        ('services.py\n(业务逻辑)', 'models.py\n(数据模型)'),
        ('visualization.py\n(可视化)', 'database.py\n(数据库)'),
    ]

    for src, dst in deps:
        sx, sy, _ = modules[src]
        dx, dy, _ = modules[dst]
        ax.annotate('', xy=(dx, dy + 0.4), xytext=(sx, sy - 0.4),
                     arrowprops=dict(arrowstyle='->', color='#555', lw=1.5))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'module_dependency.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ 模块依赖图已生成")


def generate_all_architecture_diagrams():
    """生成所有架构图"""
    print("\n🏗️ 开始生成架构图...\n")
    plot_system_architecture()
    plot_class_diagram()
    plot_er_diagram()
    plot_use_case_diagram()
    plot_flowchart()
    plot_module_dependency()
    print(f"\n✅ 所有架构图已保存到: {OUTPUT_DIR}")


if __name__ == "__main__":
    generate_all_architecture_diagrams()
