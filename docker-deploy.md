## Docker部署说明
### 开发环境
1. 生成镜像：docker-compose -f docker-compose-build.yml build
   （Mac）：docker buildx build --platform linux/x86_64 design:v1 . --load
2. push: docker push jinniudashu/design:v1
### 生产环境
1. 进入项目目录：docker-compose down
2. 下载镜像：docker pull jinniudashu/design:v1
3. 启动容器：docker-compose up
4. 删除旧镜像：docker rmi $(docker images -f "dangling=true" -q)
