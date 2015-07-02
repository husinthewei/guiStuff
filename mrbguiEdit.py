import os
import random
import socket
import sys
import time
import numpy as np
import wx
import wx.py.crust

from wxPlotPanel import PlotPanel
import busio

sys.path.insert(0, "../misc")
from peds import Ped

class UpTime:
    """Program uptime --RWH"""

    def __init__(self):
        self._starttime = time.time()
    def GetRunTimeF(self):
        "return program run time as a float"
        dt = time.time()-self._starttime
        return dt
    def GetRunTimeS(self):
        "return program run time as a string"
        dt = self.GetRunTimeF()
        return self.TimeFmt(dt)
    def TimeFmt(self, s, divideBy=1.0):
        if s==0xffff:
            return "??:??:??"
        s = int(s/divideBy)
        return "%02d:%02d:%02d"%(s/3600, (s%3600)/60, s%60)

class Model:
    def __init__(self):
        self._runtime=UpTime()    #rwh
        self.GetRunTimeF=self._runtime.GetRunTimeF    #rwh
        self.GetRunTimeS=self._runtime.GetRunTimeS    #rwh
        self.TimeFmt=self._runtime.TimeFmt    #rwh
        self.mcu = busio.ProtoMcu('192.168.1.10')
        self.mrb2 = busio.Mrb(boardid=5+2, imrb=2)
        self.mrb3 = busio.Mrb(boardid=5+3, imrb=3)
        self.mrb = [None, None, self.mrb2, self.mrb3]
        self._drspedestals = {}  # use [(2,0)] for MRB2 DRS0
        self._drspedestals[(2,0)] = np.zeros((8,1024),dtype=np.int32)
        self._trigspy = [[] for i in range(24)]
    #
    # I think there must be a way to wrap the program uptime, the 'nfail'
    # counters, and maybe other program variables so that they have an
    # 'rfmt' method the GUI can use, and perhaps resemble registers in
    # other useful ways.  But for now I'll leave this mess here.
    #

    def ClearNFail(self):
        self.mcu.b.nfail = 0
        self.mrb2.b.nfail = 0
        self.mrb3.b.nfail = 0
    def GetNFail1(self):
        return self.mcu.b.nfail
    def GetNFail2(self):
        return self.mrb2.b.nfail
    def GetNFail3(self):
        return self.mrb3.b.nfail
    def ReadTrigSpy(self, which, mrb):
        #  0 <= which < 24
        m = mrb
        msg = []
        nmsg = 0
        nw = 64  # each spy buffer is 64 words deep
        dlist = []
        baseaddr = 0x4000 + 0x0100*which
        for iword in range(nw):
            addr = baseaddr + iword
            d = m.v5rd(addr)
            dlist.append(d)
        d = np.array(dlist)
        self._trigspy[which] = d
    def ResetWfAvg(self):
        self.ped = Ped()
    def AddToWfAvg(self):
        self.ped.addtrace(self._cellid, self._adcdata)
    def FinishWfAvg(self, fnam):
        self.ped.writepeds(fnam)
        print "wrote pedestal data to %s"%(fnam,)
    def LoadPedFile(self):
        for imrb in [2,3]:
            for idrs in range(10):
                fnam = "peds_mrb%d_drs%d.txt"%(imrb,idrs)
                try:
                    pdat = np.loadtxt(fnam).transpose()
                    pdat[1:8,:] -= 500
                    pdat[0] -= np.mean(pdat[0])
                except IOError:
                    pdat = np.zeros((8,1024))
                self._drspedestals[(imrb,idrs)] = pdat
    def SubtractPeds(self):
        whichmrb = self._whichmrb
        whichdrs = self._whichdrs
        cellid = self._cellid
        pdat = self._drspedestals[(whichmrb,whichdrs)]
        adcdat = self._adcdata
        psdat = adcdat-np.roll(pdat,-cellid,1)[:,:adcdat.shape[-1]]
        self._adcdata_pedsub = psdat
        print "shapes:", adcdat.shape, psdat.shape
    def ParseRoFifoData(self, imrb):
        d = self._rofifodata
        ok = False
        AND = lambda x,y: x and y
        rc = 0
        while True:
            if len(d)<4: 
                # fewer than 4 words makes no sense
                rc = 1
                break
            if not reduce(AND, [(x&7)==0 for x in d]):
                # low 3 bits of each word should be 0 padding
                rc = 2
                break
            if not reduce(AND, [((x>>54)&3)==2 for x in d]):
                # top 2 bits of each word should be 1,0 respectively
                rc = 3
                break
            d = [(x>>3 & 0x7ffffffffffff) for x in d]
            typecode = [(x>>48 & 7) for x in d]
            d = [(x & 0xffffffffffff) for x in d]
            if typecode[0]!=1:
                # header word should be (0, timestamp_go)
                rc = 4
                break
            timestamp_go = d[0]
            if typecode[-1]!=7:
                # trailer word should be (7, whichdrs, cellid)
                rc = 5
                break
            cellid = int(d[-1] & 0x3ff)
            whichdrs = int(d[-1]>>16 & 0xf)
            # strip off header and trailer words
            d = d[1:-1]
            typecode = typecode[1:-1]
            if len(d)%2!=0:
                # number of ADC words should be even
                rc = 6
                break
            if not reduce(AND, [x==2 for x in typecode[0::2]]):
                # ADC words 0, 2, 4, ... should have typecode 2
                rc = 7
                break
            if not reduce(AND, [x==5 for x in typecode[1::2]]):
                # ADC words 1, 3, 5, ... should have typecode 5
                rc = 8
                break
            adc0 = map(int, [x>> 0 & 0xfff for x in d[1::2]])
            adc1 = map(int, [x>>12 & 0xfff for x in d[1::2]])
            adc2 = map(int, [x>>24 & 0xfff for x in d[1::2]])
            adc3 = map(int, [x>>36 & 0xfff for x in d[1::2]])
            adc4 = map(int, [x>> 0 & 0xfff for x in d[0::2]])
            adc5 = map(int, [x>>12 & 0xfff for x in d[0::2]])
            adc6 = map(int, [x>>24 & 0xfff for x in d[0::2]])
            adc7 = map(int, [x>>36 & 0xfff for x in d[0::2]])
            break
        print "ParseRoFifoData: rc=%d"%(rc,)
        if rc>0: return rc
        print "timestamp_go=%d whichdrs=%d cellid=%d"%( \
            timestamp_go, whichdrs, cellid)
        if 0:
            print "\nadc0 =", adc0
            print "\nadc1 =", adc1
            print "\nadc2 =", adc2
            print "\nadc3 =", adc3
            print "\nadc4 =", adc4
            print "\nadc5 =", adc5
            print "\nadc6 =", adc6
            print "\nadc7 =", adc7
        self._adcdata = [adc0,adc1,adc2,adc3,adc4,adc5,adc6,adc7]
        self._adcdata = np.array(self._adcdata).astype(np.int32)
        self._whichmrb = imrb
        self._whichdrs = whichdrs
        self._cellid = cellid
        self._timestamp_go = timestamp_go

