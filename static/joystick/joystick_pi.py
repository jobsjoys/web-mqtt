import paho.mqtt.client as mqtt
import json
from pygame import joystick as js
import pygame as pg
import os
from time import sleep

mqtt_username = os.environ.get('mqtt_username')
mqtt_password = os.environ.get('mqtt_password')

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.connect("maqiatto.com", 1883, 60)

pg.init()

# Initialize the joysticks.
js.init()

# Only care about first controller, if you care about more than one you need another loop
joystick = js.Joystick(0)
joystick.init()

name = joystick.get_name()
print("Joystick name: {}".format(name))

axes = joystick.get_numaxes()
print("Number of axes: {}".format(axes))

buttons = joystick.get_numbuttons()
print("Number of buttons: {}".format(buttons))

# -------- Main Program Loop -----------
while True:

    for event in pg.event.get():
        if event.type == pg.JOYAXISMOTION:
            axisdata=[]
            for i in range(axes):
                axis = int(round(joystick.get_axis(i)))  # Rounded since my controller is cheap and nasty
                item = {"axis" + str(i): axis}
                axisdata.append(item)
            jsonAxisData = json.dumps(axisdata)
            client.publish(mqtt_username + "/axis", jsonAxisData)
            print(jsonAxisData)

        elif event.type == pg.JOYBUTTONDOWN or event.type == pg.JOYBUTTONUP:
            buttondata=[]
            for i in range(buttons):
                button = int(round(joystick.get_button(i)))  # Rounded since my controller is cheap and nasty
                item = {"button" + str(i): button}
                buttondata.append(item)
            jsonButtonData = json.dumps(buttondata)
            client.publish(mqtt_username + "/buttons", jsonButtonData)
            print(jsonButtonData)
    sleep(.1)