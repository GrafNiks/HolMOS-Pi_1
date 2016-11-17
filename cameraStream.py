# Streamt Kamerabild uebers Netzwerk im h264 Format
# Moegliche Einstellung von ISO, brightness, contrast, saturation -> ansonsten automatische Belichtung/Verstaerkung

import socket
import time
import picamera
import os

# Variablen
PORT = 8000

# Kamera
x_res = 640
y_res = 480
framerate = 24

# init picam
cam = picamera.PiCamera()
cam.resolution = (x_res, y_res)
cam.framerate = framerate

# init server
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', PORT))
server_socket.listen(0)

# ------
# temp = os.popen('ifconfig eth0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
# ip=temp.read().split('\n')
# ip.pop()

ip = 123

print "--------------------------------------------"
print "Stream: Format: h264"
print "        IP: {}".format(ip)
print "        Port: {}".format(PORT)
print "VLC: tcp/h264://{}:{}/".format(ip, PORT)
print "--------------------------------------------"


duration = input("Wie lange soll der Stream gehen?")
answer = raw_input("Parameter anpassen? (y/yes/j/ja)")

# siehe http://picamera.readthedocs.io/en/release-1.12/api_camera.html

if answer in ['y','yes','j','ja']:
    cam.ISO = input("ISO? (100, 200, 320, 400, 500, 640, 800 (,1600))")
    cam.sharpness = input("Schaerfe? (-100 bis 100)")
    cam.contrast = input("Kontrast? (-100 bis 100)")
    cam.brightness = input("Helligkeit? (0-100)")
    cam.saturation = input("Saettigung? (-100 bis 100)")
    


# 1. connection: 

#connection, addr = server_socket.accept()
connection = server_socket.accept()[0].makefile('rb')

try:
    print ""
    print " ist verbunden, starte {} Sekunden Stream".format(duration)

    cam.start_recording(connection, format='h264')
    cam.wait_recording(duration)
    cam.stop_recording()
finally:
    print "Beendet."

    connection.close()
    cam.close()
    server_socket.close()
