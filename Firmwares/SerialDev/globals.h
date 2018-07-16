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

// LED Setup
#define DATA_PIN    11
#define CLK_PIN     13
#define LED_TYPE    APA102
#define COLOR_ORDER BGR
#define NUM_LEDS    64 * 4

#define DEFAULT_BRIGHTNESS  32

#define LED_WIDTH   16
#define LED_HEIGHT  16



const uint8_t layout[LED_WIDTH][LED_HEIGHT] = {
    {0, 1, 2, 3, 4, 5, 6, 7, 128, 129, 130, 131, 132, 133, 134, 135},
    {15, 14, 13, 12, 11, 10, 9, 8, 143, 142, 141, 140, 139, 138, 137, 136},
    {16, 17, 18, 19, 20, 21, 22, 23, 144, 145, 146, 147, 148, 149, 150, 151},
    {31, 30, 29, 28, 27, 26, 25, 24, 159, 158, 157, 156, 155, 154, 153, 152},
    {32, 33, 34, 35, 36, 37, 38, 39, 160, 161, 162, 163, 164, 165, 166, 167},
    {47, 46, 45, 44, 43, 42, 41, 40, 175, 174, 173, 172, 171, 170, 169, 168},
    {48, 49, 50, 51, 52, 53, 54, 55, 176, 177, 178, 179, 180, 181, 182, 183},
    {63, 62, 61, 60, 59, 58, 57, 56, 191, 190, 189, 188, 187, 186, 185, 184},
    {64, 65, 66, 67, 68, 69, 70, 71, 192, 193, 194, 195, 196, 197, 198, 199},
    {79, 78, 77, 76, 75, 74, 73, 72, 207, 206, 205, 204, 203, 202, 201, 200},
    {80, 81, 82, 83, 84, 85, 86, 87, 208, 209, 210, 211, 212, 213, 214, 215},
    {95, 94, 93, 92, 91, 90, 89, 88, 223, 222, 221, 220, 219, 218, 217, 216},
    {96, 97, 98, 99, 100, 101, 102, 103, 224, 225, 226, 227, 228, 229, 230, 231},
    {111, 110, 109, 108, 107, 106, 105, 104, 239, 238, 237, 236, 235, 234, 233, 232},
    {112, 113, 114, 115, 116, 117, 118, 119, 240, 241, 242, 243, 244, 245, 246, 247},
    {127, 126, 125, 124, 123, 122, 121, 120, 255, 254, 253, 252, 251, 250, 249, 248}
};

#define XY(x, y) layout[y][x]

#endif