class MyPlotPanel(PlotPanel):
    def __init__(self, parent, model, **kwargs):
        self.parent = parent
        self.m = model
        self.tvalues = [np.arange(450)]
        self.adcvalues = [2048+2048*np.sin(self.tvalues[0]*np.pi/100)]
        self.adctracemask = -1
        self.xyminmax = 4*[None]  # xmin xmax ymin ymax
        self.pedsubrequested = False
        self.plotmarkers = False
        PlotPanel.__init__(self, parent, **kwargs)
        self.SetColor((255,255,255))
        self._doRedrawMethod = self.draw
    def drawTrigSpy(self, peds=None):
        if peds is not None:
            self._saveTrigPeds = peds
        elif hasattr(self, "_saveTrigPeds"):
            peds = self._saveTrigPeds
        self._doRedrawMethod = self.drawTrigSpy
        print "invoking MyPlotPanel::drawTrigSpy() method"
        self.figure.clf()
        self.subplot = self.figure.add_subplot(111)
        xyminmax = [0,64,0,256]
        if self.pedsubrequested:
            xyminmax[2] = -32
            xyminmax[3] = 256-32
        for i in range(len(xyminmax)):
            if self.xyminmax[i]!=None:
                xyminmax[i] = self.xyminmax[i]
        self.subplot.axis(xyminmax)
        if hasattr(self.m, "_trigspy"):
            nch8nl = len(self.m._trigspy)
            nsampl = len(self.m._trigspy[0])
            print "found _trigspy member: nchnl=%d nsampl=%d"%(nchnl,nsampl)
            self.tvalues = []
            self.adcvalues = []
            for i in range(nchnl):
                if peds is None or not self.pedsubrequested:
                    ped = 0
                else:
                    ped = peds[i]
                self.tvalues.append(np.arange(nsampl))
                self.adcvalues.append(self.m._trigspy[i]-ped)
            self.tvalues = np.array(self.tvalues)
            self.adcvalues = np.array(self.adcvalues)
        else:
            print "did not find _trigspy member"
        for i in range(len(self.tvalues)):
            x = self.tvalues[i]
            y = self.adcvalues[i]
            if self.plotmarkers:
                lstyl = "-o"
            else:
                lstyl = "-"
            if (self.adctracemask>>i & 1):
                self.subplot.plot(x, y, lstyl)
            else:
                # do a null plot to preserve channel color assignments
                self.subplot.plot(None)
        self.subplot.axis(xyminmax)
    def draw(self):
        self._doRedrawMethod = self.draw
        print "invoking MyPlotPanel::draw() method"
        self.figure.clf()
        self.subplot = self.figure.add_subplot(111)
        xyminmax = [0,450,0,4096]
        for i in range(len(xyminmax)):
            if self.xyminmax[i]!=None:
                xyminmax[i] = self.xyminmax[i]
        self.subplot.axis(xyminmax)
        if hasattr(self.m, "_adcdata"):
            print "found _adcdata member"
            nchnl = len(self.m._adcdata)
            nsampl = len(self.m._adcdata[0])
            self.tvalues = []
            self.adcvalues = []
            if self.pedsubrequested:
                self.m.SubtractPeds()
            for i in range(nchnl):
                self.tvalues.append(np.arange(nsampl))
                if self.pedsubrequested:
                    self.adcvalues.append(self.m._adcdata_pedsub[i])
                else:
                    self.adcvalues.append(self.m._adcdata[i])
            self.tvalues = np.array(self.tvalues)
            self.adcvalues = np.array(self.adcvalues)
        else:
            print "did not find _adcdata member"
        for i in range(len(self.tvalues)):
            x = self.tvalues[i]
            y = self.adcvalues[i]
            if self.plotmarkers:
                lstyl = "-o"
            else:
                lstyl = "-"
            if (self.adctracemask>>i & 1):
                self.subplot.plot(x, y, lstyl)
            else:
                # do a null plot to preserve channel color assignments
                self.subplot.plot(None)
        self.subplot.axis(xyminmax)

class StatsPanel(wx.Panel):
    def __init__(self, parent, model, tabnum):
        self.updatelist = []
	self.updatelistMF = []
        self.parent = parent
        self.m = model
        self.tabnum = tabnum
        wx.Panel.__init__(self, parent=parent)
        self.sizer = None

    def AST(self, label="", func=None, funcList = [], szr=None):
        if func and label:
            label0 = label%("?")
        if func or funcList:
            label0 = "-"
        else:
            label0 = label
        statictext = wx.StaticText(self, label=label0)
        if szr is None: szr = self.sizer
        szr.Add(statictext)
        if func:
            if not label: label = "%s"
            self.updatelist.append((statictext, label, func))
	if funcList:
	    self.updatelistMF.append((statictext,label,funcList))
        return statictext

    def UpdateValues(self):
        for statictext,format,func in self.updatelist:
            try:
                s = func()
                s = format%(s,)
            except socket.timeout:
                s = "?"
            except AssertionError:
                s = "?"
            statictext.SetLabel(s)
        self.Layout()

    def UpdateValuesMF(self):
        for statictext,format,func in self.updatelistMF:
	    s = []
	    for i in range(len(func)):
                try:
                    s.append(func[i]())
                except socket.timeout:
                    s.append("?")
                except AssertionError:
                    s.append("?")
	
	    label = ""
	    for i in range(len(func)):
	        label = label + s[i]
	    statictext.SetLabel(label)
        self.Layout()

    def OnPaint(self,e):
        print "  OnPaint"

    def OnTimer(self,e):
        if self.parent.GetSelection()!=self.tabnum:
            # don't update contents unless I'm the selected tab
            return
        self.UpdateValues()
	self.UpdateValuesMF()
    
