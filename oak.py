import pyrealsense2 as rs
import numpy as np
import depthai as dai
import cv2
import RPi.GPIO as GPIO
import time
import imutils
import serial
from controller.imageController import ImageController

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1) 

print("Load all libraries")
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
ledPin = 12
buttonPin = 7
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Create camera config")
pipeline = dai.Pipeline()
camRgb = pipeline.createColorCamera()
xoutRgb = pipeline.createXLinkOut()
xoutRgb.setStreamName("rgb")
camRgb.setPreviewSize(1280, 720)
camRgb.preview.link(xoutRgb.input)
camRgb.setFps(60) 
device_info = dai.DeviceInfo("172.16.2.100")

print("Starting camera ...")
with dai.Device(pipeline, device_info) as device:
    qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
    i = 0
    while True:
        line = ser.readline()
        latlong = line.decode('utf-8')
        buttonState = GPIO.input(buttonPin)       
        frame = qRgb.get().getCvFrame()
        show_frame = imutils.resize(frame, width=640)    
       
        if (buttonState == False & latlong.startswith("$GPRMC")):
            GPIO.output(ledPin, GPIO.HIGH)
            time.sleep(0.8) # depois tu altera
            string = (latlong.split(',')[:10])
            file_name = string[9]+'_'+string[1]+'_'+string[3]+'_'+string[5]
            data = time.ctime()
            data = str(data)
            name_image_oak = f"./OAK1/{file_name}.jpg"
            cv2.imwrite(name_image_oak, frame) 
            print(f"OAK1: *{name_image_oak}* saved.")

            lat, lon = string[3], string[5]
            
            image_saved = ImageController.insert(name_image_oak, lat, lon)

            if image_saved:
                data_save = f'{name_image_oak} - {lat} - {lon}'
                print(f"Imagem salva no banco de dados: {data_save}")

            i += 1
        else:
            GPIO.output(ledPin, GPIO.LOW)
        cv2.imshow("OAK1", show_frame)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            pipeline.stop()
            break
       
pipeline.stop()
        