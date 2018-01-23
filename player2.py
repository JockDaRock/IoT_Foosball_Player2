import RPi.GPIO as GPIO
import json
import paho.mqtt.client as mqtt
import time
import asyncio

thread = None

score_topic = "foosball/score"
speed_topic = "foosball/speed"

# 192.168.195.7 was IR 829 Broker
broker_ip = "128.107.70.30"  # <--- Please change IP to match the location of your MQTT broker

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ir = 15
ir2 = 18

mqttc = mqtt.Client()
mqttc.connect(broker_ip)
mqttc.loop_start()

GPIO.setup(ir, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(ir2, GPIO.IN, GPIO.PUD_DOWN)

start = 0
stop = 0


async def data_collect_ir():
    GPIO.add_event_detect(ir, GPIO.BOTH, callback=process_edge, bouncetime=200)
    """while True:
        time.sleep(0)"""


"""async def data_collect_ir2():
    GPIO.add_event_detect(ir2, GPIO.RISING, callback=post_speed, bouncetime=200)
    while True:
        time.sleep(0)"""


"""def data_collect():
    GPIO.add_event_detect(ir, GPIO.FALLING, callback=process_edge, bouncetime=100)
    while True:
        pass"""


async def process_edge(channel):
    if GPIO.input(channel):  # test if pin is high
        post_speed(channel)
    else:
        post_score(channel)


def post_score(channel):
    global start
    start = time.time()
    print("Start time is:")
    print(start)
    brokerMessage = {'Status': 'scored', 'Player': '2', 'Score': 1, 'Data': '0'}
    print("message sent")
    mqttc.publish(score_topic, json.dumps(brokerMessage))


def post_speed(channel):
    global stop
    stop = time.time()
    print("Stop time is:")
    print(stop)
    if stop > start:
        elapsed = stop - start
        print("Elapsed time is:")
        print(elapsed)
        speed = .0345 / elapsed  # meters per second
        mph = 2.23694 * speed  # convert meters/s to mph
        print("posting speed")
        print(mph)
        brokerMessage = {'Status': 'speed', 'Speed': mph}
        mqttc.publish(speed_topic, json.dumps(brokerMessage))


# while GPIO.input(ir)==0:
#     start = time.time()
#     print("Start time is:")
#     print(start)

# while GPIO.input(ir)==1:
#     print("speedRead is")
#     print(speedRead)
#     if speedRead is False:


if __name__ == '__main__':
    # data_collect()
    loop = asyncio.get_event_loop()
    # tasks = [asyncio.ensure_future(data_collect_ir()), asyncio.ensure_future(data_collect_ir2())]
    tasks = [asyncio.get_event_loop().run_until_complete(data_collect_ir())]
    loop.run_forever()
    print("started")