#include "ShiftRegister74HC595.h" // Docs -> https://shiftregister.simsso.de/
// #include "TimerOne.h"

#define SHIFT_REGS 1
#define SHIFT_DATA 0
#define SHIFT_LATCH 1
#define SHIFT_CLOCK 2

#define BTN_ROW_0 14
#define BTN_ROW_1 15
#define BTN_ROW_2 16

ShiftRegister74HC595 sr(SHIFT_REGS, SHIFT_DATA, SHIFT_CLOCK, SHIFT_LATCH);
IntervalTimer btn_timer;

uint8_t col_val[] = { 0xFF };
inline void set_col(byte c) {
    // col_val[0] = 0xFF & _BV(c+5);
    // sr.setAll(col_val);
    sr.setAllLow();
    sr.set(c, HIGH);
}

volatile uint8_t btns[3][3] = {
    {0, 0, 0},
    {0, 0, 0},
    {0, 0, 0}
};

uint8_t btns_copy[3][3] = {
    {0, 0, 0},
    {0, 0, 0},
    {0, 0, 0}
};

volatile byte col = 0;

void check_btns(){
    // set_col(col);
    sr.setAllHigh();
    sr.set(col, LOW);
    btns[0][col] = !digitalRead(BTN_ROW_0);
    btns[1][col] = !digitalRead(BTN_ROW_1);
    btns[2][col] = !digitalRead(BTN_ROW_2);

    col++;
    if(col >= 3){ col = 0; }
}

void setup() {
    Serial.begin(115200);

    while(!Serial){}

    pinMode(BTN_ROW_0, INPUT_PULLUP);
    pinMode(BTN_ROW_1, INPUT_PULLUP);
    pinMode(BTN_ROW_2, INPUT_PULLUP);

    if(!btn_timer.begin(check_btns, 100)) {
        Serial.println("Failed timer init!");
    }
}


void loop() {
    // memcpy(btns_copy, btns, 9);

    Serial.print(btns[0][0]);Serial.print(" ");
    Serial.print(btns[0][1]);Serial.print(" ");
    Serial.print(btns[0][2]);Serial.println(" ");

    Serial.print(btns[1][0]);Serial.print(" ");
    Serial.print(btns[1][1]);Serial.print(" ");
    Serial.print(btns[1][2]);Serial.println(" ");

    Serial.print(btns[2][0]);Serial.print(" ");
    Serial.print(btns[2][1]);Serial.print(" ");
    Serial.print(btns[2][2]);Serial.println("\n\n");

    delay(250);
}