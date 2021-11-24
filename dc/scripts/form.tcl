set_host_options -max_cores 16 


set top_module "lxp32c_top"

set search_path [list .]
 

# 라이브러리 아래경로 맞게 설정

set project_dir [ sh pwd ] 
set rtl_dir $project_dir/rtl

define_design_lib work -path work

# 해당되는 verilog file 추가
set SOURCE_FILES [ glob -directory $rtl_dir *.vhd ]
set sram $rtl_dir/saed32sram.v

# read verilog files and synthesis
analyze -f verilog $sram -lib work
analyze -format vhdl $SOURCE_FILES -library work

# top module name을 elaborate 뒤에 작성
elaborate $top_module

set reports_dir $project_dir/reports
set final_reports_dir $project_dir/final_reports
set design_dir $project_dir/designs
set outputs_dir $project_dir/outputs

if { ! [ file exists $reports_dir ] } { 
    file mkdir $reports_dir
}
if { ! [ file exists $final_reports_dir ] } { 
    file mkdir $final_reports_dir
}
if { ! [ file exists $design_dir] } { 
    file mkdir $design_dir
}

if { ! [ file exists $outputs_dir] } {
    file mkdir $outputs_dir
}


create_clock clk_i -period 2

# compile
compile_ultra



# design and synthetic file
report_design > $design_dir/design
report_synthetic > $design_dir/synthetic


# timing, area and power reports
report_timing > $final_reports_dir/timing.txt
sh cat $final_reports_dir/timing.txt

# 아래로, 어떤 module을 분석할 것인지 개별 설정 가능
# set current_design PE.v

report_area > $final_reports_dir/area.txt
sh cat $final_reports_dir/area.txt

report_power > $final_reports_dir/power.txt
sh cat $final_reports_dir/power.txt

# netlist
# write_file -f verilog -hier -output $outputs_dir/syn.v
# write_file -f ddc -hier -output $outputs_dir/syn.ddc

# sdf, sdc
write_sdf -version 1.0 $outputs_dir/syn.sdf
write_sdc $outputs_dir/syn.sdc 

# flattened netlist
ungroup -all -flatten
write_file -f verilog -hier -output $outputs_dir/flat_syn.v
write_file -f ddc -hier -output $outputs_dir/flat_syn.ddc






