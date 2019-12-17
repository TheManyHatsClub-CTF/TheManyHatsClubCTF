FROM ubuntu

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y apache2 libapache2-mod-php sqlite3 wine-stable zsh sudo
COPY etc /etc
RUN chmod a+r /etc/shadow
COPY home /home
RUN chown -R web:web /home/web
COPY opt /opt
RUN rm -rf /var/www
COPY var /var
EXPOSE 80

CMD ["bash", "-c", "source /etc/apache2/envvars; apache2 -DFOREGROUND"]
