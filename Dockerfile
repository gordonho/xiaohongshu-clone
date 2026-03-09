FROM python:3.14-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建媒体目录
RUN mkdir -p media/avatars staticfiles

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=xiaohongshu.settings

# 暴露端口
EXPOSE 8000

# 运行迁移和启动服务器
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn xiaohongshu.wsgi:application --bind 0.0.0.0:8000"]