class BasicStatsPanel(StatsPanel):
    def __init__(self, parent, model, tabnum):
        StatsPanel.__init__(self, parent=parent, model=model, tabnum=tabnum)
        self.sizer = wx.FlexGridSizer(0, 5, 8, 8)
        ast = self.AST
        m = self.m
        ast("runtime %s", m.GetRunTimeS)
        ast("MCU"); ast("MRB2"); ast("MRB3"); ast("")
        ast("uptime")
        ast(func=m.mcu.s3uptime.rfmt)
        ast(func=m.mrb2.s3uptime.rfmt)
        ast(func=m.mrb3.s3uptime.rfmt)
        ast("")
        ast("nfail")
        ast(func=m.GetNFail1)
        ast(func=m.GetNFail2)
        ast(func=m.GetNFail3)
        btn = wx.Button(self, label="clear")
        self.sizer.Add(btn)
        btn.Bind(wx.EVT_BUTTON, self.OnBtnClear)
        ast("temp"); ast("-")
        ast(func=m.mrb2.v5temp.rfmt); ast(func=m.mrb3.v5temp.rfmt); ast("")
        ast("vccint"); ast("-"); 
        ast(func=m.mrb2.v5vccint.rfmt); ast(func=m.mrb3.v5vccint.rfmt); ast("")
        ast("ntrig"); 
        ast(func=m.mcu.ntrig.rfmt)
        ast(func=m.mrb2.ntrig.rfmt)
        ast(func=m.mrb3.ntrig.rfmt); ast("")
        ast("ncoinc");
        ast(func=m.mcu.ncoinc.rfmt)
        ast(func=m.mrb2.ncoinc.rfmt)
        ast(func=m.mrb3.ncoinc.rfmt); ast("");

        self.SetSizer(self.sizer)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(1000)

    def OnBtnClear(self,e):
	print("inClear")
        self.m.ClearNFail()

#tabRWH
#Stats Panel for MCU
#I attempted to recreate the stat panels for the MRB, but I don't know what some of the
#labels/functions do. I'm thinking that some are only for the MRB's, so I'll ignore them for now.

#!According to the verilog, registers 4,5,6, and 7 control which LED's are always on
#ngood, nbad

class McuStatsPanel(StatsPanel):
    def __init__(self, parent, model, tabnum, whichmcu):
        StatsPanel.__init__(self, parent=parent, model=model, tabnum=tabnum)
        self.sizer = wx.FlexGridSizer(16, 2, 7, 10)
	self.mcu = whichmcu
	m = self.m	
	mcu = self.mcu

	self.AST("runtime");		self.AST(func = m.GetRunTimeS);
	self.AST("nfail");		self.AST(func = m.GetNFail1);
	self.AST("0000");       	self.AST(func = mcu.r0000.rfmt);
	self.AST("beef");		self.AST(func = mcu.rbeef.rfmt);
	self.AST("dead");		self.AST(func = mcu.rdead.rfmt);
	self.AST("uptime");		self.AST(func = mcu.s3uptime.rfmt);
	self.AST("q0003");		self.AST(func = mcu.q0003.rfmt);
	
	#self.AST("LED On"); 		self.AST(mcu.ledon_1.rfmt);
	funcs = [mcu.ledon_1.rfmt, mcu.ledon_2.rfmt, mcu.ledon_3.rfmt, mcu.ledon_4.rfmt]
	self.AST("LED On"); 		self.AST(funcList = funcs);
	funcs1 = [mcu.ngood1.rfmt, mcu.ngood2.rfmt, mcu.ngood3.rfmt]
	self.AST("ngood");		self.AST(funcList = funcs1);
	funcs2 = [mcu.nbad1.rfmt, mcu.nbad2.rfmt, mcu.nbad3.rfmt]
	self.AST("nbad");		self.AST(funcList = funcs2);

	self.AST("bitslip");		self.AST(func = mcu.btslp.rfmt);
	self.AST("loopback");		self.AST(func = mcu.lpbck.rfmt);	
	self.AST("ncoinc");		self.AST(func = mcu.ncoinc.rfmt);
	self.AST("ntrig");		self.AST(func = mcu.ntrig.rfmt);	

	self.SetSizer(self.sizer)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(1000)

class MrbStatsPanel(StatsPanel):
    def __init__(self, parent, model, tabnum, whichmrb):
        StatsPanel.__init__(self, parent=parent, model=model, tabnum=tabnum)
        self.sizer = wx.FlexGridSizer(16, 2, 7, 10)
        self.mrb = whichmrb
        m = self.m
        mrb = self.mrb

	#rwh2 10 lines dropped
	labels = ["runtime", "nfail", "0000", "beef", "uptime", "q0003", "LED pattern", 
		  "q0005", "DIP sw", "AD9222 up", "AD9287 up", "DRS4 PLL Lck", "DRS4 DTAP", 
		  "Ro Fifo Flgs", "Ro Frame Cnt", "temp", "vccint", "srclkflip"]
	functions = [m.GetRunTimeS, m.GetNFail2, mrb.r0000.rfmt, mrb.rbeef.rfmt, 
		     mrb.s3uptime.rfmt, mrb.q0003.rfmt, mrb.ledpatt.rfmt, 
	             mrb.q0005.rfmt, mrb.dipsw.rfmt, mrb.ad9222up.rfmt, mrb.ad9287up.rfmt,
		     mrb.drs4plllck.rfmt, mrb.drs4dtap.rfmt, mrb.rofifoflags.rfmt, 
		     mrb.roframecount.rfmt, mrb.v5temp.rfmt, mrb.v5vccint.rfmt, 		     mrb.srclkflip.rfmt]

	for i in range(len(labels)):
	    self.AST(labels[i]);	self.AST(func = functions[i]);		
        self.AST("misaligncnt 0..9"); szr = wx.BoxSizer()
	
	#rwh3 4 lines dropped
	functions =		      [self.mrb.misaligncnt0.rfmt,self.mrb.misaligncnt1.rfmt,self.mrb.misaligncnt2.rfmt,		 	        		    self.mrb.misaligncnt3.rfmt,self.mrb.misaligncnt4.rfmt,self.mrb.misaligncnt5.rfmt,
		    self.mrb.misaligncnt6.rfmt,self.mrb.misaligncnt7.rfmt,self.mrb.misaligncnt8.rfmt,
		    self.mrb.misaligncnt9.rfmt] 

	for i in range(len(functions)):
	    self.AST(szr=szr, func= functions[i]); szr.Add((10,1))

        self.AST(szr=szr, func=self.mrb.misaligncnt9.rfmt)
        self.sizer.Add(szr)
        
        #
        self.SetSizer(self.sizer)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(1000)

