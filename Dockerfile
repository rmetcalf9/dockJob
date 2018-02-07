FROM alpine

MAINTAINER Robert Metcalf

RUN apk add --no-cache bash python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache && \
    pip3 install --upgrade pip && \
    pip3 install flask

ENV APP_DIR /app
ENV FRONTEND_APP_DIR /webfrontend
ENV VAR_DIR /vars

EXPOSE 80

RUN mkdir ${APP_DIR}
COPY ./app/src ${APP_DIR}

RUN mkdir ${FRONTEND_APP_DIR}
COPY ./webfrontend/build ${FRONTEND_APP_DIR}

RUN mkdir ${VAR_DIR}
COPY ./VERSION ${VAR_DIR}/VERSION


ENTRYPOINT ["python3"]
CMD ["/app/app.py $(cat ${VAR_DIR}/VERSION) ${FRONTEND_APP_DIR}"]

