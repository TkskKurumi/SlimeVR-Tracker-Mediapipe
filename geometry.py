from math import sqrt,atan2,asin
import math
def asign(i,eps=1e-8):
    if(i>eps):
        return 1
    elif(i<-eps):
        return -1
    else:
        return 0
def aequal(x,y,eps=1e-8):
    return asign(x-y)==0
class point3d:
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
    def __iter__(self):
        return tuple([self.x,self.y,self.z]).__iter__()
    
    def __pow__(self,other):
        if(isinstance(other,point3d)): #  _  _  _  cross product
            x1,y1,z1=tuple(self)       #| i  j  k|           _             _             _
            x2,y2,z2=tuple(other)      #|x1 y1 z1|=|y1 z1| * i + |z1 x1| * j + |x1 y1| * k
            x=y1*z2-z1*y2              #|x2 y2 z2| |y2 z2|       |z2 x2|       |x2 y2|
            y=z1*x2-x1*z2
            z=x1*y2-y1*x2
            return point3d(x,y,z)
        else:
            return NotImplemented
    def __str__(self):
        _=["%.2f"%i for i in self]
        return 'point(%s)'%(', '.join(_))
    def __equal__(self,other):
        if(isinstance(other,point3d)):
            x1,y1,z1=tuple(self)
            x2,y2,z2=tuple(other)
            return aequal(x1,x2) and aequal(y1,y2) and aequal(z1,z2)
        else:
            return NotImplemented
    def __abs__(self):
        x,y,z=self.x,self.y,self.z
        ret=x*x+y*y+z*z
        return sqrt(ret)
    def __neg__(self):
        return point3d(-self.x,-self.y,-self.z)
    def __radd__(self,other):
        if(other==0):       #for sum(list<points>)
            return point3d(*tuple(self))    #copy
        else:
            return NotImplemented
    def __add__(self,other):
        if(isinstance(other,point3d)):
            x1,y1,z1=tuple(self)
            x2,y2,z2=tuple(other)
            return point3d(x1+x2,y1+y2,z1+z2)
        else:
            return NotImplemented
    def __sub__(self,other):
        if(isinstance(other,point3d)):
            x1,y1,z1=tuple(self)
            x2,y2,z2=tuple(other)
            return point3d(x1-x2,y1-y2,z1-z2)
        else:
            return NotImplemented
    def __mul__(self,other):
        if(isinstance(other,point3d)):
            x1,y1,z1=tuple(self)
            x2,y2,z2=tuple(other)
            return x1*x2+y1*y2+z1*z2
        elif(isinstance(other,int) or isinstance(other,float)):
            x,y,z=tuple(self)
            return point3d(x*other,y*other,z*other)
        else:
            return NotImplemented
    def __truediv__(self,other):
        if(isinstance(other,int) or isinstance(other,float)):
            x,y,z=tuple(self)
            if(other==0):
                print(self)
                
            return point3d(x/other,y/other,z/other)
        else:
            return NotImplemented
    def project_on(self,other):
        if(isinstance(other,point3d)):
            return self*other/abs(other)
        else:
            return NotImplemented
    def unit(self):
        return self/abs(self)
_i=point3d(1,0,0)
_j=point3d(0,1,0)
_k=point3d(0,0,1)

class coordinate_sys:
    def __init__(self,axisX,axisY,axisZ):
        a=asign(axisX*axisY)
        b=asign(axisY*axisZ)
        c=asign(axisZ*axisX)
        if(a or b or c):
            print("Warning!! the coordinate system's axes isn't perpendicular to each other")
        
        self.axisX=axisX
        self.axisY=axisY
        self.axisZ=axisZ
    def from_approx_xy(axisX,axisY):
        axisZ=axisX**axisY
        axisY=axisZ**axisX
        return coordinate_sys(axisX,axisY,axisZ)
    def calc_rot(self,refX=_i,refY=_j,refZ=_k,in_degree=False):
        # calc rotation around x
        y=self.axisY.project_on(refY)
        z=self.axisY.project_on(refZ)
        rotX=atan2(z,y)
        #calc rotation around y
        z=self.axisZ.project_on(refZ)
        x=self.axisZ.project_on(refX)
        rotY=atan2(x,z)
        #calc rotation around z
        x=self.axisX.project_on(refX)
        y=self.axisX.project_on(refY)
        rotZ=atan2(y,x)
        if(in_degree):
            rotX*=180/math.pi
            rotY*=180/math.pi
            rotZ*=180/math.pi
        return rotX,rotY,rotZ
    def as_quaternion(self):
        x1,y1,z1=self.axisX.unit()
        x2,y2,z2=self.axisY.unit()
        x3,y3,z3=self.axisZ.unit()
        m=[[x1,x2,x3],[y1,y2,y3],[z1,z2,z3]]
        tr = m[0][0] + m[1][1] + m[2][2]
        #print(m[0])
        #print(m[1])
        #print(m[2])
        
        if(tr>0):
            #print('ln135')
            case=0
            s=sqrt(tr+1)*2
            w=s/4
            x=(m[2][1]-m[1][2])/s
            y=(m[0][2]-m[2][0])/s
            z=(m[1][0]-m[0][1])/s
        elif((m[0][0]>m[1][1]) and (m[0][0]>m[2][2])):
            case=1
            s=sqrt(1+m[0][0]-m[1][1]-m[2][2])*2
            w=(m[2][1]-m[1][2])/s
            x=s/4
            y=(m[1][0]+m[0][1])/s
            z=(m[0][2]+m[2][0])/s
        elif(m[1][1]>m[2][2]):
            case=2
            s=sqrt(1+m[1][1]-m[0][0]-m[2][2])*2
            w=(m[0][2]-m[2][0])/s
            x=(m[0][1]+m[1][0])/s
            y=s/4
            z=(m[1][2]+m[2][1])/s
        else:
            case=3
            s=sqrt(1+m[2][2]-m[0][0]-m[1][1])*2
            w=(m[1][0]-m[0][1])/s
            x=(m[0][2]+m[2][0])/s
            y=(m[1][2]+m[2][1])/s
            z=s/4
        az=x*x+y*y+z*z+w*w
        if(not aequal(az,1)):
            print("warning quat isn't unit",az,case,s)
        return x,y,z,w
def quat_to_ypr(quat,in_degree=True):
    x,y,z,w=quat
    yaw,pitch,roll=0,0,0
    try:
        yaw = atan2(2.0*(y*z + w*x), w*w - x*x -y*y + z*z)
        
        pitch = asin(-2.0*(x*z - w*y))
        roll = atan2(2.0*(x*y + w*z), w*w + x*x - y*y - z*z)
    except Exception as e:
        print(e)
        
    if(in_degree):
        yaw*=180/math.pi
        pitch*=180/math.pi
        roll*=180/math.pi
    return yaw,pitch,roll
if(__name__=='__main__'):
    def _(x,y,z):
        print(x,y,x**y,coordinate_sys(x,y,x**y).as_quaternion())
    _(_i,_j,_k)
    _(_i,_k,_j)

    