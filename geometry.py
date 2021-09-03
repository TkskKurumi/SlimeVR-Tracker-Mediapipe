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
    def __neg__(self):
        return point3d(-self.x,-self.y,-self.z)
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
if(__name__=='__main__'):
    pos_x=point3d(1,0,0)
    pos_y=point3d(0,1,0)
    print(pos_x**pos_y)
