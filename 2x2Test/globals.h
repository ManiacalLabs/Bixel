#define BTN_ROW_0 0
#define BTN_ROW_1 1

#define BTN_COL_0 2
#define BTN_COL_1 3

#define ROWS 2
#define COLS 2

volatile uint16_t btn_reads[] = {0, 0};
volatile uint16_t btns[] = {0, 0};

#define read_btn(p) !digitalReadFast(p)
#define btn_val(x, y) (bool)bitRead(btns[x], y)

// LED Setup
#define DATA_PIN    11
#define CLK_PIN     10
#define LED_TYPE    APA102
#define COLOR_ORDER BGR
#define NUM_LEDS    4

#define BRIGHTNESS  32

#define LED_WIDTH   2
#define LED_HEIGHT  2

uint8_t layout[LED_WIDTH][LED_HEIGHT] = {
    {0, 3},
    {1, 2}
};

#define XY(x, y) layout[y][x]