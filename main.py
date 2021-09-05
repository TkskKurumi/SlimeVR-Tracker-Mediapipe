import cv2,math,time
from concurrent.futures import ThreadPoolExecutor
import mediapipe as mp
import UdpClient,geometry,random
from fps_handler import fps_handler as FPSH
import detect
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
fps_handler=FPSH()
# For static images:
IMAGE_FILES = []


hip_sensor=UdpClient.client()
lankle_sensor=UdpClient.client()
rankle_sensor=UdpClient.client()
tps_handler=FPSH()
_i,_j,_k=geometry._i,geometry._j,geometry._k
hip_axis=geometry.coordinate_sys(_i,_j,_k)
hip_X=_i
hip_Y=_j
lankle_X=_i
lankle_Y=_j
rankle_X=_i
rankle_Y=_j
tp=ThreadPoolExecutor()
tp.submit(detect.run)
#print('ln29')
def linear(a,b,n):
    return a*n+b*(1-n)
def vecs2quat(axisX,axisY):
    cord_sys=geometry.coordinate_sys.from_approx_xy(axisX,axisY)
    return cord_sys.as_quaternion()
while(detect.running):
    #print('ln33')
    tps_handler.limit_fps(120)
    tps=tps_handler.frame()
    dt=1/tps
    smoothing=math.e**(-dt*4)   #dt↑，smoothing↓
                                #x(t)=x1+(x0-x1)*e^(-dt)
    lankle_X=linear(lankle_X,detect.lankle_X,smoothing)
    rankle_X=linear(rankle_X,detect.rankle_X,smoothing)
    lankle_Y=linear(lankle_Y,detect.lankle_Y,smoothing)
    rankle_Y=linear(rankle_Y,detect.rankle_Y,smoothing)
    hip_X=linear(hip_X,detect.hip_X,smoothing)
    hip_Y=linear(hip_Y,detect.hip_Y,smoothing)
    
    lankle_quat=vecs2quat(lankle_X,lankle_Y)*detect.calibrate_quat
    rankle_quat=vecs2quat(rankle_X,rankle_Y)*detect.calibrate_quat
    hip_quat=vecs2quat(hip_X,hip_Y)*detect.calibrate_quat
    
    lankle_sensor.send_quat(lankle_quat)
    rankle_sensor.send_quat(rankle_quat)
    hip_sensor.send_quat(hip_quat)
    ypr=geometry.quat_to_ypr(hip_quat)
    #print(smoothing)
    print("smooth tick/sec=%.1f, real tick/sec=%.1f, yaw=%.1f,pitch=%.1f,roll=%.1f"%(tps,detect.fps,*ypr),end='\r')
#tp.join()