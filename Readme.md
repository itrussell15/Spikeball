# Spikeball Rim Hit Detector

## Battery Life

Neopixel LEDs can take up to 60mA per LED. So the battery bank simply needs to be sized based on this. Depending on when you want the LEDs on, the battery could last longer.

Assuming we use 150 LEDs, which is standard for a led strip. That would be 9000mA, therefore if that LEDs are constantly on, then we could run our system for about 1 hour with a 10000mAh battery bank. This life would be significantly increased if the system ran with LEDs off for the majority of the time. It would be nice to be able to cycle through them, but that would all need to be handled in software.
