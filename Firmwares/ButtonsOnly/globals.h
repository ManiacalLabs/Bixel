#ifndef __GLOBALS__
#define __GLOBALS__
// Button Matrix Setup
#define SHIFT_REGS 2
#define SHIFT_DATA 0
#define SHIFT_LATCH 1
#define SHIFT_CLOCK 2

#define BTN_ROW_0 30
#define BTN_ROW_1 15
#define BTN_ROW_2 16
#define BTN_ROW_3 17
#define BTN_ROW_4 18
#define BTN_ROW_5 19
#define BTN_ROW_6 20
#define BTN_ROW_7 21
#define BTN_ROW_8 22
#define BTN_ROW_9 23
#define BTN_ROW_10 24
#define BTN_ROW_11 25
#define BTN_ROW_12 26
#define BTN_ROW_13 27
#define BTN_ROW_14 28
#define BTN_ROW_15 29

#define ROWS 16
#define COLS 16

volatile uint16_t btn_reads[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
volatile uint16_t btns[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

#define read_btn(p) !digitalReadFast(p)
#define btn_val(x, y) (bool)bitRead(btns[x], y)

#endif