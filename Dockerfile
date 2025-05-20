FROM python:3.9-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 确保数据目录存在
RUN mkdir -p /app/data

# 暴露端口
EXPOSE 8000

# 设置挂载点
VOLUME ["/app/data"]

# 启动命令
CMD ["python", "main.py", "--host", "0.0.0.0"]
