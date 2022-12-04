FROM php:7.2-apache

RUN echo 'ServerName 127.0.0.1' >> /etc/apache2/apache2.conf

COPY ./source/ /var/www/html
ENV EDIT_IMAGES_HOST="YOUR_SERVICE"
EXPOSE 80
