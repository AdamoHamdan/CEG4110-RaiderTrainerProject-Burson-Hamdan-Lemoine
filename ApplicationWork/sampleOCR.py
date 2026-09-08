#pip install easyocr
#pip uninstall opencv-python opencv-python-headless opencv-contrib-python
#pip install opencv-python

import cv2
import easyocr

#Initialize the webcam, which is typically 0
cameraFeed = cv2.VideoCapture(0)

#Initialize EasyOCR for English
reader = easyocr.Reader(['en']) 

#Open the camera and grab the image frame into cameraFrame and the camera status into cameraStatus 
while cameraFeed.isOpened():
    cameraStatus, cameraFrame = cameraFeed.read()
    if not cameraStatus:
        break

    #Read text from frame
    text = reader.readtext(cameraFrame)
    
    #Print out any recognized text into the console 
    for detection in text:
        print(detection[1])

    #Show the webcam feed 
    cv2.imshow('Webcam', cameraFrame)

    #Press 'q' to quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Perform cleanup 
cameraFeed.release()
cv2.destroyAllWindows()




