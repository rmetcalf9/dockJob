FROM alpine

MAINTAINER Robert Metcalf

RUN apk add --no-cache bash python3 curl && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache && \
    pip3 install --upgrade pip

ENV APP_DIR /app
ENV FRONTEND_APP_DIR /webfrontend
ENV API_URL http://localhost:80/dockjobapi

EXPOSE 80

RUN mkdir ${APP_DIR}
COPY ./app/src ${APP_DIR}
RUN pip3 install -r ${APP_DIR}/requirments.txt

RUN mkdir ${FRONTEND_APP_DIR}
COPY ./webfrontend/dist ${FRONTEND_APP_DIR}

COPY ./VERSION /VERSION

COPY ./app/run_app_docker.sh /run_app_docker.sh

CMD ["/run_app_docker.sh"]

HEALTHCHECK --interval=5s --timeout=3s \
  CMD curl -f http://127.0.0.1:80/dockjobfrontend/index.html || exit 1

##docker run --name dockjob -p 80:80 -d metcarob/dockjob:latest
