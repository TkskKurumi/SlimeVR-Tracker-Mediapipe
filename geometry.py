from math import sqrt,atan2
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
        tup=tuple(self)
        return 'point(%s)'%(tup,)
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
    def __div__(self,other):
        if(isinstance(other,int) or isinstance(other,float)):
            x,y,z=tuple(self)
            return point3d(x/other,y/other,z/other)
        else:
            return NotImplemented
    def project_on(self,other):
        if(isinstance(other,point3d)):
            return self*other/abs(other)
        else:
            return NotImplemented
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
if(__name__=='__main__'):
    axisX=point3d(1,1,0)
    axisY=_j
    coor=coordinate_sys.from_approx_xy(axisX,axisY)
    print(coor.calc_rot(in_degree=True))