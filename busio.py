'''
busio.py
begun 2014-03-11 by wja (ashmansk@hep.upenn.edu)

This module is intended to provide the API for accessing registers,
memories, etc.  on the LaPET Module Readout Board and other boards
implementing the MRB's Ethernet/UDP-based register-file I/O bus.

classes:

UdpBoard
'''

import numpy as np
import socket
import time
import sys

class UdpBoard:
    '''
    UdpBoard(boardid)

    Argument:

    boardid
      - if integer, then IP address is 192.168.1.(80+boardid)
      - if string (e.g. "192.168.1.123"), then IP address is as given
    
    Instantiate a UdpBoard object for UDP-based register I/O to
    MRB-like board on Ethernet network at 192.168.1.(80+boardid).  The
    UdpBoard class provides low-level register and memory access to
    the board's 16A/16D input/output bus.  Higher-level classes are
    responsible for mapping the address space mnemonically.

    In addition to basic single-register read/write functionality
    (which does one bus operation per round-trip UDP datagram),
    UdpBoard provides convenience functions for Virtex5 I/O, on the
    assumption that (as in the MRB) a Spartan3an chip exposes its I/O
    bus directly to the network, while a Virtex5 chip (connected via
    serial interface to the Spartan3an) contains a separate I/O bus
    that can be accessed via multiple bus operations to the
    Spartan3an.

    public methods:
      send
      recv
      rd
      wr
    '''
    def __init__(self, boardid):
        self.boardid = boardid
        if type(boardid)==str:
            # full IP address specified as string
            self.remhost = boardid
        else:
            # board serial number given as integer: convert to IP addr
            self.remhost = "192.168.1.%d"%(80+boardid)
        # MRB-style bus interface listens on UDP port 31416
        self.remport = 31416
        # use UDP (not TCP) for board I/O
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.connect((self.remhost, self.remport))
        # 10 millisecond I/O timeout for reponses from board
        self.socket.settimeout(self.TIMEOUT_SECONDS)
        # get my own local port number
        self.locport = self.socket.getsockname()[1]
        # allows us to enumerate and track I/O requests to board
        self.iter = 0
        # count number of times board fails to respond to I/O request
        self.nfail = 0
        # for enabling verbose debug printout
        self.debug = False
        # temporary backward compatibility with old 'Foobar' class
        self.b = self
        self.nretry = -1

    #
    # Class-wide constants
    #
    TIMEOUT_SECONDS = 0.010
    MSGPADLEN = 1022
    RECVBUFFERLEN = 2048

    def send(self, data):
        '''
        send(data)

        Zero-pad sequence of bytes ('data') to 'msgpadlen' and send
        to board as UDP datagram.
        '''
        self.iter += 1
        msg = chr(self.iter>>24 & 0xff) + chr(self.iter>>16 & 0xff) \
            + chr(self.iter>>8  & 0xff) + chr(self.iter     & 0xff)
        for x in data:
            msg += chr(x)
        msglen = len(msg)
        msgpadlen = self.MSGPADLEN
        assert(msglen<=msgpadlen)
        dgram = msg + (msgpadlen-msglen)*chr(0)
        dgram = chr(msglen>>8 & 0xff) + chr(msglen>>0 & 0xff) + dgram
        self.socket.send(dgram)

    def recv(self):
        '''
        recv()

        receive datagram reply from board (in response to previous send)
        '''
        message, address = self.socket.recvfrom(self.RECVBUFFERLEN)
        assert(message!=None)
        data = [ord(x) for x in message]
        assert(len(data)>=2)
        dlen = data[0]<<8 | data[1]
        # dlen doesn't include its own two bytes
        assert(len(data) >= 2+dlen)
        assert(data[2] == (self.iter>>24 & 0xff))
        assert(data[3] == (self.iter>>16 & 0xff))
        assert(data[4] == (self.iter>>8  & 0xff))
        assert(data[5] == (self.iter     & 0xff))
        data = data[6:][:dlen-4]
        return data

    def rd(self, addr):
        '''
        rd(addr)

        read 16-bit data word from 16-bit bus address 'addr'
        '''
        # read opcode is 0x0001
        self.send([0x00, 0x01, addr>>8 & 0xff, addr>>0 & 0xff])
        data = None
        try:
            data = self.recv()
        except socket.timeout:
            pass
        if data is None:
            self.nfail += 1
            return -1
        assert(len(data)==4)
        assert(data[0] == (addr>>8 & 0xff))
        #assert(data[1] == (addr    & 0xff))
        d = data[2]<<8 | data[3]
        if self.debug:
            print "UdpBoard.rd(%04x) -> %04x"%(addr, d)
        return d

    def wr(self, addr, d):
        '''
        wr(addr, d)

        write 16-bit data word 'd' to 16-bit bus address 'addr'
        '''
        # write opcode is 0x0002
        self.send([0x00, 0x02, addr>>8 & 0xff, addr & 0xff,
                   0x00, 0x00, d   >>8 & 0xff, d    & 0xff])
        data = self.recv()
        #assert(len(data)==4)
        #assert(data[0] == (addr>>8 & 0xff))
        #assert(data[1] == (addr    & 0xff))
        #assert(data[2] == (d   >>8 & 0xff))
        #assert(data[3] == (d       & 0xff))
        if self.debug:
            print "UdpBoard.wr(%04x := %04x)"%(addr, d)

    def v5rd(self, a):
        '''
        v5rd(a)

        Read 16-bit data word from virtex5 address 'a'.  The Virtex5
        register bus is accessible only by doing multiple I/O
        operations to the network-connected Spartan3 register bus.
        '''
        ahi = a>>8 & 0xff
        alo = a & 0xff
        m = [ 0x00, 0x01, 0x00, 0x83,   # rd 0083 (bytesseen)
              0x00, 0x02, 0x00, 0x82, 0x00, 0x00, 0x00, ahi,  # wr 0082 := ahi
              0x00, 0x03, 0x00, 0x10,   # wait 16 cycles
              0x00, 0x02, 0x00, 0x82, 0x00, 0x00, 0x00, alo,  # wr 0082 := alo
              0x00, 0x03, 0x00, 0x10,   # wait 16 cycles
              0x00, 0x02, 0x00, 0x82, 0x00, 0x00, 0x01, 0x02, # wr 0082 := 0102
              0x00, 0x03, 0x00, 0xf0,   # wait 240 cycles
              0x00, 0x01, 0x00, 0x83,   # rd 0083 (bytesseen)
              0x00, 0x01, 0x00, 0x80,   # rd 0082 (status)
              0x00, 0x01, 0x00, 0x81 ]  # rd 0081 (rddata)
        self.send(m)
        rsp = self.recv()
        assert(len(rsp)==28)
        bytesseen0 = rsp[2]<<8 | rsp[3]
        bytesseen1 = rsp[18]<<8 | rsp[19]
        status = rsp[22]<<8 | rsp[23]
        d = rsp[26]<<8 | rsp[27]
        bytesseen_expect = (bytesseen0+3)&0xffff
        if bytesseen1!=bytesseen_expect or status!=2:
            print "v5rd: a=%x bs0=%d bs1=%d bsexp=%d st=%x d=%x"%( \
                a, bytesseen0, bytesseen1, bytesseen_expect, status, d)
            self.nfail += 1
        return d

    def v5wr(self, a, d):
        '''
        v5wr(a, d)

        Write 16-bit data value 'd' to 16-bit address 'a' on Virtex5
        register bus, which can be accessed only via multiple I/O
        operations to Spartan3 register bus.
        '''
        bytesseen0 = self.rd(0x0083)
        self.wr(0x0082, d>>8 & 0xff)
        self.wr(0x0082, d    & 0xff)
        self.wr(0x0082, a>>8 & 0xff)
        self.wr(0x0082, a    & 0xff)
        self.wr(0x0082, 0x0101)
        bytesseen1 = self.rd(0x0083)
        status = self.rd(0x0080)
        bytesseen_expect = (bytesseen0+1)&0xffff
        if bytesseen1!=bytesseen_expect or status!=1:
            print "v5wr: a=%x bs0=%d bs1=%d bsexp=%d st=%x"%( \
                a, bytesseen0, bytesseen1, bytesseen_expect, status)
            self.nfail += 1


