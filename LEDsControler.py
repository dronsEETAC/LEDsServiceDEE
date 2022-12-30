import threading

import paho.mqtt.client as mqtt

import time
import board
import neopixel
import RPi.GPIO as GPIO



LEDSequenceOn = False


def led_sequence():
    global op_mode
    global LEDSequenceOn

    if op_mode == 'simulation':

        while LEDSequenceOn:
            print("RED")
            time.sleep(1)
            print("GREEN")
            time.sleep(1)
            print("YELLOW")
            time.sleep(1)
    else:
        while LEDSequenceOn:
            pixels[0] = (255, 0, 0)
            time.sleep(1)
            pixels[0] = (0, 255, 0)
            time.sleep(1)
            pixels[0] = (255, 255, 0)
            time.sleep(1)

def on_message(client, userdata, message):
    global LEDSequenceOn
    splited = message.topic.split("/")
    origin = splited[0]
    destination = splited[1]
    command = splited[2]


    if command == "startLEDsSequence":
        print("Start LED sequence")
        LEDSequenceOn = True
        w = threading.Thread(target=led_sequence)
        w.start()

    if command == "stopLEDsSequence":
        print("Stop LED sequence")
        LEDSequenceOn = False

    if command == "LEDsSequenceForNSeconds":
        seconds = int(message.payload.decode("utf-8"))
        print("LED sequence for " + str(seconds) + " seconds")
        LEDSequenceOn = True
        w = threading.Thread(target=led_sequence)
        w.start()
        time.sleep(int(seconds))
        LEDSequenceOn = False

    if op_mode == 'simulation':
        if command == 'red':
            print('RED')
            time.sleep(5)
            print ('CLEAR')

        if command == 'green':
            print('GREEN')
            time.sleep(5)
            print('CLEAR')

        if command == 'blue':
            print('BLUE')
            time.sleep(5)
            print('CLEAR')

        if command == 'drop':
            if op_mode == 'simulation':
                print('DROP')

        if command == 'reset':
            p.ChangeDutyCycle(2.5)

        if command == 'bluei':
            print('BLUE')
        if command == 'redi':
            print('RED')
        if command == 'greeni':
            print('GREEN')
        if command == 'yellowi':
            print('YELLOW')
        if command == 'pinki':
            print('PINK')
        if command == 'whitei':
            print('WHITE')
        if command == 'blacki':
            print('BLACK')
        if command == 'clear':
            print('CLEAR')
    else:
        if command == 'red':
            pixels[0] = (255, 0, 0)
            time.sleep(5)
            pixels[0] = (0, 0, 0)

        if command == 'green':
            pixels[1] = (0, 255, 0)
            time.sleep(5)
            pixels[1] = (0, 0, 0)

        if command == 'blue':
            pixels[2] = (0, 0, 255)
            time.sleep(5)
            pixels[2] = (0, 0, 0)

        if command == 'drop':
            p.ChangeDutyCycle(7.5)

        if command == 'reset':
            p.ChangeDutyCycle(2.5)
        if command == 'bluei':
            pixels[0] = (0, 0, 255)
        if command == 'redi':
            pixels[0] = (107, 0, 0)
        if command == 'greeni':
            pixels[0] = (0, 255, 0)
        if command == 'yellowi':
            pixels[0] = (255, 255, 0)
        if command == 'pinki':
            pixels[0] = (255, 192, 203)
        if command == 'whitei':
            pixels[0] = (255, 255, 255)
        if command == 'blacki':
            pixels[0] = (10, 10, 10)
        if command == 'clear':
            pixels[0] = (0, 0, 0)


def LEDsServ (connection_mode, operation_mode):

    global op_mode
    global external_client
    global internal_client
    global pixels
    global p

    print ('Connection mode: ', connection_mode)
    print ('operation mode: ', operation_mode)
    op_mode = operation_mode


    pixels = neopixel.NeoPixel(board.D18, 5)
    servoPIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    p = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz

    # The internal broker is always (global or local mode) at localhost:1884
    internal_broker_address = "localhost"
    internal_broker_port = 1884

    if connection_mode == 'global':
        # in global mode, the external broker must be running in internet
        # and must operate with websockets
        # there are several options:
        # a public broker
        external_broker_address = "broker.hivemq.com"
        # our broker (that requires credentials)
        #external_broker_address = "classpip.upc.edu"
        # a mosquitto broker running at localhost (only in simulation mode)
        #external_broker_address = "localhost"

    else:
        # in local mode, the external broker will run always in localhost
        # (either in production or simulation mode)
        external_broker_address = "localhost"

    # the external broker must run always in port 8000
    external_broker_port = 8000


    external_client = mqtt.Client("LEDs_external", transport="websockets")
    external_client.on_message = on_message
    external_client.connect(external_broker_address, external_broker_port)


    internal_client = mqtt.Client("LEDs_internal")
    internal_client.on_message = on_message
    internal_client.connect(internal_broker_address, internal_broker_port)

    print("Waiting....")
    external_client.subscribe("+/LEDsService/#")
    internal_client.subscribe("+/LEDsService/#")
    internal_client.loop_start()
    external_client.loop_forever()


if __name__ == '__main__':
    import sys
    connection_mode = sys.argv[1] # global or local
    operation_mode = sys.argv[2]  # simulation or production
    LEDsServ(connection_mode,  operation_mode)
