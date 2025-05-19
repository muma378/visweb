FROM docker.io/grafana/grafana-oss:latest

# 安装 frser-sqlite-datasource 插件
RUN grafana-cli plugins install frser-sqlite-datasource

# 确保插件被正确加载（可选：为部署自动接受插件许可证）
ENV GF_PLUGINS_ALLOW_LOADING_UNSIGNED_PLUGINS=frser-sqlite-datasource

