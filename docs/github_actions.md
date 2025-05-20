# GitHub Actions 和容器注册表集成指南

本文档介绍如何使用GitHub Actions自动构建Docker镜像并推送到GitHub Container Registry (GHCR)。

## 工作流程概述

我们设置了两个GitHub Actions工作流：

1. **Python Tests** - 运行单元测试以确保代码质量
2. **Build and Push Docker Image** - 构建Docker镜像（仅linux/amd64架构）并推送到GHCR

这些工作流会在以下情况下自动触发：
- 推送代码到主分支（main或master）
- 创建或更新Pull Request
- 手动触发工作流（使用GitHub界面）
- 为代码创建新标签（例如v1.0.0）- 这将创建对应版本的镜像

## 设置步骤

### 1. 仓库设置

在将代码推送到GitHub之前，确保：

1. 代码库已经迁移到GitHub
2. 你有推送到该仓库的权限

### 2. 启用GitHub Container Registry

1. 访问你的GitHub个人设置
2. 进入"Developer settings" > "Personal access tokens" > "Tokens (classic)"
3. 生成一个新的令牌，勾选`write:packages`权限
4. 保存此令牌，它将用于手动推送镜像

### 3. 配置仓库权限

对于自动化工作流，需要配置仓库以允许GitHub Actions写入包：

1. 在GitHub仓库页面，点击"Settings"
2. 选择"Actions" > "General"
3. 在"Workflow permissions"部分，选择"Read and write permissions"
4. 保存更改

## 使用方法

### 自动构建和发布

只需将代码推送到主分支或创建标签，GitHub Actions将自动：

1. 运行所有测试
2. 构建Docker镜像
3. 推送镜像到GHCR

例如，创建一个新版本标签：

```bash
git tag v1.0.0
git push origin v1.0.0
```

### 手动构建（不使用GitHub Actions）

你也可以在本地构建镜像并手动推送：

1. 构建镜像：
   ```bash
   docker build -t ghcr.io/你的用户名/visweb:latest .
   ```

2. 登录到GHCR：
   ```bash
   echo "你的GitHub令牌" | docker login ghcr.io -u 你的用户名 --password-stdin
   ```

3. 推送镜像：
   ```bash
   docker push ghcr.io/你的用户名/visweb:latest
   ```

或者，使用start.sh脚本中的选项10来构建镜像。

## 使用GitHub容器注册表中的镜像

发布后，你可以通过以下方式使用镜像：

```bash
docker pull ghcr.io/你的用户名/visweb:latest
```

或者在docker-compose.yml中使用：

```yaml
services:
  visweb:
    image: ghcr.io/你的用户名/visweb:latest
    # 其他配置...
```

## 标签策略

我们的工作流程会自动为镜像生成以下标签：

- `latest` - 主分支的最新版本
- `v1.0.0` - 特定版本（对应git标签）
- `v1.0` - 次要版本
- `v1` - 主要版本
- 短SHA - 提交的SHA哈希

## 故障排除

如果GitHub Actions失败，请检查：

1. 工作流日志以查看具体错误
2. 确保仓库权限已正确设置
3. 验证测试是否通过

对于手动推送问题，检查：

1. 你是否有正确的访问令牌权限
2. 镜像名称是否正确（包括用户名和仓库名）
