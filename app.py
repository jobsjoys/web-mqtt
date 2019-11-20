from flask_socketio import SocketIO
from flask import Flask, render_template
from time import sleep
from threading import Thread, Event
import paho.mqtt.client as mqtt
import os

app = Flask(__name__)

app.config['DEBUG'] = False

# turn the flask app into a socketio app
socketio = SocketIO(app)

# create Thread
thread = Thread()
thread_stop_event = Event()

MQTTDataPayload = ''

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(os.environ.get('mqtt_username') + '/topic1')


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    global MQTTDataPayload
    MQTTDataPayload = msg.topic + ' ' + str(msg.payload.decode("utf-8"))


class GetMQTTDataThread(Thread):

    def __init__(self):
        self.delay = 1
        super(GetMQTTDataThread, self).__init__()

    def getMQTTdata(self):

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.username_pw_set(os.environ.get('mqtt_username'), os.environ.get('mqtt_password'))
        client.connect("maqiatto.com", 1883, 60)

        client.loop_start()

        while not thread_stop_event.isSet():

            mqtt_string01 = MQTTDataPayload

            socketio.emit('mqtt_data', {'mqtt_string01': mqtt_string01}, namespace='/test')
            sleep(self.delay)


    def run(self):
        self.getMQTTdata()


@app.route('/')
def index():
    # only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')


@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    # Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = GetMQTTDataThread()
        thread.start()


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, '127.0.0.1', 6968)
