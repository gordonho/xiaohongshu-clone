#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""批量创建示例笔记"""

import os
import django
import sys

# 设置 Django 环境
sys.path.insert(0, '/Users/gordon/clawd-coding/xiaohongshu')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xiaohongshu.settings')
django.setup()

from django.contrib.auth.models import User
from posts.models import Post

# 创建示例用户（如果不存在）
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_user(username='admin', password='admin123', email='admin@example.com')
    print(f"Created user: {user.username}")
else:
    user = User.objects.get(username='admin')

# 示例笔记数据
sample_posts = [
    {
        "title": "2026年最火的AI工具合集",
        "content": """最近AI工具真的是层出不穷！今天给大家整理一下我日常在用的几款神器：

1. ChatGPT - 写作助手NO.1
2. Midjourney - 设计出图神器
3. Claude - 编程最佳伴侣
4. Notion AI - 笔记整理利器

每个工具都有自己的特色，关键是找到适合自己的那一款！

#AI工具 #效率提升 #科技""",
        "tags": "AI工具,效率提升,科技,2026"
    },
    {
        "title": "月薪3万的副业分享",
        "content": """今天聊聊我是怎么做副业的~

其实副业真的不难，关键是要找对方向：

1. 短视频带货 - 我做了3个月现在每月稳定5000+
2. 知识付费 - 把自己的经验整理成课程
3. 接私活 - 利用业余时间接设计单

最重要的是行动力！不要只是想，要去做！

#副业 #赚钱 #职场""",
        "tags": "副业,赚钱,职场,分享"
    },
    {
        "title": "租房必看避坑指南",
        "content": """租房这么多年，总结出来的血泪经验分享给大家：

1. 看房一定要白天去，晚上也要去一次
2. 检查水电表、门窗、厨卫
3. 合同一定要仔细看，不要签阴阳合同
4. 最好拍照留底

希望对租房的朋友有帮助！

#租房 #避坑指南 #生活""",
        "tags": "租房,避坑,生活,经验"
    },
    {
        "title": "超级好吃的红烧肉家常做法",
        "content": """今天在家做了红烧肉，秘诀在于：

1. 选五花肉要肥瘦相间的
2. 先焯水去腥
3. 炒糖色要小火慢熬
4. 加啤酒炖煮更香

做出来的肉软糯入口即化，老人小孩都爱吃！

#美食 #红烧肉 #家常菜""",
        "tags": "美食,红烧肉,做法,家常菜"
    },
    {
        "title": "iPhone使用小技巧",
        "content": """用了这么多年iPhone，这些技巧你可能不知道：

1. 摇晃撤销 - 写错字摇晃手机可撤销
2. 滚动截屏 - 截长图超方便
3. 快捷指令 - 自动化任务
4. 专注模式 - 减少干扰

学会这些效率翻倍！

#iPhone #技巧 #数码""",
        "tags": "iPhone,技巧,数码,科技"
    },
    {
        "title": "居家健身计划",
        "content": """分享我的居家健身计划：

周一：胸部+三头
周二：背部+二头
周三：肩部+核心
周四：休息
周五：臀部+腿部
周六：全身综合
周日：休息

不需要器械，徒手也能练！

#健身 #居家运动 #健康""",
        "tags": "健身,运动,健康,居家"
    },
    {
        "title": "2026年书单推荐",
        "content": """今年读过的最值得推荐的书：

1. 《原子习惯》- 习惯养成
2. 《深度工作》- 专注力
3. 《富爸爸穷爸爸》- 财商
4. 《被讨厌的勇气》- 心理学

每本都值得反复阅读！

#读书 #书单 #成长""",
        "tags": "读书,书单,推荐,成长"
    },
    {
        "title": "上海旅游攻略",
        "content": """上海三日游保姆级攻略：

Day1：外滩-陆家嘴-东方明珠
Day2：迪士尼乐园全天
Day3：田子坊-武康路-豫园

美食推荐：
- 小杨生煎
- 南翔馒头
- 光明邨

避坑提醒：不要在景区买特产！

#上海 #旅游攻略 #魔都""",
        "tags": "上海,旅游,攻略,美食"
    },
    {
        "title": "程序员必看学习资源",
        "content": """分享我常用的学习网站：

1. LeetCode - 算法刷题
2. GitHub - 开源代码
3. Stack Overflow - 问题解答
4. MDN Web Docs - 前端文档

还有几个不错的B站UP主推荐...

#程序员 #学习 #编程""",
        "tags": "程序员,学习,编程,资源"
    },
    {
        "title": "咖啡新手入门指南",
        "content": """咖啡小白必看：

1. 意式浓缩 - 基础款
2. 美式 - 稀释版意式
3. 拿铁 - 浓缩+牛奶
4. 摩卡 - 浓缩+巧克力+牛奶

手冲器具推荐：
- V60
- Kalita Wave
- 法压壶

#咖啡 #饮品 #生活""",
        "tags": "咖啡,饮品,教程,生活"
    },
]

# 批量创建笔记
created_count = 0
for post_data in sample_posts:
    post, created = Post.objects.get_or_create(
        title=post_data["title"],
        author=user,
        defaults={
            "content": post_data["content"],
            "tags": post_data["tags"]
        }
    )
    if created:
        created_count += 1
        print(f"Created: {post.title}")

print(f"\n总共创建了 {created_count} 篇笔记")

