"""
外卖系统 - 主程序入口
Python课程实践项目

功能特性:
- 用户注册/登录（角色：顾客、管理员、配送员）
- 餐厅浏览与搜索（分类筛选、关键词搜索）
- 菜品浏览与购物车管理
- 订单创建与管理（多线程异步处理）
- 评价系统
- 数据统计与可视化
- 管理员后台

技术栈:
- Python 3.x
- Tkinter (GUI)
- SQLite (数据库)
- Threading (多线程)
- Matplotlib (数据可视化)

知识点覆盖:
- 序列（列表、字典、元组）
- 函数与模块
- 面向对象编程（类、继承、封装、多态）
- 数据库操作（SQLite）
- 多线程
- 异常处理
- 图形用户界面设计（Tkinter）
"""

import os
import sys

# 确保路径正确
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import init_db, insert_sample_data
from app import FoodDeliveryApp
from visualization import generate_all_charts


def main():
    """主函数"""
    print("=" * 50)
    print("  🛵 外卖订餐系统 v1.0")
    print("  Food Delivery System")
    print("=" * 50)

    # 初始化数据库
    print("\n📦 正在初始化数据库...")
    init_db()
    insert_sample_data()
    print("✅ 数据库初始化完成")

    # 生成统计图表（可选）
    try:
        generate_all_charts()
    except Exception as e:
        print(f"⚠️ 图表生成跳过: {e}")

    # 启动GUI应用
    print("\n🚀 正在启动应用...")
    app = FoodDeliveryApp()
    app.run()


if __name__ == "__main__":
    main()
