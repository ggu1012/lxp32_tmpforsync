###################################################################

# Created by write_sdc on Mon Nov 29 19:36:32 2021

###################################################################
set sdc_version 2.0

set_units -time ns -resistance MOhm -capacitance fF -voltage V -current uA
create_clock [get_ports clk_i]  -period 2  -waveform {0 1}