class Reg:
    '''
    Reg(board, addr, **kwargs)

    Should represent everything we know about a given bus-addressable
    register within an MRB-like board, including how to access it,
    what access is permitted, and how to format the contents for
    display.
    '''
    def __init__(self, 
                 mnemboard, addr, 
                 name="unnamed", 
                 lname="no long name provided",
                 v5=False,
                 read=None,
                 fmt=None
                 ):
        '''
        Does a constructor get a docstring?
        '''
        self.mb = mnemboard
        self.b = mnemboard.b
        self.a = addr
        self.name = name
        self.lname = lname
        if fmt is None:
            fmt = Reg.format_d
        self.format_method = fmt
        if v5:
            self.read_method = Reg.read_v5
            self.write_method = Reg.write_v5
        else:
            self.read_method = Reg.read_s3
            self.write_method = Reg.write_s3
        if read is not None:
            self.read_method = read
        self.data = -1

    def write_s3(self, d):
        self.wdata = d
        self.b.wr(self.a, d)

    def write_v5(self, d):
        self.wdata = d
        self.b.v5wr(self.a, d)

    def wr(self, d):
        "wr(d): write data 'd' to register"
        self.write_method(self, d)

    def read_s3(self):
        self.data = self.b.rd(self.a)

    def read_v5(self):
        self.data = self.b.v5rd(self.a)

    def read_v5_twice(self):
        self.b.v5rd(self.a)
        self.data = self.b.v5rd(self.a)

    def read(self):
        'read(): read register and return integer result'
        self.read_method(self)
        return self.data

    def rfmt(self):
        'rfmt(): read register and return string-formated result'
        self.read()
        return self.format_method(self)

    #
    # I think it should be easy to replace these next several
    # formatters with a unified formatter for integer values that
    # takes a C-style format string as an argument.  Or maybe I will
    # eventually be smart enough to make each register aware of its
    # own width, and then all I would need to tell it is which radix
    # (hex/dec/bin) I want and whether or not to pad it to full width.
    #
    def format_d(self):
        'format data as decimal int (%d)'
        return "%d"%(self.data)

    def format_02x(self):
        'format data as 2-digit hexadecimal int (%02x)'
        return "%02x"%(self.data)

    def format_04x(self):
        'format data as 4-digit hexadecimal int (%04x)'
        return "%04x"%(self.data)

    def format_01b(self):
        'format data as a 1-bit binary int'
        return bin(0x10000 | self.data)[-1:]

    def format_02b(self):
        'format data as a 2-bit binary int'
        return bin(0x10000 | self.data)[-2:]

    def format_04b(self):
        'format data as a 4-bit binary int'
        return bin(0x10000 | self.data)[-4:]

    def format_05b(self):
        'format data as a 5-bit binary int'
        return bin(0x10000 | self.data)[-5:]

    def format_06b(self):
        'format data as a 6-bit binary int'
        return bin(0x10000 | self.data)[-6:]

    def format_08b(self):
        'format data as an 8-bit binary int'
        return bin(0x10000 | self.data)[-8:]

    def format_09b(self):
        'format data as a 9-bit binary int'
        return bin(0x10000 | self.data)[-9:]

    def format_010b(self):
        'format data as a 10-bit binary int'
        return bin(0x10000 | self.data)[-10:]

    def format_time_0875(self):
        'format data (scaled by 1/0.875) as time hh:mm:ss'
        if self.data<0:
            return "??:??:??"
        s = int(self.data/0.875)
        return "%02d:%02d:%02d"%(s/3600, (s%3600)/60, s%60)

    def format_sysmon_temp(self):
        'format data as Virtex5-SysMon-derived temperature (%.2f)'
        if self.data<0:
            return "?"
        t = self.data * 503.975/1024/64 - 273.15
        return "%.2f%sC"%(t, u"\u00B0")

    def format_sysmon_vccint(self):
        'format data as Virtex5-SysMon vccint (%.2f)'
        if self.data<0:
            return "?"
        t = self.data * 3.0/(1024*64)
        return "%.2f V"%(t)

    def format_adhoc_frzreq(self):
        'format data as mrb/frzreq'
        if self.data<0: return '?'
        return "FrzOnTrig=%d FrzReq=%d"%(self.data>>1 & 1, self.data & 1)

    def format_adhoc_rofifoflags(self):
        'format data as mrb/rofifoflags'
        if self.data<0: return '?'
        x = self.data
        return "nw=%d ne=%d af=%d"%(x>>2 & 0xfff, x>>1 & 1, x & 1)

    def format_adhoc_spyptr(self):
        'format data as mrb/spyptr'
        x = self.data
        if x<0: return '?'
        notfrozen = x>>8 & 1
        ptr = x & 0xff
        txt = ["frz", "run"]
        return "%03x=%s/%02x"%(x, txt[notfrozen], ptr)

