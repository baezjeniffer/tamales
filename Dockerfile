FROM python:3.8-slim-buster


# We copy just the requirements.txt first to leverage Docker cache

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

RUN apt-get update && apt-get -y install cron
COPY cron_tamales /etc/cron.d/cron_tamales
RUN chmod 0644 /etc/cron.d/cron_tamales
#RUN service cron start
# Apply cron job
RUN crontab /etc/cron.d/cron_tamales

ENTRYPOINT [ "/app/docker_entrypoint.sh" ]

CMD [ "/app/app.py" ]