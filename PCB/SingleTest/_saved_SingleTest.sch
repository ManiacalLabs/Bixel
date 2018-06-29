EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:switches
LIBS:relays
LIBS:motors
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:bixel
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L bixel_down B1
U 1 1 5B36BF26
P 2600 3400
F 0 "B1" V 2850 3200 60  0000 C CNN
F 1 "bixel_down" V 2350 3200 39  0000 C CNN
F 2 "custom:bixel" H 2600 3400 60  0001 C CNN
F 3 "" H 2600 3400 60  0001 C CNN
	1    2600 3400
	1    0    0    -1  
$EndComp
$Comp
L bixel_up B4
U 1 1 5B36BF6D
P 3500 3400
F 0 "B4" V 3750 3200 60  0000 C CNN
F 1 "bixel_up" V 3250 3250 39  0000 C CNN
F 2 "custom:bixel" H 3500 3400 60  0001 C CNN
F 3 "" H 3500 3400 60  0001 C CNN
	1    3500 3400
	1    0    0    -1  
$EndComp
$Comp
L bixel_down B2
U 1 1 5B36BFAC
P 2600 4450
F 0 "B2" V 2850 4250 60  0000 C CNN
F 1 "bixel_down" V 2350 4250 39  0000 C CNN
F 2 "custom:bixel" H 2600 4450 60  0001 C CNN
F 3 "" H 2600 4450 60  0001 C CNN
	1    2600 4450
	1    0    0    -1  
$EndComp
$Comp
L bixel_up B3
U 1 1 5B36BFD9
P 3500 4450
F 0 "B3" V 3750 4250 60  0000 C CNN
F 1 "bixel_up" V 3250 4300 39  0000 C CNN
F 2 "custom:bixel" H 3500 4450 60  0001 C CNN
F 3 "" H 3500 4450 60  0001 C CNN
	1    3500 4450
	1    0    0    -1  
$EndComp
Wire Wire Line
	2450 3900 2450 3950
Wire Wire Line
	2550 3950 2550 3900
Wire Wire Line
	2650 3900 2650 3950
Wire Wire Line
	2750 3950 2750 3900
Wire Wire Line
	3350 3900 3350 3950
Wire Wire Line
	3450 3950 3450 3900
Wire Wire Line
	3550 3900 3550 3950
Wire Wire Line
	3650 3950 3650 3900
Wire Wire Line
	2750 4950 3350 4950
Wire Wire Line
	2650 4950 2650 5000
Wire Wire Line
	2650 5000 3450 5000
Wire Wire Line
	3450 5000 3450 4950
Wire Wire Line
	2550 4950 2550 5050
Wire Wire Line
	2550 5050 3550 5050
Wire Wire Line
	3550 5050 3550 4950
Wire Wire Line
	2450 4950 2450 5100
Wire Wire Line
	2450 5100 3650 5100
Wire Wire Line
	3650 5100 3650 4950
Wire Wire Line
	3000 3300 3000 4450
Wire Wire Line
	3900 3300 3900 4450
Wire Wire Line
	3100 3400 3100 3750
Wire Wire Line
	3100 3750 2050 3750
Wire Wire Line
	2200 3400 2200 3750
Connection ~ 2200 3750
Wire Wire Line
	3100 4450 3100 4800
Wire Wire Line
	3100 4800 2050 4800
Wire Wire Line
	2200 4450 2200 4800
Connection ~ 2200 4800
NoConn ~ 3350 2900
NoConn ~ 3450 2900
NoConn ~ 3550 2900
NoConn ~ 3650 2900
$Comp
L Conn_01x08 J1
U 1 1 5B36C3AB
P 2350 2500
F 0 "J1" H 2350 2900 50  0000 C CNN
F 1 "Conn_01x08" H 2350 2000 50  0000 C CNN
F 2 "Socket_Strips:Socket_Strip_Straight_1x08_Pitch2.54mm" H 2350 2500 50  0001 C CNN
F 3 "" H 2350 2500 50  0001 C CNN
	1    2350 2500
	0    -1   -1   0   
$EndComp
Text GLabel 2050 3750 0    30   Input ~ 0
ROW_0
Text GLabel 2050 4800 0    30   Input ~ 0
ROW_1
Text GLabel 3000 3300 1    30   Input ~ 0
COL_0
Text GLabel 3900 3300 1    30   Input ~ 0
COL_1
Connection ~ 3000 3400
Connection ~ 3900 3400
Wire Wire Line
	2450 2700 2450 2900
Wire Wire Line
	2550 2900 2550 2700
Wire Wire Line
	2650 2700 2650 2900
Wire Wire Line
	2750 2900 2750 2700
Text GLabel 2050 2700 3    30   Input ~ 0
ROW_0
Text GLabel 2150 2700 3    30   Input ~ 0
ROW_1
Text GLabel 2250 2700 3    30   Input ~ 0
COL_0
Text GLabel 2350 2700 3    30   Input ~ 0
COL_1
$EndSCHEMATC
