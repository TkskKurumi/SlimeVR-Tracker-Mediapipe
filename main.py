import cv2,math,time
import mediapipe as mp
import UdpClient,geometry,random
from fps_handler import fps_handler as FPSH
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# For static images:
IMAGE_FILES = []
BG_COLOR = (192, 192, 192) # gray

hip_sensor=UdpClient.client()
fps_handler=FPSH()
_i,_j,_k=geometry._i,geometry._j,geometry._k
hip_axis=geometry.coordinate_sys(_i,_j,_k)
hip_X=0
hip_Y=0
# For webcam input:
cap = cv2.VideoCapture(3)
lsxyz=['x','y','z']
def landmark2point(landmark):
  x=landmark.x
  y=-landmark.z
  z=landmark.y*height/width
  return geometry.point3d(x,y,z)
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.7,model_complexity=1) as pose:
  while cap.isOpened():
    fps_handler.limit_fps(30)
    fps=fps_handler.frame()
    success, image = cap.read()
    height,width=image.shape[:2]
    #sensor1.handle_receive()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = pose.process(image)

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image//=50
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    if(results.pose_landmarks):
      right_hip=landmark2point(results.pose_landmarks.landmark[24])
      left_hip=landmark2point(results.pose_landmarks.landmark[23])
      right_shoulder=landmark2point(results.pose_landmarks.landmark[12])
      left_shoulder=landmark2point(results.pose_landmarks.landmark[11])

      smoothing=1-math.e**(-4/fps)
      _hip_X=left_shoulder+left_hip-right_hip-right_shoulder
      hip_X=hip_X*(1-smoothing)+_hip_X*smoothing
      _hip_Y=left_hip+right_hip-left_shoulder-right_shoulder
      hip_Y=hip_Y*(1-smoothing)+_hip_Y*smoothing
      hip_Z=hip_X**hip_Y

      dic={'x':hip_X,'y':hip_Y,'z':hip_Z}
      ax1=hip_X
      ax2=hip_Y
      #ax1=_i*math.sin(time.time())+_j*math.cos(time.time())
      #ax2=_i*math.sin(time.time()+math.pi/2)+_j*math.cos(time.time()+math.pi/2)
      hip_axis=geometry.coordinate_sys.from_approx_xy(ax1,ax2)
      print(hip_axis.axisX,hip_axis.axisY,hip_axis.axisZ)
      #hip_axis=geometry.coordinate_sys.fro`m_approx_xy(hip_Z,hip_X)
      #hip_axis=geometry.coordinate_sys.from_approx_xy(hip_X,hip_Z)
      hip_quat=hip_axis.as_quaternion()
      #x,y,z,w=hip_quat
      #print(geometry.aequal(x*x+y*y+z*z+w*w,1))
      hip_sensor.send_quat(hip_quat)
      yaw,pitch,roll=geometry.quat_to_ypr(hip_quat)
      az="%.2ffps"%fps+"Yaw%04dPitch%04dRoll%04d %s %.2f"%(yaw,pitch,roll,lsxyz,smoothing)
      font = cv2.FONT_HERSHEY_SIMPLEX
      cv2.putText(image,az,(300,300),font,1,(0,255,0),2)
      #hip_sensor.send_handshake()
      #i,j=random.sample([_i,_j,_k],2)
      #hip_sensor.send_quat(geometry.coordinate_sys(i,j,i**j).as_quaternion())
      #hip_sensor.handle_receive()
      pass
      #print(results.pose_landmarks.landmark[32].x,end='\r')
    cv2.imshow('MediaPipe Pose', image)
    k=cv2.waitKey(2) & 0xFF
    if k == 27:
      print()
      break
    elif(k==13 or k==10):
      random.shuffle(lsxyz)
cap.release()