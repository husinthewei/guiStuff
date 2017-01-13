set_property IOSTANDARD LVCMOS33 [get_ports {test_led[0]}]
set_property PACKAGE_PIN V8 [get_ports {test_led[0]}]

set_property IOSTANDARD LVCMOS33 [get_ports {test_led[1]}]
set_property PACKAGE_PIN T5 [get_ports {test_led[1]}]

set_property IOSTANDARD LVCMOS33 [get_ports {test_led[2]}]
set_property PACKAGE_PIN W8 [get_ports {test_led[2]}]

set_property IOSTANDARD LVCMOS33 [get_ports {test_led[3]}]
set_property PACKAGE_PIN U5 [get_ports {test_led[3]}]

# loopback connector (so that MCU proto pretends to be an MRB)
set_property IOSTANDARD LVDS_25 [get_ports loopback_a_p]
set_property IOSTANDARD LVDS_25 [get_ports loopback_a_n]
set_property PACKAGE_PIN V15 [get_ports loopback_a_p]

set_property IOSTANDARD LVDS_25 [get_ports loopback_b_p]
set_property IOSTANDARD LVDS_25 [get_ports loopback_b_n]
set_property PACKAGE_PIN U15 [get_ports loopback_b_n]

set_property IOSTANDARD LVDS_25 [get_ports loopback_c_p]
set_property DIFF_TERM TRUE [get_ports loopback_c_p]
set_property IOSTANDARD LVDS_25 [get_ports loopback_c_n]
set_property DIFF_TERM TRUE [get_ports loopback_c_n]
set_property PACKAGE_PIN T20 [get_ports loopback_c_p]
set_property PACKAGE_PIN U20 [get_ports loopback_c_n]

set_property IOSTANDARD LVDS_25 [get_ports loopback_clock_p]
set_property DIFF_TERM TRUE [get_ports loopback_clock_p]
set_property IOSTANDARD LVDS_25 [get_ports loopback_clock_n]
set_property DIFF_TERM TRUE [get_ports loopback_clock_n]
set_property PACKAGE_PIN P19 [get_ports loopback_clock_n]

# 100 MHz master clock coming in from SY89828 fanout chip
set_property IOSTANDARD LVDS_25 [get_ports mcu_clock_p]
set_property DIFF_TERM TRUE [get_ports mcu_clock_p]
set_property IOSTANDARD LVDS_25 [get_ports mcu_clock_n]
set_property DIFF_TERM TRUE [get_ports mcu_clock_n]
set_property PACKAGE_PIN U19 [get_ports mcu_clock_n]

# connector to MRB 0
set_property IOSTANDARD LVDS_25 [get_ports mrb_0a_p]
set_property DIFF_TERM TRUE [get_ports mrb_0a_p]
set_property IOSTANDARD LVDS_25 [get_ports mrb_0a_n]
set_property DIFF_TERM TRUE [get_ports mrb_0a_n]
set_property PACKAGE_PIN T11 [get_ports mrb_0a_p]
set_property PACKAGE_PIN T10 [get_ports mrb_0a_n]

set_property IOSTANDARD LVDS_25 [get_ports mrb_0b_p]
set_property DIFF_TERM TRUE [get_ports mrb_0b_p]
set_property IOSTANDARD LVDS_25 [get_ports mrb_0b_n]
set_property DIFF_TERM TRUE [get_ports mrb_0b_n]
set_property PACKAGE_PIN T12 [get_ports mrb_0b_p]
set_property PACKAGE_PIN U12 [get_ports mrb_0b_n]

set_property IOSTANDARD LVDS_25 [get_ports mrb_0c_p]
set_property IOSTANDARD LVDS_25 [get_ports mrb_0c_n]
set_property PACKAGE_PIN U13 [get_ports mrb_0c_p]
set_property PACKAGE_PIN V13 [get_ports mrb_0c_n]

# connector to MRB 1
set_property IOSTANDARD LVDS_25 [get_ports mrb_1a_p]
set_property DIFF_TERM TRUE [get_ports mrb_1a_p]
set_property IOSTANDARD LVDS_25 [get_ports mrb_1a_n]
set_property DIFF_TERM TRUE [get_ports mrb_1a_n]
set_property PACKAGE_PIN V12 [get_ports mrb_1a_p]
set_property PACKAGE_PIN W13 [get_ports mrb_1a_n]

set_property IOSTANDARD LVDS_25 [get_ports mrb_1b_p]
set_property DIFF_TERM TRUE [get_ports mrb_1b_p]
set_property IOSTANDARD LVDS_25 [get_ports mrb_1b_n]
set_property DIFF_TERM TRUE [get_ports mrb_1b_n]
set_property PACKAGE_PIN T14 [get_ports mrb_1b_p]
set_property PACKAGE_PIN T15 [get_ports mrb_1b_n]

