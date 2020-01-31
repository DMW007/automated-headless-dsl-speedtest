FROM python:3-alpine
RUN pip install speedtest-cli Jinja2 tzlocal
WORKDIR /app
COPY src/ .
ENTRYPOINT sh ./cron.sh