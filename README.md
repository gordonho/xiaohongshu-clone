# 小红书类社交平台 - Xiaohongshu Clone

基于 Django 的社交分享平台，类似于小红书的核心功能。

## 功能特性

- 📝 发布笔记（支持图片）
- ❤️ 点赞、收藏、评论
- 👥 用户关注系统
- 🏠 首页个性化推荐流
- 🔍 搜索用户和内容
- 👤 用户个人主页

## 技术栈

- Python 3.x
- Django 4.x
- SQLite（默认）/ PostgreSQL
- HTML/CSS/JavaScript

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/你的用户名/xiaohongshu-clone.git
cd xiaohongshu-clone
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 运行迁移

```bash
python manage.py migrate
```

### 5. 创建超级用户

```bash
python manage.py createsuperuser
```

### 6. 启动服务器

```bash
python manage.py runserver
```

访问 http://127.0.0.1:8000

## 项目结构

```
xiaohongshu/
├── accounts/          # 用户认证模块
│   ├── models.py      # 用户模型扩展
│   ├── views.py       # 视图函数
│   └── urls.py        # 路由配置
├── posts/             # 笔记模块
│   ├── models.py      # 帖子、评论、点赞模型
│   ├── views.py       # 视图函数
│   └── urls.py        # 路由配置
├──xiaohongshu/        # 项目配置
│   ├── settings.py    # Django 设置
│   └── urls.py        # 主路由
├── static/            # 静态文件
└── templates/        # 模板文件
```

## API 端点

| 功能 | 方法 | URL |
|------|------|-----|
| 首页 | GET | / |
| 注册 | GET/POST | /accounts/signup/ |
| 登录 | GET/POST | /accounts/login/ |
| 发布笔记 | POST | /posts/create/ |
| 点赞 | POST | /posts/like/{id}/ |
| 收藏 | POST | /posts/collect/{id}/ |
| 评论 | POST | /posts/comment/{id}/ |
| 关注 | POST | /accounts/follow/{id}/ |
| 个人主页 | GET | /user/{username}/ |

## 截图

![首页](screenshots/home.png)
![笔记详情](screenshots/post.png)

## License

MIT License
