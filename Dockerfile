FROM python
COPY . /app
ENTRYPOINT [ "/bin/bash", "/app/start.sh" ]