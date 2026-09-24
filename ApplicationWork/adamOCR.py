# pip install easyocr
# pip uninstall opencv-python opencv-python-headless opencv-contrib-python
# pip install opencv-python

import cv2
import easyocr
import re

# creates list of all valid weights to use in trainer
weights = [5, 10, 15]

#Initialize the webcam, which is typically 0
cameraFeed = cv2.VideoCapture(0)

#Initialize EasyOCR for English
reader = easyocr.Reader(['en'])

# method to scan and detect any weight in camera
def scanWeight(text):
    # scans for all text in camera
    for detection in text:
        # displays scanned text
        scannedText = detection[1]

        # tracker to show the OCR has detected text
        print("Value Scanned:", scannedText)

        # looks for numbers in the detected text
        numbers = re.findall(r'\d+', scannedText)

        # loop to check all the found values in the detected text
        for number in numbers:
            # creates a value for detected weight text
            weight = int(number)
            # checks to see if detected weight is part of the three valid weight options
            if weight in weights:
                return weight
            # if not a valid weight return nothing
            else:
                print("No valid weight scanned")
                return None

#Open the camera and grab the image frame into cameraFrame and the camera status into cameraStatus 
while cameraFeed.isOpened():
    cameraStatus, cameraFrame = cameraFeed.read()
    if not cameraStatus:
        break

    #Read text from frame
    text = reader.readtext(cameraFrame)

    # scan for a valid weight
    scannedWeight = scanWeight(text)

    # display the weight
    if scannedWeight is not None:
        # displays on OCR camera the valid weight scanned
        print("Valid Weight Scanned:", scannedWeight, "lbs")
        cv2.putText(cameraFrame, "Valid Weight:" + str(scannedWeight) + "lbs", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    # if scanned weight is not valid
    else:
        cv2.putText(cameraFrame, "Show Weight (5/10/15 lbs)", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    #Show the webcam feed
    cv2.imshow("Weight Detection Webcam:", cameraFrame)

    #Press 'q' to quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Perform cleanup
cameraFeed.release()
cv2.destroyAllWindows()