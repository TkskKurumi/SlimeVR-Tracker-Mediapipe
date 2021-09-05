import math,time
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


hip_client=UdpClient.client()
lankle_client=UdpClient.client()
rankle_client=UdpClient.client()
lleg_client=UdpClient.client()
rleg_client=UdpClient.client()
clients=[hip_client,lankle_client,rankle_client,lleg_client,rleg_client]
client_num=1

tps_handler=FPSH()
_i,_j,_k=geometry._i,geometry._j,geometry._k
hip_axis=geometry.coordinate_sys(_i,_j,_k)
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
    for i in detect.events:
        if(i[0]=='keypress'):
            k=i[1]
            c=chr(k)
            if(c in '12345'):
                client_num=int(c)
                print('client_num =',client_num)
        else:
            print(i)

    detect.events=[]
    tps_handler.limit_fps(400)
    tps=tps_handler.frame()
    dt=1/tps
    smoothing=math.e**(-dt*8)   #dt↑，smoothing↓
                                #x(t)=x1+(x0-x1)*e^(-dt)
    lankle_X=linear(lankle_X,detect.lankle_X,smoothing)
    rankle_X=linear(rankle_X,detect.rankle_X,smoothing)
    lankle_Y=linear(lankle_Y,detect.lankle_Y,smoothing)
    rankle_Y=linear(rankle_Y,detect.rankle_Y,smoothing)
    hip_X=linear(hip_X,detect.hip_X,smoothing)
    hip_Y=linear(hip_Y,detect.hip_Y,smoothing)
    lleg_X=linear(lleg_X,detect.lleg_X,smoothing)
    lleg_Y=linear(lleg_Y,detect.lleg_Y,smoothing)
    rleg_X=linear(rleg_X,detect.rleg_X,smoothing)
    rleg_Y=linear(rleg_Y,detect.rleg_Y,smoothing)

    quats=[]
    hip_quat=vecs2quat(hip_X,hip_Y)
    quats.append(hip_quat) #waist
    quats.append(vecs2quat(lankle_X,lankle_Y)) #left_ankle
    quats.append(vecs2quat(rankle_X,rankle_Y)) #right_ankle
    quats.append(vecs2quat(lleg_X,lleg_Y))
    quats.append(vecs2quat(rleg_X,rleg_Y))
    
    
    for i in range(client_num):
        clients[i].send_quat(detect.calibrate_quat*quats[i])
    ypr=geometry.quat_to_ypr(hip_quat)
    #print(smoothing)
    print("smooth tick/sec=%.1f, real tick/sec=%.1f, yaw=%.1f,pitch=%.1f,roll=%.1f"%(tps,detect.fps,*ypr),end='\r')
#tp.join()