class DrsStatsPanel(StatsPanel):
    def __init__(self, parent, model, tabnum, whichmrb):
        StatsPanel.__init__(self, parent=parent, model=model, tabnum=tabnum)
        self.sizer = wx.FlexGridSizer(16, 2, 7, 10)
        self.mrb = whichmrb
        m = self.m
        mrb = self.mrb
        self.AST("runtime");      self.AST(func=m.GetRunTimeS)
        self.AST("uptime");       self.AST(func=mrb.s3uptime.rfmt)
        self.AST("Ro Fifo Flgs"); self.AST(func=mrb.rofifoflags.rfmt)
        self.AST("Ro Frame Cnt"); self.AST(func=mrb.roframecount.rfmt)
        self.AST("TStamp");       self.AST(func=mrb.tstamp.rfmt)
        self.AST("MFifoFlags");   self.AST(func=mrb.mfifoflags.rfmt)
        self.AST("MFsmDoneCnt");  self.AST(func=mrb.mfsmdonecnt.rfmt)
        self.AST("MFsmReadCnt");  self.AST(func=mrb.mfsmreadcnt.rfmt)
        self.AST("FifoNempty");   self.AST(func=mrb.fifone.rfmt)
        self.AST("FifoFull");     self.AST(func=mrb.fifofull.rfmt)

        #
        self.AST("DRS0..9 GoCnt"); szr = wx.BoxSizer()
        self.AST(szr=szr, func=self.mrb.drs0gocnt.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs1gocnt.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs2gocnt.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs3gocnt.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs4gocnt.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs5gocnt.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs6gocnt.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs7gocnt.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs8gocnt.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs9gocnt.rfmt); szr.Add((10,1))
        self.sizer.Add(szr)
        #
        self.AST("DRS0..9 TsLast"); szr = wx.BoxSizer()
        self.AST(szr=szr, func=self.mrb.drs0tslast.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs1tslast.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs2tslast.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs3tslast.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs4tslast.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs5tslast.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs6tslast.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs7tslast.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs8tslast.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs9tslast.rfmt); szr.Add((10,1))
        self.sizer.Add(szr)
        #
        self.AST("DRS0..9 CellID"); szr = wx.BoxSizer()
        self.AST(szr=szr, func=self.mrb.drs0cidlast.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs1cidlast.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs2cidlast.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs3cidlast.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs4cidlast.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs5cidlast.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs6cidlast.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs7cidlast.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs8cidlast.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=self.mrb.drs9cidlast.rfmt); szr.Add((10,1))
        self.sizer.Add(szr)

	labels = ["DRS0 GO", "DRS0 Merge", "DRS1 GO", "DRS1 Merge", "DRS2 GO",
		  "DRS2 Merge", "DRS3 GO", "DRS3 Merge", "DRS4 Go", "DRS4 Merge", 
	          "DRS5 GO", "DRS5 Merge", "DRS6 GO", "DRS6 Merge", "DRS7 GO", 	
		  "DRS7 Merge", "DRS8 GO", "DRS8 Merge", "DRS9 GO", "DRS9 Merge", 
		  "MrbFifoReset", "DrainFifo", "Draw"]
	
	OnBtn = [self.OnBtnGo0, self.OnBtnMerge0, self.OnBtnGo1, self.OnBtnMerge1, 
		 self.OnBtnGo2, self.OnBtnMerge2, self.OnBtnGo3, self.OnBtnMerge3,
		 self.OnBtnGo4, self.OnBtnMerge4, self.OnBtnGo5, self.OnBtnMerge5, 
		 self.OnBtnGo6, self.OnBtnMerge6, self.OnBtnGo7, self.OnBtnMerge7, 
		 self.OnBtnGo8, self.OnBtnMerge8, self.OnBtnGo9, self.OnBtnMerge9,
		 self.OnBtnMrbFifoReset, self.OnBtnDrainFifo, self.OnBtnDraw]

	for i in range(len(labels)):
	    btn = wx.Button(self, label=labels[i]) #rwh1 74 lines dropped
	    self.sizer.Add(btn)
	    btn.Bind(wx.EVT_BUTTON, OnBtn[i])

        self.SetSizer(self.sizer)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(1000)
    def OnBtnGo0(self,e):
        self.mrb.fakego.wr(1<<0)
    def OnBtnMerge0(self,e):
        self.mrb.mfifobusw.wr(0)
    def OnBtnGo1(self,e):
        self.mrb.fakego.wr(1<<1)
    def OnBtnMerge1(self,e):
        self.mrb.mfifobusw.wr(1)
    def OnBtnGo2(self,e):
        self.mrb.fakego.wr(1<<2)
    def OnBtnMerge2(self,e):
        self.mrb.mfifobusw.wr(2)
    def OnBtnGo3(self,e):
        self.mrb.fakego.wr(1<<3)
    def OnBtnMerge3(self,e):
        self.mrb.mfifobusw.wr(3)
    def OnBtnGo4(self,e):
        self.mrb.fakego.wr(1<<4)
    def OnBtnMerge4(self,e):
        self.mrb.mfifobusw.wr(4)
    def OnBtnGo5(self,e):
        self.mrb.fakego.wr(1<<5)
    def OnBtnMerge5(self,e):
        self.mrb.mfifobusw.wr(5)
    def OnBtnGo6(self,e):
        self.mrb.fakego.wr(1<<6)
    def OnBtnMerge6(self,e):
        self.mrb.mfifobusw.wr(6)
    def OnBtnGo7(self,e):
        self.mrb.fakego.wr(1<<7)
    def OnBtnMerge7(self,e):
        self.mrb.mfifobusw.wr(7)
    def OnBtnGo8(self,e):
        self.mrb.fakego.wr(1<<8)
    def OnBtnMerge8(self,e):
        self.mrb.mfifobusw.wr(8)
    def OnBtnGo9(self,e):
        self.mrb.fakego.wr(1<<9)
    def OnBtnMerge9(self,e):
        self.mrb.mfifobusw.wr(9)
    def OnBtnMrbFifoReset(self,e):
        self.mrb.mrbfiforeset.wr(0)
    def OnBtnDrainFifo(self,e):
        fifodata = self.mrb.drainrofifo()
        self.m._rofifodata = fifodata
        print len(fifodata), "fifodata =", \
            ["%014x"%(x) for x in fifodata]
        self.m.ParseRoFifoData(self.mrb.imrb)
    def OnBtnDraw(self,e):
        pp = self.parent.mainwin.wavepanel.plt
        pp.draw()