set_property IOSTANDARD LVDS_25 [get_ports mrb_1c_p]
set_property IOSTANDARD LVDS_25 [get_ports mrb_1c_n]
set_property PACKAGE_PIN P14 [get_ports mrb_1c_p] 
set_property PACKAGE_PIN R14 [get_ports mrb_1c_n]

# connector to MRB 2
set_property IOSTANDARD LVDS_25 [get_ports mrb_2a_p]
set_property DIFF_TERM TRUE [get_ports mrb_2a_p]
set_property IOSTANDARD LVDS_25 [get_ports mrb_2a_n]
set_property DIFF_TERM TRUE [get_ports mrb_2a_n]
set_property PACKAGE_PIN Y16 [get_ports mrb_2a_p] 
set_property PACKAGE_PIN Y17 [get_ports mrb_2a_n] 

set_property IOSTANDARD LVDS_25 [get_ports mrb_2b_p]
set_property DIFF_TERM TRUE [get_ports mrb_2b_p]
set_property IOSTANDARD LVDS_25 [get_ports mrb_2b_n]
set_property DIFF_TERM TRUE [get_ports mrb_2b_n]
set_property PACKAGE_PIN W14 [get_ports mrb_2b_p] 
set_property PACKAGE_PIN Y14 [get_ports mrb_2b_n] 

set_property IOSTANDARD LVDS_25 [get_ports mrb_2c_p]
set_property IOSTANDARD LVDS_25 [get_ports mrb_2c_n]
set_property PACKAGE_PIN T16 [get_ports mrb_2c_p]
set_property PACKAGE_PIN U17 [get_ports mrb_2c_n] 

# connector to MRB 3
set_property IOSTANDARD LVDS_25 [get_ports mrb_3a_p]
set_property DIFF_TERM TRUE [get_ports mrb_3a_p]
set_property IOSTANDARD LVDS_25 [get_ports mrb_3a_n]
set_property DIFF_TERM TRUE [get_ports mrb_3a_n]
set_property PACKAGE_PIN V20 [get_ports mrb_3a_p] 
set_property PACKAGE_PIN W20 [get_ports mrb_3a_n] 

set_property IOSTANDARD LVDS_25 [get_ports mrb_3b_p]
set_property DIFF_TERM TRUE [get_ports mrb_3b_p]
set_property IOSTANDARD LVDS_25 [get_ports mrb_3b_n]
set_property DIFF_TERM TRUE [get_ports mrb_3b_n]
set_property PACKAGE_PIN Y18 [get_ports mrb_3b_p]
set_property PACKAGE_PIN Y19 [get_ports mrb_3b_n] 

set_property IOSTANDARD LVDS_25 [get_ports mrb_3c_p]
set_property IOSTANDARD LVDS_25 [get_ports mrb_3c_n]
set_property PACKAGE_PIN V16 [get_ports mrb_3c_p] 
set_property PACKAGE_PIN W16 [get_ports mrb_3c_n]

# connector to MRB 4
set_property IOSTANDARD LVDS_25 [get_ports mrb_4a_p]
set_property DIFF_TERM TRUE [get_ports mrb_4a_p]
set_property IOSTANDARD LVDS_25 [get_ports mrb_4a_n]
set_property DIFF_TERM TRUE [get_ports mrb_4a_n]
set_property PACKAGE_PIN R16 [get_ports mrb_4a_p]
set_property PACKAGE_PIN R17 [get_ports mrb_4a_n] 

set_property IOSTANDARD LVDS_25 [get_ports mrb_4b_p]
set_property DIFF_TERM TRUE [get_ports mrb_4b_p]
set_property IOSTANDARD LVDS_25 [get_ports mrb_4b_n]
set_property DIFF_TERM TRUE [get_ports mrb_4b_n]
set_property PACKAGE_PIN T17 [get_ports mrb_4b_p] 
set_property PACKAGE_PIN R18 [get_ports mrb_4b_n] 

set_property IOSTANDARD LVDS_25 [get_ports mrb_4c_p]
set_property IOSTANDARD LVDS_25 [get_ports mrb_4c_n]
set_property PACKAGE_PIN V17 [get_ports mrb_4c_p] 
set_property PACKAGE_PIN V18 [get_ports mrb_4c_n] 

# connector to MRB 5
set_property IOSTANDARD LVDS_25 [get_ports mrb_5a_p]
set_property DIFF_TERM TRUE [get_ports mrb_5a_p]
set_property IOSTANDARD LVDS_25 [get_ports mrb_5a_n]
set_property DIFF_TERM TRUE [get_ports mrb_5a_n]
set_property PACKAGE_PIN W18 [get_ports mrb_5a_p] 
set_property PACKAGE_PIN W19 [get_ports mrb_5a_n]

