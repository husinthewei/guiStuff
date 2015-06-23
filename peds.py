
import numpy as np
import myh5, sys


class Ped:
    def __init__(self):
        self.ntrace = 0
        self.psum = np.zeros((8,1024))
        self.npsum = np.zeros(1024)
        self.x = 8*[None]
        for i in range(8):
            self.x[i] = 1024*[None]
            for j in range(1024):
                self.x[i][j] = []
    def addtrace(self, cellid, adc):
        self.ntrace += 1
        l = len(adc[0])
        z = np.zeros(1024-l)
        o = np.ones(l)
        onepad = np.roll(np.hstack((o,z)), cellid)
        self.npsum += onepad
        for chan in range(0,8):  # was (1,8)
            adcpad = np.roll(np.hstack((adc[chan],z)), cellid)
            self.psum[chan] += adcpad
            for cap in range(1024):
                if onepad[cap]: self.x[chan][cap].append(adcpad[cap])
    def calcpeds(self):
        for chan in range(0,8):  # was (1,8)
            print "psum[%d] ="%(chan,), self.psum[chan]
            for cell in range(1024):
                if self.npsum[cell]>0:
                    self.psum[chan][cell] /= self.npsum[cell]
                if len(self.x[chan][cell]):
                    self.psum[chan][cell] = np.median(self.x[chan][cell])
        return self.psum
    def writepeds(self, fnam):
        psum = self.calcpeds()
        fp = open(fnam, "w")
        for cell in range(1024):
            #fp.write(" 0 ")
            for chan in range(0,8):  # was (1,8)
                fp.write(" %.2f"%(psum[chan][cell]))
            fp.write("\n")

def pedcalc():
    print "peds::pedcalc() starting"
    if len(sys.argv)>1:
        fnam = sys.argv[1]
    else:
        fnam = "drsana/rewrite.h5"
    nmax = None
    if len(sys.argv)>2:
        nmax = int(sys.argv[2])
    print "opening %s for R"%(fnam)
    f = myh5.File(fnam)
    ped0 = Ped()
    ped2 = Ped()
    for i in range(f.raw.shape[0]):
        if i%100==0: print i, f.ts[i]
        ped0.addtrace(f.cellid[i,0], f.raw[i,0])
        ped2.addtrace(f.cellid[i,1], f.raw[i,1])
        if nmax and i>=nmax: break
    ped0.writepeds("peds0.txt")
    ped2.writepeds("peds2.txt")
    print "closing %s"%(fnam)
    print "peds::pedcalc() done"

if __name__=="__main__":
    pedcalc()
