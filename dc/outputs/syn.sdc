###################################################################

# Created by write_sdc on Thu Nov 25 01:18:16 2021

###################################################################
set sdc_version 2.0

set_units -time ns -resistance MOhm -capacitance fF -voltage V -current uA
create_clock [get_ports clk_i]  -period 2  -waveform {0 1}
