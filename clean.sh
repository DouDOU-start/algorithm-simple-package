# 清理镜像
docker rmi $(docker images -qf "dangling=true")
# 删除容器
docker rm -f test
# 显示运行中的容器
docker ps -a