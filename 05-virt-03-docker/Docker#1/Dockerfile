FROM nginx:1.21.5-alpine

## Replace the default nginx index page with our index.html file
RUN rm -rf /usr/share/nginx/html/*
COPY ./index.html /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/nginx.conf

ENTRYPOINT ["nginx", "-g", "daemon off;"]
