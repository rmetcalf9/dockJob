FROM nginx:1.15.12-alpine

MAINTAINER Robert Metcalf

##https://vladikk.com/2013/09/12/serving-flask-with-nginx-on-ubuntu/

ENV APP_DIR /app
##APIAPP_FRONTEND is also configured in nginx conf
ENV APIAPP_FRONTEND /webfrontend


ENV APIAPP_APIURL http://localhost:80/dockjobapi
ENV APIAPP_APIDOCSURL http://localhost:80/apidocs
ENV APIAPP_FRONTENDURL http://localhost:80/frontend
ENV APIAPP_APIACCESSSECURITY '[]'
ENV APIAPP_USERFORJOBS=dockjobuser
ENV APIAPP_GROUPFORJOBS=dockjobgroup

# APIAPP_MODE is not definable here as it is hardcoded to DOCKER in the shell script
# APIAPP_VERSION is not definable here as it is read from the VERSION file inside the image

EXPOSE 80


RUN apk add --no-cache bash python3 curl python3-dev build-base linux-headers pcre-dev libffi-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache && \
    pip3 install --upgrade pip && \
    mkdir ${APP_DIR} && \
    mkdir ${APIAPP_FRONTEND} && \
    addgroup -S ${APIAPP_GROUPFORJOBS} && \
    adduser -S -G ${APIAPP_GROUPFORJOBS} ${APIAPP_USERFORJOBS} && \
    mkdir /var/log/uwsgi && \
    pip3 install uwsgi && \
    pip3 install cffi

COPY ./app/src ${APP_DIR}
RUN pip3 install -r ${APP_DIR}/requirments.txt

COPY ./webfrontend/dist/spa ${APIAPP_FRONTEND}
COPY ./VERSION /VERSION
COPY ./app/run_app_docker.sh /run_app_docker.sh
COPY ./nginx_default.conf /etc/nginx/conf.d/default.conf
COPY ./uwsgi.ini /uwsgi.ini

STOPSIGNAL SIGTERM


CMD ["/run_app_docker.sh"]

# Regular checks. Docker won't send traffic to container until it is healthy
#  and when it first starts it won't check the health until the interval so I can't have
#  a higher value without increasing the startup time
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://127.0.0.1:80/frontend/index.html?healthcheck=true || exit 1

##docker run --name dockjob -p 80:80 -d metcarob/dockjob:latest
