#!/bin/bash

# 云服务器部署脚本

# 显示彩色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}====================================${NC}"
echo -e "${BLUE}     VisWeb 云服务器部署脚本     ${NC}"
echo -e "${BLUE}====================================${NC}"

# 检查是否已安装 Docker 和 Docker Compose
if ! command -v docker &> /dev/null || ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}错误: 未检测到 Docker 或 Docker Compose${NC}"
    echo "请先安装 Docker 和 Docker Compose，然后再运行此脚本"
    exit 1
fi

# 检查配置文件是否存在
if [ ! -f .env.production ]; then
    echo -e "${RED}错误: 未找到 .env.production 配置文件${NC}"
    echo "请先创建 .env.production 文件并设置必要的环境变量"
    exit 1
fi

# 加载环境变量
set -a
source .env.production
set +a

# 验证必要的环境变量
if [ -z "$DOMAIN_NAME" ]; then
    echo -e "${RED}错误: 未设置 DOMAIN_NAME 环境变量${NC}"
    echo "请在 .env.production 中设置 DOMAIN_NAME"
    exit 1
fi

# 确保 Nginx 配置目录存在
mkdir -p nginx/conf nginx/ssl

# 提示用户配置域名
echo -e "${GREEN}您正在为域名 ${DOMAIN_NAME} 部署 VisWeb${NC}"
echo

# 生成 Nginx 配置文件
echo -e "${BLUE}正在生成 Nginx 配置...${NC}"
sed "s/\${DOMAIN_NAME}/$DOMAIN_NAME/g" nginx/conf/default.conf.template > nginx/conf/default.conf

# 检查是否已有SSL证书
if [ ! -f nginx/ssl/server.crt ] || [ ! -f nginx/ssl/server.key ]; then
    echo -e "${BLUE}未找到SSL证书，正在生成自签名证书...${NC}"
    ./scripts/generate_ssl.sh $DOMAIN_NAME
    echo
    echo -e "${GREEN}SSL证书已生成。${NC}"
    echo -e "${RED}注意: 这是自签名证书，浏览器会显示安全警告。${NC}"
    echo -e "在生产环境中，建议使用 Let's Encrypt 或其他受信任的证书。"
else
    echo -e "${GREEN}已找到SSL证书。${NC}"
fi

# 启动服务
echo
echo -e "${BLUE}正在启动服务...${NC}"
docker-compose -f docker-compose.yml --env-file .env.production up -d

# 等待服务启动
echo "等待服务启动..."
sleep 5

# 初始化数据库
echo -e "${BLUE}正在初始化数据库...${NC}"
docker-compose -f docker-compose.yml --env-file .env.production up init-db

# 检查服务状态
echo
echo -e "${BLUE}服务状态:${NC}"
docker-compose ps

# 输出访问信息
echo
echo -e "${GREEN}部署完成!${NC}"
echo -e "您的VisWeb服务已成功部署在以下地址:"
echo -e "- API文档: ${BLUE}https://${DOMAIN_NAME}/docs${NC}"
echo -e "- Grafana: ${BLUE}https://${DOMAIN_NAME}/grafana${NC} (用户名: ${GRAFANA_ADMIN_USER}, 密码请查看您的.env.production文件)"
echo
echo -e "${RED}重要安全提示:${NC}"
echo "1. 请确保更改默认密码"
echo "2. 考虑设置防火墙，只允许必要的端口(80和443)"
echo "3. 定期更新Docker镜像和系统安全补丁"
echo
echo -e "如需查看服务日志，请运行: ${BLUE}docker-compose logs -f${NC}"
