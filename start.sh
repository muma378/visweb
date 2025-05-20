#!/bin/bash

# 启动脚本 - 构建并启动VisWeb服务

# 显示菜单
show_menu() {
  echo "========================================="
  echo "        VisWeb 服务管理脚本              "
  echo "========================================="
  echo "1. 构建并启动所有服务"
  echo "2. 停止所有服务"
  echo "3. 查看服务状态"
  echo "4. 仅启动VisWeb API服务"
  echo "5. 初始化数据库"
  echo "6. 查看API日志"
  echo "7. 查看Grafana日志"
  echo "8. 重新构建并重启所有服务"
  echo "9. 运行测试"
  echo "10. 构建镜像但不推送"
  echo "0. 退出"
  echo "========================================="
  echo -n "请选择一个选项: "
}

# 构建并启动所有服务
start_all() {
  echo "正在构建并启动所有服务..."
  docker-compose up -d
  echo "服务已启动。"
  echo "- API地址: http://localhost:8000"
  echo "- API文档: http://localhost:8000/docs"
  echo "- Grafana: http://localhost:3000 (用户名/密码: admin/admin)"
}

# 停止所有服务
stop_all() {
  echo "正在停止所有服务..."
  docker-compose down
  echo "所有服务已停止。"
}

# 查看服务状态
check_status() {
  echo "服务状态："
  docker-compose ps
}

# 仅启动API服务
start_api() {
  echo "正在启动VisWeb API服务..."
  docker-compose up -d visweb
  echo "API服务已启动。"
  echo "- API地址: http://localhost:8000"
  echo "- API文档: http://localhost:8000/docs"
}

# 初始化数据库
init_database() {
  echo "正在初始化数据库..."
  docker-compose up init-db
  echo "数据库初始化完成。"
}

# 查看API日志
view_api_logs() {
  echo "显示API日志（按Ctrl+C退出）..."
  docker-compose logs -f visweb
}

# 查看Grafana日志
view_grafana_logs() {
  echo "显示Grafana日志（按Ctrl+C退出）..."
  docker-compose logs -f grafana
}

# 重新构建并重启所有服务
rebuild_all() {
  echo "正在重新构建并重启所有服务..."
  docker-compose down
  docker-compose build
  docker-compose up -d
  echo "所有服务已重新构建并启动。"
}

# 运行测试
run_tests() {
  echo "正在运行测试..."
  python -m pytest -v
  echo "测试完成。"
}

# 构建镜像但不推送
build_image() {
  echo "正在构建Docker镜像 (仅linux/amd64架构)..."
  docker build -t ghcr.io/$(whoami)/visweb:latest .
  echo "Docker镜像构建完成。"
  echo "你可以使用以下命令手动推送镜像："
  echo "docker push ghcr.io/$(whoami)/visweb:latest"
}

# 主程序循环
while true; do
  show_menu
  read choice
  
  case $choice in
    1) start_all ;;
    2) stop_all ;;
    3) check_status ;;
    4) start_api ;;
    5) init_database ;;
    6) view_api_logs ;;
    7) view_grafana_logs ;;
    8) rebuild_all ;;
    9) run_tests ;;
    10) build_image ;;
    0) echo "退出脚本。"; exit 0 ;;
    *) echo "无效选项，请重新选择。" ;;
  esac
  
  echo
  echo "按回车键继续..."
  read
  clear
done
