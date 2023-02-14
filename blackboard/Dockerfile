

# Dockerfile for RosarioSIS
# Best Dockerfile practices: http://crosbymichael.com/dockerfile-best-practices.html

FROM php:7.4-apache

ENV PGHOST=localhost \
    PGUSER=rosario \
    PGPASSWORD=rosariopwd \
    PGDATABASE=rosariosisdb \
    PGPORT=5432 \
    ROSARIOSIS_YEAR=2022 \
    ROSARIOSIS_LANG='en_US'

# Upgrade packages.
# Install git, Apache2 + PHP + PostgreSQL webserver, sendmail, wkhtmltopdf & others utilities.
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install postgresql-client wkhtmltopdf libpq-dev libpng-dev libxml2-dev libzip-dev libonig-dev sendmail nano locales -y;

# Install PHP extensions.
RUN docker-php-ext-configure gd --with-png-dir=/usr --with-jpeg-dir=/usr; \
    docker-php-ext-install -j$(nproc) gd mbstring xml pgsql gettext intl xmlrpc zip
RUN apt install postgresql postgresql-contrib -y 

# Download and extract rosariosis
ENV ROSARIOSIS_VERSION 'v10.4.4'
RUN mkdir /usr/src/rosariosis
COPY ./rosariosis /usr/src/rosariosis
RUN rm -rf /var/www/html && mkdir -p /var/www && \
    ln -s /usr/src/rosariosis/ /var/www/html && chmod 777 /var/www/html &&\
    chown -R www-data:www-data /usr/src/rosariosis

# Copy our configuration files.
COPY conf/config.inc.php /usr/src/rosariosis/config.inc.php
COPY bin/init /init
COPY setup_postgres.sh ./setup_postgres.sh
RUN chmod 111 /init


EXPOSE 80
ENTRYPOINT ["/init"]
CMD ["apache2-foreground"]


