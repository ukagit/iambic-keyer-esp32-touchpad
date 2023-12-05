from machine import Pin, Timer, PWM, ADC, I2C
from time import sleep
import utime  # utime is the micropython brother of time

# testprogram für das timing gemessen am oscilloscope
#5.12.23 dl2dbg

pin_led    = Pin(4, mode=Pin.OUT)

class cw_timing(): # cw timing wird als eigene classe verwaltet, kann daher auch ohne IAMBIC class eingesetzt werden
    def __init__(self, wpm=18, weighting= 50, ratio = 3):
        self.wpm_t = wpm # wpmt local
        self.weighting_t = weighting
        self.ratio_t = ratio
        
    # timing
    def dit_time(self): #aktive
        self.PARIS = 50
       # return 60.0 / self.wpm_t / self.PARIS * 1000 /50*(self.weighting_t) ## mili sekunden
        return 60.0 / self.wpm_t / self.PARIS * 1000 /50*(self.weighting_t) ## mili sekunden
    
    def pdit_time(self): #pasive
        self.PARIS = 50
        return 60.0 / self.wpm_t / self.PARIS * 1000  /50*(100-self.weighting_t)## mili sekunden
        
    
    def set_wpm(self, wpm):
        self.wpm_t = wpm
        
    def get_ratio(self): 
        return self.ratio_t
    
    def set_ratio(self, ratio):
        self.ratio_t = ratio
        
    def get_weighting(self): 
        return self.weighting_t
        
    
    def set_weighting(self, weighting):
        self.weighting_t = weighting



 
def cw(state):
    if state:
         pin_led.on()
          
    else:
         pin_led.off()
          
class count_time():
    def __init__(self):
        self.time = 0
    def clear(self):
        self.time = 0
    def add(self, delay):
        self.time = self.time + delay
    def get(self):
        return (self.time)

class count_dit():
    def __init__(self):
        self.count = 0
    def clear(self):
        self.count = 0
    def add(self, anzahl):
        self.count = self.count + anzahl
    def get(self):
        return (self.count)
    
    
    
 
# transmit pattern
def play(pattern):
    for sound in pattern:
        if sound == '.':
            cw(True)
            
            utime.sleep(cw_time.dit_time() / 1000)
            zeit.add(cw_time.dit_time())
            dit.add(1)
            cw(False)
            
            utime.sleep(cw_time.pdit_time() / 1000)
            zeit.add(cw_time.dit_time())
            dit.add(1)
        elif sound == '-':
            cw(True)
           
            utime.sleep(cw_time.get_ratio() * cw_time.dit_time() / 1000) # ration 2.3-3.7
            zeit.add(cw_time.get_ratio() * cw_time.dit_time())
            dit.add(1*cw_time.get_ratio())
            cw(False)
            
            utime.sleep(cw_time.pdit_time() / 1000)
            zeit.add(cw_time.dit_time())
            dit.add(1)
        elif sound == ' ':
           
            utime.sleep(4 * cw_time.pdit_time() / 1000)
            zeit.add(cw_time.dit_time())
            dit.add(4)
    utime.sleep(2 * cw_time.pdit_time() / 1000)
    #zeit.add(2*cw_time.dit_time())



zeit = count_time()
dit = count_dit()

cw_time = cw_timing(wpm=18,weighting=50,ratio=4)
print(f"weighting:{cw_time.get_weighting()} ratio:{cw_time.get_ratio()}       aktive dit_time: {cw_time.dit_time()} ms pause pdit_time: {cw_time.pdit_time()} ms  dat_time: {cw_time.get_ratio() * cw_time.dit_time()} ms")



zeit.clear()
dit.clear()

txt = "...-"
play(txt)
print(txt)

print(zeit.get())
print(dit.get())
