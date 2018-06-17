#include "ShiftRegister74HC595.h" // Docs -> https://shiftregister.simsso.de/
// #include "TimerOne.h"

#define SHIFT_REGS 2
#define SHIFT_DATA 0
#define SHIFT_LATCH 1
#define SHIFT_CLOCK 2

#define BTN_ROW_0 14
#define BTN_ROW_1 15
#define BTN_ROW_2 16
#define BTN_ROW_3 17
#define BTN_ROW_4 18
#define BTN_ROW_5 19
#define BTN_ROW_6 20
#define BTN_ROW_7 21
#define BTN_ROW_8 22
#define BTN_ROW_9 23
#define BTN_ROW_10 33
#define BTN_ROW_11 34
#define BTN_ROW_12 35
#define BTN_ROW_13 36
#define BTN_ROW_14 37
#define BTN_ROW_15 38


#define ROW_COUNT 16

ShiftRegister74HC595 sr(SHIFT_REGS, SHIFT_DATA, SHIFT_CLOCK, SHIFT_LATCH);
IntervalTimer btn_timer;

uint8_t col_val[] = { 0xFF };
inline void set_col(byte c) {
    // col_val[0] = 0xFF & _BV(c+5);
    // sr.setAll(col_val);
    sr.setAllLow();
    sr.set(c, HIGH);
}

volatile uint8_t btns[16][16] = {
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
};

uint8_t btns_copy[16][16] = {
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
};

volatile byte col = 0;

unsigned long startTime = 0;
unsigned long endTime = 0;

void check_btns(){
    // set_col(col);
    sr.setAllHigh();
    sr.set(col, LOW);
    
    btns[0][col] = !digitalRead(BTN_ROW_0);
    btns[1][col] = !digitalRead(BTN_ROW_1);
    btns[2][col] = !digitalRead(BTN_ROW_2);
    btns[3][col] = !digitalRead(BTN_ROW_3);
    btns[4][col] = !digitalRead(BTN_ROW_4);
    btns[5][col] = !digitalRead(BTN_ROW_5);
    btns[6][col] = !digitalRead(BTN_ROW_6);
    btns[7][col] = !digitalRead(BTN_ROW_7);
    btns[8][col] = !digitalRead(BTN_ROW_8);
    btns[9][col] = !digitalRead(BTN_ROW_9);
    btns[10][col] = !digitalRead(BTN_ROW_10);
    btns[11][col] = !digitalRead(BTN_ROW_11);
    btns[12][col] = !digitalRead(BTN_ROW_12);
    btns[13][col] = !digitalRead(BTN_ROW_13);
    btns[14][col] = !digitalRead(BTN_ROW_14);
    btns[15][col] = !digitalRead(BTN_ROW_15);  //(╯°□°)╯︵ ┻━┻
  
    col++;
    if(col >= 16){ col = 0;}
    
}

void setup() {
    Serial.begin(115200);

    while(!Serial){}

    pinMode(BTN_ROW_0, INPUT_PULLUP);
    pinMode(BTN_ROW_1, INPUT_PULLUP);
    pinMode(BTN_ROW_2, INPUT_PULLUP);
    pinMode(BTN_ROW_3, INPUT_PULLUP);
    pinMode(BTN_ROW_4, INPUT_PULLUP);
    pinMode(BTN_ROW_5, INPUT_PULLUP);
    pinMode(BTN_ROW_6, INPUT_PULLUP);
    pinMode(BTN_ROW_7, INPUT_PULLUP);
    pinMode(BTN_ROW_8, INPUT_PULLUP);
    pinMode(BTN_ROW_9, INPUT_PULLUP);
    pinMode(BTN_ROW_10, INPUT_PULLUP);
    pinMode(BTN_ROW_11, INPUT_PULLUP);
    pinMode(BTN_ROW_12, INPUT_PULLUP);
    pinMode(BTN_ROW_13, INPUT_PULLUP);
    pinMode(BTN_ROW_14, INPUT_PULLUP);
    pinMode(BTN_ROW_15, INPUT_PULLUP);

    if(!btn_timer.begin(check_btns, 100)) {
        Serial.println("Failed timer init!");
    }
}


void loop() {
    for(int i = 0; i < ROW_COUNT; i++){
      for(int j = 0; j < 16; j++){
        if(btns[i][j] > 0){
          Serial.print("ROW: ");Serial.print(i);
          Serial.print(" COL: ");Serial.println(j);
        }
      }
    }
    delay(250);
}
