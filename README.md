# 外卖点餐系统 · Food Delivery System

> Python + Tkinter + SQLite 的桌面外卖系统：登录/注册、餐厅浏览、菜品、购物车、下单、订单管理、评价、管理后台与统计。

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-BC744A)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-2F6B5F)

## 功能

- 用户注册/登录，顾客/管理员角色
- 餐厅列表、菜品浏览、搜索
- 购物车、数量修改、下单
- 订单列表/详情/状态流转
- 评价与评分
- 管理后台：餐厅/菜品/订单/统计
- SQLite 本地数据库，首次运行自动建表并插入示例数据

## 技术栈

| 模块 | 技术 |
|---|---|
| GUI | Python Tkinter / ttk |
| 数据库 | SQLite |
| 架构 | models / services / database 分层 |
| 图表 | matplotlib（统计/架构图脚本） |

## 运行

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install matplotlib

python main.py
# 或
python app.py
```

程序会自动创建 `food_delivery.db` 并写入示例数据。

## 目录结构

```text
food-delivery-system/
├── main.py                  # 入口
├── app.py                   # Tkinter GUI
├── database.py              # 建表/示例数据
├── models.py                # 用户/餐厅/菜品/订单/评价
├── services.py              # 业务服务
├── architecture_diagrams.py # 架构图生成
├── visualization.py         # 统计可视化
├── requirements.txt
└── README.md
```

## 测试与验收

```bash
python -m py_compile app.py database.py models.py services.py main.py
```

手工验收：

- [ ] 启动后出现登录页
- [ ] 注册/登录顾客
- [ ] 浏览餐厅/菜品，加入购物车
- [ ] 下单，订单列表可见
- [ ] 管理员登录，管理餐厅/菜品/订单
- [ ] 统计图表可生成

## 说明

- 示例数据仅用于演示；生产需接入真实支付、配送与权限系统。
- 数据库文件 `food_delivery.db` 为运行产物，已加入 `.gitignore`。

## License

MIT License，详见 [LICENSE](LICENSE)。


---

## 数据模型与业务流程

```text
User (顾客/管理员)
  └─ Restaurant 1─N Dish
  └─ CartItem N─1 Dish
  └─ Order 1─N OrderItem
  └─ Review N─1 Restaurant/Dish
```

1. 顾客登录/注册 → 浏览餐厅与菜品 → 加入购物车
2. 提交订单 → 生成订单明细与总价
3. 管理员查看/更新订单状态
4. 顾客确认收货并评价
5. 管理后台查看统计

## 常见问题

- **启动报错 Tkinter 不存在**：Linux 安装 `python3-tk`；Windows 官方 Python 自带。
- **数据库损坏**：删除 `food_delivery.db` 后重新启动，会自动建表并写入示例数据。
- **中文乱码**：使用 Python 3.10+，文件按 UTF-8 保存。

## 扩展计划

- 接入真实支付/配送 API
- 增加商家端与骑手端
- 使用 FastAPI + React 重构为 Web 版
