"""
图形用户界面模块 - 外卖系统主界面
使用Tkinter实现完整的GUI交互界面
包含：登录/注册、主界面、餐厅浏览、购物车、订单管理、管理后台
"""
import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
import threading
import os
import sys

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import init_db, insert_sample_data
from models import User, Customer, Admin
from services import (UserService, RestaurantService, DishService,
                      CartService, OrderService, ReviewService, StatsService)

# ==================== 颜色主题 ====================
COLORS = {
    'primary': '#FF6B35',       # 主色调 - 活力橙
    'primary_dark': '#E55A2B',  # 深橙
    'secondary': '#2EC4B6',     # 辅助色 - 清新绿
    'bg': '#F8F9FA',           # 背景色
    'card_bg': '#FFFFFF',      # 卡片背景
    'text': '#2D3436',         # 主文字
    'text_light': '#636E72',   # 浅色文字
    'border': '#DFE6E9',       # 边框色
    'success': '#00B894',      # 成功绿
    'warning': '#FDCB6E',      # 警告黄
    'danger': '#E17055',       # 危险红
    'star': '#F39C12',         # 星级黄
    'white': '#FFFFFF',
    'light_gray': '#F5F6FA',
}


class FoodDeliveryApp:
    """外卖系统主应用类"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("外卖系统 - Food Delivery System")
        self.root.geometry("1200x800")
        self.root.configure(bg=COLORS['bg'])
        self.root.minsize(1000, 700)

        # 当前登录用户
        self.current_user = None

        # 初始化数据库
        init_db()
        insert_sample_data()

        # 设置样式
        self._setup_styles()

        # 显示登录界面
        self._show_login_page()

    def _setup_styles(self):
        """配置全局样式"""
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # 按钮样式
        self.style.configure('Primary.TButton',
                             background=COLORS['primary'],
                             foreground='white',
                             font=('Microsoft YaHei', 11, 'bold'),
                             padding=(20, 10))
        self.style.map('Primary.TButton',
                       background=[('active', COLORS['primary_dark'])])

        self.style.configure('Secondary.TButton',
                             background=COLORS['secondary'],
                             foreground='white',
                             font=('Microsoft YaHei', 10),
                             padding=(15, 8))

        self.style.configure('Danger.TButton',
                             background=COLORS['danger'],
                             foreground='white',
                             font=('Microsoft YaHei', 10),
                             padding=(15, 8))

        # 标签样式
        self.style.configure('Title.TLabel',
                             font=('Microsoft YaHei', 24, 'bold'),
                             foreground=COLORS['primary'],
                             background=COLORS['bg'])

        self.style.configure('Subtitle.TLabel',
                             font=('Microsoft YaHei', 14),
                             foreground=COLORS['text_light'],
                             background=COLORS['bg'])

        # Frame样式
        self.style.configure('Card.TFrame',
                             background=COLORS['card_bg'],
                             relief='flat')

    def _clear_window(self):
        """清空窗口"""
        for widget in self.root.winfo_children():
            widget.destroy()

    # ==================== 登录/注册页面 ====================
    def _show_login_page(self):
        """显示登录页面"""
        self._clear_window()

        # 主容器
        main_frame = tk.Frame(self.root, bg=COLORS['primary'])
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 左侧装饰区域
        left_frame = tk.Frame(main_frame, bg=COLORS['primary'], width=500)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        left_frame.pack_propagate(False)

        tk.Label(left_frame, text="🛵", font=('Arial', 80),
                 bg=COLORS['primary'], fg='white').pack(pady=(100, 20))
        tk.Label(left_frame, text="外卖订餐系统", font=('Microsoft YaHei', 32, 'bold'),
                 bg=COLORS['primary'], fg='white').pack(pady=(0, 10))
        tk.Label(left_frame, text="Food Delivery System", font=('Arial', 16),
                 bg=COLORS['primary'], fg='#FFE0CC').pack()
        tk.Label(left_frame, text="Python课程实践 | 面向对象 | 数据库 | GUI",
                 font=('Microsoft YaHei', 11),
                 bg=COLORS['primary'], fg='#FFD0B0').pack(pady=(30, 0))

        # 右侧登录区域
        right_frame = tk.Frame(main_frame, bg=COLORS['white'], width=500)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right_frame.pack_propagate(False)

        login_container = tk.Frame(right_frame, bg=COLORS['white'])
        login_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(login_container, text="用户登录", font=('Microsoft YaHei', 22, 'bold'),
                 bg=COLORS['white'], fg=COLORS['text']).pack(pady=(0, 30))

        # 用户名
        tk.Label(login_container, text="用户名", font=('Microsoft YaHei', 11),
                 bg=COLORS['white'], fg=COLORS['text_light']).pack(anchor=tk.W, pady=(0, 5))
        self.login_username = tk.Entry(login_container, font=('Microsoft YaHei', 12),
                                       width=30, relief=tk.SOLID, bd=1)
        self.login_username.pack(pady=(0, 15), ipady=8)

        # 密码
        tk.Label(login_container, text="密码", font=('Microsoft YaHei', 11),
                 bg=COLORS['white'], fg=COLORS['text_light']).pack(anchor=tk.W, pady=(0, 5))
        self.login_password = tk.Entry(login_container, font=('Microsoft YaHei', 12),
                                       width=30, relief=tk.SOLID, bd=1, show="●")
        self.login_password.pack(pady=(0, 25), ipady=8)

        # 登录按钮
        login_btn = tk.Button(login_container, text="登  录", font=('Microsoft YaHei', 13, 'bold'),
                              bg=COLORS['primary'], fg='white', width=28, cursor='hand2',
                              relief=tk.FLAT, command=self._handle_login)
        login_btn.pack(pady=(0, 15), ipady=10)

        # 注册链接
        reg_frame = tk.Frame(login_container, bg=COLORS['white'])
        reg_frame.pack()
        tk.Label(reg_frame, text="还没有账号？", font=('Microsoft YaHei', 10),
                 bg=COLORS['white'], fg=COLORS['text_light']).pack(side=tk.LEFT)
        reg_link = tk.Label(reg_frame, text="立即注册", font=('Microsoft YaHei', 10, 'bold'),
                            bg=COLORS['white'], fg=COLORS['primary'], cursor='hand2')
        reg_link.pack(side=tk.LEFT)
        reg_link.bind("<Button-1>", lambda e: self._show_register_page())

        # 提示信息
        tk.Label(login_container, text="提示: admin/admin123 或 zhangsan/123456",
                 font=('Microsoft YaHei', 9),
                 bg=COLORS['white'], fg=COLORS['text_light']).pack(pady=(20, 0))

        # 绑定回车键
        self.login_password.bind("<Return>", lambda e: self._handle_login())

    def _show_register_page(self):
        """显示注册页面"""
        self._clear_window()

        main_frame = tk.Frame(self.root, bg=COLORS['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 返回按钮
        back_btn = tk.Button(main_frame, text="← 返回登录", font=('Microsoft YaHei', 10),
                             bg=COLORS['bg'], fg=COLORS['primary'], relief=tk.FLAT,
                             cursor='hand2', command=self._show_login_page)
        back_btn.pack(anchor=tk.NW, padx=20, pady=20)

        # 注册表单
        form_frame = tk.Frame(main_frame, bg=COLORS['white'], padx=40, pady=30)
        form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(form_frame, text="用户注册", font=('Microsoft YaHei', 22, 'bold'),
                 bg=COLORS['white'], fg=COLORS['text']).grid(row=0, column=0, columnspan=2, pady=(0, 25))

        fields = [
            ("用户名", "reg_username"),
            ("密码", "reg_password"),
            ("手机号", "reg_phone"),
            ("地址", "reg_address"),
        ]

        for i, (label_text, attr_name) in enumerate(fields):
            tk.Label(form_frame, text=label_text, font=('Microsoft YaHei', 11),
                     bg=COLORS['white'], fg=COLORS['text_light']).grid(
                row=i*2+1, column=0, sticky=tk.W, pady=(5, 0))

            entry = tk.Entry(form_frame, font=('Microsoft YaHei', 12), width=30, relief=tk.SOLID, bd=1)
            if attr_name == "reg_password":
                entry.configure(show="●")
            entry.grid(row=i*2+2, column=0, columnspan=2, pady=(0, 10), ipady=8, padx=5)
            setattr(self, attr_name, entry)

        reg_btn = tk.Button(form_frame, text="注  册", font=('Microsoft YaHei', 13, 'bold'),
                            bg=COLORS['secondary'], fg='white', width=28, cursor='hand2',
                            relief=tk.FLAT, command=self._handle_register)
        reg_btn.grid(row=len(fields)*2+1, column=0, columnspan=2, pady=(15, 0), ipady=10)

    def _handle_login(self):
        """处理登录"""
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()

        if not username or not password:
            messagebox.showwarning("提示", "请输入用户名和密码")
            return

        user = UserService.login(username, password)
        if user:
            self.current_user = user
            messagebox.showinfo("成功", f"欢迎回来，{user.username}！")
            if user.role == 'admin':
                self._show_admin_page()
            else:
                self._show_main_page()
        else:
            messagebox.showerror("错误", "用户名或密码错误")

    def _handle_register(self):
        """处理注册"""
        username = self.reg_username.get().strip()
        password = self.reg_password.get().strip()
        phone = self.reg_phone.get().strip()
        address = self.reg_address.get().strip()

        success, msg = UserService.register(username, password, phone, address)
        if success:
            messagebox.showinfo("成功", msg)
            self._show_login_page()
        else:
            messagebox.showerror("错误", msg)

    # ==================== 主页面 ====================
    def _show_main_page(self):
        """显示主页面"""
        self._clear_window()

        # 顶部导航栏
        nav_frame = tk.Frame(self.root, bg=COLORS['white'], height=60)
        nav_frame.pack(fill=tk.X)
        nav_frame.pack_propagate(False)

        # Logo
        tk.Label(nav_frame, text="🛵 外卖系统", font=('Microsoft YaHei', 16, 'bold'),
                 bg=COLORS['white'], fg=COLORS['primary']).pack(side=tk.LEFT, padx=20)

        # 导航按钮
        nav_buttons = [
            ("🏠 首页", self._show_main_page),
            ("📋 订单", self._show_orders_page),
            ("🛒 购物车", self._show_cart_page),
            ("👤 个人中心", self._show_profile_page),
        ]

        for text, command in nav_buttons:
            btn = tk.Button(nav_frame, text=text, font=('Microsoft YaHei', 11),
                            bg=COLORS['white'], fg=COLORS['text'], relief=tk.FLAT,
                            cursor='hand2', command=command, padx=15)
            btn.pack(side=tk.LEFT, padx=5)

        # 用户信息
        tk.Label(nav_frame, text=f"👤 {self.current_user.username}",
                 font=('Microsoft YaHei', 11),
                 bg=COLORS['white'], fg=COLORS['text']).pack(side=tk.RIGHT, padx=20)

        logout_btn = tk.Button(nav_frame, text="退出登录", font=('Microsoft YaHei', 10),
                               bg=COLORS['danger'], fg='white', relief=tk.FLAT,
                               cursor='hand2', command=self._handle_logout)
        logout_btn.pack(side=tk.RIGHT, padx=5)

        # 内容区域 - 使用Canvas滚动
        content_frame = tk.Frame(self.root, bg=COLORS['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(content_frame, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg'])

        scrollable_frame.bind("<Configure>",
                              lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 绑定鼠标滚轮
        def _on_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except tk.TclError:
                pass
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # 搜索栏
        search_frame = tk.Frame(scrollable_frame, bg=COLORS['white'], padx=20, pady=15)
        search_frame.pack(fill=tk.X, padx=20, pady=(20, 10))

        tk.Label(search_frame, text="🔍 搜索餐厅或菜品：", font=('Microsoft YaHei', 12),
                 bg=COLORS['white']).pack(side=tk.LEFT)

        self.search_entry = tk.Entry(search_frame, font=('Microsoft YaHei', 12), width=40,
                                     relief=tk.SOLID, bd=1)
        self.search_entry.pack(side=tk.LEFT, padx=10, ipady=6)

        search_btn = tk.Button(search_frame, text="搜索", font=('Microsoft YaHei', 11),
                               bg=COLORS['primary'], fg='white', relief=tk.FLAT,
                               cursor='hand2', command=self._handle_search)
        search_btn.pack(side=tk.LEFT, ipady=5)

        # 分类标签
        cat_frame = tk.Frame(scrollable_frame, bg=COLORS['bg'])
        cat_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

        categories = RestaurantService.get_categories()
        for cat in categories:
            btn = tk.Button(cat_frame, text=cat, font=('Microsoft YaHei', 10),
                            bg=COLORS['white'], fg=COLORS['text'], relief=tk.SOLID, bd=1,
                            cursor='hand2', padx=12, pady=5,
                            command=lambda c=cat: self._filter_by_category(c))
            btn.pack(side=tk.LEFT, padx=5)

        # 热门推荐
        tk.Label(scrollable_frame, text="🔥 热门推荐", font=('Microsoft YaHei', 16, 'bold'),
                 bg=COLORS['bg'], fg=COLORS['text']).pack(anchor=tk.W, padx=25, pady=(10, 10))

        # 餐厅列表
        self.restaurant_list_frame = tk.Frame(scrollable_frame, bg=COLORS['bg'])
        self.restaurant_list_frame.pack(fill=tk.BOTH, padx=20, pady=(0, 20))

        self._load_restaurants()

    def _load_restaurants(self, category=None, keyword=None):
        """加载餐厅列表"""
        for widget in self.restaurant_list_frame.winfo_children():
            widget.destroy()

        restaurants = RestaurantService.get_all_restaurants(category, keyword)

        if not restaurants:
            tk.Label(self.restaurant_list_frame, text="暂无餐厅",
                     font=('Microsoft YaHei', 14),
                     bg=COLORS['bg'], fg=COLORS['text_light']).pack(pady=50)
            return

        # 2列布局
        for i, restaurant in enumerate(restaurants):
            row = i // 2
            col = i % 2

            card = tk.Frame(self.restaurant_list_frame, bg=COLORS['white'],
                            relief=tk.RAISED, bd=1, padx=15, pady=15)
            card.grid(row=row, column=col, padx=10, pady=10, sticky=tk.NSEW)

            self.restaurant_list_frame.grid_columnconfigure(0, weight=1)
            self.restaurant_list_frame.grid_columnconfigure(1, weight=1)

            # 餐厅图标
            emoji_map = {'中餐': '🍜', '日料': '🍣', '西餐': '🍕', '快餐': '🍔',
                         '饮品': '☕', '火锅': '🍲'}
            emoji = emoji_map.get(restaurant.category, '🍽️')

            tk.Label(card, text=f"{emoji} {restaurant.name}",
                     font=('Microsoft YaHei', 14, 'bold'),
                     bg=COLORS['white'], fg=COLORS['text']).pack(anchor=tk.W)

            tk.Label(card, text=f"{restaurant.category} | ⭐{restaurant.rating} | 月售{restaurant.monthly_sales}",
                     font=('Microsoft YaHei', 10),
                     bg=COLORS['white'], fg=COLORS['text_light']).pack(anchor=tk.W, pady=(5, 5))

            tk.Label(card, text=f"配送费¥{restaurant.delivery_fee} | 起送¥{restaurant.min_order}",
                     font=('Microsoft YaHei', 10),
                     bg=COLORS['white'], fg=COLORS['text_light']).pack(anchor=tk.W)

            tk.Label(card, text=restaurant.description[:30] + "..." if len(restaurant.description) > 30 else restaurant.description,
                     font=('Microsoft YaHei', 9),
                     bg=COLORS['white'], fg=COLORS['text_light']).pack(anchor=tk.W, pady=(5, 10))

            enter_btn = tk.Button(card, text="进入店铺 →", font=('Microsoft YaHei', 10, 'bold'),
                                  bg=COLORS['primary'], fg='white', relief=tk.FLAT,
                                  cursor='hand2',
                                  command=lambda r=restaurant: self._show_restaurant_detail(r))
            enter_btn.pack(anchor=tk.E)

    def _filter_by_category(self, category):
        """按分类筛选"""
        self._load_restaurants(category=category)

    def _handle_search(self):
        """处理搜索"""
        keyword = self.search_entry.get().strip()
        if keyword:
            self._load_restaurants(keyword=keyword)

    # ==================== 餐厅详情页面 ====================
    def _show_restaurant_detail(self, restaurant):
        """显示餐厅详情和菜单"""
        self._clear_window()

        # 顶部
        nav_frame = tk.Frame(self.root, bg=COLORS['white'], height=60)
        nav_frame.pack(fill=tk.X)
        nav_frame.pack_propagate(False)

        back_btn = tk.Button(nav_frame, text="← 返回", font=('Microsoft YaHei', 11),
                             bg=COLORS['white'], fg=COLORS['primary'], relief=tk.FLAT,
                             cursor='hand2', command=self._show_main_page)
        back_btn.pack(side=tk.LEFT, padx=20)

        tk.Label(nav_frame, text=f"🍽️ {restaurant.name}",
                 font=('Microsoft YaHei', 16, 'bold'),
                 bg=COLORS['white'], fg=COLORS['text']).pack(side=tk.LEFT, padx=20)

        cart_btn = tk.Button(nav_frame, text="🛒 购物车", font=('Microsoft YaHei', 11),
                             bg=COLORS['primary'], fg='white', relief=tk.FLAT,
                             cursor='hand2', command=self._show_cart_page)
        cart_btn.pack(side=tk.RIGHT, padx=20)

        # 内容区域
        content_frame = tk.Frame(self.root, bg=COLORS['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(content_frame, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=COLORS['bg'])

        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 餐厅信息卡
        info_card = tk.Frame(scrollable, bg=COLORS['white'], padx=25, pady=20)
        info_card.pack(fill=tk.X, padx=20, pady=20)

        tk.Label(info_card, text=f"⭐ {restaurant.rating}  |  月售 {restaurant.monthly_sales}  |  配送费 ¥{restaurant.delivery_fee}  |  起送 ¥{restaurant.min_order}",
                 font=('Microsoft YaHei', 12),
                 bg=COLORS['white'], fg=COLORS['text']).pack(anchor=tk.W)

        tk.Label(info_card, text=f"📍 {restaurant.description}",
                 font=('Microsoft YaHei', 10),
                 bg=COLORS['white'], fg=COLORS['text_light']).pack(anchor=tk.W, pady=(5, 0))

        # 菜品列表
        tk.Label(scrollable, text="📋 菜单", font=('Microsoft YaHei', 16, 'bold'),
                 bg=COLORS['bg'], fg=COLORS['text']).pack(anchor=tk.W, padx=25, pady=(10, 10))

        dishes = DishService.get_dishes_by_restaurant(restaurant.id)

        # 按分类分组
        dish_categories = {}
        for dish in dishes:
            cat = dish.category if dish.category else "其他"
            if cat not in dish_categories:
                dish_categories[cat] = []
            dish_categories[cat].append(dish)

        for cat_name, cat_dishes in dish_categories.items():
            # 分类标题
            tk.Label(scrollable, text=f"▸ {cat_name}",
                     font=('Microsoft YaHei', 13, 'bold'),
                     bg=COLORS['bg'], fg=COLORS['primary']).pack(anchor=tk.W, padx=30, pady=(10, 5))

            for dish in cat_dishes:
                dish_card = tk.Frame(scrollable, bg=COLORS['white'], padx=15, pady=12)
                dish_card.pack(fill=tk.X, padx=30, pady=3)

                # 菜品信息
                left_info = tk.Frame(dish_card, bg=COLORS['white'])
                left_info.pack(side=tk.LEFT, fill=tk.X, expand=True)

                tk.Label(left_info, text=dish.name,
                         font=('Microsoft YaHei', 12, 'bold'),
                         bg=COLORS['white'], fg=COLORS['text']).pack(anchor=tk.W)

                desc_text = dish.description[:25] + "..." if len(dish.description) > 25 else dish.description
                tk.Label(left_info, text=desc_text,
                         font=('Microsoft YaHei', 9),
                         bg=COLORS['white'], fg=COLORS['text_light']).pack(anchor=tk.W)

                sales_text = f"月售{dish.sales_count}"
                tk.Label(left_info, text=sales_text,
                         font=('Microsoft YaHei', 9),
                         bg=COLORS['white'], fg=COLORS['text_light']).pack(anchor=tk.W)

                # 价格和添加按钮
                right_action = tk.Frame(dish_card, bg=COLORS['white'])
                right_action.pack(side=tk.RIGHT)

                price_text = f"¥{dish.price}"
                if dish.has_discount():
                    price_text = f"¥{dish.price} ¥{dish.original_price}"

                tk.Label(right_action, text=price_text,
                         font=('Microsoft YaHei', 12, 'bold'),
                         bg=COLORS['white'], fg=COLORS['danger']).pack()

                add_btn = tk.Button(right_action, text="+ 加入购物车",
                                    font=('Microsoft YaHei', 9),
                                    bg=COLORS['primary'], fg='white', relief=tk.FLAT,
                                    cursor='hand2',
                                    command=lambda d=dish, r=restaurant: self._add_to_cart(d, r))
                add_btn.pack(pady=(5, 0))

        # 底部间距
        tk.Label(scrollable, text="", bg=COLORS['bg']).pack(pady=20)

    def _add_to_cart(self, dish, restaurant):
        """添加到购物车"""
        success = CartService.add_to_cart(
            self.current_user.id, dish.id, restaurant.id
        )
        if success:
            messagebox.showinfo("成功", f"已将 {dish.name} 加入购物车")

    # ==================== 购物车页面 ====================
    def _show_cart_page(self):
        """显示购物车页面"""
        self._clear_window()

        # 顶部
        nav_frame = tk.Frame(self.root, bg=COLORS['white'], height=60)
        nav_frame.pack(fill=tk.X)
        nav_frame.pack_propagate(False)

        back_btn = tk.Button(nav_frame, text="← 返回", font=('Microsoft YaHei', 11),
                             bg=COLORS['white'], fg=COLORS['primary'], relief=tk.FLAT,
                             cursor='hand2', command=self._show_main_page)
        back_btn.pack(side=tk.LEFT, padx=20)

        tk.Label(nav_frame, text="🛒 我的购物车",
                 font=('Microsoft YaHei', 16, 'bold'),
                 bg=COLORS['white'], fg=COLORS['text']).pack(side=tk.LEFT, padx=20)

        # 内容区域
        content_frame = tk.Frame(self.root, bg=COLORS['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 获取购物车内容
        cart_items = CartService.get_cart_items(self.current_user.id)

        if not cart_items:
            tk.Label(content_frame, text="🛒 购物车是空的",
                     font=('Microsoft YaHei', 18),
                     bg=COLORS['bg'], fg=COLORS['text_light']).pack(pady=100)
            tk.Button(content_frame, text="去逛逛", font=('Microsoft YaHei', 12),
                      bg=COLORS['primary'], fg='white', relief=tk.FLAT,
                      command=self._show_main_page).pack()
            return

        # 购物车列表
        cart_canvas = tk.Canvas(content_frame, bg=COLORS['bg'], highlightthickness=0)
        cart_scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=cart_canvas.yview)
        cart_scrollable = tk.Frame(cart_canvas, bg=COLORS['bg'])

        cart_scrollable.bind("<Configure>", lambda e: cart_canvas.configure(scrollregion=cart_canvas.bbox("all")))
        cart_canvas.create_window((0, 0), window=cart_scrollable, anchor=tk.NW)
        cart_canvas.configure(yscrollcommand=cart_scrollbar.set)

        cart_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cart_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        total_price = 0
        for item in cart_items:
            item_frame = tk.Frame(cart_scrollable, bg=COLORS['white'], padx=20, pady=15)
            item_frame.pack(fill=tk.X, pady=5)

            tk.Label(item_frame, text=f"🍽️ {item['dish_name']}",
                     font=('Microsoft YaHei', 13, 'bold'),
                     bg=COLORS['white'], fg=COLORS['text']).pack(anchor=tk.W)

            tk.Label(item_frame, text=f"来自: {item['restaurant_name']}",
                     font=('Microsoft YaHei', 10),
                     bg=COLORS['white'], fg=COLORS['text_light']).pack(anchor=tk.W)

            price_frame = tk.Frame(item_frame, bg=COLORS['white'])
            price_frame.pack(fill=tk.X, pady=(10, 0))

            subtotal = item['price'] * item['quantity']
            total_price += subtotal

            tk.Label(price_frame, text=f"¥{item['price']} × {item['quantity']} = ¥{subtotal:.2f}",
                     font=('Microsoft YaHei', 12),
                     bg=COLORS['white'], fg=COLORS['danger']).pack(side=tk.LEFT)

            # 数量调整按钮
            btn_frame = tk.Frame(price_frame, bg=COLORS['white'])
            btn_frame.pack(side=tk.RIGHT)

            tk.Button(btn_frame, text="-", font=('Arial', 12, 'bold'),
                      bg=COLORS['border'], relief=tk.FLAT, width=3,
                      command=lambda cid=item['id'], q=item['quantity']: self._update_cart(cid, q - 1)).pack(side=tk.LEFT, padx=2)

            tk.Label(btn_frame, text=str(item['quantity']),
                     font=('Microsoft YaHei', 12), width=3,
                     bg=COLORS['white']).pack(side=tk.LEFT)

            tk.Button(btn_frame, text="+", font=('Arial', 12, 'bold'),
                      bg=COLORS['primary'], fg='white', relief=tk.FLAT, width=3,
                      command=lambda cid=item['id'], q=item['quantity']: self._update_cart(cid, q + 1)).pack(side=tk.LEFT, padx=2)

            tk.Button(btn_frame, text="删除", font=('Microsoft YaHei', 9),
                      bg=COLORS['danger'], fg='white', relief=tk.FLAT,
                      command=lambda cid=item['id']: self._update_cart(cid, 0)).pack(side=tk.LEFT, padx=(10, 0))

        # 底部结算栏
        bottom_frame = tk.Frame(self.root, bg=COLORS['white'], height=80)
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)
        bottom_frame.pack_propagate(False)

        inner_bottom = tk.Frame(bottom_frame, bg=COLORS['white'])
        inner_bottom.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)

        tk.Label(inner_bottom, text=f"合计: ¥{total_price:.2f}",
                 font=('Microsoft YaHei', 18, 'bold'),
                 bg=COLORS['white'], fg=COLORS['danger']).pack(side=tk.LEFT)

        tk.Button(inner_bottom, text="去结算", font=('Microsoft YaHei', 14, 'bold'),
                  bg=COLORS['primary'], fg='white', relief=tk.FLAT,
                  cursor='hand2', padx=40, pady=10,
                  command=self._show_checkout_page).pack(side=tk.RIGHT)

    def _update_cart(self, cart_id, quantity):
        """更新购物车"""
        CartService.update_quantity(cart_id, quantity)
        self._show_cart_page()

    # ==================== 结算页面 ====================
    def _show_checkout_page(self):
        """显示结算页面"""
        self._clear_window()

        main_frame = tk.Frame(self.root, bg=COLORS['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="📋 确认订单", font=('Microsoft YaHei', 20, 'bold'),
                 bg=COLORS['bg'], fg=COLORS['text']).pack(pady=(30, 20))

        form_frame = tk.Frame(main_frame, bg=COLORS['white'], padx=30, pady=25)
        form_frame.pack(fill=tk.X, padx=50)

        tk.Label(form_frame, text="配送地址", font=('Microsoft YaHei', 12, 'bold'),
                 bg=COLORS['white']).pack(anchor=tk.W)
        self.checkout_address = tk.Entry(form_frame, font=('Microsoft YaHei', 12), width=50, relief=tk.SOLID, bd=1)
        self.checkout_address.insert(0, self.current_user.address if self.current_user.address else "")
        self.checkout_address.pack(fill=tk.X, pady=(5, 15), ipady=8)

        tk.Label(form_frame, text="联系电话", font=('Microsoft YaHei', 12, 'bold'),
                 bg=COLORS['white']).pack(anchor=tk.W)
        self.checkout_phone = tk.Entry(form_frame, font=('Microsoft YaHei', 12), width=50, relief=tk.SOLID, bd=1)
        self.checkout_phone.insert(0, self.current_user.phone if self.current_user.phone else "")
        self.checkout_phone.pack(fill=tk.X, pady=(5, 15), ipady=8)

        tk.Label(form_frame, text="备注", font=('Microsoft YaHei', 12, 'bold'),
                 bg=COLORS['white']).pack(anchor=tk.W)
        self.checkout_remark = tk.Entry(form_frame, font=('Microsoft YaHei', 12), width=50, relief=tk.SOLID, bd=1)
        self.checkout_remark.pack(fill=tk.X, pady=(5, 15), ipady=8)

        # 订单摘要
        cart_items = CartService.get_cart_items(self.current_user.id)
        total = sum(item['price'] * item['quantity'] for item in cart_items)

        summary_frame = tk.Frame(main_frame, bg=COLORS['white'], padx=30, pady=20)
        summary_frame.pack(fill=tk.X, padx=50, pady=20)

        tk.Label(summary_frame, text=f"共 {len(cart_items)} 种菜品，合计: ¥{total:.2f}",
                 font=('Microsoft YaHei', 14),
                 bg=COLORS['white'], fg=COLORS['text']).pack(anchor=tk.W)

        btn_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="提交订单", font=('Microsoft YaHei', 14, 'bold'),
                  bg=COLORS['primary'], fg='white', relief=tk.FLAT, padx=40, pady=10,
                  command=self._submit_order).pack(side=tk.LEFT, padx=10)

        tk.Button(btn_frame, text="返回购物车", font=('Microsoft YaHei', 14),
                  bg=COLORS['border'], relief=tk.FLAT, padx=40, pady=10,
                  command=self._show_cart_page).pack(side=tk.LEFT, padx=10)

    def _submit_order(self):
        """提交订单"""
        address = self.checkout_address.get().strip()
        phone = self.checkout_phone.get().strip()
        remark = self.checkout_remark.get().strip()

        if not address:
            messagebox.showwarning("提示", "请输入配送地址")
            return
        if not phone:
            messagebox.showwarning("提示", "请输入联系电话")
            return

        # 使用多线程处理订单（体现多线程知识点）
        def process_order():
            success, msg = OrderService.create_order(
                self.current_user.id, address, phone, remark
            )
            self.root.after(0, lambda: self._on_order_result(success, msg))

        thread = threading.Thread(target=process_order, daemon=True)
        thread.start()

        # 显示加载提示
        messagebox.showinfo("处理中", "正在提交订单，请稍候...")

    def _on_order_result(self, success, msg):
        """订单处理结果回调"""
        if success:
            messagebox.showinfo("成功", msg)
            self._show_orders_page()
        else:
            messagebox.showerror("错误", msg)

    # ==================== 订单页面 ====================
    def _show_orders_page(self):
        """显示订单页面"""
        self._clear_window()

        # 顶部
        nav_frame = tk.Frame(self.root, bg=COLORS['white'], height=60)
        nav_frame.pack(fill=tk.X)
        nav_frame.pack_propagate(False)

        back_btn = tk.Button(nav_frame, text="← 返回", font=('Microsoft YaHei', 11),
                             bg=COLORS['white'], fg=COLORS['primary'], relief=tk.FLAT,
                             cursor='hand2', command=self._show_main_page)
        back_btn.pack(side=tk.LEFT, padx=20)

        tk.Label(nav_frame, text="📋 我的订单",
                 font=('Microsoft YaHei', 16, 'bold'),
                 bg=COLORS['white'], fg=COLORS['text']).pack(side=tk.LEFT, padx=20)

        # 内容区域
        content_frame = tk.Frame(self.root, bg=COLORS['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 状态筛选
        filter_frame = tk.Frame(content_frame, bg=COLORS['bg'])
        filter_frame.pack(fill=tk.X, pady=(0, 10))

        statuses = ["全部", "pending", "confirmed", "preparing", "delivering", "completed", "cancelled"]
        status_names = {"全部": "全部", "pending": "待确认", "confirmed": "已确认",
                        "preparing": "准备中", "delivering": "配送中", "completed": "已完成", "cancelled": "已取消"}

        for status in statuses:
            btn = tk.Button(filter_frame, text=status_names[status],
                            font=('Microsoft YaHei', 10),
                            bg=COLORS['white'], relief=tk.SOLID, bd=1,
                            cursor='hand2', padx=10, pady=3,
                            command=lambda s=status: self._filter_orders(s))
            btn.pack(side=tk.LEFT, padx=3)

        # 订单列表
        self.order_list_frame = tk.Frame(content_frame, bg=COLORS['bg'])
        self.order_list_frame.pack(fill=tk.BOTH, expand=True)

        self._load_orders()

    def _load_orders(self, status=None):
        """加载订单列表"""
        for widget in self.order_list_frame.winfo_children():
            widget.destroy()

        orders = OrderService.get_user_orders(self.current_user.id, status)

        if not orders:
            tk.Label(self.order_list_frame, text="暂无订单",
                     font=('Microsoft YaHei', 14),
                     bg=COLORS['bg'], fg=COLORS['text_light']).pack(pady=50)
            return

        for order in orders:
            card = tk.Frame(self.order_list_frame, bg=COLORS['white'], padx=20, pady=15)
            card.pack(fill=tk.X, pady=5)

            # 订单头部
            header = tk.Frame(card, bg=COLORS['white'])
            header.pack(fill=tk.X)

            tk.Label(header, text=f"📦 {order['order_no']}",
                     font=('Microsoft YaHei', 12, 'bold'),
                     bg=COLORS['white'], fg=COLORS['text']).pack(side=tk.LEFT)

            status_colors = {
                'pending': COLORS['warning'], 'confirmed': COLORS['secondary'],
                'preparing': COLORS['primary'], 'delivering': '#3498DB',
                'completed': COLORS['success'], 'cancelled': COLORS['danger']
            }
            status_names = {
                'pending': '待确认', 'confirmed': '已确认',
                'preparing': '准备中', 'delivering': '配送中',
                'completed': '已完成', 'cancelled': '已取消'
            }

            status_label = tk.Label(header, text=status_names.get(order['status'], order['status']),
                                    font=('Microsoft YaHei', 10, 'bold'),
                                    bg=status_colors.get(order['status'], COLORS['border']),
                                    fg='white', padx=10, pady=2)
            status_label.pack(side=tk.RIGHT)

            # 订单信息
            tk.Label(card, text=f"🏪 {order['restaurant_name']}",
                     font=('Microsoft YaHei', 11),
                     bg=COLORS['white'], fg=COLORS['text']).pack(anchor=tk.W, pady=(10, 0))

            tk.Label(card, text=f"📍 {order['address']}",
                     font=('Microsoft YaHei', 10),
                     bg=COLORS['white'], fg=COLORS['text_light']).pack(anchor=tk.W)

            # 订单详情
            items = OrderService.get_order_items(order['id'])
            items_text = "、".join([f"{item['dish_name']}×{item['quantity']}" for item in items])
            tk.Label(card, text=f"🍽️ {items_text}",
                     font=('Microsoft YaHei', 10),
                     bg=COLORS['white'], fg=COLORS['text_light']).pack(anchor=tk.W)

            # 底部
            bottom = tk.Frame(card, bg=COLORS['white'])
            bottom.pack(fill=tk.X, pady=(10, 0))

            tk.Label(bottom, text=f"¥{order['total_price']:.2f}",
                     font=('Microsoft YaHei', 14, 'bold'),
                     bg=COLORS['white'], fg=COLORS['danger']).pack(side=tk.LEFT)

            tk.Label(bottom, text=order['created_at'][:16] if order['created_at'] else "",
                     font=('Microsoft YaHei', 9),
                     bg=COLORS['white'], fg=COLORS['text_light']).pack(side=tk.LEFT, padx=20)

            # 操作按钮
            if order['status'] == 'pending':
                tk.Button(bottom, text="取消订单", font=('Microsoft YaHei', 9),
                          bg=COLORS['danger'], fg='white', relief=tk.FLAT,
                          command=lambda oid=order['id']: self._cancel_order(oid)).pack(side=tk.RIGHT)

            if order['status'] == 'completed':
                tk.Button(bottom, text="评价", font=('Microsoft YaHei', 9),
                          bg=COLORS['secondary'], fg='white', relief=tk.FLAT,
                          command=lambda o=order: self._show_review_dialog(o)).pack(side=tk.RIGHT, padx=5)

    def _filter_orders(self, status):
        """筛选订单"""
        self._load_orders(status if status != "全部" else None)

    def _cancel_order(self, order_id):
        """取消订单"""
        if messagebox.askyesno("确认", "确定要取消该订单吗？"):
            success, msg = OrderService.cancel_order(order_id, self.current_user.id)
            if success:
                messagebox.showinfo("成功", msg)
                self._load_orders()
            else:
                messagebox.showerror("错误", msg)

    def _show_review_dialog(self, order):
        """显示评价对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("评价订单")
        dialog.geometry("400x350")
        dialog.configure(bg=COLORS['white'])

        tk.Label(dialog, text="⭐ 评分", font=('Microsoft YaHei', 14, 'bold'),
                 bg=COLORS['white']).pack(pady=(20, 10))

        rating_var = tk.IntVar(value=5)
        rating_frame = tk.Frame(dialog, bg=COLORS['white'])
        rating_frame.pack()

        for i in range(1, 6):
            tk.Radiobutton(rating_frame, text=f"{i}星", variable=rating_var, value=i,
                           font=('Microsoft YaHei', 11), bg=COLORS['white']).pack(side=tk.LEFT, padx=10)

        tk.Label(dialog, text="评价内容", font=('Microsoft YaHei', 14, 'bold'),
                 bg=COLORS['white']).pack(pady=(20, 10))

        review_text = tk.Text(dialog, font=('Microsoft YaHei', 11), width=40, height=5,
                              relief=tk.SOLID, bd=1)
        review_text.pack(padx=20)

        def submit_review():
                success = ReviewService.add_review(
                    order['id'], self.current_user.id, order['restaurant_id'],
                    rating_var.get(), review_text.get("1.0", tk.END).strip()
                )
                if success:
                    messagebox.showinfo("成功", "评价成功！")
                    dialog.destroy()
                else:
                    messagebox.showerror("错误", "评价失败")

        tk.Button(dialog, text="提交评价", font=('Microsoft YaHei', 12, 'bold'),
                  bg=COLORS['primary'], fg='white', relief=tk.FLAT,
                  command=submit_review).pack(pady=20)

    # ==================== 个人中心 ====================
    def _show_profile_page(self):
        """显示个人中心"""
        self._clear_window()

        nav_frame = tk.Frame(self.root, bg=COLORS['white'], height=60)
        nav_frame.pack(fill=tk.X)
        nav_frame.pack_propagate(False)

        back_btn = tk.Button(nav_frame, text="← 返回", font=('Microsoft YaHei', 11),
                             bg=COLORS['white'], fg=COLORS['primary'], relief=tk.FLAT,
                             cursor='hand2', command=self._show_main_page)
        back_btn.pack(side=tk.LEFT, padx=20)

        tk.Label(nav_frame, text="👤 个人中心",
                 font=('Microsoft YaHei', 16, 'bold'),
                 bg=COLORS['white'], fg=COLORS['text']).pack(side=tk.LEFT, padx=20)

        content_frame = tk.Frame(self.root, bg=COLORS['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 用户信息卡
        user_card = tk.Frame(content_frame, bg=COLORS['white'], padx=30, pady=25)
        user_card.pack(fill=tk.X, pady=(0, 20))

        tk.Label(user_card, text=f"👤 {self.current_user.username}",
                 font=('Microsoft YaHei', 20, 'bold'),
                 bg=COLORS['white'], fg=COLORS['text']).pack(anchor=tk.W)

        tk.Label(user_card, text=f"📱 {self.current_user.phone or '未设置'}",
                 font=('Microsoft YaHei', 12),
                 bg=COLORS['white'], fg=COLORS['text_light']).pack(anchor=tk.W, pady=(10, 0))

        tk.Label(user_card, text=f"📍 {self.current_user.address or '未设置'}",
                 font=('Microsoft YaHei', 12),
                 bg=COLORS['white'], fg=COLORS['text_light']).pack(anchor=tk.W, pady=(5, 0))

        # 功能菜单
        menu_items = [
            ("📋 我的订单", self._show_orders_page),
            ("🛒 购物车", self._show_cart_page),
            ("✏️ 修改资料", self._show_edit_profile),
            ("📊 数据统计", self._show_stats_page),
            ("🚪 退出登录", self._handle_logout),
        ]

        for text, command in menu_items:
            btn = tk.Button(content_frame, text=text, font=('Microsoft YaHei', 13),
                            bg=COLORS['white'], fg=COLORS['text'], relief=tk.FLAT,
                            cursor='hand2', anchor=tk.W, padx=30, pady=15,
                            command=command)
            btn.pack(fill=tk.X, pady=3)

    def _show_edit_profile(self):
        """修改资料页面"""
        self._clear_window()

        main_frame = tk.Frame(self.root, bg=COLORS['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="✏️ 修改资料", font=('Microsoft YaHei', 20, 'bold'),
                 bg=COLORS['bg'], fg=COLORS['text']).pack(pady=(30, 20))

        form_frame = tk.Frame(main_frame, bg=COLORS['white'], padx=40, pady=30)
        form_frame.pack(fill=tk.X, padx=50)

        tk.Label(form_frame, text="手机号", font=('Microsoft YaHei', 12, 'bold'),
                 bg=COLORS['white']).pack(anchor=tk.W)
        phone_entry = tk.Entry(form_frame, font=('Microsoft YaHei', 12), width=50, relief=tk.SOLID, bd=1)
        phone_entry.insert(0, self.current_user.phone or "")
        phone_entry.pack(fill=tk.X, pady=(5, 15), ipady=8)

        tk.Label(form_frame, text="地址", font=('Microsoft YaHei', 12, 'bold'),
                 bg=COLORS['white']).pack(anchor=tk.W)
        addr_entry = tk.Entry(form_frame, font=('Microsoft YaHei', 12), width=50, relief=tk.SOLID, bd=1)
        addr_entry.insert(0, self.current_user.address or "")
        addr_entry.pack(fill=tk.X, pady=(5, 15), ipady=8)

        def save_profile():
            success = UserService.update_profile(
                self.current_user.id,
                phone=phone_entry.get().strip(),
                address=addr_entry.get().strip()
            )
            if success:
                self.current_user._phone = phone_entry.get().strip()
                self.current_user._address = addr_entry.get().strip()
                messagebox.showinfo("成功", "资料更新成功")
                self._show_profile_page()
            else:
                messagebox.showerror("错误", "更新失败")

        tk.Button(form_frame, text="保存修改", font=('Microsoft YaHei', 13, 'bold'),
                  bg=COLORS['primary'], fg='white', relief=tk.FLAT, padx=30, pady=10,
                  command=save_profile).pack(pady=(10, 0))

    def _show_stats_page(self):
        """数据统计页面"""
        self._clear_window()

        nav_frame = tk.Frame(self.root, bg=COLORS['white'], height=60)
        nav_frame.pack(fill=tk.X)
        nav_frame.pack_propagate(False)

        back_btn = tk.Button(nav_frame, text="← 返回", font=('Microsoft YaHei', 11),
                             bg=COLORS['white'], fg=COLORS['primary'], relief=tk.FLAT,
                             cursor='hand2', command=self._show_profile_page)
        back_btn.pack(side=tk.LEFT, padx=20)

        tk.Label(nav_frame, text="📊 数据统计",
                 font=('Microsoft YaHei', 16, 'bold'),
                 bg=COLORS['white'], fg=COLORS['text']).pack(side=tk.LEFT, padx=20)

        content_frame = tk.Frame(self.root, bg=COLORS['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 获取统计数据
        order_stats = StatsService.get_order_stats()
        restaurant_stats = StatsService.get_restaurant_stats()
        popular_dishes = StatsService.get_popular_dishes()

        # 订单统计卡
        stats_card = tk.Frame(content_frame, bg=COLORS['white'], padx=25, pady=20)
        stats_card.pack(fill=tk.X, pady=(0, 15))

        tk.Label(stats_card, text="📦 订单概览", font=('Microsoft YaHei', 14, 'bold'),
                 bg=COLORS['white']).pack(anchor=tk.W, pady=(0, 10))

        stats_grid = tk.Frame(stats_card, bg=COLORS['white'])
        stats_grid.pack(fill=tk.X)

        stat_items = [
            ("总订单数", str(order_stats['total_orders']), "📦"),
            ("总营业额", f"¥{order_stats['total_amount']}", "💰"),
            ("平均订单金额", f"¥{order_stats['avg_amount']}", "📊"),
        ]

        for i, (label, value, emoji) in enumerate(stat_items):
            item_frame = tk.Frame(stats_grid, bg=COLORS['light_gray'], padx=20, pady=15)
            item_frame.grid(row=0, column=i, padx=5, sticky=tk.NSEW)
            stats_grid.grid_columnconfigure(i, weight=1)

            tk.Label(item_frame, text=emoji, font=('Arial', 24),
                     bg=COLORS['light_gray']).pack()
            tk.Label(item_frame, text=value, font=('Microsoft YaHei', 18, 'bold'),
                     bg=COLORS['light_gray'], fg=COLORS['primary']).pack()
            tk.Label(item_frame, text=label, font=('Microsoft YaHei', 10),
                     bg=COLORS['light_gray'], fg=COLORS['text_light']).pack()

        # 各状态订单
        status_card = tk.Frame(content_frame, bg=COLORS['white'], padx=25, pady=20)
        status_card.pack(fill=tk.X, pady=(0, 15))

        tk.Label(status_card, text="📈 订单状态分布", font=('Microsoft YaHei', 14, 'bold'),
                 bg=COLORS['white']).pack(anchor=tk.W, pady=(0, 10))

        status_names = {
            'pending': '待确认', 'confirmed': '已确认',
            'preparing': '准备中', 'delivering': '配送中',
            'completed': '已完成', 'cancelled': '已取消'
        }
        status_colors = {
            'pending': '#F39C12', 'confirmed': '#3498DB',
            'preparing': '#E67E22', 'delivering': '#2ECC71',
            'completed': '#27AE60', 'cancelled': '#E74C3C'
        }

        for status, count in order_stats.get('status_counts', {}).items():
            row = tk.Frame(status_card, bg=COLORS['white'])
            row.pack(fill=tk.X, pady=3)

            tk.Label(row, text=f"  {status_names.get(status, status)}",
                     font=('Microsoft YaHei', 11), width=12, anchor=tk.W,
                     bg=COLORS['white']).pack(side=tk.LEFT)

            # 进度条
            bar_bg = tk.Frame(row, bg=COLORS['border'], height=20, width=300)
            bar_bg.pack(side=tk.LEFT, padx=10)
            bar_bg.pack_propagate(False)

            max_count = max(order_stats.get('status_counts', {}).values(), default=1)
            bar_width = max(int(300 * count / max_count), 5)
            bar = tk.Frame(bar_bg, bg=status_colors.get(status, COLORS['primary']),
                           height=20, width=bar_width)
            bar.place(x=0, y=0)

            tk.Label(row, text=str(count), font=('Microsoft YaHei', 11, 'bold'),
                     bg=COLORS['white'], fg=COLORS['primary']).pack(side=tk.LEFT, padx=5)

        # 热门菜品
        hot_card = tk.Frame(content_frame, bg=COLORS['white'], padx=25, pady=20)
        hot_card.pack(fill=tk.X, pady=(0, 15))

        tk.Label(hot_card, text="🔥 热门菜品 TOP10", font=('Microsoft YaHei', 14, 'bold'),
                 bg=COLORS['white']).pack(anchor=tk.W, pady=(0, 10))

        for i, dish in enumerate(popular_dishes):
            row = tk.Frame(hot_card, bg=COLORS['white'])
            row.pack(fill=tk.X, pady=2)

            medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"{i+1}."
            tk.Label(row, text=f" {medal} {dish['name']}",
                     font=('Microsoft YaHei', 11), width=25, anchor=tk.W,
                     bg=COLORS['white']).pack(side=tk.LEFT)

            tk.Label(row, text=dish['restaurant_name'],
                     font=('Microsoft YaHei', 10), width=15, anchor=tk.W,
                     bg=COLORS['white'], fg=COLORS['text_light']).pack(side=tk.LEFT)

            tk.Label(row, text=f"¥{dish['price']}",
                     font=('Microsoft YaHei', 11), width=10,
                     bg=COLORS['white'], fg=COLORS['danger']).pack(side=tk.LEFT)

            tk.Label(row, text=f"销量 {dish['sales_count']}",
                     font=('Microsoft YaHei', 10),
                     bg=COLORS['white'], fg=COLORS['text_light']).pack(side=tk.LEFT, padx=10)

        # 餐厅销售排行
        rest_card = tk.Frame(content_frame, bg=COLORS['white'], padx=25, pady=20)
        rest_card.pack(fill=tk.X, pady=(0, 15))

        tk.Label(rest_card, text="🏪 餐厅销售排行", font=('Microsoft YaHei', 14, 'bold'),
                 bg=COLORS['white']).pack(anchor=tk.W, pady=(0, 10))

        for i, stat in enumerate(restaurant_stats):
            row = tk.Frame(rest_card, bg=COLORS['white'])
            row.pack(fill=tk.X, pady=2)

            tk.Label(row, text=f" {i+1}. {stat['name']}",
                     font=('Microsoft YaHei', 11), width=20, anchor=tk.W,
                     bg=COLORS['white']).pack(side=tk.LEFT)

            tk.Label(row, text=f"⭐{stat['rating']}",
                     font=('Microsoft YaHei', 10), width=8,
                     bg=COLORS['white'], fg=COLORS['star']).pack(side=tk.LEFT)

            tk.Label(row, text=f"订单 {stat['order_count']}",
                     font=('Microsoft YaHei', 10), width=10,
                     bg=COLORS['white']).pack(side=tk.LEFT)

            tk.Label(row, text=f"营收 ¥{stat['total_revenue']:.2f}",
                     font=('Microsoft YaHei', 10),
                     bg=COLORS['white'], fg=COLORS['danger']).pack(side=tk.LEFT, padx=10)

    # ==================== 管理员页面 ====================
    def _show_admin_page(self):
        """管理员后台"""
        self._clear_window()

        nav_frame = tk.Frame(self.root, bg=COLORS['primary'], height=60)
        nav_frame.pack(fill=tk.X)
        nav_frame.pack_propagate(False)

        tk.Label(nav_frame, text="🔧 管理后台",
                 font=('Microsoft YaHei', 16, 'bold'),
                 bg=COLORS['primary'], fg='white').pack(side=tk.LEFT, padx=20)

        tk.Label(nav_frame, text=f"管理员: {self.current_user.username}",
                 font=('Microsoft YaHei', 11),
                 bg=COLORS['primary'], fg='white').pack(side=tk.RIGHT, padx=20)

        tk.Button(nav_frame, text="退出", font=('Microsoft YaHei', 10),
                  bg=COLORS['danger'], fg='white', relief=tk.FLAT,
                  command=self._handle_logout).pack(side=tk.RIGHT, padx=5)

        # 内容区域
        content_frame = tk.Frame(self.root, bg=COLORS['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 功能面板
        panels = [
            ("👥 用户管理", "查看和管理所有用户", self._admin_users),
            ("🏪 餐厅管理", "查看和管理餐厅信息", self._admin_restaurants),
            ("📦 订单管理", "查看和处理所有订单", self._admin_orders),
            ("📊 数据统计", "查看系统数据统计", self._show_stats_page),
        ]

        for i, (title, desc, command) in enumerate(panels):
            card = tk.Frame(content_frame, bg=COLORS['white'], padx=25, pady=20)
            card.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky=tk.NSEW)
            content_frame.grid_columnconfigure(0, weight=1)
            content_frame.grid_columnconfigure(1, weight=1)

            tk.Label(card, text=title, font=('Microsoft YaHei', 16, 'bold'),
                     bg=COLORS['white'], fg=COLORS['text']).pack(anchor=tk.W)

            tk.Label(card, text=desc, font=('Microsoft YaHei', 11),
                     bg=COLORS['white'], fg=COLORS['text_light']).pack(anchor=tk.W, pady=(10, 15))

            tk.Button(card, text="进入管理", font=('Microsoft YaHei', 11),
                      bg=COLORS['primary'], fg='white', relief=tk.FLAT,
                      command=command).pack(anchor=tk.E)

    def _admin_users(self):
        """管理员 - 用户管理"""
        self._clear_window()

        nav_frame = tk.Frame(self.root, bg=COLORS['white'], height=60)
        nav_frame.pack(fill=tk.X)
        nav_frame.pack_propagate(False)

        tk.Button(nav_frame, text="← 返回", font=('Microsoft YaHei', 11),
                  bg=COLORS['white'], fg=COLORS['primary'], relief=tk.FLAT,
                  command=self._show_admin_page).pack(side=tk.LEFT, padx=20)

        tk.Label(nav_frame, text="👥 用户管理",
                 font=('Microsoft YaHei', 16, 'bold'),
                 bg=COLORS['white'], fg=COLORS['text']).pack(side=tk.LEFT, padx=20)

        content_frame = tk.Frame(self.root, bg=COLORS['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        users = UserService.get_all_users()

        # 用户表格
        columns = ('ID', '用户名', '角色', '手机号', '余额', '注册时间')
        tree = ttk.Treeview(content_frame, columns=columns, show='headings', height=20)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.CENTER)

        for user in users:
            tree.insert('', tk.END, values=(
                user['id'], user['username'], user['role'],
                user['phone'] or '', f"¥{user['balance']:.2f}",
                user['created_at'][:10] if user['created_at'] else ''
            ))

        tree.pack(fill=tk.BOTH, expand=True)

    def _admin_restaurants(self):
        """管理员 - 餐厅管理"""
        self._clear_window()

        nav_frame = tk.Frame(self.root, bg=COLORS['white'], height=60)
        nav_frame.pack(fill=tk.X)
        nav_frame.pack_propagate(False)

        tk.Button(nav_frame, text="← 返回", font=('Microsoft YaHei', 11),
                  bg=COLORS['white'], fg=COLORS['primary'], relief=tk.FLAT,
                  command=self._show_admin_page).pack(side=tk.LEFT, padx=20)

        tk.Label(nav_frame, text="🏪 餐厅管理",
                 font=('Microsoft YaHei', 16, 'bold'),
                 bg=COLORS['white'], fg=COLORS['text']).pack(side=tk.LEFT, padx=20)

        content_frame = tk.Frame(self.root, bg=COLORS['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        restaurants = RestaurantService.get_all_restaurants()

        columns = ('ID', '名称', '分类', '评分', '月销量', '配送费', '起送价')
        tree = ttk.Treeview(content_frame, columns=columns, show='headings', height=20)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.CENTER)

        for r in restaurants:
            tree.insert('', tk.END, values=(
                r.id, r.name, r.category, f"⭐{r.rating}",
                r.monthly_sales, f"¥{r.delivery_fee}", f"¥{r.min_order}"
            ))

        tree.pack(fill=tk.BOTH, expand=True)

    def _admin_orders(self):
        """管理员 - 订单管理"""
        self._clear_window()

        nav_frame = tk.Frame(self.root, bg=COLORS['white'], height=60)
        nav_frame.pack(fill=tk.X)
        nav_frame.pack_propagate(False)

        tk.Button(nav_frame, text="← 返回", font=('Microsoft YaHei', 11),
                  bg=COLORS['white'], fg=COLORS['primary'], relief=tk.FLAT,
                  command=self._show_admin_page).pack(side=tk.LEFT, padx=20)

        tk.Label(nav_frame, text="📦 订单管理",
                 font=('Microsoft YaHei', 16, 'bold'),
                 bg=COLORS['white'], fg=COLORS['text']).pack(side=tk.LEFT, padx=20)

        content_frame = tk.Frame(self.root, bg=COLORS['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        orders = OrderService.get_all_orders()

        columns = ('订单号', '用户', '餐厅', '金额', '状态', '时间')
        tree = ttk.Treeview(content_frame, columns=columns, show='headings', height=20)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140, anchor=tk.CENTER)

        status_names = {
            'pending': '待确认', 'confirmed': '已确认',
            'preparing': '准备中', 'delivering': '配送中',
            'completed': '已完成', 'cancelled': '已取消'
        }

        for o in orders:
            tree.insert('', tk.END, values=(
                o['order_no'], o.get('username', ''), o['restaurant_name'],
                f"¥{o['total_price']:.2f}", status_names.get(o['status'], o['status']),
                o['created_at'][:16] if o['created_at'] else ''
            ))

        tree.pack(fill=tk.BOTH, expand=True)

        # 操作按钮
        btn_frame = tk.Frame(content_frame, bg=COLORS['bg'])
        btn_frame.pack(fill=tk.X, pady=10)

        def confirm_selected():
            selected = tree.selection()
            if selected:
                for item in selected:
                    order_no = tree.item(item)['values'][0]
                    # 查找订单ID
                    for o in orders:
                        if o['order_no'] == order_no:
                            OrderService.update_order_status(o['id'], 'confirmed')
                            break
                messagebox.showinfo("成功", "已确认选中订单")
                self._admin_orders()

        tk.Button(btn_frame, text="确认选中订单", font=('Microsoft YaHei', 11),
                  bg=COLORS['success'], fg='white', relief=tk.FLAT,
                  command=confirm_selected).pack(side=tk.LEFT, padx=5)

        def deliver_selected():
            selected = tree.selection()
            if selected:
                for item in selected:
                    order_no = tree.item(item)['values'][0]
                    for o in orders:
                        if o['order_no'] == order_no:
                            OrderService.update_order_status(o['id'], 'delivering')
                            break
                messagebox.showinfo("成功", "已标记为配送中")
                self._admin_orders()

        tk.Button(btn_frame, text="标记配送中", font=('Microsoft YaHei', 11),
                  bg=COLORS['secondary'], fg='white', relief=tk.FLAT,
                  command=deliver_selected).pack(side=tk.LEFT, padx=5)

    def _handle_logout(self):
        """退出登录"""
        if messagebox.askyesno("确认", "确定要退出登录吗？"):
            self.current_user = None
            self._show_login_page()

    def run(self):
        """运行应用"""
        self.root.mainloop()


if __name__ == "__main__":
    app = FoodDeliveryApp()
    app.run()