class MnemBoard:
    '''
    MnemBoard(boardid)

    Instantiate board having MRB-style UDP interface for register-bus
    I/O.  This base class is intended to be extended by MRB, MCU, etc.
    '''
    def __init__(self, boardid):
        self.b = UdpBoard(boardid)

    def _newreg(self, a, **kwargs):
        '''
        newreg(a, **kwargs)

        Define new register at bus address 'a'
        '''
        return Reg(self, a, **kwargs)

    def rd(self, a):
        'rd(a): read from S3 register (deprecated)'
        return self.b.rd(a)

    def v5rd(self, a):
        'v5rd(a): read from V5 register (deprecated)'
        return self.b.v5rd(a)

    def wr(self, a, d):
        'wr(a,d): write to S3 register (deprecated)'
        self.b.wr(a, d)

    def v5wr(self, a, d):
        'v5wr(a,d): write to V5 register (deprecated)'
        self.b.v5wr(a, d)

class Mrb(MnemBoard):
    '''
    Mrb(boardid)

    Instantiate MRB (Module Readout Board) for register-bus I/O.
    Argument 'boardid' is passed verbatim to 'UdpBoard' constructor.
    Unlike 'UdpBoard', this class should be smart enough to provide
    mnemonic names for the MRB's registers and memories.  (Indeed,
    that should be its main purpose.)
    '''
    def __init__(self, boardid, imrb=-1):
        MnemBoard.__init__(self, boardid)
        self.imrb = imrb

        self.r0000 = self._newreg(
            a=0x0000,
            name="r0000",
            lname="read-only register that should always read 0x0000",
            fmt=Reg.format_04x)

        self.rbeef = self._newreg(
            a=0x0001,
            name="rbeef",
            lname="read-only register that should always read 0xbeef",
            fmt=Reg.format_04x)

        self.s3uptime = self._newreg(
            a=0x0002, 
            name="s3uptime", 
            lname="Spartan3AN uptime (0.875s ticks)",
            fmt=Reg.format_time_0875)

        self.q0003 = self._newreg(
            a=0x0003,
            name="q0003",
            lname="16-bit S3 R/W (needs better name & defn)",
            fmt=Reg.format_04x)

        self.ledpatt = self._newreg(
            a=0x0004,
            name="ledpatt",
            lname="9-bit LED pattern",
            fmt=Reg.format_09b)

        self.q0005 = self._newreg(
            a=0x0005,
            name="q0005",
            lname="16-bit S3 R/W (needs better name & defn)",
            fmt=Reg.format_04x)

        self.dipsw = self._newreg(
            a=0x0006,
            name="dipsw",
            lname="8-bit DIP switch pattern",
            fmt=Reg.format_08b)

        self.ad9222up = self._newreg(
            a=0x0007,
            name="ad9222up",
            lname="10-bit AD9222 power-up R/W",
            fmt=Reg.format_010b)

        self.ad9287up = self._newreg(
            a=0x0008,
            name="ad9287up",
            lname="6-bit AD9287 power-up R/W",
            fmt=Reg.format_06b)

        self.drs4plllck = self._newreg(
            a=0x0009,
            name="drs4plllck",
            lname="10-bit DRS4 PLL-locked status",
            fmt=Reg.format_010b)

        self.drs4dtap = self._newreg(
            a=0x000a,
            name="drs4dtap",
            lname="10-bit DRS4 DTAP state",
            fmt=Reg.format_010b)

        self.rofifosclr = self._newreg(
            a=0x000b,
            name="rofifosclr",
            lname="readout FIFO sclr (sticky - that's dumb)",
            fmt=Reg.format_01b)

        self.rofifoflags = self._newreg(
            a=0x000c,
            name="rofifoflags",
            lname="readout FIFO (nwords,notempty,nearlyfull)",
            fmt=Reg.format_adhoc_rofifoflags)

        self.roframecount = self._newreg(
            a=0x000d,
            name="roframecount",
            lname="readout frame count (seen by S3 from V5)",
            fmt=Reg.format_d)

        self.mrbfiforeset = self._newreg(
            a=0x000e,
            name="mrbfiforeset",
            lname="send MRB-side mrbfiforeset signal (on write)",
            fmt=Reg.format_d)

        self.v5reconfig = self._newreg(
            a=0x0042,
            name="v5reconfig",
            lname="reconfigure Virtex5 from flash contents (on write)",
            fmt=Reg.format_d)

        self.sdac0 = self._newreg(
            a=0x0140,
            name="sdac0",
            lname="serial DAC 0 read/write word",
            fmt=Reg.format_04x)

        self.sdac1 = self._newreg(
            a=0x0141,
            name="sdac1",
            lname="serial DAC 1 read/write word",
            fmt=Reg.format_04x)

        self.spiadcwdat = self._newreg(
            a=0x0200,
            name="spiadcwdat",
            lname="(addr,data) to write to selected ADC via SPI",
            fmt=Reg.format_04x)

        self.spiadcrdat = self._newreg(
            a=0x0201,
            name="spiadcrdat",
            lname="(addr,data) to read from selected ADC via SPI",
            fmt=Reg.format_04x)

        self.spiadcwhich = self._newreg(
            a=0x0202,
            name="spiadcwhich",
            lname="which of 16 ADCs is addressed via SPI (bit4=all)",
            fmt=Reg.format_05b)

        self.readoutport = self._newreg(
            a=0x0301,
            name="readoutport",
            lname="readout destination UDP port number",
            fmt=Reg.format_04x)

        self.tstamp = self._newreg(
            a=0x0004, v5=True,
            name="tstamp",
            lname="truncated (16-bit) time stamp",
            fmt=Reg.format_d)

        self.al9287 = self._newreg(
            a=0x0005, v5=True,
            name="al9287",
            lname="ad9827 'aligned' status (6 bits)",
            fmt=Reg.format_06b)

        self.srclkflip = self._newreg(
            a=0x0006, v5=True,
            name="srclkflip",
            lname="delay srclk one-half cycle (10 bits)",
            fmt=Reg.format_010b)

        self.coinc_ena = self._newreg(
            a=0x000e, v5=True,
            name="coinc_ena",
            lname="{coinc_always, coinc_enabled}",
            fmt=Reg.format_02b)

        self.ntrig = self._newreg(
            a=0x0020, v5=True,
            name="ntrig",
            lname="single trigger count (kludge)",
            fmt=Reg.format_d)

        self.ncoinc = self._newreg(
            a=0x0021, v5=True,
            name="ncoinc",
            lname="coincidence count (kludge)",
            fmt=Reg.format_d)

        self.misaligncnt0 = self._newreg(
            a=0x0030, v5=True,
            name="misaligncnt0",
            lname="AD9222 ADC0 misalign count",
            fmt=Reg.format_d)

        self.misaligncnt1 = self._newreg(
            a=0x0031, v5=True,
            name="misaligncnt1",
            lname="AD9222 ADC1 misalign count",
            fmt=Reg.format_d)

        self.misaligncnt2 = self._newreg(
            a=0x0032, v5=True,
            name="misaligncnt2",
            lname="AD9222 ADC2 misalign count",
            fmt=Reg.format_d)

        self.misaligncnt3 = self._newreg(
            a=0x0033, v5=True,
            name="misaligncnt3",
            lname="AD9222 ADC3 misalign count",
            fmt=Reg.format_d)

        self.misaligncnt4 = self._newreg(
            a=0x0034, v5=True,
            name="misaligncnt4",
            lname="AD9222 ADC4 misalign count",
            fmt=Reg.format_d)

        self.misaligncnt5 = self._newreg(
            a=0x0035, v5=True,
            name="misaligncnt5",
            lname="AD9222 ADC5 misalign count",
            fmt=Reg.format_d)

        self.misaligncnt6 = self._newreg(
            a=0x0036, v5=True,
            name="misaligncnt6",
            lname="AD9222 ADC6 misalign count",
            fmt=Reg.format_d)

        self.misaligncnt7 = self._newreg(
            a=0x0037, v5=True,
            name="misaligncnt7",
            lname="AD9222 ADC7 misalign count",
            fmt=Reg.format_d)

        self.misaligncnt8 = self._newreg(
            a=0x0038, v5=True,
            name="misaligncnt8",
            lname="AD9222 ADC8 misalign count",
            fmt=Reg.format_d)

        self.misaligncnt9 = self._newreg(
            a=0x0039, v5=True,
            name="misaligncnt9",
            lname="AD9222 ADC9 misalign count",
            fmt=Reg.format_d)

        self.drs0gocnt = self._newreg(
            a=0x0060, v5=True,
            name="drs0gocnt",
            lname="DRS0 GO count",
            fmt=Reg.format_d)

        self.drs1gocnt = self._newreg(
            a=0x0061, v5=True,
            name="drs1gocnt",
            lname="DRS1 GO count",
            fmt=Reg.format_d)

        self.drs2gocnt = self._newreg(
            a=0x0062, v5=True,
            name="drs2gocnt",
            lname="DRS2 GO count",
            fmt=Reg.format_d)

        self.drs3gocnt = self._newreg(
            a=0x0063, v5=True,
            name="drs3gocnt",
            lname="DRS3 GO count",
            fmt=Reg.format_d)

        self.drs4gocnt = self._newreg(
            a=0x0064, v5=True,
            name="drs4gocnt",
            lname="DRS4 GO count",
            fmt=Reg.format_d)

        self.drs5gocnt = self._newreg(
            a=0x0065, v5=True,
            name="drs5gocnt",
            lname="DRS5 GO count",
            fmt=Reg.format_d)

        self.drs6gocnt = self._newreg(
            a=0x0066, v5=True,
            name="drs6gocnt",
            lname="DRS6 GO count",
            fmt=Reg.format_d)

        self.drs7gocnt = self._newreg(
            a=0x0067, v5=True,
            name="drs7gocnt",
            lname="DRS7 GO count",
            fmt=Reg.format_d)

        self.drs8gocnt = self._newreg(
            a=0x0068, v5=True,
            name="drs8gocnt",
            lname="DRS8 GO count",
            fmt=Reg.format_d)

        self.drs9gocnt = self._newreg(
            a=0x0069, v5=True,
            name="drs9gocnt",
            lname="DRS9 GO count",
            fmt=Reg.format_d)

        self.drs0tslast = self._newreg(
            a=0x0070, v5=True,
            name="drs0tslast",
            lname="DRS0 timestamp at last GO",
            fmt=Reg.format_d)

        self.drs1tslast = self._newreg(
            a=0x0071, v5=True,
            name="drs1tslast",
            lname="DRS1 timestamp at last GO",
            fmt=Reg.format_d)

        self.drs2tslast = self._newreg(
            a=0x0072, v5=True,
            name="drs2tslast",
            lname="DRS2 timestamp at last GO",
            fmt=Reg.format_d)

        self.drs3tslast = self._newreg(
            a=0x0073, v5=True,
            name="drs3tslast",
            lname="DRS3 timestamp at last GO",
            fmt=Reg.format_d)

        self.drs4tslast = self._newreg(
            a=0x0074, v5=True,
            name="drs4tslast",
            lname="DRS4 timestamp at last GO",
            fmt=Reg.format_d)

        self.drs5tslast = self._newreg(
            a=0x0075, v5=True,
            name="drs5tslast",
            lname="DRS5 timestamp at last GO",
            fmt=Reg.format_d)

        self.drs6tslast = self._newreg(
            a=0x0076, v5=True,
            name="drs6tslast",
            lname="DRS6 timestamp at last GO",
            fmt=Reg.format_d)

        self.drs7tslast = self._newreg(
            a=0x0077, v5=True,
            name="drs7tslast",
            lname="DRS7 timestamp at last GO",
            fmt=Reg.format_d)

        self.drs8tslast = self._newreg(
            a=0x0078, v5=True,
            name="drs8tslast",
            lname="DRS8 timestamp at last GO",
            fmt=Reg.format_d)

        self.drs9tslast = self._newreg(
            a=0x0079, v5=True,
            name="drs9tslast",
            lname="DRS9 timestamp at last GO",
            fmt=Reg.format_d)

        self.drs0cidlast = self._newreg(
            a=0x0080, v5=True,
            name="drs0cidlast",
            lname="DRS0 cellid from last readout",
            fmt=Reg.format_d)

        self.drs1cidlast = self._newreg(
            a=0x0081, v5=True,
            name="drs1cidlast",
            lname="DRS1 cellid from last readout",
            fmt=Reg.format_d)

        self.drs2cidlast = self._newreg(
            a=0x0082, v5=True,
            name="drs2cidlast",
            lname="DRS2 cellid from last readout",
            fmt=Reg.format_d)

        self.drs3cidlast = self._newreg(
            a=0x0083, v5=True,
            name="drs3cidlast",
            lname="DRS3 cellid from last readout",
            fmt=Reg.format_d)

        self.drs4cidlast = self._newreg(
            a=0x0084, v5=True,
            name="drs4cidlast",
            lname="DRS4 cellid from last readout",
            fmt=Reg.format_d)

        self.drs5cidlast = self._newreg(
            a=0x0085, v5=True,
            name="drs5cidlast",
            lname="DRS5 cellid from last readout",
            fmt=Reg.format_d)

        self.drs6cidlast = self._newreg(
            a=0x0086, v5=True,
            name="drs6cidlast",
            lname="DRS6 cellid from last readout",
            fmt=Reg.format_d)

        self.drs7cidlast = self._newreg(
            a=0x0087, v5=True,
            name="drs7cidlast",
            lname="DRS7 cellid from last readout",
            fmt=Reg.format_d)

        self.drs8cidlast = self._newreg(
            a=0x0088, v5=True,
            name="drs8cidlast",
            lname="DRS8 cellid from last readout",
            fmt=Reg.format_d)

        self.drs9cidlast = self._newreg(
            a=0x0089, v5=True,
            name="drs9cidlast",
            lname="DRS9 cellid from last readout",
            fmt=Reg.format_d)

        self.v5myreset = self._newreg(
            a=0x0203, v5=True,
            name="v5myreset",
            lname="assert 'myreset' signal in V5 (W/O, bit 0, sticky)",
            fmt=Reg.format_d)

        self.fakego = self._newreg(
            a=0x0204, v5=True,
            name="fakego",
            lname="send fake GO to readoutfsm (W/O mask[9:0])",
            fmt=Reg.format_010b)

        self.frzreq = self._newreg(
            a=0x0330, v5=True,
            name="frzreq",
            lname="trigger spy freeze request {frzontrig,frzreq}",
            fmt=Reg.format_adhoc_frzreq)

        self.spyptr = self._newreg(
            a=0x0331, v5=True,
            name="spyptr",
            lname="trigger spy pointer {!frozen,00,ptr[5:0]})",
            fmt=Reg.format_adhoc_spyptr)

        self.qmin_trig = self._newreg(
            a=0x0360, v5=True,
            name="qmin_trig",
            lname="minimum drssum Q for trigger",
            fmt=Reg.format_d)

        self.qmax_trig = self._newreg(
            a=0x0361, v5=True,
            name="qmax_trig",
            lname="maximum drssum Q for trigger",
            fmt=Reg.format_d)

        self.zone_ena_mask = self._newreg(
            a=0x0362, v5=True,
            name="zone_ena_mask",
            lname="bit mask of which trigger zones to enable",
            fmt=Reg.format_010b)

        self.max_ntrig = self._newreg(
            a=0x0363, v5=True,
            name="max_ntrig",
            lname="stop after accepting this number of triggers",
            fmt=Reg.format_d)

        self.count_ok = self._newreg(
            a=0x0364, v5=True,
            name="count_ok",
            lname="count total single-trigger events",
            fmt=Reg.format_d)

        self.count_ok0 = self._newreg(
            a=0x0365, v5=True,
            name="count_ok0",
            lname="count single-trigger events for zone 0",
            fmt=Reg.format_d)

        self.count_ok1 = self._newreg(
            a=0x0366, v5=True,
            name="count_ok1",
            lname="count single-trigger events for zone 1",
            fmt=Reg.format_d)

        self.count_ok2 = self._newreg(
            a=0x0367, v5=True,
            name="count_ok2",
            lname="count single-trigger events for zone 2",
            fmt=Reg.format_d)

        self.count_ok3 = self._newreg(
            a=0x0368, v5=True,
            name="count_ok3",
            lname="count single-trigger events for zone 3",
            fmt=Reg.format_d)

        self.mfsmreadcnt = self._newreg(
            a=0x04fa, v5=True,
            name="mfsmreadcnt",
            lname="merger FSM read count",
            fmt=Reg.format_d)

        self.mfsmdonecnt = self._newreg(
            a=0x04fb, v5=True,
            name="mfsmdonecnt",
            lname="merger FSM done count",
            fmt=Reg.format_d)

        self.fifofull = self._newreg(
            a=0x04fc, v5=True,
            name="fifofull",
            lname="readoutfsm fifo full flags [9:0]",
            fmt=Reg.format_010b)

        self.fifone = self._newreg(
            a=0x04fd, v5=True,
            name="fifone",
            lname="readoutfsm fifo not-empty flags [9:0]",
            fmt=Reg.format_010b)

        self.mfifobusw = self._newreg(
            a=0x04fe, v5=True,
            name="mfifobusw",
            lname="merger FIFO bus-write (idrs[3:0])",
            fmt=Reg.format_04b)

        self.mfifoflags = self._newreg(
            a=0x04ff, v5=True,
            name="mfifoflags",
            lname="merger FIFO (AF,NE,Q[3:0])",
            fmt=Reg.format_02x)

        self.v5temp = self._newreg(
            a=0xaa00, v5=True,
            name="v5temp",
            lname="Virtex5 raw temperature reading (0.0077 K steps)",
            read=Reg.read_v5_twice,
            fmt=Reg.format_sysmon_temp)

        self.v5vccint = self._newreg(
            a=0xaa01, v5=True,
            name="v5vccint",
            lname="Virtex5 raw vccint reading (0.046 mV steps)",
            read=Reg.read_v5_twice,
            fmt=Reg.format_sysmon_vccint)

        self.trigpeds = np.zeros(self.NTRIGADC, dtype=np.int32)

    # static data members (mostly constants)
    NTRIGADC = 24

    def adcteston(self, which, word0, word1):
        '"which" is 0-5 for ad9287 and 6-15 for ad9222'
        w0lo = word0 & 0xff
        w0hi = word0>>8 & 0xff
        w1lo = word1 & 0xff
        w1hi = word1>>8 & 0xff
        self.spiadcwhich.wr(which)         # select this AD92xx ADC
        self.spiadcwdat.wr(0x1900 | w0lo)  # pattern 1 LSB
        self.spiadcwdat.wr(0x1a00 | w0hi)  # pattern 1 MSB
        self.spiadcwdat.wr(0x1b00 | w1lo)  # pattern 2 LSB
        self.spiadcwdat.wr(0x1c00 | w1hi)  # pattern 2 MSB
        self.spiadcwdat.wr(0x0d48)         # test mode ON
        self.spiadcwdat.wr(0xff01)         # execute/update

    def adctestoff(self, which):
        self.spiadcwhich.wr(which)         # select this AD92xx ADC
        self.spiadcwdat.wr(0x0d00)         # test mode OFF
        self.spiadcwdat.wr(0xff01)         # execute/update

    def drsadcteston(self, word0=0xfff, word1=0x000):
        for iadc in range(6,16):
            self.adcteston(iadc, word0, word1)

    def drsadctestoff(self):
        for iadc in range(6,16):
            self.adctestoff(iadc)

    def trigadcteston(self, word0=0xff, word1=0x00):
        for iadc in range(6):
            self.adcteston(iadc, word0, word1)

    def trigadctestoff(self):
        for iadc in range(6):
            self.adctestoff(iadc)

    def drainrofifo(self):
        time0 = time.time()
        m = self
        d = []
        flags = m.rd(0x000c)
        #if flags==0xffff: flags = 0  # don't loop if board looks dead
        fifone = flags>>1 & 1
        fifonw = flags>>2 & 0xfff
        print "drainrofifo: fifonw=%d"%(fifonw,)
        msg = []
        nmsg = 0
        for iword in range(fifonw):
            mm = [0x00, 0x02, 0x00, 0x0f, 0x00, 0x00, 0x00, 0x00,  # w 000f:=0
                  0x00, 0x01, 0x00, 0x13,  # rd 0013
                  0x00, 0x01, 0x00, 0x12,  # rd 0012
                  0x00, 0x01, 0x00, 0x11,  # rd 0011
                  0x00, 0x01, 0x00, 0x10]  # rd 0010
            msg = msg+mm
            nmsg += 1
            if len(msg)>900 or iword==fifonw-1:
                m.b.send(msg)
                rsp = m.b.recv()
                if 0:
                    print "len(rsp)=%d"%(len(rsp),), \
                        " ".join(["%02x"%(rsp[j]) for j in range(len(rsp))])
                for j in range(nmsg):
                    x13hi = rsp[20*j +  6]
                    x13lo = rsp[20*j +  7]
                    x12hi = rsp[20*j + 10]
                    x12lo = rsp[20*j + 11]
                    x11hi = rsp[20*j + 14]
                    x11lo = rsp[20*j + 15]
                    x10hi = rsp[20*j + 18]
                    x10lo = rsp[20*j + 19]
                    x =             x13lo<<48 | \
                        x12hi<<40 | x12lo<<32 | \
                        x11hi<<24 | x11lo<<16 | \
                        x10hi<<8  | x10lo
                    fifone = x13hi>>1 & 1
                    d.append(x)
                msg = []
                nmsg = 0
        print "drainrofifo: final fifone=%d"%(fifone,)
        self.rofifodata = d
        time1 = time.time()
        dt = 1000*(time1-time0)
        print "drainrofifo: dt = %.1f ms"%(dt,)
        return d

    def miscinit(self):
        'MRB power-up misc register writes formerly done in test.py'
        m = self
        m.sdac0.wr(0x803c)        # SDAC0 also enable x2 voltage gain
        #m.sdac0.wr(0x0510)        # set BUF_VCM to 0.80 volts
        m.sdac0.wr(0x0000)        # set BUF_VCM to 0.00 volts
        m.sdac0.wr(0x1c20)        # set ROFS    to 1.85 volts
        m.sdac1.wr(0x800c)        # SDAC1 enable signal buffering
        m.sdac1.wr(0x6a00)        # set SAM_DAC_CM_DRS to ?
        m.sdac1.wr(0x7bc0)        # set SAM_DAC_CM_TRIG to 0.90 volts
        #m.ad9222up.wr(0x0015)     # power up AD9222 ADCs 0+2+4
        m.ad9222up.wr(0x001f)     # power up AD9222 ADCs 0-4
        m.ad9287up.wr(0x0007)     # power up AD9287 ADCs 0+1+2
        m.readoutport.wr(0x1234)  # readout destination UDP port number
        m.rofifosclr.wr(1)        # clear readout FIFO
        m.rofifosclr.wr(0)        # sticky register -- silly!


