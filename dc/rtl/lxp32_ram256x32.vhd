---------------------------------------------------------------------
-- Generic dual-port memory
--
-- Part of the LXP32 CPU
--
-- Copyright (c) 2016 by Alex I. Kuznetsov
--
-- Portable description of a dual-port memory block with one write
-- port. Major FPGA synthesis tools can infer on-chip block RAM
-- from this description. Can be replaced with a library component
-- wrapper if needed.
---------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity lxp32_ram256x32 is
	port(
		clk_i: in std_logic;
		
		we_i: in std_logic;
		waddr_i: in std_logic_vector(7 downto 0);
		wdata_i: in std_logic_vector(31 downto 0);
		
		re_i: in std_logic;
		raddr_i: in std_logic_vector(7 downto 0);
		rdata_o: out std_logic_vector(31 downto 0)
	);
end entity;

architecture rtl of lxp32_ram256x32 is

type ram_type is array(255 downto 0) of std_logic_vector(31 downto 0);
signal ram: ram_type:=(others=>(others=>'0')); -- zero-initialize for SRAM-based FPGAs

attribute syn_ramstyle: string;
attribute syn_ramstyle of ram: signal is "no_rw_check";
attribute ram_style: string; -- for Xilinx
attribute ram_style of ram: signal is "block";


signal web1: std_logic; -- 1 : read, 0 : write
signal oeb1: std_logic;
signal web2: std_logic;
signal oeb2: std_logic;
signal csb1_oneblk: std_logic;
signal csb2_oneblk: std_logic;
signal csb1_twoblk: std_logic;
signal csb2_twoblk: std_logic;

signal out_1: std_logic_vector(31 downto 0);
signal out_2: std_logic_vector(31 downto 0);
signal dummy_bus: std_logic_vector(31 downto 0);

signal raddr_i_before: std_logic_vector(7 downto 0);

begin

-- channel 1 for only read
-- channel 2 for only write

web1 <= re_i; -- 1 : read, 0 : write
oeb1 <= '0';
web2 <= not we_i;
oeb2 <= '1';
csb1_oneblk <= ((not re_i) or raddr_i(0));
csb2_oneblk <= ((not we_i) or waddr_i(0));
csb1_twoblk <= not (re_i and raddr_i(0));
csb2_twoblk <= not (we_i and waddr_i(0));

sram_inst1: entity work.lxp32_ram128x32(rtl)
	port map(
		CE1 => clk_i, -- clk
		CE2 => clk_i, -- clk
		WEB1 => web1, -- write enable, active low
		WEB2 => web2, -- write enable, active low
		OEB1=> oeb1, -- output enable, active low
		OEB2=> oeb2, -- output enable, active low
		CSB1=>csb1_oneblk, -- chip select, active low
		CSB2=>csb2_oneblk, -- chip select, active low

		A1=> std_logic_vector(raddr_i(7 downto 1)), -- R/W address
		A2=> std_logic_vector(waddr_i(7 downto 1)), -- R/W address
		I1=>wdata_i, -- input data bus
		I2=>wdata_i, -- input data bus
		O1=>out_1, -- output data bus
		O2=>dummy_bus  -- output data bus
	);

sram_inst2: entity work.lxp32_ram128x32(rtl)
	port map(
		CE1 => clk_i, -- clk
		CE2 => clk_i, -- clk
		WEB1 => web1, -- write enable, active low
		WEB2 => web2, -- write enable, active low
		OEB1=> oeb1, -- output enable, active low
		OEB2=> oeb2, -- output enable, active low
		CSB1=> csb1_twoblk, -- chip select, active low
		CSB2=> csb2_twoblk, -- chip select, active low

		A1=> std_logic_vector(raddr_i(7 downto 1)), -- R/W address
		A2=> std_logic_vector(waddr_i(7 downto 1)), -- R/W address
		I1=>wdata_i, -- input data bus
		I2=>wdata_i, -- input data bus
		O1=>out_2, -- output data bus
		O2=>dummy_bus  -- output data bus
	);

process (clk_i) is
begin
	if (rising_edge(clk_i)) then
		raddr_i_before <= raddr_i;
	end if;
end process;

rdata_o <= out_1 when raddr_i_before(0) = '0' else out_2;

end architecture;
