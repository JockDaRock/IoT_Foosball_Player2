FROM resin/raspberrypi3-alpine-python

ENV INITSYSTEM on

RUN pip install --no-cache paho-mqtt RPi.Gpio

COPY . /usr/src/app
WORKDIR /usr/src/app

EXPOSE 80

CMD ["python", "player2.py"]