class ProtoMcu(MnemBoard):
    '''
    ProtoMcu(boardid)

    Instantiate a prototype MCU (Master Coincidence Unit) for
    register-bus I/O.  (The prototype MCU is a partially assembled MRB
    programmed to carry out a subset of MCU functionality.)  Argument
    'boardid' is passed verbatim to 'UdpBoard' constructor.  Unlike
    'UdpBoard', this class should be smart enough to provide mnemonic
    names for the MCU's registers and memories.  (Indeed, that should
    be its main purpose.)
    '''
    def __init__(self, boardid):
        MnemBoard.__init__(self, boardid)

        self.s3uptime = self._newreg(
            #a=0x0003,
	    a=0x0008, #rwh
            name="s3uptime", 
            lname="Spartan3AN uptime (0.875s ticks)",
            fmt=Reg.format_time_0875)

        self.ncoinc = self._newreg(
            a=0x0503,
            name="ncoinc",
            lname="trigger coincidence count",
            fmt=Reg.format_d)

        self.ntrig = self._newreg(
            a=0x0505,
            name="ntrig",
            lname="single trigger count",
            fmt=Reg.format_d)

if __name__ == "__main__": 
    demo = ProtoMcu("192.168.1.10")
    addr = int(sys.argv[2], 16)
    if(len(sys.argv) == 3):
	data = demo.rd(addr)
	print("Data in address %x:%x"%(addr,data))
    if(len(sys.argv) == 4):
	data = int(sys.argv[3],16)
	demo.wr(addr, data)
	print("Data in address %x: %x"%(addr,data))
	
