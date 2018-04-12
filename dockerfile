FROM python:3.6.4-stretch

ENV APP_DIRECTORY /var/www/mnemotopy
ENV C_FORCE_ROOT 1
ADD requirements.txt /app/requirements.txt
RUN easy_install pip
RUN pip install pip==9.0.1
RUN pip install -r /app/requirements.txt
ADD . $APP_DIRECTORY
WORKDIR $APP_DIRECTORY

ENTRYPOINT cd $APP_DIRECTORY/src && celery -A mnemotopy -Q medias -l info worker