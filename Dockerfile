ARG RJM_BUILDQUASARAPP_IMAGE
ARG RJM_VERSION

# TODO it would be nice if the build process run the python tests

FROM ${RJM_BUILDQUASARAPP_IMAGE} as quasar_build

COPY ./frontend /frontend

RUN build_quasar_app /frontend pwa ${RJM_VERSION}

FROM python:3.8-buster

MAINTAINER Robert Metcalf


ENV APP_DIR /app
##APIAPP_FRONTEND is also configured in nginx conf
ENV APIAPP_FRONTEND /frontend


ENV APIAPP_APIURL http://localhost:80/dockjobapi
ENV APIAPP_APIDOCSURL http://localhost:80/apidocs
ENV APIAPP_FRONTENDURL http://localhost:80/frontend
ENV APIAPP_APIACCESSSECURITY '[]'
ENV APIAPP_USERFORJOBS=dockjobuser
ENV APIAPP_GROUPFORJOBS=dockjobgroup

# APIAPP_MODE is not definable here as it is hardcoded to DOCKER in the shell script
# APIAPP_VERSION is not definable here as it is read from the VERSION file inside the image

EXPOSE 80


# RUN apk add --no-cache bash python3 curl python3-dev build-base linux-headers pcre-dev libffi-dev && \
#    python3 -m ensurepip && \
#    rm -r /usr/lib/python*/ensurepip && \
#    pip3 install --upgrade pip setuptools && \
#    rm -r /root/.cache && \
#    pip3 install --upgrade pip && \
#    mkdir ${APP_DIR} && \
#    mkdir ${APIAPP_FRONTEND} && \
#    addgroup ${APIAPP_GROUPFORJOBS} && \
#    adduser --quiet --disabled-password --gecos "" --ingroup ${APIAPP_GROUPFORJOBS} ${APIAPP_USERFORJOBS} && \
#    mkdir /var/log/uwsgi && \
#    pip3 install uwsgi && \
#    pip3 install cffi

COPY install-nginx-debian.sh /

RUN apt-get install ca-certificates curl && \
    bash /install-nginx-debian.sh && \
    mkdir ${APP_DIR} && \
    mkdir ${APIAPP_FRONTEND} && \
    addgroup ${APIAPP_GROUPFORJOBS} && \
    adduser --quiet --disabled-password --gecos "" --ingroup ${APIAPP_GROUPFORJOBS} ${APIAPP_USERFORJOBS} && \
    usermod -a -G ${APIAPP_GROUPFORJOBS} ${APIAPP_USERFORJOBS} && \
    mkdir /var/log/uwsgi && \
    pip3 install uwsgi && \
    wget --ca-directory=/etc/ssl/certs https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem -O /rds-combined-ca-bundle.pem


COPY ./app/src ${APP_DIR}
RUN pip3 install -r ${APP_DIR}/requirments.txt

COPY --from=quasar_build ./frontend/dist/pwa ${APIAPP_FRONTEND}
COPY ./VERSION /VERSION
COPY ./app/run_app_docker.sh /run_app_docker.sh
COPY ./nginx_default.conf /etc/nginx/conf.d/default.conf
COPY ./uwsgi.ini /uwsgi.ini
COPY ./healthcheck.sh /healthcheck.sh

STOPSIGNAL SIGTERM


CMD ["/run_app_docker.sh"]

# Regular checks. Docker won't send traffic to container until it is healthy
#  and when it first starts it won't check the health until the interval so I can't have
#  a higher value without increasing the startup time
HEALTHCHECK --interval=30s --timeout=3s \
  CMD /healthcheck.sh

##docker run --name dockjob -p 80:80 -d metcarob/dockjob:latest
