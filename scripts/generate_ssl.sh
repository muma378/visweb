#!/bin/bash

# 生成自签名SSL证书脚本
# 在生产环境中应使用Let's Encrypt或其他受信任的证书提供商

# 脚本接受一个参数作为域名
if [ "$#" -ne 1 ]; then
    echo "用法: $0 域名"
    echo "例如: $0 example.com"
    exit 1
fi

DOMAIN=$1
SSL_DIR="./nginx/ssl"

# 确保SSL目录存在
mkdir -p $SSL_DIR

# 生成私钥
openssl genrsa -out $SSL_DIR/server.key 2048

# 生成证书签名请求(CSR)
openssl req -new -key $SSL_DIR/server.key -out $SSL_DIR/server.csr -subj "/CN=$DOMAIN/O=VisWeb/C=CN"

# 生成自签名证书（有效期10年）
openssl x509 -req -days 3650 -in $SSL_DIR/server.csr -signkey $SSL_DIR/server.key -out $SSL_DIR/server.crt

# 删除CSR文件
rm $SSL_DIR/server.csr

echo "自签名SSL证书已生成:"
echo "私钥: $SSL_DIR/server.key"
echo "证书: $SSL_DIR/server.crt"
echo ""
echo "警告: 这是自签名证书，浏览器会显示安全警告。"
echo "在生产环境中，应使用Let's Encrypt或其他受信任的证书。"
