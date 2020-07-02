FROM python:3.8 as builder

ARG VERSION

COPY Makefile /
COPY src /src
COPY requirements.txt /

RUN make VERSION=$VERSION build

FROM python:3.8

WORKDIR /app
COPY --from=builder /build .

USER 65534
EXPOSE 5000

ENTRYPOINT [ "/app/venv/bin/uwsgi", "--http", "0.0.0.0:5000", "--wsgi-file", "/app/main.py", "--callable", "app_dispatch" ]
