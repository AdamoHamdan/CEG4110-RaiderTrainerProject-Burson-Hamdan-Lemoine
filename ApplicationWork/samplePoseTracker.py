import cv2
from ultralytics import YOLO
import numpy as np
import time

#Load pre-trained model. n indicates that it is the nano size, i.e. the smallest model. The example uses YOLOv8, you can also use yolo11n-pose.pt or yolo26n-pose.pt.
model = YOLO("yolov8n-pose.pt")

#Initialize the camera. This example uses a webcam which is by default 0. 
inputCamera = cv2.VideoCapture(0)

RestedPosition = False # bool that says if the person has done the downward motion of the exercise
Reps = 0 # number of current reps completed
TotReps = 3 # number of total reps selected by the user
Sets = 0 # number of completed sets
TotSets = 2 # number of total sets selected by the user
RestTime = 5 # the rest time selected by the user
Curl = True # whether they are doing a curl or not
RightSide = True # whether they are using the right or left arm



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
        # V Data for the calcs, do not edit V
        annotatedFrame = r.plot()
        xy_coords = r.keypoints.xy 
        body = xy_coords[0]
        LShoulder = body[5]
        RShoulder = body[6]
        LElbow = body[7]
        RElbow = body[8]
        LWrist = body[9]
        RWrist = body[10]
        LHip = body[11]
        RHip = body[12]
        # ^ Data for the calcs, do not edit ^
        print("Number of Reps: ", Reps) #printed reps
        print("Number of Sets: ", Sets) #printed sets

        #code for calcing the reps and sets
        if(Curl == True and RightSide):# right arm curl
          ElbowToShoulder = np.array(RShoulder) - np.array(RElbow)
          ElbowToWrist = np.array(RWrist) - np.array(RElbow)
          cosine_angle = np.dot(ElbowToShoulder, ElbowToWrist) / (np.linalg.norm(ElbowToShoulder) * np.linalg.norm(ElbowToWrist))
          angle = np.arccos(cosine_angle)
          if(np.degrees(angle) > 150):
            RestedPosition = True
          if(np.degrees(angle) < 40 and RestedPosition):
            RestedPosition = False
            Reps = Reps + 1
        elif(Curl == True and RightSide == False):# left arm curl
          ElbowToShoulder = np.array(LShoulder) - np.array(LElbow)
          ElbowToWrist = np.array(LWrist) - np.array(LElbow)
          cosine_angle = np.dot(ElbowToShoulder, ElbowToWrist) / (np.linalg.norm(ElbowToShoulder) * np.linalg.norm(ElbowToWrist))
          angle = np.arccos(cosine_angle)
          if(np.degrees(angle) > 150):
            RestedPosition = True
          if(np.degrees(angle) < 40 and RestedPosition):
            RestedPosition = False
            Reps = Reps + 1
        elif(Curl == False and RightSide):# right arm raise
          ShoulderToHip = np.array(RHip) - np.array(RShoulder)
          ShoulderToWrist = np.array(RWrist) - np.array(RShoulder)
          cosine_angle = np.dot(ShoulderToHip, ShoulderToWrist) / (np.linalg.norm(ShoulderToHip) * np.linalg.norm(ShoulderToWrist))
          angle = np.arccos(cosine_angle)
          if(np.degrees(angle) > 150):
            RestedPosition = True
          if(np.degrees(angle) < 40 and RestedPosition):
            RestedPosition = False 
            Reps = Reps + 1
        elif(Curl == False and RightSide):# left arm raise
          ShoulderToHip = np.array(RHip) - np.array(RShoulder)
          ShoulderToWrist = np.array(RWrist) - np.array(RShoulder)
          cosine_angle = np.dot(ShoulderToHip, ShoulderToWrist) / (np.linalg.norm(ShoulderToHip) * np.linalg.norm(ShoulderToWrist))
          angle = np.arccos(cosine_angle)
          if(np.degrees(angle) > 150):
            RestedPosition = True
          if(np.degrees(angle) < 40 and RestedPosition):
            RestedPosition = False
            Reps = Reps + 1

        if(Reps == TotReps):# code for the rest period
          print("Resting")
          time.sleep(RestTime)
          print("Rest Over Continue")
          Sets = Sets + 1
          Reps = 0

        if(Sets == TotSets):
          print("Workout Finished")

        
          

   
    

  #Display the annotated frame. 
    cv2.imshow("Pose Estimation", annotatedFrame)

  #Allow a quit option by pressing 'q'. 
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

#Clean up. 
inputCamera.release()
cv2.destroyAllWindows()

