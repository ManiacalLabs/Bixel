#include "ShiftRegister74HC595.h" // Docs -> https://shiftregister.simsso.de/


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

    if(!btn_timer.begin(check_btns, 2000)) {
        // Serial.println("Failed timer init!");
    }
}

void setup() {
    Serial.begin(1000000);

    setup_btns();
}

unsigned long m = 0;

#define CMD_CONNECT 1
#define CMD_BTNS 2 

#define RES_SUCCESS 255 // anything else error

void loop() {
    static char cmd = 0;

    if (Serial.available())
    {
        cmd = Serial.read();

        if (cmd == CMD_CONNECT)
        {
            Serial.write(RES_SUCCESS); //Success
        }
        else if (cmd == CMD_BTNS) //there's only 1 command, get buttons
        {
            Serial.write(RES_SUCCESS); //Success
            noInterrupts();
            Serial.write((uint8_t*)btns, 32);
            interrupts();
        }
        else
        {
            Serial.write(0); // Error, bad command
        }


        Serial.flush();
    }
}
