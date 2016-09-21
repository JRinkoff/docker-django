FROM django:1.8-python2

# Nano, cURL, wget and Pillow
RUN apt-get update && apt-get install -y nano curl wget libjpeg-dev
ENV TERM xterm

# Varnish and Redis tools
RUN apt-get update && apt-get install -y varnish redis-tools

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["bash", "entrypoint.sh"]
