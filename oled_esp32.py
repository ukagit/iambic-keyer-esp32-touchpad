from machine import Pin, I2C
import ssd1306
import machine
from time import sleep
import writer
import framebuf
import freesans20


#i2c = I2C(-1, scl=Pin(22), sda=Pin(21)) #For ESP32: pin initializing
#i2c = I2C(-1, scl=Pin(5), sda=Pin(4))  #For ESP8266: pin initializing
i2c = machine.I2C(1, scl = machine.Pin(18), sda = machine.Pin(19), freq = 400000)  #esp32

k = i2c.scan()
print("Device Address      : ")
print(k)


oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
oled.rotate(0)       


def show():
        oled.fill(0)
        oled.text("test",5,5)
        font_writer = writer.Writer(oled, freesans20,False)
        font_writer.set_textpos(5,20)
        font_writer.printstring("20")
        oled.show()
        
def show_test():
        
        oled.invert(0)
        oled.text('DL2DBG', 0, 0)
        oled.show()

#show_test()
show()