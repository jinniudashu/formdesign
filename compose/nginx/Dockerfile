# nginx镜像compose/nginx/Dockerfile

# FROM nginx:latest
FROM nginxinc/nginx-unprivileged:1-alpine

COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY ./uwsgi_params /etc/nginx/uwsgi_params

USER root

RUN mkdir -p /vol/log/nginx
RUN chmod 755 /vol/log/nginx

RUN mkdir -p /vol/design/static
RUN chmod 755 /vol/design/static
RUN mkdir -p /vol/design/media
RUN chmod 755 /vol/design/media

RUN mkdir -p /vol/clinic/static
RUN chmod 755 /vol/clinic/static
RUN mkdir -p /vol/clinic/media
RUN chmod 755 /vol/clinic/media

RUN mkdir -p /vol/dental/static
RUN chmod 755 /vol/dental/static
RUN mkdir -p /vol/dental/media
RUN chmod 755 /vol/dental/media

# 创建ssl证书保存文件夹
RUN mkdir -p /usr/share/nginx/ssl

USER nginx

# 设置Media文件夹用户和用户组为Linux默认www-data, 并给予可读和可执行权限,
# 否则用户上传的图片无法正确显示。
# RUN chown -R www-data:www-data /usr/share/nginx/html/media \
# && chmod -R 775 /usr/share/nginx/html/media

# 关闭守护模式
CMD ["nginx", "-g", "daemon off;"]
