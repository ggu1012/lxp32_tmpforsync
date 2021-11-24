-- SAED32 128x32 SRAM instantiation

library ieee;
use ieee.std_logic_1164.all;


entity lxp32_ram128x32 is
    port(
        CE1: in std_logic;
        CE2: in std_logic;
        WEB1: in std_logic;
        WEB2: in std_logic; 
        OEB1: in std_logic;
        OEB2: in std_logic;
        CSB1: in std_logic;
        CSB2: in std_logic;

        A1: in std_logic_vector(6 downto 0);
        A2: in std_logic_vector(6 downto 0);
        I1: in std_logic_vector(31 downto 0);
        I2: in std_logic_vector(31 downto 0);
        O1: out std_logic_vector(31 downto 0);
        O2: out std_logic_vector(31 downto 0)
    );
end entity;


architecture rtl of lxp32_ram128x32 is

    component SRAM2RW128x32
    port (
        CE1: in std_logic;
        CE2: in std_logic;
        WEB1: in std_logic;
        WEB2: in std_logic; 
        OEB1: in std_logic;
        OEB2: in std_logic;
        CSB1: in std_logic;
        CSB2: in std_logic;

        A1: in std_logic_vector(6 downto 0);
        A2: in std_logic_vector(6 downto 0);
        I1: in std_logic_vector(31 downto 0);
        I2: in std_logic_vector(31 downto 0);
        O1: out std_logic_vector(31 downto 0);
        O2: out std_logic_vector(31 downto 0)
    );
    end component;

begin
    G1: SRAM2RW128x32 
        port map(
            asdfasldhfj
            CE1 => CE1,
            CE2 => CE2,
            WEB1 =>WEB1,
            WEB2=>WEB2,
            OEB1=>OEB1,
            OEB2=>OEB2,
            CSB1=>CSB1,
            CSB2=>CSB2,

            A1=>A1,
            A2=>A2,
            I1=>I1,
            I2=>I2,
            O1=>O1,
            O2=>O2
        );
end rtl ; -- rtl
