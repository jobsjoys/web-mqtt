import paho.mqtt.client as mqtt
import random
import string
from time import sleep
import os

mqtt_username = os.environ.get('mqtt_username')
mqtt_password = os.environ.get('mqtt_password')

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.connect("maqiatto.com", 1883, 60)


def id_generator(size=100, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


while True:
    client.publish(mqtt_username + "/axis", id_generator())
    client.publish(mqtt_username + "/buttons", id_generator())
    sleep(1)