class MrbTrigStatsPanel(StatsPanel):
    def __init__(self, parent, model, tabnum, whichmrb):
        StatsPanel.__init__(self, parent=parent, model=model, tabnum=tabnum)
        self.mrb = whichmrb
        mrb = self.mrb
        self.sizer = wx.FlexGridSizer(0, 2, 7, 10)
        self.AST("uptime");       self.AST(func=mrb.s3uptime.rfmt)
        self.AST("TStamp");       self.AST(func=mrb.tstamp.rfmt)
        self.AST("AD9287 up");    self.AST(func=mrb.ad9287up.rfmt)
        self.AST("FrzReq");       self.AST(func=mrb.frzreq.rfmt)
        self.AST("SpyPtr");       self.AST(func=mrb.spyptr.rfmt)
        self.pedtext = []
        for i in range(3):
            lbl = "adcped %d-%d"%(8*i, 8*i+7)
            self.AST(lbl);
            szr = wx.BoxSizer()
            for j in range(0,8):
                tx = wx.StaticText(self, label="-")
                self.pedtext.append(tx)
                szr.Add(tx)
                szr.Add((10,1))
            self.sizer.Add(szr)
        #
        self.AST("coinc alwys/ena")
        self.AST(func=mrb.coinc_ena.rfmt)
        #
        self.AST("trig qmin/qmax/zoneena/max_n")
        szr = wx.BoxSizer()
        self.AST(szr=szr, func=mrb.qmin_trig.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=mrb.qmax_trig.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=mrb.zone_ena_mask.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=mrb.max_ntrig.rfmt); szr.Add((10,1))
        self.sizer.Add(szr)
        #
        self.AST("count_ok/ok0-3")
        szr = wx.BoxSizer()
        self.AST(szr=szr, func=mrb.count_ok.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=mrb.count_ok0.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=mrb.count_ok1.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=mrb.count_ok2.rfmt); szr.Add((10,1))
        self.AST(szr=szr, func=mrb.count_ok3.rfmt); szr.Add((10,1))
        self.sizer.Add(szr)
	
	#rwh4 40 lines
	labels = ["Freeze", "UnFreeze", "FreezeOnTrigger", None , "ReadPeds",
		  "CalcPeds", "ZeroPeds", "WritePeds", "SingleAcq", "SingleTrig",
		  "Draw", "Dump", "TrigAdcTestOn", "TrigAdcTestOff"]
	OnBtn = [self.OnBtnFreeze, self.OnBtnUnFreeze, self.OnBtnFreezeOnTrigger, 
		 None, self.OnBtnReadPeds, self.OnBtnCalcPeds, self.OnBtnZeroPeds,
	         self.OnBtnWritePeds, self.OnBtnSingleAcq, self.OnBtnSingleTrig,
		 self.OnBtnDraw, self.OnBtnDump, self.OnBtnTrigAdcTestOn, self.OnBtnTrigAdcTestOff]

	for i in range(len(labels)):
	    if(labels[i] == None):
		self.sizer.Add((1,1))
	    else: 
		btn = wx.Button(self, label=labels[i])
        	self.sizer.Add(btn)
        	btn.Bind(wx.EVT_BUTTON, OnBtn[i])

	#
        self.SetSizer(self.sizer)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(1000)
    def OnBtnFreeze(self,e):
        self.mrb.frzreq.wr(1)
    def OnBtnUnFreeze(self,e):
        self.mrb.frzreq.wr(0)
    def OnBtnFreezeOnTrigger(self,e):
        self.mrb.frzreq.wr(2)
    def OnBtnReadPeds(self,e):
        for i in range(24):
            x = self.mrb.v5rd(0x0340+i) & 0xff
            if (x>127): x -= 256
            self.mrb.trigpeds[i] = x
            self.pedtext[i].SetLabel("%d"%(x,))
    def OnBtnWritePeds(self,e):
        for i in range(24):
            ped = int(self.mrb.trigpeds[i])
            self.mrb.v5wr(0x0340+i, ped)
    def OnBtnZeroPeds(self,e):
        for i in range(24):
            self.mrb.trigpeds[i] = 0
            self.mrb.v5wr(0x0340+i, 0)
    def OnBtnCalcPeds(self,e):
        # this sort of intelligence should move to Model or to Mrb
        ts = self.m._trigspy
        ntrigadc = self.mrb.NTRIGADC
        ped = ntrigadc*[0]
        assert(len(ts)==ntrigadc)
        for i in range(len(ts)):
            x = np.array(ts[i])
            xmean = np.mean(x)
            xrms = np.sqrt(np.mean((x-xmean)**2))
            if xrms>3.0 or xmean<10 or xmean>70:
                print "OnBtnCalcPeds: warning i=%d xmean=%.1f xrms=%.2f"% (
                    i, xmean, xrms)
            ped[i] = int(round(xmean))
            self.mrb.trigpeds[i] = ped[i]-32
            print "calcpeds:", i, "%04x"%(0x0340+i,), self.mrb.trigpeds[i]
            self.mrb.v5wr(0x0340+i, self.mrb.trigpeds[i])
        print "peds(adcmean): ", ped
    def OnBtnSingleAcq(self,e):
        t0 = time.time()
        print "SingleAcq (imrb=%d)"%(self.mrb.imrb,)
        save_frzreq = self.mrb.frzreq.read()
        self.mrb.frzreq.wr(1)
        spyptr = self.mrb.spyptr.read() & 0x3f
        for i in range(24):
            self.m.ReadTrigSpy(i, self.mrb)
            self.m._trigspy[i] = np.roll(self.m._trigspy[i], -spyptr)
        # return 'freeze' register to previous state
        self.mrb.frzreq.wr(save_frzreq)
        print "SingleAcq done: dt=%.1f ms"%(1000*(time.time()-t0),)
    def OnBtnSingleTrig(self,e):
        print "SingleTrig"
    def OnBtnDraw(self,e):
        pp = self.parent.mainwin.wavepanel.plt
        pp.drawTrigSpy(peds=self.mrb.trigpeds)
    def OnBtnDump(self,e):
        ts = self.m._trigspy
        print "== trigspy dump (%s) =="
        for i in range(len(ts)):
            x = np.array(ts[i])
            xmean = np.mean(x)
            xrms = np.sqrt(np.mean((x-xmean)**2))
            print "trigspy[%d] (mean=%.1f rms=%.2f) ="%(i, xmean, xrms), \
                " ".join(["%02x"%(x) for x in ts[i]])
    def OnBtnTrigAdcTestOn(self,e):
        self.mrb.trigadcteston()
    def OnBtnTrigAdcTestOff(self,e):
        self.mrb.trigadctestoff()

