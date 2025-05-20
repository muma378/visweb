# VisWeb

VisWeb是一个个人健康和健身追踪API，允许您通过简单的API记录和可视化健康指标和运动数据。它旨在通过强大的API和Grafana可视化支持，使个人数据追踪变得简单。

## 特性

- 用于追踪健康指标的RESTful API（体重、心率、睡眠等）
- 追踪运动数据（跑步、骑行等）的持续时间、距离和卡路里消耗
- 通过URL参数快速记录数据，便于数据收集
- 使用SQLite数据库实现简单的设置和维护
- OpenAPI文档（Swagger UI）
- Grafana集成实现数据可视化

## 安装与部署

### 从GitHub容器注册表拉取（最简单）

如果您只想使用该服务而不需要修改代码，可以直接从GitHub容器注册表拉取镜像：

```bash
# 替换 username 为实际的GitHub用户名
docker pull ghcr.io/username/visweb:latest
```

然后创建一个docker-compose.yml文件：

```yaml
version: '3.8'

services:
  visweb:
    image: ghcr.io/username/visweb:latest
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
```

运行 `docker-compose up -d` 启动服务。

### 使用Docker（推荐）

如果您想自己构建镜像：

1. 确保已安装Docker和Docker Compose
2. 运行提供的启动脚本：

```bash
./start.sh
```

3. 通过脚本菜单选择"构建并启动所有服务"选项
4. 初始化数据库（从脚本菜单中选择）

详细的Docker部署说明可以在[Docker部署文档](docs/docker_deployment.md)中找到。

### 持续集成/持续部署

本项目配置了GitHub Actions用于自动化测试和镜像构建。每次推送到主分支或创建标签时，都会：

1. 运行所有单元测试
2. 构建Docker镜像
3. 将镜像推送到GitHub容器注册表(GHCR)

更多信息请参阅[GitHub Actions文档](docs/github_actions.md)。

### 手动安装

1. 克隆仓库
2. 安装所需依赖：

```bash
pip install -r requirements.txt
```

3. 复制示例环境文件：

```bash
cp .env.example .env
```

4. 启动应用程序：

```bash
python main.py
```

## 快速开始

启动应用程序后，您可以：

1. 访问API文档：http://localhost:8000/docs
2. 使用示例数据初始化数据库：

```bash
python scripts/init_db.py
```

3. 使用快速记录端点记录数据：

```
http://localhost:8000/api/v1/quick/log?user_id=1&type=weight&value=75.5
```

4. 设置Grafana进行可视化（参见[Grafana集成指南](docs/grafana_integration.md)）

## API端点

API提供以下端点：

- `GET /api/v1/users/` - 列出所有用户
- `POST /api/v1/users/` - 创建新用户
- `GET /api/v1/metric-types/` - 列出所有指标类型
- `POST /api/v1/metric-types/` - 创建新指标类型
- `GET /api/v1/exercise-types/` - 列出所有运动类型
- `POST /api/v1/exercise-types/` - 创建新运动类型
- `GET /api/v1/health-metrics/` - 使用过滤器列出健康指标
- `POST /api/v1/health-metrics/` - 创建新健康指标
- `GET /api/v1/exercises/` - 使用过滤器列出运动记录
- `POST /api/v1/exercises/` - 创建新运动记录
- `GET /api/v1/quick/log` - 通过URL参数快速记录

## 数据可视化

本项目与Grafana集成以实现数据可视化。有关设置说明和示例仪表板，请参阅[Grafana集成指南](docs/grafana_integration.md)。

## 使用场景

- 个人健康追踪（体重、睡眠、心率）
- 健身追踪（跑步、骑行、锻炼）
- 长期健康趋势分析
- 设定和监控健康目标

## 许可证

MIT