# Taken from:
# https://stackoverflow.com/questions/45364877/interpreting-keypresses-sent-to-raspberry-pi-through-uv4l-webrtc-datachannel
# based on:
# https://raspberrypi.stackexchange.com/questions/29480/how-to-use-pigpio-to-control-a-servo-motor-with-a-keyboard
# public domain

import socket
import time
import pigpio
import os
socket_path = '/tmp/uv4l.socket'

try:
    os.unlink(socket_path)
except OSError:
    if os.path.exists(socket_path):
        raise

s = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)


print 'socket_path: %s' % socket_path
s.bind(socket_path)
s.listen(1)
pan = 1500
tilt = 1500
pand = 0
tiltd = 0
while True:
    print 'awaiting connection...'
    connection, client_address = s.accept()
    print 'client_address %s' % client_address
    try:
        print 'established connection with', client_address

        pi = pigpio.pi()

        while True:
            data = connection.recv(16)
            pi.set_servo_pulsewidth(12, tilt)
            pi.set_servo_pulsewidth(13, pan)
            print tilt, pan
            if data == 'up':
                pand = -20
            elif data == 'down':
                pand = 20
            elif data == 'left':
                tilt = 1300
            elif data == 'right':
                tilt = 1700
            elif data == 'stop':
                pand = tiltd = 0
                tilt = 1500
            else:
                continue

            if (data == 'up' or data == 'down') and pan + pand >= 500 and pan + pand <= 2000:
                pan = pan+pand

    finally:

        connection.close()
