# Docker 部署说明

这个文档将指导您如何使用 Docker 和 Docker Compose 来部署 VisWeb 服务。

## 先决条件

- 已安装 [Docker](https://docs.docker.com/get-docker/)
- 已安装 [Docker Compose](https://docs.docker.com/compose/install/)

## 快速开始

我们提供了一个便捷的脚本来管理服务：

```bash
./start.sh
```

这个脚本提供了多种操作选项，包括启动服务、查看日志、初始化数据库等。

## 手动部署步骤

如果您想手动部署，可以按照以下步骤操作：

### 1. 构建并启动所有服务

```bash
docker-compose up -d
```

这将启动 VisWeb API 服务和 Grafana 可视化服务。

### 2. 初始化数据库（首次使用时）

```bash
docker-compose up init-db
```

这会在数据库中创建测试用户和样例数据。

### 3. 访问服务

- **API 服务**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs
- **Grafana 仪表板**: http://localhost:3000 (用户名/密码: admin/admin)

## 数据持久化

所有数据都存储在以下位置：

- SQLite 数据库文件: `./data/visweb.db`
- Grafana 配置和数据: Docker 卷 `grafana-storage`

## 自定义配置

您可以通过修改 `docker-compose.yml` 文件来自定义服务配置。常见的自定义选项包括：

- 更改端口映射
- 修改环境变量
- 添加额外的服务

## 常见问题排查

### 服务无法启动

检查 Docker 日志：

```bash
docker-compose logs visweb
docker-compose logs grafana
```

### 数据库初始化失败

确保 API 服务已经启动并正在运行：

```bash
docker-compose ps
```

然后再次运行初始化命令：

```bash
docker-compose up init-db
```

### Grafana 无法连接到数据库

确保 SQLite 数据源插件已正确安装，并且数据库文件路径配置正确。您可以在 Grafana 界面中检查数据源配置。
