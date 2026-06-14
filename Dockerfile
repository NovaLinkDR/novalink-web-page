FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY index.html /usr/share/nginx/html/
COPY contacto.html /usr/share/nginx/html/
COPY demo.html /usr/share/nginx/html/
COPY sobre-nosotros.html /usr/share/nginx/html/
COPY demo/ /usr/share/nginx/html/demo/
COPY config.js  /usr/share/nginx/html/
COPY assets/    /usr/share/nginx/html/assets/

EXPOSE 80