set_property IOSTANDARD LVDS_25 [get_ports mrb_5b_p]
set_property DIFF_TERM TRUE [get_ports mrb_5b_p]
set_property IOSTANDARD LVDS_25 [get_ports mrb_5b_n]
set_property DIFF_TERM TRUE [get_ports mrb_5b_n]
set_property PACKAGE_PIN N17 [get_ports mrb_5b_p]
set_property PACKAGE_PIN P18 [get_ports mrb_5b_n] 

set_property IOSTANDARD LVDS_25 [get_ports mrb_5c_p]
set_property IOSTANDARD LVDS_25 [get_ports mrb_5c_n]
set_property PACKAGE_PIN P15 [get_ports mrb_5c_p] 
set_property PACKAGE_PIN P16 [get_ports mrb_5c_n]

# connector to MRB 6
set_property IOSTANDARD LVDS_25 [get_ports mrb_6a_p]
set_property DIFF_TERM TRUE [get_ports mrb_6a_p]
set_property IOSTANDARD LVDS_25 [get_ports mrb_6a_n]
set_property DIFF_TERM TRUE [get_ports mrb_6a_n]
set_property PACKAGE_PIN D19 [get_ports mrb_6a_p] 
set_property PACKAGE_PIN D20 [get_ports mrb_6a_n]

set_property IOSTANDARD LVDS_25 [get_ports mrb_6b_p]
set_property DIFF_TERM TRUE [get_ports mrb_6b_p]
set_property IOSTANDARD LVDS_25 [get_ports mrb_6b_n]
set_property DIFF_TERM TRUE [get_ports mrb_6b_n] 
set_property PACKAGE_PIN F16 [get_ports mrb_6b_p]
set_property PACKAGE_PIN F17 [get_ports mrb_6b_n] 

set_property IOSTANDARD LVDS_25 [get_ports mrb_6c_p]
set_property IOSTANDARD LVDS_25 [get_ports mrb_6c_n]
set_property PACKAGE_PIN L16 [get_ports mrb_6c_p] 
set_property PACKAGE_PIN L17 [get_ports mrb_6c_n] 

# connector to MRB 7
set_property IOSTANDARD LVDS_25 [get_ports mrb_7a_p]
set_property DIFF_TERM TRUE [get_ports mrb_7a_p]
set_property PACKAGE_PIN F19 [get_ports mrb_7a_p]
set_property IOSTANDARD LVDS_25 [get_ports mrb_7a_n]
set_property DIFF_TERM TRUE [get_ports mrb_7a_n]
set_property PACKAGE_PIN G17 [get_ports mrb_7a_p] 
set_property PACKAGE_PIN F20 [get_ports mrb_7a_n]

set_property IOSTANDARD LVDS_25 [get_ports mrb_7b_p]
set_property DIFF_TERM TRUE [get_ports mrb_7b_p]
set_property PACKAGE_PIN K14 [get_ports mrb_7b_p]
set_property IOSTANDARD LVDS_25 [get_ports mrb_7b_n]
set_property DIFF_TERM TRUE [get_ports mrb_7b_n]
set_property PACKAGE_PIN H15 [get_ports mrb_7b_p]
set_property PACKAGE_PIN J14 [get_ports mrb_7b_n] 

set_property IOSTANDARD LVDS_25 [get_ports mrb_7c_p]
set_property IOSTANDARD LVDS_25 [get_ports mrb_7c_n]
set_property PACKAGE_PIN M14 [get_ports mrb_7c_p] 
set_property PACKAGE_PIN M15 [get_ports mrb_7c_n]

set_property DONT_TOUCH true [get_cells design_1_i/processing_system7_0/inst]
set_property DONT_TOUCH true [get_cells design_1_i/processing_system7_0]
set_property DONT_TOUCH true [get_cells design_1_i/processing_system7_0_axi_periph/s00_couplers/auto_pc]
set_property DONT_TOUCH true [get_cells design_1_i/processing_system7_0_axi_periph]
set_property DONT_TOUCH true [get_cells design_1_i/rst_processing_system7_0_100M]
set_property DONT_TOUCH true [get_cells design_1_i/wja_bus_lite_0]
set_property DONT_TOUCH true [get_cells design_1_i]


create_clock -period 10.000 -name loopback_clock_p -waveform {0.000 5.000} [get_ports loopback_clock_p]
create_clock -period 10.000 -name mcu_clock_p -waveform {0.000 5.000} [get_ports mcu_clock_p]
