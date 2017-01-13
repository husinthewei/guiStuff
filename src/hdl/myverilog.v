/*
 * myverilog.v
 * Programmable Logic to run in MicroZed Zynq FPGA
 * 2014-12-15 wja
 */

`timescale 1ns / 1ps
`default_nettype none

module myverilog
  (input  wire        clk,
   output wire  [3:0] led,
   // loopback connector (so that MCU proto pretends to be an MRB)
   output wire        loopback_a_p, loopback_a_n,
   output wire        loopback_b_p, loopback_b_n,
   input  wire        loopback_c_p, loopback_c_n,
   input  wire        loopback_clock_p, loopback_clock_n,
   // 100 MHz master clock coming in from SY89828 fanout chip
   input  wire        mcu_clock_p, mcu_clock_n,
   // connector to MRB 0
   input  wire        mrb_0a_p, mrb_0a_n, mrb_0b_p, mrb_0b_n,
   output wire        mrb_0c_p, mrb_0c_n,
   // connector to MRB 1
   input  wire        mrb_1a_p, mrb_1a_n, mrb_1b_p, mrb_1b_n,
   output wire        mrb_1c_p, mrb_1c_n,
   // connector to MRB 2
   input wire         mrb_2a_p, mrb_2a_n, mrb_2b_p, mrb_2b_n,
   output wire        mrb_2c_p, mrb_2c_n,
   // connector to MRB 3
   input wire         mrb_3a_p, mrb_3a_n, mrb_3b_p, mrb_3b_n,
   output wire        mrb_3c_p, mrb_3c_n,
   // connector to MRB 4
   input wire         mrb_4a_p, mrb_4a_n, mrb_4b_p, mrb_4b_n,
   output wire        mrb_4c_p, mrb_4c_n,
   // connector to MRB 5
   input wire         mrb_5a_p, mrb_5a_n, mrb_5b_p, mrb_5b_n,
   output wire        mrb_5c_p, mrb_5c_n,
   // connector to MRB 6
   input wire         mrb_6a_p, mrb_6a_n, mrb_6b_p, mrb_6b_n,
   output wire        mrb_6c_p, mrb_6c_n,
   // connector to MRB 7
   input wire         mrb_7a_p, mrb_7a_n, mrb_7b_p, mrb_7b_n,
   output wire        mrb_7c_p, mrb_7c_n,
   
   
   // for communication with PS (CPU) side
   input  wire [31:0] r0, r1, r2,
   output wire [31:0] r3, r4, r5, r6, r7
   );
    wire loopback_a, loopback_b;
    wire loopback_c, loopback_clock, mcu_clock;
    wire mrb_0a, mrb_0b, mrb_1a, mrb_1b, mrb_2a, mrb_2b, mrb_3a, mrb_3b, mrb_4a, mrb_4b, mrb_5a, mrb_5b, mrb_6a, mrb_6b, mrb_7a, mrb_7b;
    wire mrb_0c, mrb_1c, mrb_2c, mrb_3c, mrb_4c, mrb_5c, mrb_6c, mrb_7c;
    olvds o_loopback_a(loopback_a, loopback_a_p, loopback_a_n);
    olvds o_loopback_b(loopback_b, loopback_b_p, loopback_b_n);
    ilvds i_loopback_c(loopback_c, loopback_c_p, loopback_c_n);
    ilvds i_loopback_clock(loopback_clock, loopback_clock_p, loopback_clock_n);
    ilvds i_mcu_clock(mcu_clock, mcu_clock_p, mcu_clock_n);
    ilvds i_mrb_0a(mrb_0a, mrb_0a_p, mrb_0a_n);
    ilvds i_mrb_0b(mrb_0b, mrb_0b_p, mrb_0b_n);
    olvds o_mrb_0c(mrb_0c, mrb_0c_p, mrb_0c_n);
    ilvds i_mrb_1a(mrb_1a, mrb_1a_p, mrb_1a_n);
    ilvds i_mrb_1b(mrb_1b, mrb_1b_p, mrb_1b_n);
    olvds o_mrb_1c(mrb_1c, mrb_1c_p, mrb_1c_n);
    ilvds i_mrb_2a(mrb_2a, mrb_2a_p, mrb_2a_n);
    ilvds i_mrb_2b(mrb_2b, mrb_2b_p, mrb_2b_n);
    olvds o_mrb_2c(mrb_2c, mrb_2c_p, mrb_2c_n);
    ilvds i_mrb_3a(mrb_3a, mrb_3a_p, mrb_3a_n);
    ilvds i_mrb_3b(mrb_3b, mrb_3b_p, mrb_3b_n);
    olvds o_mrb_3c(mrb_3c, mrb_3c_p, mrb_3c_n); 
    ilvds i_mrb_4a(mrb_4a, mrb_4a_p, mrb_4a_n);
    ilvds i_mrb_4b(mrb_4b, mrb_4b_p, mrb_4b_n);
    olvds o_mrb_4c(mrb_4c, mrb_4c_p, mrb_4c_n); 
    ilvds i_mrb_5a(mrb_5a, mrb_5a_p, mrb_5a_n);
    ilvds i_mrb_5b(mrb_5b, mrb_5b_p, mrb_5b_n);
    olvds o_mrb_5c(mrb_5c, mrb_5c_p, mrb_5c_n); 
    ilvds i_mrb_6a(mrb_6a, mrb_6a_p, mrb_6a_n);
    ilvds i_mrb_6b(mrb_6b, mrb_6b_p, mrb_6b_n);
    olvds o_mrb_6c(mrb_6c, mrb_6c_p, mrb_6c_n);
    ilvds i_mrb_7a(mrb_7a, mrb_7a_p, mrb_7a_n);
    ilvds i_mrb_7b(mrb_7b, mrb_7b_p, mrb_7b_n);
    olvds o_mrb_7c(mrb_7c, mrb_7c_p, mrb_7c_n);
    // Instantiate "bus" I/O
    wire [15:0] baddr, bwrdata;
    wire [15:0] brddata;
    wire 	bwr, bstrobe;
    wire [33:0] ibus = {clk, bwr, baddr, bwrdata};
    wire [15:0] obus;
    assign brddata = obus;
    bus_zynq_gpio bus_zynq_gpio
      (.clk(clk), .r0(r0), .r1(r1), .r2(r2),
       .r3(r3), .r4(r4), .r5(), .r6(r6), .r7(r7),
       .baddr(baddr), .bwr(bwr), .bstrobe(bstrobe),
       .bwrdata(bwrdata), .brddata(brddata));
    assign r5 = {brddata,baddr};
    bror #(16'h0000) r0000(ibus, obus, 16'h1255);
    bror #(16'h0001) r0001(ibus, obus, 16'hbeef);
    bror #(16'h0002) r0002(ibus, obus, 16'hdead);
    wire [15:0] q0003;
    breg #(16'h0003) r0003(ibus, obus, q0003);
    // Blink LEDs on MCU prototype (PTB) board
    reg [28:0] count=0;
    reg [2:0]  state=0;
    always @ (posedge mcu_clk100) begin
      count <= count + 1;
      if (q0003[0] ? count[23:0]==0 : count[25:0]==0)
	state <= state==5 ? 0 : state+1;
    end
    wire [3:0] ledpattern =
		state==0 ? 'b0001 :
		state==1 ? 'b0010 :
		state==2 ? 'b0100 :
		state==3 ? 'b1000 :
		state==4 ? 'b0100 :
		state==5 ? 'b0010 : 'b1010;
    // Each of these four registers (corresponding to the 4 LEDs on
    // Weiwei's board) is 2 bits wide, so it has possible values
    // 0,1,2,3.  If the value is 1, then the corresponding LED stays
    // on.  If the value is 2, then the LED stays off.  If the value
    // is 0 or 3 then the LED is part of the blinking pattern.
    wire [15:0] q0004, q0005, q0006, q0007;
    breg #(16'h0004,2) r0004(ibus, obus, q0004);
    breg #(16'h0005,2) r0005(ibus, obus, q0005);
    breg #(16'h0006,2) r0006(ibus, obus, q0006);
    breg #(16'h0007,2) r0007(ibus, obus, q0007);
    assign led[0] = q0004==1 ? 1 :
		    q0004==2 ? 0 :
		    ledpattern[0];
    assign led[1] = q0005==1 ? 1 :
		    q0005==2 ? 0 :
		    ledpattern[1];
    assign led[2] = q0006==1 ? 1 :
		    q0006==2 ? 0 :
		    ledpattern[2];
    assign led[3] = q0007==1 ? 1 :
		    q0007==2 ? 0 :
		    ledpattern[3];
    // Divide down 100MHz 'clk' to count milliseconds and seconds
    reg [16:0] countto1ms = 0;  // wraps around once per millisecond
    reg [9:0]  countto1s  = 0;  // wraps around once per second
    reg        earlytick_1kHz = 0, tick_1kHz = 0, tick_1Hz = 0;
    reg [15:0] uptime = 0;      // count seconds since power-up
    always @ (posedge clk) begin
	// 'earlytick' exists so that tick_1Hz and tick_1kHz coincide
	countto1ms <= (countto1ms==99999 ? 0 : countto1ms+1);
	earlytick_1kHz <= (countto1ms==99999);
	tick_1kHz <= earlytick_1kHz;
	if (earlytick_1kHz) countto1s <= (countto1s==500 ? 0 : countto1s+1);//
	tick_1Hz <= earlytick_1kHz && countto1s==(500);
	if (tick_1Hz) uptime <= uptime+1;
    end
    // Make 'uptime' register bus-readable at address 0008
    wire [15:0] q0008;
    bror #(16'h0008) r0008(ibus, obus, uptime);
    // Make a register that counts milliseconds since it was last zeroed
    reg [15:0] countms = 0;
    wire [15:0] q0009;
    bror #(16'h0009) r0009(ibus, obus, countms);
    always @ (posedge clk) begin
	if (bwr && baddr=='h0009) begin
	    countms <= 0;  // zero the count upon write to address 0009
	end else if (tick_1kHz) begin
	    countms <= countms+1;
	end
    end
    // Clock generation
    wire mcu_clk100_ub, mcu_clk200_ub;  // "unbuffered" clocks
    wire mcu_clk100, mcu_clk200;
    wire clkfb;
    MMCME2_BASE
      #(.CLKFBOUT_MULT_F(8), .CLKIN1_PERIOD(10.0),
	.CLKOUT0_DIVIDE_F(8), .CLKOUT1_DIVIDE(4))
    mymmcm (.CLKIN1(loopback_clock), .RST(1'b0), .PWRDWN(1'b0),
	    .CLKOUT0(mcu_clk100_ub), .CLKOUT1(mcu_clk200_ub),
	    .CLKFBOUT(clkfb), .CLKFBIN(clkfb));
    BUFG bufg_mcu_clk100 (.I(mcu_clk100_ub), .O(mcu_clk100));
    BUFG bufg_mcu_clk200 (.I(mcu_clk200_ub), .O(mcu_clk200));
    // Let's try out LVDS serialization
    reg [27:0] powerup = 0;
