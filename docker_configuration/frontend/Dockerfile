FROM nginx:alpine AS base

RUN cp /usr/share/zoneinfo/America/Belem /etc/localtime

RUN echo "America/Belem" >  /etc/timezone

ENV TZ America/Belem

# Copy the local configuration to the server
ADD nginx.conf /etc/nginx/conf.d/default.conf


