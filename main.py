import cv2
import mediapipe as mp
import UdpClient,geometry,random
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# For static images:
IMAGE_FILES = []
BG_COLOR = (192, 192, 192) # gray

hip_sensor=UdpClient.client()
_i,_j,_k=geometry._i,geometry._j,geometry._k
hip_axis=geometry.coordinate_sys(_i,_j,_k)
# For webcam input:
cap = cv2.VideoCapture(r"C:\[WPF]JJDown\Download\【MV】昨日に奏でる明日の歌 - 1.【MV】昨日に奏でる明日の歌 _ YURiMental(Av333232413,P1).mp4")
def landmark2point(landmark):
  return geometry.point3d(landmark.x,landmark.y*height/width,landmark.z)
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
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

      hip_X=left_shoulder-right_shoulder+left_hip-right_hip
      hip_Y=left_hip+right_hip-left_shoulder-right_shoulder
      hip_axis=geometry.coordinate_sys.from_approx_xy(hip_X,hip_Y)
      hip_quat=hip_axis.as_quaternion()
      #x,y,z,w=hip_quat
      #print(geometry.aequal(x*x+y*y+z*z+w*w,1))
      hip_sensor.send_quat(hip_quat)
      #hip_sensor.send_handshake()
      #i,j=random.sample([_i,_j,_k],2)
      #hip_sensor.send_quat(geometry.coordinate_sys(i,j,i**j).as_quaternion())
      #hip_sensor.handle_receive()
      pass
      #print(results.pose_landmarks.landmark[32].x,end='\r')
    cv2.imshow('MediaPipe Pose', image)
    if cv2.waitKey(2) & 0xFF == 27:
      print()
      break
cap.release()