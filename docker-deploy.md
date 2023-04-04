## Docker部署说明
### 开发环境
1. 生成镜像：docker-compose -f docker-compose-build.yml build
2. tag: docker tag design:v1 jinniudashu/design:v1
3. push: docker push jinniudashu/design:v1
### 生产环境
1. 进入项目目录：cd design
2. 查看容器：docker ps
3. 停止容器：docker stop design
4. 删除容器：docker rm design
5. 查看镜像：docker images
6. 删除镜像：docker rmi design:v1
7. 查看volume：docker volume ls
8. 删除volume：docker volume rm design_app
9. 下载镜像：docker pull jinniudashu/design:v1
10. 启动容器：docker-compose up
11. 浏览器访问，修改密码