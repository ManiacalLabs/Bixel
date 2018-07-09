#include <FastLED.h>
#include "globals.h"

FASTLED_USING_NAMESPACE

IntervalTimer btn_timer;

// FastLED Stuff
CRGB leds[NUM_LEDS];

volatile byte col = 0;

void check_btns(){
    if(col == 0) {
      digitalWriteFast(BTN_COL_0, LOW);
      digitalWriteFast(BTN_COL_1, HIGH);
    }
    else {
      digitalWriteFast(BTN_COL_0, HIGH);
      digitalWriteFast(BTN_COL_1, LOW);
    }

    delay(5);
    bitWrite(btn_reads[col], 0, read_btn(BTN_ROW_0));
    bitWrite(btn_reads[col], 1, read_btn(BTN_ROW_1));

    col++;
    if(col >= 2){
        col = 0;
        // complete cycle, copy btns
        // memcpy doesn't work on volatile
        static uint8_t i;
        for(i=0; i<2; i++){
            btns[i] = btn_reads[i];
        }
    }

}

inline void setup_btns() {
    pinMode(BTN_ROW_0, INPUT_PULLUP);
    pinMode(BTN_ROW_1, INPUT_PULLUP);

    pinMode(BTN_COL_0, OUTPUT);
    pinMode(BTN_COL_1, OUTPUT);

    if(!btn_timer.begin(check_btns, 25000)) {
        Serial.println("Failed timer init!");
    }
}

inline void setup_leds() {
  FastLED.addLeds<LED_TYPE,DATA_PIN,CLK_PIN,COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);

  // set master brightness control
  FastLED.setBrightness(BRIGHTNESS);
}

void setup() {
    Serial.begin(115200);

    while(!Serial){}

    setup_leds();
    setup_btns();
}


void loop() {
    static uint8_t x, y;
    fill_solid(leds, NUM_LEDS, CRGB(0,0,0));
    for(y = 0; y < ROWS; y++){
      for(x = 0; x < COLS; x++){
        if(btn_val(x, y)){
          leds[XY(x,y)] = CRGB(255,0,0);
          Serial.print(x);Serial.print(",");Serial.println(y);
        }
      }
    }

    FastLED.show();
    FastLED.delay(50);
    // delay(50);
}