`ifdef XILINX_SIMULATOR
    // In simulation, it's boring to wait too long
    wire [27:0] powerup_max = 28'h00000ff;
`else
    // In hardware, reset after about 2.7 seconds
    wire [27:0] powerup_max = 28'hfffffff;
`endif    
    reg powerup_reset = 0;
    always @ (posedge mcu_clk100) begin
	if (powerup!=powerup_max) begin
	    powerup <= powerup + 1;
	    powerup_reset <= 1;
	end else begin
	    powerup_reset <= 0;
	end
    end
    reg [3:0] cnt = 0;
    always @ (posedge mcu_clk100) 
      cnt <= cnt + 1;
    // We will play the 4-bit contents of "loopback_reg" out to
    // "oserdes_loopback_b" on each clock cycle of mcu_clk100.  If
    // q000c[4]==0, then the contents will be the 4-bit counter "cnt".
    // Otherwise, the contents will be fixed at q000c[3:0].
    wire [15:0] q000c;
    breg #(16'h000c) r000c(ibus, obus, q000c);
    reg [3:0] loopback_reg = 0;
    always @ (posedge mcu_clk100) begin
	loopback_reg <= q000c[4] ? q000c[3:0] : cnt;
    end
 
    /*OSERDESE2 oserdes_loopback_a 
      (.OQ(loopback_a), .CLK(mcu_clk200), .CLKDIV(mcu_clk100),
       .D1(loopbackc[0]), .D2(loopbackc[1]), 
       .D3(loopbackc[2]), .D4(loopbackc[3]),
       .RST(powerup_reset), .OCE(1'b1));

    OSERDESE2 oserdes_loopback_b 
      (.OQ(loopback_b), .CLK(mcu_clk200), .CLKDIV(mcu_clk100),
       .D1(loopbackc[0]), .D2(loopbackc[1]), 
       .D3(loopbackc[2]), .D4(loopbackc[3]),
       .RST(powerup_reset), .OCE(1'b1));*/

    //assign loopback_a = loopbackc[0];
    //assign loopback_b = loopbackc[0];
    OSERDESE2 oserdes_mrb_0c 
      (.OQ(mrb_0c), .CLK(mcu_clk200), .CLKDIV(mcu_clk100),
       .D1(loopback_reg[0]), .D2(loopback_reg[1]), 
       .D3(loopback_reg[2]), .D4(loopback_reg[3]),
       .RST(powerup_reset), .OCE(1'b1));

    OSERDESE2 oserdes_mrb_1c 
      (.OQ(mrb_1c), .CLK(mcu_clk200), .CLKDIV(mcu_clk100),
       .D1(loopback_reg[0]), .D2(loopback_reg[1]), 
       .D3(loopback_reg[2]), .D4(loopback_reg[3]),
       .RST(powerup_reset), .OCE(1'b1));

    OSERDESE2 oserdes_mrb_2c 
      (.OQ(mrb_2c), .CLK(mcu_clk200), .CLKDIV(mcu_clk100),
       .D1(loopback_reg[0]), .D2(loopback_reg[1]), 
       .D3(loopback_reg[2]), .D4(loopback_reg[3]),
       .RST(powerup_reset), .OCE(1'b1));    
    
    OSERDESE2 oserdes_mrb_3c 
      (.OQ(mrb_3c), .CLK(mcu_clk200), .CLKDIV(mcu_clk100),
       .D1(loopback_reg[0]), .D2(loopback_reg[1]), 
       .D3(loopback_reg[2]), .D4(loopback_reg[3]),
       .RST(powerup_reset), .OCE(1'b1));
       
    OSERDESE2 oserdes_mrb_4c 
      (.OQ(mrb_4c), .CLK(mcu_clk200), .CLKDIV(mcu_clk100),
       .D1(loopback_reg[0]), .D2(loopback_reg[1]), 
       .D3(loopback_reg[2]), .D4(loopback_reg[3]),
       .RST(powerup_reset), .OCE(1'b1));
       
    OSERDESE2 oserdes_mrb_5c 
         (.OQ(mrb_5c), .CLK(mcu_clk200), .CLKDIV(mcu_clk100),
          .D1(loopback_reg[0]), .D2(loopback_reg[1]), 
          .D3(loopback_reg[2]), .D4(loopback_reg[3]),
          .RST(powerup_reset), .OCE(1'b1));
              
    OSERDESE2 oserdes_mrb_6c 
         (.OQ(mrb_6c), .CLK(mcu_clk200), .CLKDIV(mcu_clk100),
          .D1(loopback_reg[0]), .D2(loopback_reg[1]), 
          .D3(loopback_reg[2]), .D4(loopback_reg[3]),
          .RST(powerup_reset), .OCE(1'b1));
             
    OSERDESE2 oserdes_mrb_7c 
         (.OQ(mrb_7c), .CLK(mcu_clk200), .CLKDIV(mcu_clk100),
          .D1(loopback_reg[0]), .D2(loopback_reg[1]), 
          .D3(loopback_reg[2]), .D4(loopback_reg[3]),
          .RST(powerup_reset), .OCE(1'b1));
    
                
    // If IDELAYE2 is instantiated in the design, then IDELAYCTRL must
    // be instantiated.  Actually, an IDELAYCTRL calibrates all
    // IDELAYE2 within its clock region.  I'm not sure whether or not
    // I need to instantiate multiple IDELAYCTRL modules if I use
    // IDELAYE2 modules in multiple clock regions.
    IDELAYCTRL idc (.REFCLK(mcu_clk200), .RST(powerup_reset));

    // Make "CE" (to increment the delay value) and "LD" (to reset it
    // to zero) writable via bus, for each IDELAYE2 module.
    reg mrb_0a_ce = 0, mrb_0a_ld = 0;
    reg mrb_0b_ce = 0, mrb_0b_ld = 0;
    reg mrb_1a_ce = 0, mrb_1a_ld = 0;
    reg mrb_1b_ce = 0, mrb_1b_ld = 0;
    reg loopback_c_ce = 0, loopback_c_ld = 0;
    always @ (posedge clk) begin
	mrb_0a_ce <= bwr && bstrobe && (baddr==16'h000e) && bwrdata[0];
	mrb_0a_ld <= bwr && bstrobe && (baddr==16'h000e) && bwrdata[1];
	mrb_0b_ce <= bwr && bstrobe && (baddr==16'h000e) && bwrdata[2];
	mrb_0b_ld <= bwr && bstrobe && (baddr==16'h000e) && bwrdata[3];
	loopback_c_ce <= bwr && bstrobe && (baddr==16'h000e) && bwrdata[4];
	loopback_c_ld <= bwr && bstrobe && (baddr==16'h000e) && bwrdata[5];
	mrb_1a_ce <= bwr && bstrobe && (baddr==16'h000e) && bwrdata[6];
	mrb_1a_ld <= bwr && bstrobe && (baddr==16'h000e) && bwrdata[7];
	mrb_1b_ce <= bwr && bstrobe && (baddr==16'h000e) && bwrdata[8];
	mrb_1b_ld <= bwr && bstrobe && (baddr==16'h000e) && bwrdata[9];
    end

    // mrb_0a_p and _n are the two differential input pins, which are
    // combined by the LVDS receiver into mrb_0a, which is the input
    // to the IDELAYE2 module, whose output is the delayed signal,
    // mrb_0a_dly.  Then mrb_0a_dly is the input for an ISERDESE2
    // module, which does serial-to-parallel conversion, from a
    // 400Mbps bit stream into 4-bit parallel words at 100 MHz.
    wire mrb_0a_dly;
    IDELAYE2 #(.IDELAY_TYPE("VARIABLE"), .IDELAY_VALUE(0))
    idelay_mrb_0a (.C(clk), .IDATAIN(mrb_0a), .DATAOUT(mrb_0a_dly),
		   .CE(mrb_0a_ce), .INC(1'b1), .LD(mrb_0a_ld));

    // Same as above, for mrb_0b.
    wire mrb_0b_dly;
    IDELAYE2 #(.IDELAY_TYPE("VARIABLE"), .IDELAY_VALUE(0))
    idelay_mrb_0b (.C(clk), .IDATAIN(mrb_0b), .DATAOUT(mrb_0b_dly),
		   .CE(mrb_0b_ce), .INC(1'b1), .LD(mrb_0b_ld));

    // Same as above, for mrb_1a.
    wire mrb_1a_dly;
    IDELAYE2 #(.IDELAY_TYPE("VARIABLE"), .IDELAY_VALUE(0))
    idelay_mrb_1a (.C(clk), .IDATAIN(mrb_1a), .DATAOUT(mrb_1a_dly),
		   .CE(mrb_1a_ce), .INC(1'b1), .LD(mrb_1a_ld));

    // Same as above, for mrb_1b.
    wire mrb_1b_dly;
    IDELAYE2 #(.IDELAY_TYPE("VARIABLE"), .IDELAY_VALUE(0))
    idelay_mrb_1b (.C(clk), .IDATAIN(mrb_1b), .DATAOUT(mrb_1b_dly),
		   .CE(mrb_1b_ce), .INC(1'b1), .LD(mrb_1b_ld));
    
    // Same as above, for mrb_2a.
    wire mrb_2a_dly;
    IDELAYE2 #(.IDELAY_TYPE("VARIABLE"), .IDELAY_VALUE(0))
    idelay_mrb_2a (.C(clk), .IDATAIN(mrb_2a), .DATAOUT(mrb_2a_dly),
           .CE(0), .INC(0), .LD(0));    
    
    // Same as above, for mrb_2b.
    wire mrb_2b_dly;
    IDELAYE2 #(.IDELAY_TYPE("VARIABLE"), .IDELAY_VALUE(0))
    idelay_mrb_2b (.C(clk), .IDATAIN(mrb_2b), .DATAOUT(mrb_2b_dly),
           .CE(0), .INC(0), .LD(0));  
                          
       
    // Same as above, for mrb_3a.
    wire mrb_3a_dly;
    IDELAYE2 #(.IDELAY_TYPE("VARIABLE"), .IDELAY_VALUE(0))
    idelay_mrb_3a (.C(clk), .IDATAIN(mrb_3a), .DATAOUT(mrb_3a_dly),
           .CE(0), .INC(0), .LD(0));  
           
    // Same as above, for mrb_3b.
    wire mrb_3b_dly;
    IDELAYE2 #(.IDELAY_TYPE("VARIABLE"), .IDELAY_VALUE(0))
    idelay_mrb_3b (.C(clk), .IDATAIN(mrb_3b), .DATAOUT(mrb_3b_dly),
           .CE(0), .INC(0), .LD(0));  
       
    // Same as above, for mrb_4a.
    wire mrb_4a_dly;
    IDELAYE2 #(.IDELAY_TYPE("VARIABLE"), .IDELAY_VALUE(0))
    idelay_mrb_4a (.C(clk), .IDATAIN(mrb_4a), .DATAOUT(mrb_4a_dly),
           .CE(0), .INC(0), .LD(0));  
           
    // Same as above, for mrb_4b.
    wire mrb_4b_dly;
    IDELAYE2 #(.IDELAY_TYPE("VARIABLE"), .IDELAY_VALUE(0))
    idelay_mrb_4b (.C(clk), .IDATAIN(mrb_4b), .DATAOUT(mrb_4b_dly),
           .CE(0), .INC(0), .LD(0)); 
 
    // Same as above, for mrb_5a.
    wire mrb_5a_dly;
    IDELAYE2 #(.IDELAY_TYPE("VARIABLE"), .IDELAY_VALUE(0))
    idelay_mrb_5a (.C(clk), .IDATAIN(mrb_5a), .DATAOUT(mrb_5a_dly),
           .CE(0), .INC(0), .LD(0));  
           
    // Same as above, for mrb_5b.
    wire mrb_5b_dly;
    IDELAYE2 #(.IDELAY_TYPE("VARIABLE"), .IDELAY_VALUE(0))
    idelay_mrb_5b (.C(clk), .IDATAIN(mrb_5b), .DATAOUT(mrb_5b_dly),
           .CE(0), .INC(0), .LD(0));  
        
    // Same as above, for mrb_6a.
    wire mrb_6a_dly;
    IDELAYE2 #(.IDELAY_TYPE("VARIABLE"), .IDELAY_VALUE(0))
    idelay_mrb_6a (.C(clk), .IDATAIN(mrb_6a), .DATAOUT(mrb_6a_dly),
           .CE(0), .INC(0), .LD(0));  
           
    // Same as above, for mrb_6b.
    wire mrb_6b_dly;
    IDELAYE2 #(.IDELAY_TYPE("VARIABLE"), .IDELAY_VALUE(0))
    idelay_mrb_6b (.C(clk), .IDATAIN(mrb_6b), .DATAOUT(mrb_6b_dly),
           .CE(0), .INC(0), .LD(0)); 
            
    // Same as above, for mrb_7a.
    wire mrb_7a_dly;
    IDELAYE2 #(.IDELAY_TYPE("VARIABLE"), .IDELAY_VALUE(0))
    idelay_mrb_7a (.C(clk), .IDATAIN(mrb_7a), .DATAOUT(mrb_7a_dly),
           .CE(0), .INC(0), .LD(0));  
           
    // Same as above, for mrb_7b.
    wire mrb_7b_dly;
    IDELAYE2 #(.IDELAY_TYPE("VARIABLE"), .IDELAY_VALUE(0))
    idelay_mrb_7b (.C(clk), .IDATAIN(mrb_7b), .DATAOUT(mrb_7b_dly),
           .CE(0), .INC(0), .LD(0));  
    
    
    // Same as above, for loopback_c.
    wire loopback_c_dly;
    IDELAYE2 #(.IDELAY_TYPE("VARIABLE"), .IDELAY_VALUE(0))
    idelay_loopback_c (.C(clk), .IDATAIN(loopback_c), .DATAOUT(loopback_c_dly),
		       .CE(0), .INC(0), .LD(0));
    
    // "mrb_0b_word" holds the latest 4-bit word captured from the
    // deserializer "isrds_mrb0b".  For now I'm using the ILA to watch
    // its contents.  I'll reserve q000d[3:0] as a mechanism for
    // reading back a recent value from mrb_0b_word, e.g. for
    // calibration.  If I write a 1 to q000d[4] (when its previous
    // contents were 0), the result should be that BITSLIP is asserted
    // for one CLKDIV clock cycle, before returning to the quiescent
    // deasserted state.  I am currently allowing for my 100 MHz "bus"
    // clock to be different from "mcu_clk100".  I may decide later to
    // eliminate this complication.  To make the firmware simple for
    // now, I'll complicate the job of the software by requiring the
    // software to set q000d[4] back to 0 with a separate write
    // operation.  This section of code is a kludge and needs to be
    // redone once I've fixed the bus clock issue.  Comment should be
    // updated to reflect the fact that I now use bits 8..9 to select
    // which of several bitslip signals is enabled.
    wire [15:0] q000d;
    breg #(16'h000d) r000d(ibus, obus, q000d);
    reg [1:0] q000d_4_sync = 0;
    reg [1:0] bitslip_state = 0;
    reg       bitslip_now_0a = 0;
    reg       bitslip_now_0b = 0;
    reg       bitslip_now_lbc = 0;
    reg       bitslip_now_1a = 0;
    reg       bitslip_now_1b = 0;
    reg       bitslip_now_2a = 0;
    reg       bitslip_now_2b = 0;
    reg       bitslip_now_3a = 0;
    reg       bitslip_now_3b = 0;
    reg       bitslip_now_4a = 0;
    reg       bitslip_now_4b = 0;
    reg       bitslip_now_5a = 0;
    reg       bitslip_now_5b = 0;
    reg       bitslip_now_6a = 0;
    reg       bitslip_now_6b = 0;
    reg       bitslip_now_7a = 0;
    reg       bitslip_now_7b = 0;
    
    
    // This state machine will be totally unnecessary once I make the
    // "bus" be synchronous with mcu_clk100.
    always @ (posedge mcu_clk100) begin
    	q000d_4_sync[1] <= q000d[4];
    	q000d_4_sync[0] <= q000d_4_sync[1];
    	if (bitslip_state==0) begin
    	    bitslip_state <= (q000d_4_sync[0] ? 1 : 0);
    	end else if (bitslip_state==1) begin
    	    bitslip_state <= 2;
    	end else if (bitslip_state==2) begin
    	    bitslip_state <= (q000d_4_sync[0] ? 2 : 0);
    	end else begin
    	    bitslip_state <= 0;
    	end
	//Available Indexes: !0,!1,!2,!3,!5,!6,7,!13,!14
	bitslip_now_6a  <= bitslip_state==1 && q000d[0];
	bitslip_now_6b  <= bitslip_state==1 && q000d[1];
	bitslip_now_7a  <= bitslip_state==1 && q000d[2];
    bitslip_now_7b  <= bitslip_state==1 && q000d[3];
	bitslip_now_5a  <= bitslip_state==1 && q000d[5];
    bitslip_now_5b  <= bitslip_state==1 && q000d[6];    
	bitslip_now_0a  <= bitslip_state==1 && q000d[8];
	bitslip_now_0b  <= bitslip_state==1 && q000d[9];
	bitslip_now_lbc <= bitslip_state==1 && q000d[10];
	bitslip_now_1a  <= bitslip_state==1 && q000d[11];
	bitslip_now_1b  <= bitslip_state==1 && q000d[12];
	bitslip_now_2a  <= bitslip_state==1 && q000d[13];
	bitslip_now_2b  <= bitslip_state==1 && q000d[14];
    end

    // Input deserializer for mrb_0a
    wire [3:0] mrb_0a_word;
    reg  [3:0] mrb0a = 0;
    always @ (posedge mcu_clk100) mrb0a <= mrb_0a_word;
    ISERDESE2 #(.INTERFACE_TYPE("NETWORKING"), .IOBDELAY("BOTH"))
    isrds_mrb0a (.Q1(mrb_0a_word[3]), .Q2(mrb_0a_word[2]),
    		 .Q3(mrb_0a_word[1]), .Q4(mrb_0a_word[0]),
    		 .DDLY(mrb_0a_dly),
    		 .CLK(mcu_clk200), .CLKB(~mcu_clk200),
    		 .CLKDIV(mcu_clk100),
    		 .BITSLIP(bitslip_now_0a),
    		 .RST(powerup_reset), .CE1(1'b1), .CE2(1'b1));

    // Input deserializer for mrb_0b
    wire [3:0] mrb_0b_word;
    reg  [3:0] mrb0b = 0;
    always @ (posedge mcu_clk100) mrb0b <= mrb_0b_word;
    ISERDESE2 #(.INTERFACE_TYPE("NETWORKING"), .IOBDELAY("BOTH"))
    isrds_mrb0b (.Q1(mrb_0b_word[3]), .Q2(mrb_0b_word[2]),
    		 .Q3(mrb_0b_word[1]), .Q4(mrb_0b_word[0]),
    		 .DDLY(mrb_0b_dly),
    		 .CLK(mcu_clk200), .CLKB(~mcu_clk200),
    		 .CLKDIV(mcu_clk100),
    		 .BITSLIP(bitslip_now_0b),
    		 .RST(powerup_reset), .CE1(1'b1), .CE2(1'b1));

    // Input deserializer for mrb_1a
    wire [3:0] mrb_1a_word;
    reg  [3:0] mrb1a = 0;
    always @ (posedge mcu_clk100) mrb1a <= mrb_1a_word;
    ISERDESE2 #(.INTERFACE_TYPE("NETWORKING"), .IOBDELAY("BOTH"))
    isrds_mrb1a (.Q1(mrb_1a_word[3]), .Q2(mrb_1a_word[2]),
    		 .Q3(mrb_1a_word[1]), .Q4(mrb_1a_word[0]),
    		 .DDLY(mrb_1a_dly),
    		 .CLK(mcu_clk200), .CLKB(~mcu_clk200),
    		 .CLKDIV(mcu_clk100),
    		 .BITSLIP(bitslip_now_1a),
    		 .RST(powerup_reset), .CE1(1'b1), .CE2(1'b1));

    // Input deserializer for mrb_1b
    wire [3:0] mrb_1b_word;
    reg  [3:0] mrb1b = 0;
    always @ (posedge mcu_clk100) mrb1b <= mrb_1b_word;
    ISERDESE2 #(.INTERFACE_TYPE("NETWORKING"), .IOBDELAY("BOTH"))
    isrds_mrb1b (.Q1(mrb_1b_word[3]), .Q2(mrb_1b_word[2]),
    		 .Q3(mrb_1b_word[1]), .Q4(mrb_1b_word[0]),
    		 .DDLY(mrb_1b_dly),
    		 .CLK(mcu_clk200), .CLKB(~mcu_clk200),
    		 .CLKDIV(mcu_clk100),
    		 .BITSLIP(bitslip_now_1b),
    		 .RST(powerup_reset), .CE1(1'b1), .CE2(1'b1));
    
    // Input deserializer for mrb_2a
    wire [3:0] mrb_2a_word;
    reg  [3:0] mrb2a = 0;
    always @ (posedge mcu_clk100) mrb2a <= mrb_2a_word;
    ISERDESE2 #(.INTERFACE_TYPE("NETWORKING"), .IOBDELAY("BOTH"))
    isrds_mrb2a (.Q1(mrb_2a_word[3]), .Q2(mrb_2a_word[2]),
             .Q3(mrb_2a_word[1]), .Q4(mrb_2a_word[0]),
             .DDLY(mrb_2a_dly),
             .CLK(mcu_clk200), .CLKB(~mcu_clk200),
             .CLKDIV(mcu_clk100),
             .BITSLIP(bitslip_now_2a),
             .RST(powerup_reset), .CE1(1'b1), .CE2(1'b1));

    // Input deserializer for mrb_2b
    wire [3:0] mrb_2b_word;
    reg  [3:0] mrb2b = 0;
    always @ (posedge mcu_clk100) mrb2b <= mrb_2b_word;
    ISERDESE2 #(.INTERFACE_TYPE("NETWORKING"), .IOBDELAY("BOTH"))
    isrds_mrb2b (.Q1(mrb_2b_word[3]), .Q2(mrb_2b_word[2]),
    		 .Q3(mrb_2b_word[1]), .Q4(mrb_2b_word[0]),
    		 .DDLY(mrb_2b_dly),
    		 .CLK(mcu_clk200), .CLKB(~mcu_clk200),
    		 .CLKDIV(mcu_clk100),
    		 .BITSLIP(bitslip_now_2b),
    		 .RST(powerup_reset), .CE1(1'b1), .CE2(1'b1));

    // Input deserializer for mrb_3a
    wire [3:0] mrb_3a_word;
    reg  [3:0] mrb3a = 0;
    always @ (posedge mcu_clk100) mrb3a <= mrb_3a_word;
    ISERDESE2 #(.INTERFACE_TYPE("NETWORKING"), .IOBDELAY("BOTH"))
    isrds_mrb3a (.Q1(mrb_3a_word[3]), .Q2(mrb_3a_word[2]),
    		 .Q3(mrb_3a_word[1]), .Q4(mrb_3a_word[0]),
    		 .DDLY(mrb_3a_dly),
    		 .CLK(mcu_clk200), .CLKB(~mcu_clk200),
    		 .CLKDIV(mcu_clk100),
    		 .BITSLIP(bitslip_now_3a),
    		 .RST(powerup_reset), .CE1(1'b1), .CE2(1'b1));

    // Input deserializer for mrb_3b
    wire [3:0] mrb_3b_word;
    reg  [3:0] mrb3b = 0;
    always @ (posedge mcu_clk100) mrb3b <= mrb_3b_word;
    ISERDESE2 #(.INTERFACE_TYPE("NETWORKING"), .IOBDELAY("BOTH"))
    isrds_mrb3b (.Q1(mrb_3b_word[3]), .Q2(mrb_3b_word[2]),
    		 .Q3(mrb_3b_word[1]), .Q4(mrb_3b_word[0]),
    		 .DDLY(mrb_3b_dly),
    		 .CLK(mcu_clk200), .CLKB(~mcu_clk200),
    		 .CLKDIV(mcu_clk100),
    		 .BITSLIP(bitslip_now_3b),
    		 .RST(powerup_reset), .CE1(1'b1), .CE2(1'b1));

    // Input deserializer for mrb_4a
    wire [3:0] mrb_4a_word;
    reg  [3:0] mrb4a = 0;
    always @ (posedge mcu_clk100) mrb4a <= mrb_4a_word;
    ISERDESE2 #(.INTERFACE_TYPE("NETWORKING"), .IOBDELAY("BOTH"))
    isrds_mrb4a (.Q1(mrb_4a_word[3]), .Q2(mrb_4a_word[2]),
    		 .Q3(mrb_4a_word[1]), .Q4(mrb_4a_word[0]),
    		 .DDLY(mrb_4a_dly),
    		 .CLK(mcu_clk200), .CLKB(~mcu_clk200),
    		 .CLKDIV(mcu_clk100),
    		 .BITSLIP(bitslip_now_4a),
    		 .RST(powerup_reset), .CE1(1'b1), .CE2(1'b1));

    // Input deserializer for mrb_4b
    wire [3:0] mrb_4b_word;
    reg  [3:0] mrb4b = 0;
    always @ (posedge mcu_clk100) mrb4b <= mrb_4b_word;
    ISERDESE2 #(.INTERFACE_TYPE("NETWORKING"), .IOBDELAY("BOTH"))
    isrds_mrb4b (.Q1(mrb_4b_word[3]), .Q2(mrb_4b_word[2]),
    		 .Q3(mrb_4b_word[1]), .Q4(mrb_4b_word[0]),
    		 .DDLY(mrb_4b_dly),
    		 .CLK(mcu_clk200), .CLKB(~mcu_clk200),
    		 .CLKDIV(mcu_clk100),
    		 .BITSLIP(bitslip_now_4b),
    		 .RST(powerup_reset), .CE1(1'b1), .CE2(1'b1));

     // Input deserializer for mrb_5a
    wire [3:0] mrb_5a_word;
    reg  [3:0] mrb5a = 0;
    always @ (posedge mcu_clk100) mrb5a <= mrb_5a_word;
    ISERDESE2 #(.INTERFACE_TYPE("NETWORKING"), .IOBDELAY("BOTH"))
    isrds_mrb5a (.Q1(mrb_5a_word[3]), .Q2(mrb_5a_word[2]),
    		 .Q3(mrb_5a_word[1]), .Q4(mrb_5a_word[0]),
    		 .DDLY(mrb_5a_dly),
    		 .CLK(mcu_clk200), .CLKB(~mcu_clk200),
    		 .CLKDIV(mcu_clk100),
    		 .BITSLIP(bitslip_now_5a),
    		 .RST(powerup_reset), .CE1(1'b1), .CE2(1'b1));

    // Input deserializer for mrb_5b
    wire [3:0] mrb_5b_word;
    reg  [3:0] mrb5b = 0;
    always @ (posedge mcu_clk100) mrb5b <= mrb_5b_word;
    ISERDESE2 #(.INTERFACE_TYPE("NETWORKING"), .IOBDELAY("BOTH"))
    isrds_mrb5b (.Q1(mrb_5b_word[3]), .Q2(mrb_5b_word[2]),
    		 .Q3(mrb_5b_word[1]), .Q4(mrb_5b_word[0]),
    		 .DDLY(mrb_5b_dly),
    		 .CLK(mcu_clk200), .CLKB(~mcu_clk200),
    		 .CLKDIV(mcu_clk100),
    		 .BITSLIP(bitslip_now_5b),
    		 .RST(powerup_reset), .CE1(1'b1), .CE2(1'b1));   	

     // Input deserializer for mrb_6a
    wire [3:0] mrb_6a_word;
    reg  [3:0] mrb6a = 0;
    always @ (posedge mcu_clk100) mrb6a <= mrb_6a_word;
    ISERDESE2 #(.INTERFACE_TYPE("NETWORKING"), .IOBDELAY("BOTH"))
    isrds_mrb6a (.Q1(mrb_6a_word[3]), .Q2(mrb_6a_word[2]),
    		 .Q3(mrb_6a_word[1]), .Q4(mrb_6a_word[0]),
    		 .DDLY(mrb_6a_dly),
    		 .CLK(mcu_clk200), .CLKB(~mcu_clk200),
    		 .CLKDIV(mcu_clk100),
    		 .BITSLIP(bitslip_now_6a),
    		 .RST(powerup_reset), .CE1(1'b1), .CE2(1'b1));

    // Input deserializer for mrb_6b
    wire [3:0] mrb_6b_word;
    reg  [3:0] mrb6b = 0;
    always @ (posedge mcu_clk100) mrb6b <= mrb_6b_word;
    ISERDESE2 #(.INTERFACE_TYPE("NETWORKING"), .IOBDELAY("BOTH"))
    isrds_mrb6b (.Q1(mrb_6b_word[3]), .Q2(mrb_6b_word[2]),
    		 .Q3(mrb_6b_word[1]), .Q4(mrb_6b_word[0]),
    		 .DDLY(mrb_6b_dly),
    		 .CLK(mcu_clk200), .CLKB(~mcu_clk200),
    		 .CLKDIV(mcu_clk100),
    		 .BITSLIP(bitslip_now_6b),
    		 .RST(powerup_reset), .CE1(1'b1), .CE2(1'b1)); 

     // Input deserializer for mrb_7a
    wire [3:0] mrb_7a_word;
    reg  [3:0] mrb7a = 0;
    always @ (posedge mcu_clk100) mrb7a <= mrb_7a_word;
    ISERDESE2 #(.INTERFACE_TYPE("NETWORKING"), .IOBDELAY("BOTH"))
    isrds_mrb7a (.Q1(mrb_7a_word[3]), .Q2(mrb_7a_word[2]),
    		 .Q3(mrb_7a_word[1]), .Q4(mrb_7a_word[0]),
    		 .DDLY(mrb_7a_dly),
    		 .CLK(mcu_clk200), .CLKB(~mcu_clk200),
    		 .CLKDIV(mcu_clk100),
    		 .BITSLIP(bitslip_now_7a),
    		 .RST(powerup_reset), .CE1(1'b1), .CE2(1'b1));

    // Input deserializer for mrb_7b
    wire [3:0] mrb_7b_word;
    reg  [3:0] mrb7b = 0;
    always @ (posedge mcu_clk100) mrb7b <= mrb_7b_word;
    ISERDESE2 #(.INTERFACE_TYPE("NETWORKING"), .IOBDELAY("BOTH"))
    isrds_mrb7b (.Q1(mrb_7b_word[3]), .Q2(mrb_7b_word[2]),
    		 .Q3(mrb_7b_word[1]), .Q4(mrb_7b_word[0]),
    		 .DDLY(mrb_7b_dly),
    		 .CLK(mcu_clk200), .CLKB(~mcu_clk200),
    		 .CLKDIV(mcu_clk100),
    		 .BITSLIP(bitslip_now_7b),
    		 .RST(powerup_reset), .CE1(1'b1), .CE2(1'b1)); 

    		 
    // Input deserializer for loopback_c
    wire [3:0] loopback_c_word;
    reg  [3:0] loopbackc = 0;
    always @ (posedge mcu_clk100) loopbackc <= loopback_c_word;
    ISERDESE2 #(.INTERFACE_TYPE("NETWORKING"), .IOBDELAY("BOTH"))
    isrds_loopback_c (.Q1(loopback_c_word[3]), .Q2(loopback_c_word[2]),
    		      .Q3(loopback_c_word[1]), .Q4(loopback_c_word[0]),
    		      .DDLY(loopback_c_dly),
    		      .CLK(mcu_clk200), .CLKB(~mcu_clk200),
    		      .CLKDIV(mcu_clk100),
    		      .BITSLIP(bitslip_now_lbc),
    		      .RST(powerup_reset), .CE1(1'b1), .CE2(1'b1));
    
    //WeiweiEdit
    OSERDESE2 oserdes_loopback_a 
      (.OQ(loopback_a), .CLK(mcu_clk200), .CLKDIV(mcu_clk100),
       .D1(loopbackc[0]), .D2(loopbackc[1]), 
       .D3(loopbackc[2]), .D4(loopbackc[3]),
       .RST(powerup_reset), .OCE(1'b1));

    OSERDESE2 oserdes_loopback_b 
      (.OQ(loopback_b), .CLK(mcu_clk200), .CLKDIV(mcu_clk100),
       .D1(loopbackc[0]), .D2(loopbackc[1]), 
       .D3(loopbackc[2]), .D4(loopbackc[3]),
       .RST(powerup_reset), .OCE(1'b1));
    
    // Count correct and incorrect words received on data link
    reg [47:0] ngood = 0;
    reg [47:0] nbad = 0;
    wire [3:0] goodval = loopback_reg - 1;  // was -7 on baord#2
    always @ (posedge mcu_clk100) begin
	if (q000d[15]) begin
	    ngood <= 0;
	    nbad <= 0;
	end else begin
	    if (//mrb7a==goodval && 
		//mrb7b==goodval &&
		loopbackc==goodval)
	      ngood <= ngood + 1;
	    else
	      nbad <= nbad + 1;
	end
    end
    bror #(16'h0010) r0010(ibus, obus, ngood[15: 0]);
    bror #(16'h0011) r0011(ibus, obus, ngood[31:16]);
    bror #(16'h0012) r0012(ibus, obus, ngood[47:32]);
    bror #(16'h0013) r0013(ibus, obus, nbad [15: 0]);
    bror #(16'h0014) r0014(ibus, obus, nbad [31:16]);
    bror #(16'h0015) r0015(ibus, obus, nbad [47:32]);

    // Integrated Logic Analyzer for initial check-out / debug
    wire [31:0] probe;
    assign probe[31:0] = {mrb6b,mrb6a,loopbackc,loopback_reg,mrb7b,mrb7a};
    ila_0 ila(.clk(mcu_clk100), .probe0(probe[31:0]));
endmodule


// integrated logic analyzer
module ila_0(clk, probe0)
  /* synthesis syn_black_box black_box_pad_pin="clk,probe0[31:0]" */;
    input wire clk;
    input wire [31:0] probe0;
endmodule


module bus_zynq_gpio
  (input  wire        clk,
   input  wire [31:0] r0, r1, r2,
   output wire [31:0] r3, r4, r5, r6, r7,
   output wire [15:0] baddr,
   output wire        bwr,
   output wire        bstrobe,
   output wire [15:0] bwrdata, 
   input  wire [15:0] brddata
   );
    /*
     * Note for future:  See logbook entries for 2015-05-19 and 05-18.  At 
     * some point I want to make the entire "bus" synchronous to 
     * "mcu_clk100" so that the main FPGA logic all runs off of a single 
     * clock.  When I do that, it may be helpful to use a spare AXI register
     * to allow me to debug the presence of mcu_clk100.
     */

    /*
     * Register assignments:
     *   == read/write by PS (read-only by PL) ==
     *   r0: 32-bit data (reserved for future use)
     *   r1: current operation addr (16 bits) + data (16 bits)
     *   r2: strobe (from PS to PL) + opcode for current operation
     *   == read-only by PS (write-only by PL) ==
     *   r3: status register (includes strobe from PL to PS)
     *   r4: data from last operation (16 bits, may expand to 32)
     *   r5: opcode + addr from last operation
     *   r6: number of "bus" writes (16 bits) + reads (16 bits)
     *   r7: constant 0xfab40001 (could be redefined later)
     */
    // baddr, bwr, bwrdata are output ports of this module whose
    // contents come from the corresponding D-type flipflops.  The
    // "_reg" variable is the FF's "Q" output, and the "_next"
    // variable is the FF's "D" input, which I declare as a "reg" so
    // that its value can be set by a combinational always block.
    // I've added a new "bstrobe" signal to the bus, which could be
    // useful for FIFO R/W or for writing to an asynchronous RAM.
    reg [15:0] baddr_reg=0, baddr_next=0;
    reg [15:0] bwrdata_reg=0, bwrdata_next=0;
    reg        bwr_reg=0, bwr_next=0;
    reg        bstrobe_reg=0, bstrobe_next=0;
    assign baddr = baddr_reg;
    assign bwr = bwr_reg;
    assign bstrobe = bstrobe_reg;
    assign bwrdata = bwrdata_reg;
    // nwr and nrd will be DFFEs that count the number of read and
    // write operations to the bus.  Send results to PS on r6.
    reg [15:0] nwr=0, nrd=0;
    assign r6 = {nwr,nrd};
    // r7 reports to PS this identifying fixed value for now.
    assign r7 = 'hfab40001;
    // These bits of r2 are how the PS tells us to "go" to do the next
    // read or write operation.
    wire ps_rdstrobe = r2[0];  // "read strobe" from PS
    wire ps_wrstrobe = r2[1];  // "write strobe" from PS
    // Enumerate the states of the FSM that executes the bus I/O
    localparam 
      FsmStart=0, FsmIdle=1, FsmRead=2, FsmRead1=3,
      FsmWrite=4, FsmWrite1=5, FsmWait=6;
    reg [2:0] fsm=0, fsm_next=0;  // current and next FSM state
    reg       pl_ack=0, pl_ack_next=0;  // "ack" strobe from PL back to PS
    assign r3 = {fsm, 3'b000, pl_ack};
    reg [31:0] r4_reg=0, r4_next=0;
    assign r4 = r4_reg;
    reg [31:0] r5_reg=0, r5_next=0;
    assign r5 = r5_reg;
    always @(posedge clk) begin
	fsm <= fsm_next;
	baddr_reg <= baddr_next;
	bwrdata_reg <= bwrdata_next;
	bwr_reg <= bwr_next;
	bstrobe_reg <= bstrobe_next;
	pl_ack <= pl_ack_next;
	r4_reg <= r4_next;
	r5_reg <= r5_next;
	if (fsm==FsmRead1) nrd <= nrd + 1;
	if (fsm==FsmWrite1) nwr <= nwr + 1;
    end
    always @(*) begin
    // compiler points out that brwrdata_next sho
	// these default to staying in same state
	fsm_next = fsm;
	baddr_next = baddr_reg;
	r4_next = r4_reg;
	r5_next = r5_reg;
	// these default to zero
	bwr_next = 0;
	bstrobe_next = 0;
	pl_ack_next = 0;
	case (fsm)
	    FsmStart: begin
		// Start state: wait for both read and write strobes
		// from PS to be deasserted, then go to Idle state to
		// wait for first bus transaction.
		if (!ps_rdstrobe && !ps_wrstrobe)
		  fsm_next = FsmIdle;
	    end
	    FsmIdle: begin
		// Idle state: When we first arrive here, both read and
		// write strobes from PS should be deasserted.  Wait
		// for one or the other to be asserted, then initiate
		// Read or Write operation, accordingly.
		if (ps_rdstrobe) begin
		    // Before asserting its "read strobe," the PS
		    // should have already put the target bus address
		    // into r1[15:0].  These go out onto my "bus" on
		    // the next clock cycle.
		    fsm_next = FsmRead;
		    baddr_next = r1[15:0];
		end else if (ps_wrstrobe) begin
		    // Before asserting its "write strobe," the PS
		    // should have already put the target bus address
		    // into r1[15:0] and the data to be written into
		    // r1[31:16].  These go out onto my "bus" on the
		    // next clock cycle.
		    fsm_next = FsmWrite;
		    baddr_next = r1[15:0];
		    bwrdata_next = r1[31:16];
		    bwr_next = 1;
		end
	    end
	    FsmWrite: begin
		// On this clock cycle, baddr, bwrdata, and bwr are
		// already out on the bus, but no bstrobe yet.
		fsm_next = FsmWrite1;
		bstrobe_next = 1;
		bwr_next = 1;
	    end
	    FsmWrite1: begin
		// bstrobe is asserted for just this clock cycle.  bwr
		// is asserted for both this and previous cycle.  On
		// next cycle, it will be safe to tell the PS that
		// we're done.
		fsm_next = FsmWait;
		r4_next = bwrdata;
		pl_ack_next = 1;
		r5_next = {16'h0002,baddr};
	    end
	    FsmRead: begin
		// On this clock cycle, baddr is already out on the
		// bus, but no bstrobe yet.
		fsm_next = FsmRead1;
		bstrobe_next = 1;
	    end
	    FsmRead1: begin
		// bstrobe is asserted for just this clock cycle.  On
		// the next cycle, it will be safe to tell the PS that
		// we're done and that it can find our answer on r4.
		fsm_next = FsmWait;
		r4_next = brddata;
		pl_ack_next = 1;
		r5_next = {16'h0001,baddr};
	    end
	    FsmWait: begin
		// On this cycle, pl_ack is asserted, informing the PS
		// that we're done with this operation.  We sit here
		// until the PS drops its read or write strobe, thus
		// acknowledging our being done.  Once that happens,
		// we can drop our pl_ack and go to Idle to wait for
		// the next operation.
		pl_ack_next = 1;
		if (!ps_rdstrobe && !ps_wrstrobe) begin
		    pl_ack_next = 0;
		    fsm_next = FsmIdle;
		end
	    end
	    default: begin
		// We somehow find ourselves in an illegal state: 
		// go back to the start state.
		fsm_next = FsmStart;
	    end
	endcase
    end
endmodule

// a read/write register to live on the "bus"
module breg #( parameter MYADDR=0, W=16, PU=0 )
    (
     input  wire [1+1+16+16-1:0] i,
     output wire [15:0]          o,
     output wire [W-1:0]         q
     );
    wire        clk, wr;
    wire [15:0] addr, wrdata;
    wire [15:0] rddata;
    assign {clk, wr, addr, wrdata} = i;
    assign o = {rddata};
    // boilerplate ends here
    reg [W-1:0] regdat = PU;
    wire addrok = (addr==MYADDR);
    assign rddata = addrok ? regdat : 16'hzzzz;
    always @ (posedge clk)
      if (wr && addrok)
	regdat <= wrdata[W-1:0];
    assign q = regdat;
endmodule // breg

// a read-only register to live on the "bus"
module bror #( parameter MYADDR=0, W=16 )
    (
     input  wire [1+1+16+16-1:0] i,
     output wire [15:0]          o,
     input  wire [W-1:0]         d
     );
    wire 	clk, wr;
    wire [15:0] addr, wrdata;
    wire [15:0] rddata;
    assign {clk, wr, addr, wrdata} = i;
    assign o = {rddata};
    // boilerplate ends here
    wire addrok = (addr==MYADDR);
    assign rddata = addrok ? d : 16'hzzzz;
endmodule // bror

module ilvds 
  (
   output wire o,
   input  wire i, ib
   );
    IBUFDS #(.DIFF_TERM("TRUE"))
    buffer(.O(o), .I(i), .IB(ib));
endmodule

module olvds
  (
   input  wire i,
   output wire o, ob
   );
    OBUFDS buffer(.O(o), .OB(ob), .I(i));
endmodule