class WavePanel(StatsPanel):
    def __init__(self, parent, model, tabnum):
        StatsPanel.__init__(self, parent=parent, model=model, tabnum=tabnum)
        self._needRedraw = False
        self.sizer = wx.FlexGridSizer(0, 1)
        self.m = model
        #
        self.adcCheckBoxes = []
        for j in range(3):
            chkboxsizer = wx.BoxSizer()
            for i in range(8):
                ckbox = wx.CheckBox(self, label="adc%d"%(8*j + i,))
                ckbox.SetValue(True)
                ckbox.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)
                chkboxsizer.Add(ckbox)
                self.adcCheckBoxes.append(ckbox)
            self.sizer.Add(chkboxsizer)
        #
        chkboxsizer = wx.BoxSizer()
        ckbox = wx.CheckBox(self, label="subtract pedestals")
        ckbox.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)
        self.pedSubCheckBox = ckbox
        chkboxsizer.Add(ckbox)
        ckbox = wx.CheckBox(self, label="rapidfire readout")
        ckbox.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)
        self.rapidFireCheckBox = ckbox
        chkboxsizer.Add(ckbox)
        ckbox = wx.CheckBox(self, label="plot markers")
        ckbox.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)
        self.plotMarkersCheckBox = ckbox
        chkboxsizer.Add(ckbox)
        self.sizer.Add(chkboxsizer)
        #
        tcsizer = wx.BoxSizer()
        labels = "xmin xmax ymin ymax".split()
        self.tc_xyminmax = []
        for l in labels:
            tx = wx.StaticText(self, label=l)
            tcsizer.Add(tx)
            tc = wx.TextCtrl(self, size=(50,20))
            tc.Bind(wx.EVT_TEXT, self.OnText)
            tcsizer.Add(tc)
            self.tc_xyminmax.append(tc)
            tcsizer.Add((20,0))
        self.sizer.Add(tcsizer)
        #
        btn = wx.Button(self, label="Mrb2Drs0SoftTrigReadDraw")
        self.sizer.Add(btn)
        btn.Bind(wx.EVT_BUTTON, self.OnBtnMrb2Drs0SoftTrigReadDraw)
        #
        pnl = wx.Panel(self)
        self.plt = MyPlotPanel(pnl, self.m)
        self.sizer.Add(pnl, 1, wx.ALL|wx.EXPAND)
        #
        self.sizer.AddGrowableCol(0, 1)
        nchildren = len(self.sizer.GetChildren())
        self.sizer.AddGrowableRow(nchildren-1, 1)
        #
        self.SetSizer(self.sizer)
        if 1:
            self.timer = wx.Timer(self)
            self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
            self.timer.Start(1000)
    def OnText(self,e):
        for i,tc in enumerate(self.tc_xyminmax):
            v = tc.GetValue()
            try:
                iv = int(v)
                v = "%d"%(iv)
            except ValueError:
                iv = None
                v = ""
            self.plt.xyminmax[i] = iv
        print "xyminmax -> ", self.plt.xyminmax
        self._needRedraw = True
    def OnCheckBox(self,e):
        mask = 0
        for i,ckbox in enumerate(self.adcCheckBoxes):
            if ckbox.IsChecked():
                mask |= (1<<i)
        self.plt.pedsubrequested = self.pedSubCheckBox.IsChecked()
        self.plt.adctracemask = mask
        self.plt.plotmarkers = self.plotMarkersCheckBox.IsChecked()
        self._needRedraw = True
    def OnTimer(self,e):
        if self._needRedraw:
            self._needRedraw = False
            self.plt._doRedrawMethod()
    def OnBtnMrb2Drs0SoftTrigReadDraw(self,e):
        print "OnBtnMrb2Drs0SoftTrigReadDraw"
        nloop = 1
        if self.rapidFireCheckBox.IsChecked():
            nloop = 10
        for i in range(nloop):
            self.m.mrb2.fakego.wr(1)
            self.m.mrb2.mfifobusw.wr(0)
            self.m.Mrb2DrainRoFifo()
        self.m.ParseRoFifoData(self.m.mrb2.imrb)
        self.plt.draw()

class LogPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        log = wx.TextCtrl(
            self, -1,
            style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        self.log = log
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(log, 1, wx.ALL|wx.EXPAND, 10)
        self.SetSizer(sizer)

class TabPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        colors = ["red", "blue", "gray", "yellow", "green"]
        self.SetBackgroundColour(random.choice(colors))
        btn = wx.Button(self, label="Press Me")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btn, 0, wx.ALL, 10)
        self.SetSizer(sizer)

