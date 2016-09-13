FROM django:1.8-python2

# Nano, cURL and Pillow
RUN apt-get update && apt-get install -y nano curl libjpeg-dev
ENV TERM xterm

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["bash", "entrypoint.sh"]
