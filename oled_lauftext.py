# Lauftext mit OLED-Display auf ESP32

import machine
import ssd1306
import time

# Pin-Konfiguration für ESP32 und OLED-Display
i2c = machine.I2C(1, scl=machine.Pin(18), sda=machine.Pin(19), freq=400000)  # esp32

oled = ssd1306.SSD1306_I2C(128, 32, i2c)
 
class Ticker():
    def __init__(self):
        self.basis_string = ""
    def clear_buffer():
        self.basis_string = ""
        
    def fifo_buffer(self, txt):
        self.basis_string = self.basis_string + str(txt)

        # Länge auf 10 Zeichen begrenzen, indem am Anfang abgeschnitten wird
        if len(self.basis_string) >= 15:
            self.basis_string = self.basis_string[-15:]
        print(self.basis_string)
        return self.basis_string

        

# Funktion für den Lauftext
def scroll_text(text, delay=0.1):
    for i in range(len(text) * 6 + 128):
        oled.fill(0)
        oled.rotate(0)
        oled.text(text, +i, 20)
        oled.show()
        time.sleep(delay)
        
def print_ticker_oled(txt):
    
        oled.fill(0)  # Lösche den Bildschirm
        oled.rotate(0)
        oled.text(tik.fifo_buffer(txt) ,1,1)
        oled.show()
        time.sleep(0.1)
# Hauptprogramm
if __name__ == "__main__":
    tik = Ticker()
    
    while True:
        oled.fill(0)  # Lösche den Bildschirm
        oled.rotate(0)
        oled.text("Lauftext Demo", 20, 0)
        print_ticker_oled("dl2dbg")
        time.sleep(0.4)
        
        text =" Merry Christmas and a Happy New Year      "
        for t in text:
            print_ticker_oled(t)
        
        time.sleep(2)
            
        
       
    