#tabRwh
#Attemping to add a panel in which you can directly read or write to registers from the gui
class comPanel(StatsPanel):
    def __init__(self, parent, model, tabnum):
	self.m = model
        StatsPanel.__init__(self, parent=parent, model=model, tabnum=tabnum)
        self.sizer = wx.FlexGridSizer(0, 2, 3, 8)
	self.label = wx.StaticText(self, label="Register")
	self.fieldReg = wx.TextCtrl(self, value="", size=(300, 20))
	self.sizer.Add(self.label)
	self.sizer.Add(self.fieldReg)
	self.label = wx.StaticText(self, label="New Value / Read Value")
	self.fieldVal = wx.TextCtrl(self, value="", size=(300, 20))
	self.sizer.Add(self.label)
	self.sizer.Add(self.fieldVal)
	btn = wx.Button(self, label="Read")
        btn.Bind(wx.EVT_BUTTON, self.OnBtnRead)
        self.sizer.Add(btn)
        btn = wx.Button(self, label="Write")
        btn.Bind(wx.EVT_BUTTON, self.OnBtnWrite)
        self.sizer.Add(btn)
	btn2 = wx.Button(self, label="Slow")
        self.sizer.Add(btn2)
        btn2.Bind(wx.EVT_BUTTON, self.OnBtnSlow)
        btn3 = wx.Button(self, label="Fast")
        self.sizer.Add(btn3)
        btn3.Bind(wx.EVT_BUTTON, self.OnBtnFast)
	self.SetSizer(self.sizer)
    def OnBtnRead(self,e):
	reg = self.fieldReg.GetValue()
	print("Reading from: %s"%reg)
	data = self.m.mcu.rd(int(reg,16))
	print("Data Received: %x"%data)
	self.fieldVal.SetValue("%x"%data)
    def OnBtnWrite(self,e):
	reg = self.fieldReg.GetValue()
	data = self.fieldVal.GetValue()
	model.mcu.wr(int(reg,16), int(data,16))
    def OnBtnSlow(self,e):
	addrS = 0x003
	dataS = 0
	model.mcu.wr(addrS, dataS)
    def OnBtnFast(self,e):
	print("in Method Fast")
	addrF = 0x003
	dataF = 1
	model.mcu.wr(addrF, dataF)

class MiscPanel(StatsPanel):
    def __init__(self, parent, model, tabnum):
        StatsPanel.__init__(self, parent=parent, model=model, tabnum=tabnum)
        self.sizer = wx.FlexGridSizer(0, 3, 7, 10)
        ast = self.AST
        m, m2, m3 = self.m, self.m.mrb2, self.m.mrb3
        #
        ast("uptime"); ast(func=m2.s3uptime.rfmt); ast(func=m3.s3uptime.rfmt)
        ast("AD9222 up"); ast(func=m2.ad9222up.rfmt); ast(func=m3.ad9222up.rfmt)
        ast("TStamp"); ast(func=m2.tstamp.rfmt); ast(func=m3.tstamp.rfmt)
        #
        btn = wx.Button(self, label="StartPyCrust")
        btn.Bind(wx.EVT_BUTTON, self.OnPyCrust)
        self.sizer.Add(btn)
        btn = wx.Button(self, label="Mrb2MiscInit")
        btn.Bind(wx.EVT_BUTTON, self.OnBtnMrb2MiscInit)
        self.sizer.Add(btn)
        btn = wx.Button(self, label="Mrb3MiscInit")
        btn.Bind(wx.EVT_BUTTON, self.OnBtnMrb3MiscInit)
        self.sizer.Add(btn)
        #
        btn = wx.Button(self, label="LoadPedestalFile")
        btn.Bind(wx.EVT_BUTTON, self.OnBtnLoadPedestalFile)
        self.sizer.Add(btn)
        btn = wx.Button(self, label="Mrb2CfgVirtex5")
        btn.Bind(wx.EVT_BUTTON, self.OnBtnMrb2CfgVirtex5)
        self.sizer.Add(btn)
        btn = wx.Button(self, label="Mrb3CfgVirtex5")
        btn.Bind(wx.EVT_BUTTON, self.OnBtnMrb3CfgVirtex5)
        self.sizer.Add(btn)
        #
        btn = wx.Button(self, label="CollectMrb2Drs0Peds")
        btn.Bind(wx.EVT_BUTTON, self.OnBtnMrb2Drs0Peds)
        self.sizer.Add(btn)
        btn = wx.Button(self, label="Stop")
        btn.Bind(wx.EVT_BUTTON, self.OnBtnStop)
        self.sizer.Add(btn)
        self.pediter = wx.StaticText(self, label="-")
        self.sizer.Add(self.pediter)
        #
        btn = wx.Button(self, label="CollectMrb2Drs2Peds")
        btn.Bind(wx.EVT_BUTTON, self.OnBtnMrb2Drs2Peds)
        self.sizer.Add(btn)
        btn = wx.Button(self, label="CollectMrb3Drs0Peds")
        btn.Bind(wx.EVT_BUTTON, self.OnBtnMrb3Drs0Peds)
        self.sizer.Add(btn)
        btn = wx.Button(self, label="CollectMrb3Drs1Peds")
        btn.Bind(wx.EVT_BUTTON, self.OnBtnMrb3Drs1Peds)
        self.sizer.Add(btn)
        btn = wx.Button(self, label="CollectMrb3Drs2Peds")
        btn.Bind(wx.EVT_BUTTON, self.OnBtnMrb3Drs2Peds)
        self.sizer.Add(btn)
        btn = wx.Button(self, label="CollectMrb3Drs3Peds")
        btn.Bind(wx.EVT_BUTTON, self.OnBtnMrb3Drs3Peds)
        self.sizer.Add(btn)
        btn = wx.Button(self, label="CollectMrb3Drs4Peds")
        btn.Bind(wx.EVT_BUTTON, self.OnBtnMrb3Drs4Peds)
        self.sizer.Add(btn)
        #
        self.SetSizer(self.sizer)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(1000)
    def OnPyCrust(self,e):
        mw = self.parent.mainwin
        if hasattr(self, "crustFrame"):
            print "OnPyCrust: crustFrame already exists!"
            return
        print "starting up CrustFrame()"
        self.crustFrame = wx.py.crust.CrustFrame(parent=mw)
        self.crustFrame.Show()
    def OnBtnMrb2MiscInit(self,e):
        self.m.mrb2.miscinit()
    def OnBtnMrb3MiscInit(self,e):
        self.m.mrb3.miscinit()
    def OnBtnLoadPedestalFile(self,e):
        print "MiscPanel::OnBtnLoadPedestalFile"
        self.m.LoadPedFile()
    def OnBtnMrb2CfgVirtex5(self,e):
        self.m.mrb2.v5reconfig.wr(0)
    def OnBtnMrb3CfgVirtex5(self,e):
        self.m.mrb3.v5reconfig.wr(0)
    def OnBtnMrb2Drs0Peds(self,e):
        self.DrsPeds(imrb=2, idrs=0)
    def OnBtnMrb2Drs2Peds(self,e):
        self.DrsPeds(imrb=2, idrs=2)
    def OnBtnMrb3Drs0Peds(self,e):
        self.DrsPeds(imrb=3, idrs=0)
    def OnBtnMrb3Drs1Peds(self,e):
        self.DrsPeds(imrb=3, idrs=1)
    def OnBtnMrb3Drs2Peds(self,e):
        self.DrsPeds(imrb=3, idrs=2)
    def OnBtnMrb3Drs3Peds(self,e):
        self.DrsPeds(imrb=3, idrs=3)
    def OnBtnMrb3Drs4Peds(self,e):
        self.DrsPeds(imrb=3, idrs=4)
    def DrsPeds(self, imrb, idrs):
        #tmp_adcdat = []
        #tmp_cellid = []
        self.pediter_stop = False
        self.pediter.SetLabel("-start-")
        self.m.ResetWfAvg()
        mrb = self.m.mrb[imrb]
        for i in range(10000):
            self.pediter.SetLabel("mrb%d/drs%d: iter %d"%(imrb,idrs,i))
            wx.Yield()
            if self.pediter_stop:
                self.pediter.SetLabel(
                    "mrb%d/drs%d: stopped (%d)"%(imrb,idrs,i))
                break
            mrb.fakego.wr(1<<idrs)
            mrb.mfifobusw.wr(idrs)
            fifodata = mrb.drainrofifo()
            self.m._rofifodata = fifodata
            self.m.ParseRoFifoData(imrb)
            self.m.AddToWfAvg()
            #tmp_cellid.append(self.m._cellid)
            #tmp_adcdat.append(self.m._adcdata[0])
        if not self.pediter_stop:
            self.pediter.SetLabel("mrb%d/drs%d: done (%d)"%(imrb,idrs,i+1))
        self.m.FinishWfAvg(fnam="peds_mrb%d_drs%d.txt"%(imrb,idrs))
        #tmp_cellid = np.array(tmp_cellid)
        #tmp_adcdat = np.array(tmp_adcdat)
        #np.savetxt("peddat_cellid_mrb%d_drs%d.txt"%(imrb,idrs), tmp_cellid)
        #np.savetxt("peddat_adcdat_mrb%d_drs%d.txt"%(imrb,idrs), tmp_adcdat)
    def OnBtnStop(self,e):
        self.pediter_stop = True

