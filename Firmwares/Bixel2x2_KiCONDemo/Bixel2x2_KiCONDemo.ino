/*
 * Bixel2x2 Demo: Shortcut Keyboard
 * Author: Dan T.
 * 
 * REQUIRES: FastLED
 * 
 * Emulates keystrokes to perform:
 * WIN+R to Open Run prompt, types "shortcut[0,1,2,3 based on button pushed]", then hits enter
 * 
 * Set up batch files or links to batch files in a folder that actually perform desired
 * actions on the PC
 * Title the batch files "shortcut[0,1,2,3].bat"
 * Make sure the folder with the batch files is in your user PATH!
 * Teensy Keyboard help: https://www.pjrc.com/teensy/td_keyboard.html
 */

#include "FastLED.h"
#include "globals.h"

#define MAX_BRIGHT 31

FASTLED_USING_NAMESPACE

IntervalTimer btn_timer;

// FastLED Stuff
CRGB leds[NUM_LEDS];

volatile byte col = 0;

uint8_t gHue = 0;
uint8_t hHue = 0;

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

uint8_t brightness = MAX_BRIGHT;
inline void setup_leds() {
  FastLED.addLeds<LED_TYPE,DATA_PIN,CLK_PIN,COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);

  // set master brightness control
  FastLED.setBrightness(brightness);
}

void setup() {

    setup_leds();
    setup_btns();

    fill_solid(leds, NUM_LEDS, CRGB(0,0,0));
    //leds[XY(0,0)] = CRGB(155,0,0);
    //leds[XY(0,1)] = CRGB(0,155,0);
    //leds[XY(1,0)] = CRGB(0,0,155);
    //leds[XY(1,1)] = CRGB(155,155,0);
    FastLED.show();
    FastLED.delay(50);
}

void loop() {

    if(btn_val(0,0)){
      /*Keyboard.press(MODIFIERKEY_GUI);
      Keyboard.press(KEY_R);
      Keyboard.release(MODIFIERKEY_GUI);
      Keyboard.release(KEY_R);
      delay(200);
      Keyboard.println("shortcut0");
      delay(500);*/
      fill_solid(leds, NUM_LEDS, CRGB(0,0,0));
      while(btn_val(0,0)){
        leds[XY(0,0)].setHue(hHue);
        hHue=hHue+5;
        FastLED.show();
        FastLED.delay(5);
        if(btn_val(0,1) && btn_val(1,0) && btn_val(1,1)){
          Keyboard.println("======================================");
          Keyboard.println("======================================");
          Keyboard.println("Greetings From Maniacal Labs! :D :D :D");
          Keyboard.println("=========www.ManiacalLabs.com=========");
          Keyboard.println("======================================");
          FastLED.setBrightness(200);
          for(int x=0; x<1000; x++){
            fill_rainbow( leds, NUM_LEDS, gHue, 64);
            gHue++;
            FastLED.show();
            FastLED.delay(3);
          }
          FastLED.setBrightness(brightness);
        }
      }
    }
    if(btn_val(0,1)){
      fill_solid(leds, NUM_LEDS, CRGB(0,0,0));
      /*Keyboard.press(MODIFIERKEY_GUI);
      Keyboard.press(KEY_R);
      Keyboard.release(MODIFIERKEY_GUI);
      Keyboard.release(KEY_R);
      delay(200);
      Keyboard.println("shortcut1");
      delay(500);*/
      while(btn_val(0,1)){
        leds[XY(0,1)].setHue(hHue);
        hHue=hHue+5;
        FastLED.show();
        FastLED.delay(5);
      }
    }
    if(btn_val(1,0)){
      fill_solid(leds, NUM_LEDS, CRGB(0,0,0));
      /*Keyboard.press(MODIFIERKEY_GUI);
      Keyboard.press(KEY_R);
      Keyboard.release(MODIFIERKEY_GUI);
      Keyboard.release(KEY_R);
      delay(200);
      Keyboard.println("shortcut2");
      delay(500);*/
      while(btn_val(1,0)){
        leds[XY(1,0)].setHue(hHue);
        hHue=hHue+5;
        FastLED.show();
        FastLED.delay(5);
      }
    }
    if(btn_val(1,1)){
      fill_solid(leds, NUM_LEDS, CRGB(0,0,0));
      /*Keyboard.press(MODIFIERKEY_GUI);
      Keyboard.press(KEY_R);
      Keyboard.release(MODIFIERKEY_GUI);
      Keyboard.release(KEY_R);
      delay(200);
      Keyboard.println("shortcut3");
      delay(500);*/
      while(btn_val(1,1)){
        leds[XY(1,1)].setHue(hHue);
        hHue=hHue+5;
        FastLED.show();
        FastLED.delay(5);
      }
    }

    fill_rainbow( leds, NUM_LEDS, gHue, 64);
    gHue++;
    FastLED.show();
    FastLED.delay(30);
}
