import machine
from machine import Pin, I2C, ADC, PWM
import ssd1306
import dht
import time


def reads():
    senable = None
    with open('settings.fos', 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith('478325'):
                for i in line:
                    senable = line[6]
        f.seek(0)
    return senable

senable = int(reads())

led = Pin(25, Pin.OUT)
pot = ADC(Pin(26, Pin.IN))
but = Pin(10, Pin.IN, Pin.PULL_DOWN)
sound = PWM(Pin(20))
bot = 0


def clockcyc():
    time.sleep(0.3)


def playtone(frequency):
    try:
        if senable == 1:
            sound.duty_u16(6000)
            sound.freq(frequency)
        elif boot == 1:
            sound.duty_u16(6000)
            sound.freq(frequency)
        else:
            return
    except OSError:
        oserror()


def aerror(attribute):
    print(f"Could not find attribute: {attribute}")

    Pin(25).low()
    clockcyc()
    Pin(25).high()
    time.sleep(0.1)
    Pin(25).low()
    time.sleep(0.1)
    Pin(25).high()
    time.sleep(0.1)
    Pin(25).low()
    time.sleep(0.5)
    machine.soft_reset()


def oserror():
    print("Could not find IO")
    Pin(25).low()
    clockcyc()
    Pin(25).high()
    time.sleep(0.1)
    Pin(25).low()
    time.sleep(0.1)
    Pin(25).high()
    time.sleep(0.1)
    Pin(25).low()
    time.sleep(0.1)
    Pin(25).high()
    time.sleep(0.1)
    Pin(25).low()
    time.sleep(0.5)
    machine.soft_reset()


def booterror():
    print("Could not boot")
    playtone(900)
    Pin(25).low()
    clockcyc()
    Pin(25).high()
    time.sleep(0.1)
    Pin(25).low()
    time.sleep(0.1)
    Pin(25).high()
    time.sleep(0.1)
    Pin(25).low()
    time.sleep(0.1)
    Pin(25).high()
    time.sleep(0.1)
    Pin(25).low()
    time.sleep(0.5)
    machine.soft_reset()


def text(text, x, y):
    program = Program()

    program.oled.text(str(text), x, y)


class Program:
    select = 0
    try:
        HEIGHT, WIDTH = 64, 128

        sda = machine.Pin(4)
        scl = machine.Pin(5)

        button = Pin(10, Pin.IN, Pin.PULL_DOWN)

        i2c = machine.I2C(0, sda=sda, scl=scl, freq=2000000)
        oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

        sensor = dht.DHT11(Pin(11))
        potval = int(int(pot.read_u16()) / 4096)
        butstate = but.value()
        potvalb = potval
    except OSError:
        oserror()

    def __init__(self):
        self.butstate = None
        self.potval = None
        self.potvalb = None

    def run(self):
        while True:
            self.potval = int(int(int(pot.read_u16()) / 4096) / 2)
            self.butstate = but.value()
            Pin(25).low()
            with open('settings.fos', 'r+') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if line.startswith('478325'):
                        lines[i] = "478325" + str(int(senable))
                f.seek(0)
                for line in lines:
                    f.write(line)
            print(senable)
            try:
                self.manager()
            except OSError:
                OSError()
            clockcyc()

    def temp_hum(self):
        try:
            self.oled.fill(0)
            self.sensor.measure()
            temp = self.sensor.temperature()
            hum = self.sensor.humidity()
            temp_f = temp * (9 / 5) + 32.0
            text("Temperature: ", 15, 10)
            text(str(int(temp_f)) + " F", 55, 25)
            text("Humidty: ", 30, 40)
            text(str(int(hum)), 55, 50)
            self.oled.show()
        except AttributeError:
            aerror("Sensor")

    def settings(self):
        self.oled.fill(0)
        text("Beep?", 15, 20)
        self.oled.show()
        if self.potval <= 3:
            text("Yes", 60, 20)
            if self.potval != self.potvalb:
                self.potvalb = self.potval
                playtone(600)
                time.sleep(0.1)
                sound.duty_u16(0)
            self.oled.show()
            global senable
            senable = 1
        else:
            text("No", 60, 20)
            self.oled.show()
            senable = 0

    def ledsettings(self):
        pass

    def motor(self):
        pass

    def relay(self):
        pass

    def led(self):
        pass

    def sound(self):
        pass

    def box(self):
        self.oled.fill(0)

        text('________________', 0, -6)
        text('________________', 0, 56)

        text('|', -3, 0)
        text('|', -3, 8)
        text('|', -3, 16)
        text('|', -3, 24)
        text('|', -3, 32)
        text('|', -3, 40)
        text('|', -3, 48)
        text('|', -3, 56)

        text('|', 123, 0)
        text('|', 123, 8)
        text('|', 123, 16)
        text('|', 123, 24)
        text('|', 123, 32)
        text('|', 123, 40)
        text('|', 123, 48)
        text('|', 123, 56)
        self.oled.show()

    def manager(self):
        try:
            if self.select != 0 and self.butstate == 1:
                self.select = 0
                self.butstate = 0
                self.oled.fill(0)
                self.oled.show()
                playtone(550)
                time.sleep(0.1)
                sound.duty_u16(0)
                time.sleep(0.5)
            if self.select == 0:
                if self.potval == 0:
                    if self.butstate == 1:
                        self.select = 1
                        playtone(600)
                        time.sleep(0.1)
                        sound.duty_u16(0)
                        self.settings()

                    self.box()
                    text("Settings", 15, 26)
                    self.oled.show()
                    if self.potval != self.potvalb:
                        self.potvalb = self.potval
                        playtone(500)
                        time.sleep(0.1)
                        sound.duty_u16(0)

                elif self.potval == 1:
                    if self.butstate == 1:
                        self.select = 2
                        playtone(600)
                        time.sleep(0.1)
                        sound.duty_u16(0)
                        self.temp_hum()

                    self.box()
                    text("Temperature", 15, 10)
                    text("and", 20, 18)
                    text("Humidity", 15, 26)
                    self.oled.show()
                    if self.potval != self.potvalb:
                        self.potvalb = self.potval
                        playtone(500)
                        time.sleep(0.1)
                        sound.duty_u16(0)
                elif self.potval == 2:
                    if self.butstate == 1:
                        self.select = 3
                        playtone(600)
                        time.sleep(0.1)
                        sound.duty_u16(0)
                        self.ledsettings()

                    self.box()
                    text("LED Settings", 10, 26)
                    self.oled.show()
                    if self.potval != self.potvalb:
                        self.potvalb = self.potval
                        playtone(500)
                        time.sleep(0.1)
                        sound.duty_u16(0)

                elif self.potval == 3:
                    if self.butstate == 1:
                        self.select = 4
                        playtone(600)
                        time.sleep(0.1)
                        sound.duty_u16(0)
                        self.motor()

                    self.box()
                    text("Motor", 15, 10)
                    self.oled.show()
                    if self.potval != self.potvalb:
                        self.potvalb = self.potval
                        playtone(500)
                        time.sleep(0.1)
                        sound.duty_u16(0)

                elif self.potval == 4:
                    if self.butstate == 1:
                        self.select = 5
                        playtone(600)
                        time.sleep(0.1)
                        sound.duty_u16(0)
                        self.relay()

                    self.box()
                    text("Relay", 15, 10)
                    self.oled.show()
                    if self.potval != self.potvalb:
                        self.potvalb = self.potval
                        playtone(500)
                        time.sleep(0.1)
                        sound.duty_u16(0)

                elif self.potval == 5:
                    if self.butstate == 1:
                        self.select = 6
                        playtone(600)
                        time.sleep(0.1)
                        sound.duty_u16(0)
                        self.relay()

                    self.box()
                    text("LED", 15, 10)
                    self.oled.show()
                    if self.potval != self.potvalb:
                        self.potvalb = self.potval
                        playtone(500)
                        time.sleep(0.1)
                        sound.duty_u16(0)

                elif self.potval == 6:
                    if self.butstate == 1:
                        self.select = 7
                        playtone(600)
                        time.sleep(0.1)
                        sound.duty_u16(0)
                        self.relay()

                    self.box()
                    text("Sound", 15, 10)
                    self.oled.show()
                    if self.potval != self.potvalb:
                        self.potvalb = self.potval
                        playtone(500)
                        time.sleep(0.1)
                        sound.duty_u16(0)

                else:
                    self.oled.fill(0)
                    text("How did you", 5, 15)
                    text("even get here?", 5, 24)
                    self.oled.show()

            elif self.select == 1:
                self.settings()
            elif self.select == 2:
                self.temp_hum()
            elif self.select == 3:
                self.ledsettings()
            elif self.select == 4:
                self.motor()
            elif self.select == 5:
                self.relay()
            elif self.select == 6:
                self.led()
            elif self.select == 7:
                self.sound()
        except OSError:
            oserror()

    def bootlogo(self):
        self.oled.fill(0)

        # F
        text("__", 10, 10)
        text("|", 10, 18)
        text("__", 10, 20)
        text("|", 10, 24)
        text("|", 10, 28)
        text("|", 10, 30)

        # L
        text("|", 30, 16)
        text("|", 30, 18)
        text("|", 30, 24)
        text("|", 30, 28)
        text("_", 33, 28)

        # A
        text("/", 50, 16)
        text("/", 49, 16)
        text("|", 47, 22)
        text("|", 47, 28)
        text("\\", 54, 16)
        text("\\", 55, 16)
        text("|", 58, 22)
        text("|", 58, 28)
        text("_", 50, 20)
        text("_", 53, 20)

        # R
        text("_", 70, 10)
        text("\\", 75, 16)
        text("\\", 76, 16)
        text("/", 75, 21)
        text("/", 76, 21)
        text("\\", 75, 26)
        text("\\", 76, 26)
        text("\\", 77, 28)
        text("\\", 78, 28)
        text("|", 67, 16)
        text("|", 67, 20)
        text("|", 67, 28)

        # E
        text("|", 86, 17)
        text("__", 89, 11)
        text("|", 86, 24)
        text("_", 89, 19)
        text("|", 86, 28)
        text("__", 89, 28)

        text("OS", 74, 45)
        text("a0.2.1", 0, 56)
        self.oled.show()


if __name__ == "__main__":
    Pin(25).low()
    program = Program()
    boot = 1
    print(f"Boot {boot}")
    try:
        program.bootlogo()
        time.sleep(0.5)
        playtone(900)
        time.sleep(0.1)
        sound.duty_u16(0)
        time.sleep(0.1)
        playtone(900)
        time.sleep(0.1)
        sound.duty_u16(0)
    except OSError:
        oserror()
    time.sleep(1)
    boot = 0
    print(f"Boot {boot}")
    program.run()
