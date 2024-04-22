## Docker部署说明
### 开发环境
1. 生成镜像：docker-compose -f docker-compose-build.yml build
   （Mac）：docker buildx build --platform linux/x86_64 design:v1 . --load
2. push: docker push jinniudashu/design:v1
### 生产环境
1. docker pull jinniudashu/design:v1
2. docker-compose down -v
3. docker-compose up
4. docker rmi $(docker images -f "dangling=true" -q)
