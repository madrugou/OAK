import pyrealsense2 as rs
import numpy as np
import depthai as dai
import cv2
import RPi.GPIO as GPIO
import time
import imutils


print("Load all libraries")
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
ledPin = 12
buttonPin = 7
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#camera quadrada
print("Create camera config")
pipeline = dai.Pipeline()
camRgb = pipeline.createColorCamera()
xoutRgb = pipeline.createXLinkOut()
xoutRgb.setStreamName("rgb")
camRgb.setPreviewSize(1280, 720)
camRgb.preview.link(xoutRgb.input)
camRgb.setFps(60) 
device_info = dai.DeviceInfo("172.16.2.100")

#realsense
# Configure depth and color streams
#pipeline_rs = rs.pipeline()
#config = rs.config()

# Get device product line for setting a supporting resolution
#pipeline_wrapper = rs.pipeline_wrapper(pipeline_rs)
#pipeline_profile = config.resolve(pipeline_wrapper)
#device_rs = pipeline_profile.get_device()


#config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)

# Start streaming

#pipeline_rs.start(config)


print("Starting camera ...")
with dai.Device(pipeline, device_info) as device:
    qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
    i = 0
    while True:
        buttonState = GPIO.input(buttonPin)
        
        # get frame oak-d
        frame = qRgb.get().getCvFrame()
        show_frame = imutils.resize(frame, width=640)
        
        # get frame realsense
 #       frames = pipeline_rs.wait_for_frames()
  #      color_frame = frames.get_color_frame()
   #     color_image = np.asanyarray(color_frame.get_data())
       
       
        if buttonState == False:
            GPIO.output(ledPin, GPIO.HIGH)
            time.sleep(0.8) # depois tu altera
            
            data = time.ctime()
            data = str(data)
            
            name_image_oak = "./OAK1/{}.jpg".format(data)
 #           name_image_rs = "./realsenseprint/{}.jpg".format(data)
            
            cv2.imwrite(name_image_oak, frame) 
   #         cv2.imwrite(name_image_rs, color_image)
            print(f"OAK1: *{name_image_oak}* saved.")
  #          print(f"REALSENSE: *{name_image_rs}* saved.")

            i += 1
        else:
            GPIO.output(ledPin, GPIO.LOW)

        
        #final_frame = np.hstack((frame, color_image))
        #cv2.imshow("Stream", final_frame)

        
        cv2.imshow("OAK1", show_frame)
    #    cv2.imshow("realsense", color_image)
        
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            pipeline_rs.stop()
            break
       
pipeline_rs.stop()
        

        #if key == ord('s'):
        #   cv2.imwrite(f"image_{i}.jpg", frame)
        #    print("Image saved :)")
        #i += 1

