import time

class UpTime:
    """Program uptime"""

    def __init__(self):
        self._starttime = time.time()
    def GetRunTimeF(self):
        "return program run time as a float"
        dt = time.time()-self._starttime
        return dt
    def GetRunTimeS(self):
        "return program run time as a string"
        dt = self.GetRunTimeF()
        #hh = int(dt/3600)
        #mm = int((dt-3600*hh)/60)
        #ss = int(dt)%60
        return self.TimeFmt(dt)
    def TimeFmt(self, s, divideBy=1.0):
        if s==0xffff:
            return "??:??:??"
        s = int(s/divideBy)
        return "%02d:%02d:%02d"%(s/3600, (s%3600)/60, s%60)
        
class classname:
    def  createname(self, name):
        self.name = name
    def displayname(self):
        return self.name
    def saying(self):
        print("Hello %s" % self.name)

if __name__ == "__main__":
    first=classname()
    first.createname('hu')
    f=first.displayname
    print(first.displayname())
    print(f())

