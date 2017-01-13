//Copyright 1986-2015 Xilinx, Inc. All Rights Reserved.
//--------------------------------------------------------------------------------
//Tool Version: Vivado v.2015.1 (lin64) Build 1215546 Mon Apr 27 19:07:21 MDT 2015
//Date        : Tue Jun  2 14:23:14 2015
//Host        : xray.hep.upenn.edu running 64-bit Scientific Linux release 6.6 (Carbon)
//Command     : generate_target design_1_wrapper.bd
//Design      : design_1_wrapper
//Purpose     : IP block netlist
//--------------------------------------------------------------------------------
`timescale 1 ps / 1 ps

module design_1_wrapper
   (DDR_addr,
    DDR_ba,
    DDR_cas_n,
    DDR_ck_n,
    DDR_ck_p,
    DDR_cke,
    DDR_cs_n,
    DDR_dm,
    DDR_dq,
    DDR_dqs_n,
    DDR_dqs_p,
    DDR_odt,
    DDR_ras_n,
    DDR_reset_n,
    DDR_we_n,
    //++wja++
    // FCLK_CLK0,
    //--wja--
    FIXED_IO_ddr_vrn,
    FIXED_IO_ddr_vrp,
    FIXED_IO_mio,
    FIXED_IO_ps_clk,
    FIXED_IO_ps_porb,
    FIXED_IO_ps_srstb,
    //++wja++
    // R3,
    // R4,
    // R5,
    // R6,
    // R7,
    // reg0,
    // reg1,
    // reg2
    loopback_a_p, loopback_a_n,
    loopback_b_p, loopback_b_n,
    loopback_c_p, loopback_c_n,
    loopback_clock_p, loopback_clock_n,
    mcu_clock_p, mcu_clock_n,
    mrb_0a_p, mrb_0a_n,
    mrb_0b_p, mrb_0b_n,
    mrb_0c_p, mrb_0c_n,
    mrb_1a_p, mrb_1a_n,
    mrb_1b_p, mrb_1b_n,
    mrb_1c_p, mrb_1c_n,
    test_led);
    //--wja--
  inout [14:0]DDR_addr;
  inout [2:0]DDR_ba;
  inout DDR_cas_n;
  inout DDR_ck_n;
  inout DDR_ck_p;
  inout DDR_cke;
  inout DDR_cs_n;
  inout [3:0]DDR_dm;
  inout [31:0]DDR_dq;
  inout [3:0]DDR_dqs_n;
  inout [3:0]DDR_dqs_p;
  inout DDR_odt;
  inout DDR_ras_n;
  inout DDR_reset_n;
  inout DDR_we_n;
  //++wja++
  // output FCLK_CLK0;
  //--wja--
  inout FIXED_IO_ddr_vrn;
  inout FIXED_IO_ddr_vrp;
  inout [53:0]FIXED_IO_mio;
  inout FIXED_IO_ps_clk;
  inout FIXED_IO_ps_porb;
  inout FIXED_IO_ps_srstb;
  //++wja++
  // input [31:0]R3;
  // input [31:0]R4;
  // input [31:0]R5;
  // input [31:0]R6;
  // input [31:0]R7;
  // output [31:0]reg0;
  // output [31:0]reg1;
  // output [31:0]reg2;
  output loopback_a_p, loopback_a_n;
  output loopback_b_p, loopback_b_n;
  input  loopback_c_p, loopback_c_n;
  input  loopback_clock_p, loopback_clock_n;
  input  mcu_clock_p, mcu_clock_n;
  input  mrb_0a_p, mrb_0a_n;
  input  mrb_0b_p, mrb_0b_n;
  output mrb_0c_p, mrb_0c_n;
  input  mrb_1a_p, mrb_1a_n;
  input  mrb_1b_p, mrb_1b_n;
  output mrb_1c_p, mrb_1c_n;
  output [3:0] test_led;
  //--wja--

  wire [14:0]DDR_addr;
  wire [2:0]DDR_ba;
  wire DDR_cas_n;
  wire DDR_ck_n;
  wire DDR_ck_p;
  wire DDR_cke;
  wire DDR_cs_n;
  wire [3:0]DDR_dm;
  wire [31:0]DDR_dq;
  wire [3:0]DDR_dqs_n;
  wire [3:0]DDR_dqs_p;
  wire DDR_odt;
  wire DDR_ras_n;
  wire DDR_reset_n;
  wire DDR_we_n;
  wire FCLK_CLK0;
  wire FIXED_IO_ddr_vrn;
  wire FIXED_IO_ddr_vrp;
  wire [53:0]FIXED_IO_mio;
  wire FIXED_IO_ps_clk;
  wire FIXED_IO_ps_porb;
  wire FIXED_IO_ps_srstb;
  wire [31:0]R3;
  wire [31:0]R4;
  wire [31:0]R5;
  wire [31:0]R6;
  wire [31:0]R7;
  wire [31:0]reg0;
  wire [31:0]reg1;
  wire [31:0]reg2;
  //++wja++
  wire loopback_a_p, loopback_a_n;
  wire loopback_b_p, loopback_b_n;
  wire loopback_c_p, loopback_c_n;
  wire loopback_clock_p, loopback_clock_n;
  wire mcu_clock_p, mcu_clock_n;
  wire mrb_0a_p, mrb_0a_n;
  wire mrb_0b_p, mrb_0b_n;
  wire mrb_0c_p, mrb_0c_n;
  wire mrb_1a_p, mrb_1a_n;
  wire mrb_1b_p, mrb_1b_n;
  wire mrb_1c_p, mrb_1c_n;
  wire [3:0] test_led;
  
  myverilog mv
    (.clk(FCLK_CLK0), .led(test_led),
     .loopback_a_p(loopback_a_p), .loopback_a_n(loopback_a_n), 
     .loopback_b_p(loopback_b_p), .loopback_b_n(loopback_b_n), 
     .loopback_c_p(loopback_c_p), .loopback_c_n(loopback_c_n),
     .loopback_clock_p(loopback_clock_p), .loopback_clock_n(loopback_clock_n),
     .mcu_clock_p(mcu_clock_p), .mcu_clock_n(mcu_clock_n),
     .mrb_0a_p(mrb_0a_p), .mrb_0a_n(mrb_0a_n), 
     .mrb_0b_p(mrb_0b_p), .mrb_0b_n(mrb_0b_n), 
     .mrb_0c_p(mrb_0c_p), .mrb_0c_n(mrb_0c_n),
     .mrb_1a_p(mrb_1a_p), .mrb_1a_n(mrb_1a_n), 
     .mrb_1b_p(mrb_1b_p), .mrb_1b_n(mrb_1b_n), 
     .mrb_1c_p(mrb_1c_p), .mrb_1c_n(mrb_1c_n),  
     .r0(reg0), .r1(reg1), .r2(reg2), 
     .r3(R3), .r4(R4), .r5(R5), .r6(R6), .r7(R7));
  //--wja--

  design_1 design_1_i
       (.DDR_addr(DDR_addr),
        .DDR_ba(DDR_ba),
        .DDR_cas_n(DDR_cas_n),
        .DDR_ck_n(DDR_ck_n),
        .DDR_ck_p(DDR_ck_p),
        .DDR_cke(DDR_cke),
        .DDR_cs_n(DDR_cs_n),
        .DDR_dm(DDR_dm),
        .DDR_dq(DDR_dq),
        .DDR_dqs_n(DDR_dqs_n),
        .DDR_dqs_p(DDR_dqs_p),
        .DDR_odt(DDR_odt),
        .DDR_ras_n(DDR_ras_n),
        .DDR_reset_n(DDR_reset_n),
        .DDR_we_n(DDR_we_n),
        .FCLK_CLK0(FCLK_CLK0),
        .FIXED_IO_ddr_vrn(FIXED_IO_ddr_vrn),
        .FIXED_IO_ddr_vrp(FIXED_IO_ddr_vrp),
        .FIXED_IO_mio(FIXED_IO_mio),
        .FIXED_IO_ps_clk(FIXED_IO_ps_clk),
        .FIXED_IO_ps_porb(FIXED_IO_ps_porb),
        .FIXED_IO_ps_srstb(FIXED_IO_ps_srstb),
        .R3(R3),
        .R4(R4),
        .R5(R5),
        .R6(R6),
        .R7(R7),
        .reg0(reg0),
        .reg1(reg1),
        .reg2(reg2));
endmodule
