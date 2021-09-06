from myGeometry import point as gPoint
import random
import numpy as np
class point:
	def __init__(self,arr):
		self.arr=arr
		self.hash=None
		self.id=None
	def dist(self,other):
		ret=0
		
		for idx,i in enumerate(self.arr):
			ret+=(i-other.arr[idx])**2
		return ret
	
	def __str__(self):
		return str(self.arr)
	def __repr__(self):
		return self.arr.__repr__()
	def __eq__(self,other):
		return hash(self)==hash(other)
	def __hash__(self):
		if(self.hash is not None):
			return self.hash
		if(isinstance(self.arr,gPoint)):
			return hash(self.arr)
		elif(isinstance(self.arr,np.ndarray)):
			
			enmiao=1e2
			h=hash(tuple([int(i*enmiao) for i in self.arr]))
			self.hash=h
			return h
		else:
			return hash(self.arr)
	def aspoint(self):
		return gPoint(self.arr[0],self.arr[1])
	def __mul__(self,other):
		ret=0
		for idx,i in enumerate(self.arr):
			ret+=i*other.arr[idx]
		return ret
	def __sub__(self,other):
		arr=[i-other.arr[idx] for idx,i in enumerate(self.arr)]
		return point(arr)
	def distO(self):
		return sum([i*i for i in self.arr])**0.5
	def dist_line(self,A,B):
		AB=B-A
		AP=self-A
		dot=AB*AP
		dAP=AP.distO()
		tmp=dot/AB.distO()
		if(dAP*dAP<tmp*tmp-(1e-4)):
			print(dAP,tmp)
			print('cosine=',tmp/AB.distO())
			print(AB.arr,AP.arr,dot)
			exit()
		
		return abs((dAP*dAP-tmp*tmp)**0.5)
class kdt:
	def __init__(self):
		self.node_points=[]
		self.left_child=[]
		self.right_child=[]
		self.left_point=[]
		self.right_point=[]
		self.root=None
		self.size=0
	def _new_index(self):
		self.node_points.append(None)
		self.left_child.append(None)
		self.right_child.append(None)
		self.left_point.append(None)
		self.right_point.append(None)
		if(self.root is None):
			self.root=len(self.node_points)-1
		self.size=len(self.node_points)
		return self.size-1
	def build(self,points,stop_num=3,select_point='random',depth=0,stop_depth=20,set_id=True):
		if(set_id):
			for id,i in enumerate(points):
				i.id=id
		
		u=self._new_index()
		if(len(points)<=stop_num or depth>stop_depth):
			self.node_points[u]=points
			return u
		if(select_point=='random'):
			lpoint,rpoint=random.sample(points,2)
		lpoints=[]
		rpoints=[]
		for p in points:
			if(p.dist(lpoint)<p.dist(rpoint)):
				lpoints.append(p)
			else:
				rpoints.append(p)
		self.left_point[u]=lpoint
		self.right_point[u]=rpoint
		self.left_child[u]=self.build(lpoints,select_point=select_point,stop_num=stop_num,depth=depth+1,set_id=False)
		self.right_child[u]=self.build(rpoints,select_point=select_point,stop_num=stop_num,depth=depth+1,set_id=False)
		return u
	def ann1(self,p,u=None):
		if(u is None):
			return self.ann1(p,u=self.root)
		if(self.left_point[u] is None):
			ret=None
			for i in self.node_points[u]:
				if((ret is None) or(p.dist(ret)<p.dist(i))):
					return i
			return ret
		if(p.dist(self.left_point[u])<p.dist(self.right_point[u])):
			ret=self.ann1(p,self.left_child[u])
			return ret
			if(ret.dist(p)>p.dist_line(self.left_point[u],self.right_point[u])):
				ret1=self.ann1(p,self.right_child[u])
				if(ret1.dist(p)<ret.dist(p)):
					return ret1
				else:
					return ret
			else:
				return ret
		else:
			ret=self.ann1(p,self.right_child[u])
			return ret
			if(ret.dist(p)>p.dist_line(self.left_point[u],self.right_point[u])):
				ret1=self.ann1(p,self.left_child[u])
				if(ret1.dist(p)<ret.dist(p)):
					return ret1
				else:
					return ret
			else:
				return ret