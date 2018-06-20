#include <FastLED.h>

FASTLED_USING_NAMESPACE

// FastLED "100-lines-of-code" demo reel, showing just a few
// of the kinds of animation patterns you can quickly and easily
// compose using FastLED.
//
// This example also shows one easy way to define multiple
// animations patterns and have them automatically rotate.
//
// -Mark Kriegsman, December 2014

#if defined(FASTLED_VERSION) && (FASTLED_VERSION < 3001000)
#warning "Requires FastLED 3.1 or later; check github for latest code."
#endif

#define DATA_PIN    11
#define CLK_PIN   13
#define LED_TYPE    APA102
#define COLOR_ORDER BGR
#define NUM_LEDS    64 * 4
CRGB leds[NUM_LEDS];

#define WIDTH 16
#define HEIGHT 16

#define BRIGHTNESS          32
#define FRAMES_PER_SECOND  120

uint8_t layout[WIDTH][HEIGHT] = {
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

uint8_t XY(uint8_t x, uint8_t y){ return layout[y][x]; }

void setup() {
//   delay(3000); // 3 second delay for recovery

  FastLED.addLeds<LED_TYPE,DATA_PIN,CLK_PIN,COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);

  // set master brightness control
  FastLED.setBrightness(BRIGHTNESS);
}

int i = 0, x = 0, y = 0;
void loop() {
    // fill_solid(leds, NUM_LEDS, CRGB(0,0,0));
    // fill_solid(leds, i+1, CRGB(255,0,0));
    // FastLED.show();
    // FastLED.delay(100);
    // i++;
    // if(i>=NUM_LEDS) { i = 0; }

    fill_solid(leds, NUM_LEDS, CRGB(0,0,0));
    leds[XY(x, y)] = CRGB(255,0,0);
    FastLED.show();
    FastLED.delay(500);
    x++;
    if(x>=WIDTH) { x = 0; }
    y++;
    if(y>=HEIGHT) { y = 0; }
}

// List of patterns to cycle through.  Each is defined as a separate function below.
typedef void (*SimplePatternList[])();
SimplePatternList gPatterns = { rainbow, rainbowWithGlitter, confetti, sinelon, juggle, bpm };

uint8_t gCurrentPatternNumber = 0; // Index number of which pattern is current
uint8_t gHue = 0; // rotating "base color" used by many of the patterns

void loop_old()
{
  // Call the current pattern function once, updating the 'leds' array
  gPatterns[gCurrentPatternNumber]();

  // send the 'leds' array out to the actual LED strip
  FastLED.show();
  // insert a delay to keep the framerate modest
  FastLED.delay(1000/FRAMES_PER_SECOND);

  // do some periodic updates
  EVERY_N_MILLISECONDS( 20 ) { gHue++; } // slowly cycle the "base color" through the rainbow
  EVERY_N_SECONDS( 10 ) { nextPattern(); } // change patterns periodically
}

#define ARRAY_SIZE(A) (sizeof(A) / sizeof((A)[0]))

void nextPattern()
{
  // add one to the current pattern number, and wrap around at the end
  gCurrentPatternNumber = (gCurrentPatternNumber + 1) % ARRAY_SIZE( gPatterns);
}

void rainbow()
{
  // FastLED's built-in rainbow generator
  fill_rainbow( leds, NUM_LEDS, gHue, 7);
}

void rainbowWithGlitter()
{
  // built-in FastLED rainbow, plus some random sparkly glitter
  rainbow();
  addGlitter(80);
}

void addGlitter( fract8 chanceOfGlitter)
{
  if( random8() < chanceOfGlitter) {
    leds[ random16(NUM_LEDS) ] += CRGB::White;
  }
}

void confetti()
{
  // random colored speckles that blink in and fade smoothly
  fadeToBlackBy( leds, NUM_LEDS, 10);
  int pos = random16(NUM_LEDS);
  leds[pos] += CHSV( gHue + random8(64), 200, 255);
}

void sinelon()
{
  // a colored dot sweeping back and forth, with fading trails
  fadeToBlackBy( leds, NUM_LEDS, 20);
  int pos = beatsin16( 13, 0, NUM_LEDS-1 );
  leds[pos] += CHSV( gHue, 255, 192);
}

void bpm()
{
  // colored stripes pulsing at a defined Beats-Per-Minute (BPM)
  uint8_t BeatsPerMinute = 62;
  CRGBPalette16 palette = PartyColors_p;
  uint8_t beat = beatsin8( BeatsPerMinute, 64, 255);
  for( int i = 0; i < NUM_LEDS; i++) { //9948
    leds[i] = ColorFromPalette(palette, gHue+(i*2), beat-gHue+(i*10));
  }
}

void juggle() {
  // eight colored dots, weaving in and out of sync with each other
  fadeToBlackBy( leds, NUM_LEDS, 20);
  byte dothue = 0;
  for( int i = 0; i < 8; i++) {
    leds[beatsin16( i+7, 0, NUM_LEDS-1 )] |= CHSV(dothue, 200, 255);
    dothue += 32;
  }
}
