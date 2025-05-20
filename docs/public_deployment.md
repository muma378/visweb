# 公网部署指南

本文档提供了如何将VisWeb服务部署到公网的详细步骤和最佳实践。

## 先决条件

- 一台运行Linux的云服务器（推荐Ubuntu 20.04 LTS或更高版本）
- 已配置的域名，指向您的服务器IP
- 安装了Docker和Docker Compose
- 开放了80（HTTP）和443（HTTPS）端口

## 快速部署

我们提供了一个简化的部署脚本，可以帮助您快速部署服务：

1. 将项目文件复制到服务器
2. 编辑`.env.production`文件配置环境变量
3. 运行部署脚本：

```bash
./deploy.sh
```

## 手动部署步骤

如果你需要更多控制，可以按照以下步骤手动部署：

### 1. 准备服务器

首先，确保已安装Docker和Docker Compose：

```bash
# 安装Docker
curl -fsSL https://get.docker.com | sh

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.18.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. 配置环境变量

复制示例环境文件并编辑：

```bash
cp .env.production.example .env.production
nano .env.production
```

至少要设置以下变量：
- `DOMAIN_NAME`：您的域名
- `GRAFANA_ADMIN_PASSWORD`：更安全的Grafana管理员密码

### 3. 配置SSL证书

对于生产环境，建议使用Let's Encrypt获取免费的SSL证书：

```bash
# 安装certbot
sudo apt update
sudo apt install certbot

# 获取证书
sudo certbot certonly --standalone -d yourdomain.com

# 复制证书到项目目录
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/server.crt
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/server.key
```

或者，您可以使用我们提供的脚本生成自签名证书（不推荐用于生产环境）：

```bash
./scripts/generate_ssl.sh yourdomain.com
```

### 4. 配置Nginx

生成Nginx配置文件：

```bash
sed "s/\${DOMAIN_NAME}/yourdomain.com/g" nginx/conf/default.conf.template > nginx/conf/default.conf
```

### 5. 启动服务

使用Docker Compose启动所有服务：

```bash
docker-compose -f docker-compose.yml --env-file .env.production up -d
```

### 6. 初始化数据库

初始化数据库并创建示例数据：

```bash
docker-compose -f docker-compose.yml --env-file .env.production up init-db
```

## 安全最佳实践

当将服务部署到公网时，安全性至关重要。请考虑以下建议：

1. **强密码策略**：
   - 为Grafana管理员设置强密码
   - 考虑为API添加认证

2. **防火墙配置**：
   - 只开放必要的端口（80和443）
   - 使用`ufw`或云提供商的安全组来限制访问

3. **定期更新**：
   - 定期更新Docker镜像
   - 保持系统安全补丁更新

4. **监控与备份**：
   - 设置日志监控
   - 定期备份数据库

## 故障排查

**无法访问服务？**

1. 检查容器运行状态：
```bash
docker-compose ps
```

2. 查看服务日志：
```bash
docker-compose logs nginx
docker-compose logs visweb
docker-compose logs grafana
```

3. 验证防火墙设置：
```bash
sudo ufw status
```

4. 检查DNS配置是否正确指向您的服务器

**SSL证书问题？**

如果使用Let's Encrypt，确保证书未过期：
```bash
certbot certificates
```

如需续期：
```bash
certbot renew
```

## 监控和维护

为确保服务稳定运行，建议设置：

1. 自动备份SQLite数据库
2. Docker容器健康检查
3. 服务器资源监控

以上步骤可以根据您的具体需求进行调整和扩展。
