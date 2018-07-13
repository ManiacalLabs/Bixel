#include "FastLED.h"
#include "ShiftRegister74HC595.h" // Docs -> https://shiftregister.simsso.de/
#include "globals.h"
#include "serial_led.h"

FASTLED_USING_NAMESPACE

// Button Multiplexing
ShiftRegister74HC595 sr(SHIFT_REGS, SHIFT_DATA, SHIFT_CLOCK, SHIFT_LATCH);
IntervalTimer btn_timer;


volatile byte col = 0;

void check_btns(){
    sr.setAllHigh();
    sr.set(15 - col, LOW);

    bitWrite(btn_reads[col], 0, read_btn(BTN_ROW_0));
    bitWrite(btn_reads[col], 1, read_btn(BTN_ROW_1));
    bitWrite(btn_reads[col], 2, read_btn(BTN_ROW_2));
    bitWrite(btn_reads[col], 3, read_btn(BTN_ROW_3));
    bitWrite(btn_reads[col], 4, read_btn(BTN_ROW_4));
    bitWrite(btn_reads[col], 5, read_btn(BTN_ROW_5));
    bitWrite(btn_reads[col], 6, read_btn(BTN_ROW_6));
    bitWrite(btn_reads[col], 7, read_btn(BTN_ROW_7));
    bitWrite(btn_reads[col], 8, read_btn(BTN_ROW_8));
    bitWrite(btn_reads[col], 9, read_btn(BTN_ROW_9));
    bitWrite(btn_reads[col], 10, read_btn(BTN_ROW_10));
    bitWrite(btn_reads[col], 11, read_btn(BTN_ROW_11));
    bitWrite(btn_reads[col], 12, read_btn(BTN_ROW_12));
    bitWrite(btn_reads[col], 13, read_btn(BTN_ROW_13));
    bitWrite(btn_reads[col], 14, read_btn(BTN_ROW_14));
    bitWrite(btn_reads[col], 15, read_btn(BTN_ROW_15));

    col++;
    if(col >= 16){
        col = 0;
        // complete cycle, copy btns
        // memcpy doesn't work on volatile
        static uint8_t i;
        for(i=0; i<16; i++){
            btns[i] = btn_reads[i];
        }
    }

}

inline void setup_btns() {
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

    if(!btn_timer.begin(check_btns, 1000)) {
        // Serial.println("Failed timer init!");
    }
}

void setup() {
    Serial.begin(1000000);

    while(!Serial){}

    setup_leds();
    setup_btns();

    // Serial.println("Init Complete 2");
}

unsigned long m = 0;

void loop() {
    // static uint8_t x, y;
    // noInterrupts();
    // FastLED.clear();
    // for(y = 0; y < ROWS; y++){
    //   for(x = 0; x < COLS; x++){
    //     if(btn_val(x, y)){
    //       leds[XY(x,y)] = CRGB(255,0,0);
    //     //   Serial.print(x);Serial.print(",");Serial.println(y);
    //     }
    //   }
    // }


    // FastLED.show();
    // interrupts();
    // // Serial.println(millis(), DEC);
    // delay(100);

    getData();
}
