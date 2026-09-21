import cv2
from ultralytics import YOLO
import numpy as np

#Load pre-trained model. n indicates that it is the nano size, i.e. the smallest model. The example uses YOLOv8, you can also use yolo11n-pose.pt or yolo26n-pose.pt.
model = YOLO("yolov8n-pose.pt")

#Initialize the camera. This example uses a webcam which is by default 0. 
inputCamera = cv2.VideoCapture(0)

rested = False
succesful = 0

#Loop as long as inputCamera remains open. In other words, you can quit by pressing 'q' or if the camera crashes. 
while inputCamera.isOpened():
    success, frame = inputCamera.read()
    if not success:
        print("ERROR: Empty frame.")
        break

  #Run pose prediction on the current frame.
  #CPU only: poseResults = model(frame, stream=True, device="cpu")
  #GPU: poseResults = model(frame, stream=True)
    poseResults = model(frame, stream=True)  

  #Visualize the results and draw it on the current frame. 
    for r in poseResults:
    #Draw the 17 keypoints. Details for the keypoints are here: https://docs.ultralytics.com/tasks/pose. 
        annotatedFrame = r.plot()
        xy_coords = r.keypoints.xy 
        body = xy_coords[0]
        LShoulder = body[5]
        RShoulder = body[6]
        LElbow = body[7]
        RElbow = body[8]
        LWrist = body[9]
        RWrist = body[10]
       # print("LShoulder:",LShoulder)
       # print("RShoulder:",RShoulder)
       # print("LElbow:",LElbow)
       # print("RElbow:",RElbow)
       # print("LWrist:",LWrist)
       # print("RWist:",RWrist) 
        ElbowShoulder = np.array(RShoulder) - np.array(RElbow)
        ElbowWrist = np.array(RWrist) - np.array(RElbow)
        cosine_angle = np.dot(ElbowShoulder, ElbowWrist) / (np.linalg.norm(ElbowShoulder) * np.linalg.norm(ElbowWrist))
        angle = np.arccos(cosine_angle)
        print (np.degrees(angle))
        if np.degrees(angle) > 150:
          rested = True
        print (rested)
        if np.degrees(angle) < 40 and rested:
          rested = False
          succesful = succesful + 1
        print (succesful)
          

   
    

  #Display the annotated frame. 
    cv2.imshow("Pose Estimation", annotatedFrame)

  #Allow a quit option by pressing 'q'. 
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

#Clean up. 
inputCamera.release()
cv2.destroyAllWindows()

