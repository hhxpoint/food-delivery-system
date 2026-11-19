"""
数据可视化模块 - 生成统计图表
使用matplotlib生成各种统计图表，用于报告展示
"""
import os
import sys
import sqlite3

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置中文字体
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 尝试设置中文字体
def setup_chinese_font():
    """设置中文字体"""
    font_paths = [
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            fm.fontManager.addfont(fp)
            prop = fm.FontProperties(fname=fp)
            plt.rcParams['font.family'] = prop.get_name()
            plt.rcParams['axes.unicode_minus'] = False
            return True
    # fallback
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    return False

setup_chinese_font()

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db", "food_delivery.db")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def plot_order_status_distribution():
    """订单状态分布饼图"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status, COUNT(*) as count FROM orders GROUP BY status")
    data = cursor.fetchall()
    conn.close()

    status_names = {
        'pending': '待确认', 'confirmed': '已确认',
        'preparing': '准备中', 'delivering': '配送中',
        'completed': '已完成', 'cancelled': '已取消'
    }

    labels = [status_names.get(row['status'], row['status']) for row in data]
    sizes = [row['count'] for row in data]
    colors = ['#F39C12', '#3498DB', '#E67E22', '#2ECC71', '#27AE60', '#E74C3C']
    explode = [0.05] * len(labels)

    fig, ax = plt.subplots(figsize=(8, 6))
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors[:len(labels)],
                                       autopct='%1.1f%%', shadow=True, startangle=90,
                                       textprops={'fontsize': 12})
    for autotext in autotexts:
        autotext.set_fontsize(11)
        autotext.set_fontweight('bold')
    ax.set_title('订单状态分布图', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'order_status_pie.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ 订单状态分布饼图已生成")


def plot_restaurant_sales_bar():
    """餐厅销售额柱状图"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT r.name, COALESCE(SUM(o.total_price), 0) as revenue
        FROM restaurants r
        LEFT JOIN orders o ON r.id = o.restaurant_id AND o.status != 'cancelled'
        GROUP BY r.id
        ORDER BY revenue DESC
    ''')
    data = cursor.fetchall()
    conn.close()

    names = [row['name'] for row in data]
    revenues = [row['revenue'] for row in data]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(names, revenues, color=['#FF6B35', '#2EC4B6', '#E17055', '#00B894',
                                           '#6C5CE7', '#FDCB6E', '#E74C3C', '#3498DB'])
    ax.set_title('各餐厅销售额统计', fontsize=16, fontweight='bold', pad=15)
    ax.set_ylabel('销售额 (元)', fontsize=12)
    ax.set_xlabel('餐厅名称', fontsize=12)

    # 在柱状图上显示数值
    for bar, revenue in zip(bars, revenues):
        if revenue > 0:
            ax.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 20,
                    f'¥{revenue:.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'restaurant_sales_bar.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ 餐厅销售额柱状图已生成")


def plot_popular_dishes_horizontal_bar():
    """热门菜品横向柱状图"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT d.name, d.sales_count, r.name as restaurant_name
        FROM dishes d
        JOIN restaurants r ON d.restaurant_id = r.id
        ORDER BY d.sales_count DESC
        LIMIT 10
    ''')
    data = cursor.fetchall()
    conn.close()

    names = [f"{row['name']}({row['restaurant_name']})" for row in data][::-1]
    sales = [row['sales_count'] for row in data][::-1]

    fig, ax = plt.subplots(figsize=(10, 7))
    colors = plt.cm.RdYlGn([i / len(names) for i in range(len(names))])
    bars = ax.barh(names, sales, color=colors)
    ax.set_title('热门菜品销量 TOP10', fontsize=16, fontweight='bold', pad=15)
    ax.set_xlabel('销量 (份)', fontsize=12)

    for bar, sale in zip(bars, sales):
        ax.text(bar.get_width() + 20, bar.get_y() + bar.get_height() / 2.,
                str(sale), ha='left', va='center', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'popular_dishes_bar.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ 热门菜品横向柱状图已生成")


def plot_restaurant_rating_comparison():
    """餐厅评分对比图"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, rating, monthly_sales FROM restaurants ORDER BY rating DESC")
    data = cursor.fetchall()
    conn.close()

    names = [row['name'] for row in data]
    ratings = [row['rating'] for row in data]
    sales = [row['monthly_sales'] for row in data]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    x = range(len(names))
    bars = ax1.bar(x, ratings, color='#FF6B35', alpha=0.8, width=0.6, label='评分')
    ax1.set_ylabel('评分', fontsize=12, color='#FF6B35')
    ax1.set_ylim(3.5, 5.5)
    ax1.tick_params(axis='y', labelcolor='#FF6B35')

    ax2 = ax1.twinx()
    ax2.plot(x, sales, 'o-', color='#2EC4B6', linewidth=2, markersize=8, label='月销量')
    ax2.set_ylabel('月销量', fontsize=12, color='#2EC4B6')
    ax2.tick_params(axis='y', labelcolor='#2EC4B6')

    ax1.set_xticks(x)
    ax1.set_xticklabels(names, rotation=20, ha='right')
    ax1.set_title('餐厅评分与月销量对比', fontsize=16, fontweight='bold', pad=15)

    # 合并图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'restaurant_rating_sales.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ 餐厅评分对比图已生成")


def plot_category_distribution():
    """餐厅分类分布图"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category, COUNT(*) as count FROM restaurants GROUP BY category")
    data = cursor.fetchall()
    conn.close()

    labels = [row['category'] for row in data]
    sizes = [row['count'] for row in data]
    colors = ['#FF6B35', '#2EC4B6', '#E17055', '#00B894', '#6C5CE7', '#FDCB6E']

    fig, ax = plt.subplots(figsize=(8, 6))
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors[:len(labels)],
                                       autopct='%1.1f%%', shadow=True, startangle=140,
                                       textprops={'fontsize': 12})
    ax.set_title('餐厅分类分布', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'category_pie.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ 餐厅分类分布图已生成")


def plot_order_trend():
    """订单趋势折线图（模拟数据）"""
    import random
    days = [f"5/{i}" for i in range(1, 16)]
    orders = [random.randint(15, 45) for _ in range(15)]
    revenue = [random.uniform(800, 2500) for _ in range(15)]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.plot(days, orders, 'o-', color='#FF6B35', linewidth=2, markersize=6, label='订单数')
    ax1.fill_between(days, orders, alpha=0.2, color='#FF6B35')
    ax1.set_ylabel('订单数', fontsize=12, color='#FF6B35')
    ax1.tick_params(axis='y', labelcolor='#FF6B35')

    ax2 = ax1.twinx()
    ax2.plot(days, revenue, 's-', color='#2EC4B6', linewidth=2, markersize=6, label='营业额')
    ax2.set_ylabel('营业额 (元)', fontsize=12, color='#2EC4B6')
    ax2.tick_params(axis='y', labelcolor='#2EC4B6')

    ax1.set_xlabel('日期', fontsize=12)
    ax1.set_title('近15天订单趋势', fontsize=16, fontweight='bold', pad=15)
    plt.xticks(rotation=45, ha='right')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'order_trend.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ 订单趋势折线图已生成")


def plot_price_distribution():
    """菜品价格分布直方图"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT price FROM dishes")
    data = cursor.fetchall()
    conn.close()

    prices = [row['price'] for row in data]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.hist(prices, bins=15, color='#FF6B35', edgecolor='white', alpha=0.8)
    ax.set_title('菜品价格分布', fontsize=16, fontweight='bold', pad=15)
    ax.set_xlabel('价格 (元)', fontsize=12)
    ax.set_ylabel('菜品数量', fontsize=12)
    ax.axvline(x=sum(prices)/len(prices), color='#E74C3C', linestyle='--', linewidth=2, label=f'均价: ¥{sum(prices)/len(prices):.1f}')
    ax.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'price_distribution.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ 菜品价格分布图已生成")


def plot_user_order_ranking():
    """用户订单排行"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT u.username, COUNT(o.id) as order_count, COALESCE(SUM(o.total_price), 0) as total_spent
        FROM users u
        LEFT JOIN orders o ON u.id = o.user_id AND o.status != 'cancelled'
        WHERE u.role = 'customer'
        GROUP BY u.id
        ORDER BY total_spent DESC
    ''')
    data = cursor.fetchall()
    conn.close()

    names = [row['username'] for row in data]
    spent = [row['total_spent'] for row in data]
    orders = [row['order_count'] for row in data]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.bar(names, spent, color='#FF6B35')
    ax1.set_title('用户消费排行', fontsize=14, fontweight='bold')
    ax1.set_ylabel('消费金额 (元)', fontsize=11)

    ax2.bar(names, orders, color='#2EC4B6')
    ax2.set_title('用户订单数排行', fontsize=14, fontweight='bold')
    ax2.set_ylabel('订单数', fontsize=11)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'user_ranking.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ 用户排行图已生成")


def generate_all_charts():
    """生成所有图表"""
    print("\n📊 开始生成统计图表...\n")
    plot_order_status_distribution()
    plot_restaurant_sales_bar()
    plot_popular_dishes_horizontal_bar()
    plot_restaurant_rating_comparison()
    plot_category_distribution()
    plot_order_trend()
    plot_price_distribution()
    plot_user_order_ranking()
    print(f"\n✅ 所有图表已保存到: {OUTPUT_DIR}")


if __name__ == "__main__":
    generate_all_charts()
