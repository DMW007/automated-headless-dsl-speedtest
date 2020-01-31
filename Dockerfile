FROM python:3-alpine
RUN pip install speedtest-cli Jinja2 tzlocal python-dateutil
WORKDIR /app
COPY src/ .
ENTRYPOINT sh ./cron.sh