import cv2
from ultralytics import YOLO

#Load pre-trained model. n indicates that it is the nano size, i.e. the smallest model. The example uses YOLOv8, you can also use yolo11n-pose.pt or yolo26n-pose.pt.
model = YOLO("yolov8n-pose.pt")

#Initialize the camera. This example uses a webcam which is by default 0. 
inputCamera = cv2.VideoCapture(0)

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

  #Display the annotated frame. 
  cv2.imshow("Pose Estimation", annotatedFrame)

  #Allow a quit option by pressing 'q'. 
  if cv2.waitKey(1) & 0xFF == ord("q"):
    break

#Clean up. 
inputCamera.release()
cv2.destroyAllWindows()
