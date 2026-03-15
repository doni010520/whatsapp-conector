FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/
COPY monitor-x7k9m2p4.html /usr/share/nginx/html/
EXPOSE 80
