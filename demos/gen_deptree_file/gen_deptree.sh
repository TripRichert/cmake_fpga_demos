mkdir -p build

ghdl -i hdl/*.vhdl
ghdl -i tb/*.vhdl

topname=DFlipFlop_tb
topfile=hdl/DFlipFlop_tb.vhdl
echo "$topfile <= " $(ghdl --elab-order $topname | tr '\r\n' ' ') > deptree.txt
