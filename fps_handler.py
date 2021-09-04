import time
class fps_handler:
    def __init__(self):
        self.t=time.time()
    def frame(self):
        t=time.time()
        if(not(t-self.t)):
            return 1
        ret=1/(t-self.t)
        self.t=t
        return ret
    def limit_fps(self,fps):
        t=time.time()
        wt=self.t+1/fps-t
        if(wt>0):
            time.sleep(wt)
        