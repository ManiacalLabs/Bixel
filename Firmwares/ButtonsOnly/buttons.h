namespace RETURN_CODES
{
    enum RETURN_CODES
    {
        SUCCESS = 255
        ERROR = 0,
        ERROR_SIZE = 1,
        ERROR_UNSUPPORTED = 2,
        ERROR_PIXEL_COUNT = 3,
        ERROR_BAD_CMD = 4,
    };
}

inline void serve_btns()
{
    static char cmd = 0;
    static uint16_t size = 0;

    if (Serial.available())
    {
        cmd = Serial.read();
        size = 0;
        Serial.readBytes((char*)&size, 2);

        if (cmd == 42) //there's only 1 command, get buttons
        {
            Serial.write(255); //Success
            noInterrupts();
            Serial.write((uint8_t*)btns, 32);
            interrupts();
        }
        else
        {
            Serial.write(4); //Bad Command
        }


        Serial.flush();
    }
}
