import cv2,math,time,traceback,kdt
import mediapipe as mp
import UdpClient,geometry,random
from fps_handler import fps_handler as FPSH
from threading import Lock
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
fps_handler=FPSH()
cap = cv2.VideoCapture(2)
hide_image=True
_i,_j,_k=geometry._i,geometry._j,geometry._k
hip_X=_i
hip_Y=_j
lankle_X=_i
lankle_Y=_j
rankle_X=_i
rankle_Y=_j
lleg_X=_i
lleg_Y=_j
rleg_X=_i
rleg_Y=_j

BG_COLOR = (192, 192, 192) # gray
height=720
width=1280
def landmark2point(landmark):
    
    #Oh no I wrote wrong quat2yaw pitch roll convertion that actually
    #returns pitch roll yaw, which is in wrong order
    #But I didn't noticed that and thought that may be SlimeVR coordinate
    #isn't same as camera coordinate and tried to convert this.
    global height,width
    x=landmark.x
    y=-landmark.z
    z=landmark.y*height/width
    return geometry.point3d(x,y,z)
lm2p=landmark2point
running=True
fps=1
#calibrate_quat=geometry.quaternion.e()
events=[]
def vecs2quat(axisX,axisY):
    cord_sys=geometry.coordinate_sys.from_approx_xy(axisX,axisY)
    return cord_sys.as_quaternion()

calibrate_key=[]
calibrate_value=[]
calibrate_kdt=None
kdt_lock=Lock()
def get_calibrate(k=None):
    #when facing direction change, the MediaPipe's Z detection may be not stable
    #I'm trying to use different calibrate quat according to facing direction
    global calibrate_key,calibrate_value,calibrate_kdt,hip_X,hip_Y,landmark
    if(not calibrate_kdt):
        return geometry.quaternion.e()
    if(calibrate_num>len(calibrate_key)):
        return geometry.quaternion.e()
    if(k is None):
        #k=tuple(hip_X)+tuple(hip_Y)
        k=get_calibrate_vec(landmarks)
    kdt_lock.acquire()
    id=calibrate_kdt.ann1(kdt.point(tuple(k))).id
    kdt_lock.release()
    #print(id)
    return calibrate_value[id]
calibrate_num=0
camera_base=geometry.coordinate_sys(_i,_j,_k)
slimevr_base=geometry.coordinate_sys(lm2p(_i),lm2p(_j),lm2p(_k)).united()
#print(slimevr_base.axisZ)
def get_calibrate_vec(landmarks):
    base=lm2p(landmarks[11])
    ret=[]
    for i in landmarks[12:]:
        ret.extend(lm2p(i)-base)
    return ret
def run():
    
    global cap,hide_image,fps_handler,height,width,running,fps,events
    global hip_X,hip_Y,lankle_X,lankle_Y,rankle_X,rankle_Y
    global lleg_X,lleg_Y,rleg_X,rleg_Y
    global calibrate_key,calibrate_value,calibrate_kdt,calibrate_num
    global landmarks
    try:
        
        with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.7,model_complexity=1) as pose:
            calibrate_time=0

            #I found that x=x,y=-z,z=y make the axis of rotation right
            #but I don't know why
            
            
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
                    left_foot=landmark2point(landmarks[31])
                    right_foot=landmark2point(landmarks[32])
                    left_heel=landmark2point(landmarks[29])
                    right_heel=landmark2point(landmarks[30])

                    v_left_leg=landmarks[27].visibility+landmarks[25].visibility
                    v_right_leg=landmarks[26].visibility+landmarks[28].visibility
                    v_left_foot=landmarks[31].visibility
                    v_right_foot=landmarks[23].visibility
                    #print(v_left_leg,v_right_leg)
                    
                    #update waist tracker info
                    hip_X=left_shoulder+left_hip-right_hip-right_shoulder
                    #hip_X=left_hip-right_hip
                    
                    hip_Y=left_hip+right_hip-left_shoulder-right_shoulder
                    
                    
                    hip_axis=geometry.coordinate_sys.from_approx_xy(hip_X,hip_Y)
                    hip_quat=hip_axis.as_quaternion()
                    #hip_sensor.send_quat(hip_quat)

                    if(v_left_leg>1): #left leg visible
                        lankle_Y=left_ankle-left_knee
                        if(v_left_foot<0.5):
                            lankle_Z=hip_X**lankle_Y
                        else:
                            lankle_Z=left_heel-left_foot
                        lankle_X=lankle_Y**lankle_Z
                        
                        lleg_Y=left_knee-left_hip
                        lleg_Z=hip_X**lleg_Y
                        lleg_X=lleg_Y**lleg_Z

                    if(v_right_leg>1):
                        #rankle_X=hip_X
                        rankle_Y=right_ankle-right_knee
                        if(v_right_foot<0.5):
                            rankle_Z=hip_X**rankle_Y
                        else:
                            rankle_Z=right_heel-right_foot
                        rankle_X=rankle_Y**rankle_Z
                        
                        
                        rleg_Y=right_knee-right_hip
                        rleg_Z=hip_X**rleg_Y
                        rleg_X=rleg_Y**rleg_Z

                    yaw,pitch,roll=geometry.quat_to_ypr(get_calibrate()*hip_quat)
                    if(calibrate_time<time.time()):
                        az="%.2ffps"%fps+"Yaw%04dPitch%04dRoll%04d"%(yaw,pitch,roll)
                        if(calibrate_num>len(calibrate_key)):
                            calibrated=True
                            az="calibrating"
                            #q1=slimevr_base.as_quaternion()
                            q2=hip_quat
                            hip_X1=geometry.point3d(hip_X.x,hip_X.y,0)  #no camera y, hotizontal
                            hip_Y1=geometry.point3d(0,0,hip_Y.z)        #only camera y, vertical
                            print('ln177',(hip_X1**hip_Y1).z>0)

                            #the this should make body aligned vertical
                            q1=vecs2quat(hip_X1,hip_Y1)
                            print(geometry.quat_to_ypr(q1))
                            calibrate_quat=q1/q2
                            key=get_calibrate_vec(landmarks)
                            #key=tuple(hip_X)+tuple(hip_Y)
                            calibrate_key.append(kdt.point(key))
                            calibrate_value.append(calibrate_quat)
                            if(calibrate_num<=len(calibrate_key)): #==
                                kdt_lock.acquire()
                                calibrate_kdt=kdt.kdt()
                                
                                calibrate_kdt.build(calibrate_key)
                                kdt_lock.release()
                            #yaw,pitch,roll=geometry.quat_to_ypr(calibrate_quat*hip_quat)
                            #print("Yaw%04dPitch%04dRoll%04d"%(yaw,pitch,roll))
                            print(geometry.quat_to_ypr(calibrate_quat*q2))
                    else:
                        az="%.1f seconds to calibrate,%d"%(calibrate_time-time.time(),calibrate_num)
                        
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(image,az,(300,300),font,1,(0,255,0),2)
                    
                cv2.imshow('MediaPipe Pose', image)
                k=cv2.waitKey(2) & 0xFF
                if k == 27:
                    break
                elif k==ord('h'):
                    hide_image=not hide_image
                elif k==ord('c'):
                    calibrate_time=time.time()+3
                    calibrate_num+=int(fps)*10
                else:
                    events.append(('keypress',k))
    except Exception as e:
        traceback.print_exc()
    running=False
    cv2.destroyAllWindows()