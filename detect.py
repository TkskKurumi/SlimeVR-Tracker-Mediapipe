import cv2,math,time,traceback
import mediapipe as mp
import UdpClient,geometry,random
from fps_handler import fps_handler as FPSH
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
fps_handler=FPSH()
cap = cv2.VideoCapture(3)
hide_image=True
_i,_j,_k=geometry._i,geometry._j,geometry._k
hip_X=_i
hip_Y=_j
lankle_X=_i
lankle_Y=_j
rankle_X=_i
rankle_Y=_j
BG_COLOR = (192, 192, 192) # gray
def landmark2point(landmark):
  global height,width
  x=landmark.x
  y=-landmark.z
  z=landmark.y*height/width
  return geometry.point3d(x,y,z)
running=True
fps=1
def run():
    global cap,hide_image,fps_handler,height,width,running,fps
    global hip_X,hip_Y,lankle_X,lankle_Y,rankle_X,rankle_Y
    try:
        
        with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.7,model_complexity=2) as pose:
            while cap.isOpened():
                fps_handler.limit_fps(30)
                fps=fps_handler.frame()
                success, image = cap.read()
                height,width=image.shape[:2]
                
                if not success:
                    print("Ignoring empty camera frame.")
                    continue

                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                
                
                image.flags.writeable = False
                results = pose.process(image)

                # Draw the pose annotation on the image.
                image.flags.writeable = True
                
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if(hide_image):
                    image//=50
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                
                if(results.pose_landmarks):
                    landmarks=results.pose_landmarks.landmark
                    right_hip=landmark2point(landmarks[24])
                    left_hip=landmark2point(landmarks[23])
                    right_shoulder=landmark2point(landmarks[12])
                    left_shoulder=landmark2point(landmarks[11])
                    left_ankle=landmark2point(landmarks[27])
                    right_ankle=landmark2point(landmarks[28])
                    left_knee=landmark2point(landmarks[25])
                    right_knee=landmark2point(landmarks[26])
                    left_foot=landmark2point(landmark2point[31])
                    right_foot=landmark2point(landmark2point[32])

                    v_left_leg=landmarks[27].visibility+landmarks[25].visibility
                    v_right_leg=landmarks[26].visibility+landmarks[28].visibility
                    v_left_foot=landmarks[31].visibility
                    v_right_foot=landmarks[23].visibility
                    #print(v_left_leg,v_right_leg)
                    
                    #update waist tracker info
                    hip_X=left_shoulder+left_hip-right_hip-right_shoulder
                    #hip_X=hip_X*(1-smoothing)+_hip_X*smoothing
                    hip_Y=left_hip+right_hip-left_shoulder-right_shoulder
                    #hip_Y=hip_Y*(1-smoothing)+_hip_Y*smoothing
                    hip_Z=hip_X**hip_Y
                    hip_axis=geometry.coordinate_sys.from_approx_xy(hip_X,hip_Y)
                    hip_quat=hip_axis.as_quaternion()
                    #hip_sensor.send_quat(hip_quat)

                    if(v_left_leg>1): #left leg visible
                        lankle_Y=left_ankle-left_knee
                        if(v_left_foot<0.5):
                            lankle_Z=hip_X**lankle_Y
                        else:
                            lankle_Z=left_ankle-left_foot
                        lankle_X=lankle_Y**lankle_Z
                        #lankle_axis=geometry.coordinate_sys.from_approx_xy(lankle_X,lankle_Y)
                        #lankle_quat=lankle_axis.as_quaternion()
                        #lankle_sensor.send_quat(lankle_quat)
                    if(v_right_leg>1):
                        #rankle_X=hip_X
                        rankle_Y=right_ankle-right_knee
                        if(v_right_foot<0.5):
                            rankle_Z=hip_X**rankle_Y
                        else:
                            rankle_Z=right_ankle-right_foot
                        rankle_X=rankle_Y**rankle_Z
                        #rankle_axis=geometry.coordinate_sys.from_approx_xy(rankle_X,rankle_Y)
                        #rankle_quat=rankle_axis.as_quaternion()
                        #rankle_sensor.send_quat(rankle_quat)
                    yaw,pitch,roll=geometry.quat_to_ypr(hip_quat)
                    az="%.2ffps"%fps+"Yaw%04dPitch%04dRoll%04d"%(yaw,pitch,roll)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(image,az,(300,300),font,1,(0,255,0),2)
                    
                cv2.imshow('MediaPipe Pose', image)
                k=cv2.waitKey(2) & 0xFF
                if k == 27:
                    
                    break
                elif k==ord('h'):
                    hide_image=not hide_image
    except Exception as e:
        print(e)
    running=False
    cv2.destroyAllWindows()