class RedirectText:
    # recipe for redirecting stderr from
    #   http://bytes.com/topic/python/answers/
    #     665106-wxpython-redirect-stdout-textctrl
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl
        self.t0 = time.time()
    def write(self, string):
        t = time.time()
        if t-self.t0>2.0:
            string = time.ctime()+"\n"+string
            self.t0 = t
        self.out.WriteText(string)


class MainWindow(wx.Frame):
    def __init__(self, model):
        self.m = model
        wx.Frame.__init__(self, None, wx.ID_ANY, "MRB GUI", size=(760,700))
        panel = wx.Panel(self)
        self.CreateStatusBar()
        self.SetStatusText("status: this is the status bar")
        filemenu = wx.Menu()
        menuHelloWorld = filemenu.Append(
            -1, "Hello world", "run the 'hello world' test method")
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", "Quit MRB GUI")
        # menu bar and menus
        helpmenu = wx.Menu()
        menuAbout = helpmenu.Append(
            wx.ID_ABOUT, "&About", "This doesn't do much yet")
        mb = wx.MenuBar()
        mb.Append(filemenu, "&File")
        mb.Append(helpmenu, "&Help")
        self.SetMenuBar(mb)
        self.Bind(wx.EVT_MENU, self.OnHelloWorld, menuHelloWorld)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        # tabbed notebook panels
        notebook = wx.Notebook(panel)
        notebook.mainwin = self
        tabnum = 0
        tab = BasicStatsPanel(notebook, self.m, tabnum)
        notebook.AddPage(tab, "basic")
        tabnum += 1
	tab = McuStatsPanel(notebook, self.m, tabnum, self.m.mcu)
	notebook.AddPage(tab, "mcu")
	tabnum += 1
        tab = MrbStatsPanel(notebook, self.m, tabnum, self.m.mrb2)
        notebook.AddPage(tab, "mrb2")
        tabnum += 1
        tab = MrbStatsPanel(notebook, self.m, tabnum, self.m.mrb3)
        notebook.AddPage(tab, "mrb3")
        tabnum += 1
        tab = DrsStatsPanel(notebook, self.m, tabnum, self.m.mrb2)
        notebook.AddPage(tab, "m2/drs")
        tabnum += 1
        tab = DrsStatsPanel(notebook, self.m, tabnum, self.m.mrb3)
        notebook.AddPage(tab, "m3/drs")
        tabnum += 1
        tab = WavePanel(notebook, self.m, tabnum)
        self.wavepanel = tab
        notebook.AddPage(tab, "waveforms")
        tabnum += 1
        tab = MrbTrigStatsPanel(notebook, self.m, tabnum, self.m.mrb2)
        notebook.AddPage(tab, "m2/trig")
        tabnum += 1
        tab = MrbTrigStatsPanel(notebook, self.m, tabnum, self.m.mrb3)
        notebook.AddPage(tab, "m3/trig")
        tabnum += 1
        tab = MiscPanel(notebook, self.m, tabnum)
        notebook.AddPage(tab, "misc")
        tabnum += 1
        tab = LogPanel(notebook)
        notebook.AddPage(tab, "stdout")
        self.logpanel = tab
        tabnum += 1
	tab = comPanel(notebook, self.m, tabnum)
        notebook.AddPage(tab, "com")
        tabnum += 1
        tab = LogPanel(notebook)
        notebook.AddPage(tab, "stderr")
        self.logpanel2 = tab
        self.notebook = notebook
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)
        self.Layout()
        self.Show()

    def OnExit(self,e):
        self.Close(True)

    def OnHelloWorld(self,e):
        print "%s  Hello, World!"%(time.ctime())

    def OnAbout(self,e):
        dlg = wx.MessageDialog(
            self, "This is the MRB GUI", "About MRB GUI", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

if __name__ == "__main__":
    model = Model()
    app = wx.App(False)
    frame = MainWindow(model)
    redir = RedirectText(frame.logpanel.log)
    sys.stdout = redir
    redir = RedirectText(frame.logpanel2.log)
    sys.stderr = redir
    print time.ctime()+"  test"
    print os.popen("pwd").read()
    app.MainLoop()
