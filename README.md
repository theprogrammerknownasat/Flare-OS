# Flare-OS

Flare OS is an open-source OS designed for the Raspberry Pi Pico.

It outputs to a ssd1306 display through pins 4(sda) and 5(scl)

It requires this display and also:

 - A potentiometer on pin 26

 - A pushbutton on pin 10

 - A mini buzer on pan 20

 - And a DHT11 sensor on pin 11
 
 All pin numbers are marked by GP
 
 You will need to install micropython on the Pi pico, and you will also need to get the "micropython-ssd1306" and "micropython-dht12" packages. If you don't have them, you will get an error.
 
 **If the internal LED blinks three times, that means the io modules are not being picked up or you don't have their drivers**
 
 (Update)
 Robotistan PicoBricks seems to have all the modules you need already hooked up to the correct spots.


