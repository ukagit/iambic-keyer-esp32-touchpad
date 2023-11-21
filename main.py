# bluetooth module gelöscht
# esp32 Version 24.12.2022 save data in filesystem
# esp32 Version  25.07.2022 poti wpm
# esp32 Version  22.07.2022
# esp32 Version  11.07.2022
# esp32 version  2.4.2023 text2cw break eingebaut
#
# 
#
# Copyright (C) 2022 dl2dbg
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.



from machine import Pin, Timer, PWM, ADC, I2C
import ssd1306
import writer
#import framebuf
#import freesans20

import machine

from machine import TouchPad
#from machine import deepsleep
from time import sleep
import esp32



 
import utime # utime is the micropython brother of time
import time
import ujson


class OLED_Print():
    def print_smal(self,data,inv):
        print(data)
        oled.fill(0)
        oled.invert(inv)
        oled.text(data, 0, 0)
        oled.show()
        
    def print_big(self,data,inv):
        oled.fill(0)
        #oled.text("test",5,5)
        font_writer = writer.Writer(oled, freesans20,False)
        font_writer.set_textpos(5,20)
        font_writer.printstring(data)
        oled.show()
    
oe = OLED_Print()


    

#xiaoKey - a computer connected iambic keyer
# Copyright 2022 Mark Woodworth (AC9YW)
#https://github.com/MarkWoodworth/xiaokey/blob/master/code/code.py
          
# setup encode and decode
encodings = {}
def encode(char):
    global encodings
    if char in encodings:
        return encodings[char]
    elif char.lower() in encodings:
        return encodings[char.lower()]
    else:
        return ''
    
decodings = {}
def decode(char):
    global decodings
    if char in decodings:
        return decodings[char]
    else:
        return '('+char+'?)'

def MAP(pattern,letter):
    decodings[pattern] = letter
    encodings[letter ] = pattern
    
MAP('.-'   ,'a') ; MAP('-...' ,'b') ; MAP('-.-.' ,'c') ; MAP('-..'  ,'d') ; MAP('.'    ,'e')
MAP('..-.' ,'f') ; MAP('--.'  ,'g') ; MAP('....' ,'h') ; MAP('..'   ,'i') ; MAP('.---' ,'j')
MAP('-.-'  ,'k') ; MAP('.-..' ,'l') ; MAP('--'   ,'m') ; MAP('-.'   ,'n') ; MAP('---'  ,'o')
MAP('.--.' ,'p') ; MAP('--.-' ,'q') ; MAP('.-.'  ,'r') ; MAP('...'  ,'s') ; MAP('-'    ,'t')
MAP('..-'  ,'u') ; MAP('...-' ,'v') ; MAP('.--'  ,'w') ; MAP('-..-' ,'x') ; MAP('-.--' ,'y')
MAP('--..' ,'z')
              
MAP('.----','1') ; MAP('..---','2') ; MAP('...--','3') ; MAP('....-','4') ; MAP('.....','5')
MAP('-....','6') ; MAP('--...','7') ; MAP('---..','8') ; MAP('----.','9') ; MAP('-----','0')

MAP('.-.-.-','.') # period
MAP('--..--',',') # comma
MAP('..--..','?') # question mark
MAP('-...-', '=') # equals, also /BT separator
MAP('-....-','-') # hyphen
MAP('-..-.', '/') # forward slash
MAP('.--.-.','@') # at sign




class watch_ideal():
    '''
    20.11.2022 watch ideal time
    '''

    def __init__(self):
        self.ideal_start = time.time()
        

    def update(self):
        self.ideal_start = time.time()
        
    def diff(self):
        return (time.time() - self.ideal_start)

        
class tx_opt():
    
    '''
    3.3.2022
    simple pin on/off for tx optocopler
    # 
    '''

   
    def __init__(self,tx_pin):
        self.tx_opt_pin = Pin(tx_pin,Pin.OUT)
        self.on_off = 1
        
        
        
    def on(self):
        self.on_off = 1
    def off(self):
        self.on_off = 0
        
    def send(self,state):
        if self.on_off == 1:
            self.tx_opt_pin.value(state)
        
    
    

class command_button():
    '''
    6.3.2022 button for Command request
    7.8.2022 touch key
    '''

    def __init__(self, tcommand,twpm,led1,led2):
         
        self.led1   =  Pin(led1, Pin.OUT)
        self.led2   =  Pin(led2, Pin.OUT)
        
        self.button_save = 0
        self.button_save_wpm = 1
        self.btimer = 0 # timer for debounce
        self.comannd_state = 1 # im keyer mode
        self.comannd_state_wpm = 0 # im keyer mode
        self.comannd_state_wpm_cq = 0 # im keyer mode
        
        
        
        self.touchcommand=TouchPad(Pin(tcommand))
        self.touchwpm=TouchPad(Pin(twpm))
#         
#         self.save_tfreq =  cwt.tonfreq()
#         self.ton_freq_command = cwt.tonfreq_command()
        
    def state_key_command(self):
        #print("..",self.touchcommand.read())
        #print("..",self.touchwpm.read())
        #sleep(0.5)
        try:
            self.touch_val = self.touchcommand.read()
        # ggf. Fehler abfangen
        except ValueError:
            #print("..",self.touchcommand.read())
            return(1)
            #print("ValueError while reading touch_pin")
            #print(self.touch_val)
        
        if (self.touch_val <= 200):
            #print("..",self.touchcommand.read())
            return(0)
        return(1)
       #return(self.dit_key.value())
    
    def state_key_wpm(self):
        #print("..",self.touchwpm.read())
        #sleep(0.5)
        try:
            self.touch_val1 = self.touchwpm.read()
        # ggf. Fehler abfangen
        except ValueError:
            #print("..",self.touchcommand.read())
            return(1)
            #print("ValueError while reading touch_pin")
            #print(self.touch_val)
        
        if (self.touch_val1 <= 200):
            #print("..",self.touchcommand.read())
            return(0)
        return(1)
       #return(self.dit_key.value())
    
        
    def button_press(self):
        #print("command key: ",self.state_key_command())
        return(self.state_key_command())
    
    def button_command_off(self):
         
        print("command off")
        self.comannd_state =  0
        self.led1(self.comannd_state)
        self.led2(self.comannd_state)
        oe.print_smal("command:off",self.comannd_state)
        iambic.write_jsondata() # save parameter afer change
        iambic.char = ""
        iambic.word = ""
        #text2cw("e")
             
        
    def button_state(self):
        
        if self.state_key_command() == 0 and self.button_save == 1: # 1 0 ->button is press
            #utime.ticks_ms()
            #self.btimer  = utime.ticks_ms()
            self.button_save = 0
            
        elif self.state_key_command() == 1 and self.button_save == 0 : #0 0 ->button IS press
            #elif self.state_key_command() == 1 and self.button_save == 0 and utime.ticks_ms() > self.btimer + 10 : #0 0 ->button IS press
             self.button_save = 1
             
             self.led1(not self.comannd_state)
             
             self.comannd_state =  not self.comannd_state
             oe.print_smal("Command:"+str(self.comannd_state),self.comannd_state)
             
             if not self.comannd_state:
                 self.button_command_off()
                 self.comannd_state_wpm =  0
             
                 
                
             
             if self.comannd_state:
                     # in command mode immer ton on 
                     cwt.set2cton()
                     cwt.onoff(True)
             else :
                     cwt.set2ton()
                     cwt.onoff(iambic.sidetone_enable)
                     
            
             #text2cw("e") #keine Peep am ende :-)
             
        return(self.button_save)
            
    
    def button_state_wpm(self):
        
            
        if self.state_key_wpm() == 0 and self.button_save_wpm == 1: # 1 0 ->button is press
            #utime.ticks_ms()
            #self.btimer  = utime.ticks_ms()
            self.button_save_wpm = 0
            print("WPM press 0")
            
        elif self.state_key_wpm() == 1 and self.button_save_wpm == 0 : #0 0 ->button IS press
            
             self.button_save_wpm = 1
             print("WPM press 1")
             self.comannd_state_wpm_cq  = not self.comannd_state_wpm_cq  # toggle zwischen wpm and cq call
             
             print("WPM_CW",self.comannd_state_wpm_cq)
             
             self.led2(not self.comannd_state)
             
             #self.comannd_state_wpm =  not self.comannd_state_wpm
             self.comannd_state_wpm =  1 
             #self.comannd_state =  1
            
             if self.comannd_state_wpm_cq :
                 
                 cw_time.set_wpm(iambic.wpm)
                 oe.print_smal("Command_mode_wpm:"+str(self.comannd_state_wpm),1)
                 oe.print_big("WPM:  "+str(iambic.wpm),1)
                 cb.comannd_state = 1
                 
             else:
                 
                 oe.print_big("cq",1)
                          
             
        return(self.button_save_wpm)
            
        
class watch_ideal():
    '''
    20.11.2022 watch ideal time
    # clear display when ideal 
    '''

    def __init__(self):
        
        self.ideal_start = time.time()
     

    def update(self):
        self.ideal_start = time.time()
        
    def diff(self):
        return  time.time() - self.ideal_start
        
        
    
        
class cw_sound():
    '''
    6.3.2020 simple sound with pwm 
    '''

    def __init__(self,pin=22):
        #GPIO welcher als PWM Pin benutzt werden soll
        self.pwm_ton = PWM(Pin(pin))
        #eine Frequenz von 1000hz also 1kHz
        self.freq = 600
        self.Ton_freq_command = 1500
        self.pwm_ton.freq(self.freq)
        self.cwvolum = 300  #30000 laut
        self.on_off = 1
     

    def set_tonfreq(self,freq):
        self.freq = freq
        self.pwm_ton.freq(self.freq)##
        
    def set2ton(self):
        self.pwm_ton.freq(self.freq)
        
    def set2cton(self):
        self.pwm_ton.freq(self.Ton_freq_command)
        
    def tonfreq(self):
        return self.freq
    
    def tonfreq_command(self):
        return self.Ton_freq_command
       
        
    def volume(self,volume):
        print("set volume")
        self.cwvolum = volume
        

    def tone(self,on):
        if self.on_off == 1:
            if on:
                self.pwm_ton.duty_u16(self.cwvolum)
            else:
                self.pwm_ton.duty_u16(1)
                
    def onoff(self,state):
        self.on_off = state
    

def cw(state):
    cwt.tone(state)
  
    txopt.send(state)
    
    
class cw_timing():
    def __init__(self,wpm=18):
        self.wpm = wpm
    # timing
    def dit_time(self):
        self.PARIS = 50 
        return 60.0 / self.wpm / self.PARIS *1000  ## mili sekunden
    
    def set_wpm(self, wpm):
        self.wpm = wpm
       



# decode iambic b paddles
class Iambic:
    """
Command
a -> Iambic Mode A
b -> Iambic Mode B
m -> request Iambic Mode A/B

? -> request value of ...
/ -> schow value all

i -> TX_opt enable(on) disable(off)

o -> Sidetone toggle (on) (off)

f -> adjust sidetone frequenz
v -> adjust sidetone volume 1-100

w -> adjust WPM (Word per minute)

t -> tune mode, end with command mode
s -> save parameter to  file

x -> exit Command mode




"""
    
    def __init__(self,tdit,tdah):
         
        
       # self.touchdit=TouchPad(Pin(32)) 
       # self.touchdah=TouchPad(Pin(33))
        
        self.touchdit=TouchPad(Pin(tdit)) 
        self.touchdah=TouchPad(Pin(tdah))
        
      
        self.dit = False ; self.dah = False
        self.ktimer = 0
        self.ktimer_end = 0
        
        self.in_char = True 
        self.in_word = True
        
        self.char = ""
        self.word = ""

    
        
        self.IDLE=0; self.CHK_DIT=1; self.CHK_DAH=2; self.KEYED_PREP=3; self.KEYED=4; self.INTER_ELEMENT=5 
        self.keyerState = self.IDLE
        self.keyerControl = 0 #keyerControl = IAMBICB;      // Or 0 for IAMBICA
        
        #  keyerControl bit definitions
        self.DIT_L     = 0x01     # Dit latch
        self.DAH_L     = 0x02     #Dah latch
        self.DIT_PROC  = 0x04     # Dit is being processed
        self.PDLSWAP   = 0x08     # 0 for normal, 1 for swap
        #self.iambic_mode  = 0x10     # 0 for Iambic A, 1 for Iambic B
        self.LOW = 0
        self.HIGH = 1
        
        self.tune = 0 # transmit
        self.transmit_tune= 0
        
        self.adj_sidetone = 0
        self.adj_wpm = 0
       
        self.adj_sidetone_volume = 0
        
# this variable are default an will be overwrite with the json file
#
        self.iambic_mode  = 0x10     # 0 for Iambic A, 1 for Iambic B
        self.wpm = 18
        self.wpm_m = 0
        self.cq = 0
        self.cq_liste =["","cq cq de dl2dbg dl2dbg bk","dl2dbg","cq cq test dl2dbg","cq","uli","cq cq"]
        
        self.tx_enable = 0
        self.txt_enable = 0
        self.sidetone_enable = 1
        self.sidetone_freq = 700 #
        self.sidetone_volume = 10 # range 1,100 * 200 -> 2000 #30000 laut
#        
        
        
        
        
        
        self.request = 0 # request of parameters 
        
#--------------
        
        self.iambic_data = {} # create date store
        self.read_jsondata()
        print("....read button....... from json-file")
        
        self.wpm = self.iambic_data["wpm"]
        cw_time.set_wpm(self.wpm)
        
        
        if cb.button_press() == 0: # not press "0" -> json date read,and init, if "0" use factory setting 
            print("**** default data")
            #self.read_jsondata()
            self.init_iambic_data()  

    def set_data(self,key,value):
        #self.iambic_data
        self.key=key
        self.value= value
        self.iambic_data[self.key]=self.value
    #    print ('setting',menu_data)


    def write_data2file(self):
        #self.iambic_data
        self.json_string = ujson.dumps(self.iambic_data)

       
        with open('json_iambic.json', 'w') as outfile:
            ujson.dump(self.json_string, outfile)
            
    def read_jsondata(self):
        with open('json_iambic.json') as json_file:
            self.data = ujson.load(json_file)

        self.iambic_data = ujson.loads(self.data)
        
        
    def write_jsondata(self): # write new json file
        print("write_jsondata")
        self.set_data("iambic_mode",self.iambic_mode) # transmit
        self.set_data("wpm",self.wpm)
        
        self.set_data("sidetone_enable",self.sidetone_enable)
        self.set_data("sidetone_freq",self.sidetone_freq)
        self.set_data("sidetone_volume",self.sidetone_volume)
          
        self.set_data("tx_enamble",self.tx_enable)
        self.set_data("txt_emable",self.txt_enable)
     
        self.write_data2file()
        
    def print_parameter(self): # write new json file
        #print("write_jsondata")
        
        oe.print_smal("---Paramter",0)
        oe.print_smal("iambic_mode     :" + str(self.iambic_mode),0) # transmit
        oe.print_smal("wpm             :" +str(self.wpm),0)
        
        oe.print_smal("sidetone_enable :" + str(self.sidetone_enable),0)
        oe.print_smal("sidetone_freq   :" +str(self.sidetone_freq),0)
        oe.print_smal("sidetone_volume :" +str(self.sidetone_volume),0)
          
        oe.print_smal("tx_enamble      :" +str(self.tx_enable),0)
        oe.print_smal("txt_emable      :" +str(self.txt_enable),0)
        oe.print_smal("",0)
     
        
        
    
    def init_iambic_data(self): # is only use at the begin to create new json file
        
        self.iambic_mode = self.iambic_data["iambic_mode"]
        self.wpm = self.iambic_data["wpm"]
       
        
        self.sidetone_enable = self.iambic_data["sidetone_enable"]
        self.sidetone_freq    = self.iambic_data["sidetone_freq"]
        self.sidetone_volume  = self.iambic_data["sidetone_volume"]
        
        self.tx_enamble = self.iambic_data["tx_enamble"]
        self.txt_emable = self.iambic_data["txt_emable"]
        
        # set extern Parameter
        cw_time.set_wpm(self.wpm)
        cwt.set_tonfreq(self.sidetone_freq)
        cwt.volume(self.sidetone_volume*200)
        
        
        cwt.onoff(self.sidetone_enable)
        
        
#---------------
    def state_key_dit(self):
       
        try:
            self.touch_val = self.touchdit.read()
        # ggf. Fehler abfangen
        except ValueError:
            return(self.HIGH)
            #print("ValueError while reading touch_pin")
            #print(self.touch_val)
        
        if (self.touch_val <= 200):
           return(self.LOW)
        
    
    def state_key_dah(self):
       
        try:
            self.touch_val = self.touchdah.read()
        # ggf. Fehler abfangen
        except ValueError:
            return(self.HIGH)
            #print("ValueError while reading touch_pin")
            #print(self.touch_val)
        
        if (self.touch_val <= 200):
           return(self.LOW)
        
    

        
        
     



    def update_PaddleLatch(self):


        if (self.state_key_dit() == self.LOW):
            self.keyerControl |= self.DIT_L
        if (self.state_key_dah() == self.LOW):
            self.keyerControl |= self.DAH_L
        
    def cycle(self):
        #utime.sleep(0.3)
        cb.button_state() ## Comand button abfragen
        cb.button_state_wpm() ## Comand button WPM  abfragen
        
        # clear display when ideal 
        if w_ideal.diff() >= 3 and cb.comannd_state == 0:
            oe.print_big("",0)
            w_ideal.update()
            
        
        if cb.comannd_state == 1 : # "1" ->comand mode
        
            
            
            if self.tune == 1: # begin tune
        
                self.keyerSate = self.IDLE
                
                if self.state_key_dah() == self.LOW: # transmit on
                    self.transmit_tune= 1
                    
                    cw(1)
                elif self.state_key_dit() == self.LOW: #transmit off
                    self.transmit_tune= 0
                    
                    cw(0)
                return
                
                
                
            elif self.adj_sidetone == 1: # begin tune
        
                self.keyerSate = self.IDLE
                
                if self.state_key_dah() == self.LOW: # transmit on
                    if self.sidetone_freq > 2000:
                        text2cw("max")
                    else:
                        self.sidetone_freq =self.sidetone_freq +10
                        cwt.set_tonfreq(self.sidetone_freq) # change the Freq
                        oe.print_smal("sidetone_freq:"+str(self.sidetone_freq),cb.comannd_state)
                        
                        play("-")
                elif self.state_key_dit() == self.LOW: #transmit off
                    if self.sidetone_freq < 50:
                        text2cw("min")
                    else:
                        self.sidetone_freq = self.sidetone_freq -10
                        cwt.set_tonfreq(self.sidetone_freq)
                        oe.print_smal("sidetone_freq:"+str(self.sidetone_freq),cb.comannd_state)
                        
                        play(".")
                return
             
            
            elif self.adj_sidetone_volume == 1: # adjust sidetone volume
        
                self.keyerSate = self.IDLE
                self.tx_enable = 1
                #tx.on()
                
                if self.state_key_dah() == self.LOW: # transmit on
                    if self.sidetone_volume >= 100:
                        text2cw("max")
                    else:
                        self.sidetone_volume = self.sidetone_volume + 1
                        cwt.volume(self.sidetone_volume*200)
                        oe.print_smal("sidetone:"+str(self.sidetone_volume*200),cb.comannd_state)
                        #print(self.sidetone_volume)
                        play("-")
                        
                elif self.state_key_dit() == self.LOW: #transmit off
                    if self.sidetone_volume <= 0:
                        text2cw("min")
                    else:
                        self.sidetone_volume = self.sidetone_volume - 1
                        cwt.volume(self.sidetone_volume*200)
                        oe.print_smal("sidetone:"+str(self.sidetone_volume*200),cb.comannd_state)
                        #print(self.sidetone_volume)
                        play(".")
                return
            
            elif self.adj_wpm == 1 or cb.comannd_state_wpm == 1 : # begin tune
        
                self.keyerSate = self.IDLE
                
                if cb.comannd_state_wpm == 1 : txopt.off()
                
                if cb.comannd_state_wpm_cq :
                # wpm mode    
                
                    if self.state_key_dah() == self.LOW: # transmit on
                        self.wpm = self.wpm+1
                        cw_time.set_wpm(self.wpm)
                        oe.print_big("WPM:  "+str(self.wpm),cb.comannd_state)
                        play(".")
                        
                    elif self.state_key_dit() == self.LOW: #transmit off
                        if self.wpm >= 10:
                            self.wpm = self.wpm-1
                        cw_time.set_wpm(self.wpm)
                        oe.print_big("WPM:  "+str(self.wpm),cb.comannd_state)
                        play(".")
                else:
                    # cq mode
                    if self.state_key_dah() == self.LOW: # transmit on
                        if self.cq <= 4:
                            self.cq = self.cq+1
                        else:
                            self.cq = 0
                        
                        oe.print_smal(""+ self.cq_liste[self.cq],cb.comannd_state)
                        play(".")
                        
                    elif self.state_key_dit() == self.LOW: #transmit off
                        txopt.on()
                        text2cw(self.cq_liste[self.cq])
                        txopt.off()
                        play(".")
                       
                    
                        
                txopt.on()
                return
            
            
                
                
                
        else: # wenn  commad mode ende dann auch tune :-)
            self.tune = 0
            
           
            self.adj_sidetone = 0
            self.adj_wpm = 0
            self.adj_sidetone_volume = 0
            self.request = 0
                
            
        
        if self.keyerState == self.IDLE:
            # Wait for direct or latched paddle press
            #word grenze erkennen
            
               
                    
                    
            if utime.ticks_ms() > (self.ktimer_end + cw_time.dit_time()*4.5):
                if self.in_word:
                    self.in_word = False
                    #print(utime.ticks_ms(),self.ktimer_end)
                    #print(self.word)
                    oe.print_smal(self.word,0)
                    self.word = ""
            
            if utime.ticks_ms() > (self.ktimer_end + cw_time.dit_time()*1.5):
                
                
                
                if self.in_char:
                    self.in_char = False
                    #print(utime.ticks_ms(),self.ktimer_end)
                    #print("char",self.char)
                    self.deep_sleep = False
                    self.deep_sleep_timer = utime.ticks_ms() #timmer aktualisieren
                    self.word = self.word+decode(self.char)
            
                    
                    #if cb.comannd_stare_wpm == 1:
                        
                    if cb.comannd_state == 1: # "1" ->comand mode
                        Char = decode(self.char)
# comand mode ----------------                        
                        if  Char == "i" : # TX enable(on) disable(off)
                            oe.print_smal("i tx enable",cb.comannd_state)
                            if self.request == 1:
                                
                                if self.tx_enable :
                                    text2cw("on")
                                else:
                                    text2cw("off")
                            else:    
                                self.tx_enable = not self.tx_enable
                                if self.tx_enable:
                                    txopt.on()
                                    oe.print_smal("tx_enable:on",cb.comannd_state)
                                    text2cw("on")
                                else:
                                    text2cw("off")
                                    oe.print_smal("tx_enable:off",cb.comannd_state)
                                    txopt.off()
                                #print("Transmit", self.tx_enable)
                                cb.button_command_off()
                                
                        
                                
                        elif  Char == "o" : # TX enable(on) disable(off)
                            oe.print_smal("o sidetone on/off",cb.comannd_state)
                            if self.request == 1:
                                if self.sidetone_enable :
                                    text2cw("on")
                                else:
                                    text2cw("off")
                                    
                                
                            else:
                                self.sidetone_enable = not self.sidetone_enable
                                if self.sidetone_enable:
                                    cwt.onoff(1)
                                    oe.print_smal("sideton_enable:on",cb.comannd_state)
                                    text2cw("on")
                                else:
                                    text2cw("off")
                                    cwt.onoff(0)
                                    oe.print_smal("sideton_enable:off",cb.comannd_state)
                                    cb.button_command_off()
                                print("sidetone", self.tx_enable)
                                
                        elif  Char == "t" : # tune mode
                            oe.print_smal("T tune mode",cb.comannd_state)
                            self.tune = 1
                            if self.tune:
                                text2cw("on")
                                
                        
                                    
                        elif  Char == "v" : # sidetone volume controll
                            oe.print_smal("v sidetone volume",cb.comannd_state)
                            if self.request == 1:
                                text2cw(str(self.sidetone_volume))
                                
                            else:
                                self.adj_sidetone_volume = 1
                            
                        elif  Char == "?" : # request of parameters
                            oe.print_smal("? tx request of parameters",cb.comannd_state)
                            self.request = 1
                            
                        elif  Char == "/" : # command exit
                                oe.print_smal("/ command exit",cb.comannd_state)
                                
                                self.print_parameter()
                                cwt.set2ton()
                                cb.button_command_off()
                            
                            
                        elif  Char == "x" : # command exit
                                
                                cwt.set2ton()
                                cb.button_command_off()
                                
                                
                        elif  Char == "f" : # adjust sidetone frequenz
                            oe.print_smal("f adjust sidetone",cb.comannd_state)
                            if self.request == 1:
                                text2cw(str(self.sidetone_freq))
                            else:
                                self.adj_sidetone = 1
                        
                        
                        
                        elif  Char == "m" : # Iambic mode a/b
                            if self.request == 1:
                                if self.iambic_mode== 16 : text2cw("b")
                                else : text2cw("a")
                            
                        elif  Char == "a" : # 
                                oe.print_smal("a set iambic a",cb.comannd_state)
                                self.iambic_mode  = 0 #  0x10     # 0 for Iambic A, 1 for Iambic B
                                cb.button_command_off()
                                
                                self.write_jsondata() # save parameter afer change
                                
                        elif  Char == "s" : #  save parameter to  file
                                oe.print_smal("s save parameter",cb.comannd_state)
                                self.write_jsondata() # save parameter afer change
                                text2cw("save")
                                cb.button_command_off()
                        
                                
                        elif  Char == "b" : # adjust sidetone frequenz
                                oe.print_smal("b set iambic b",cb.comannd_state)
                                self.iambic_mode  = 0x10 #  0x10     # 0 for Iambic A, 1 for Iambic B
                                cb.button_command_off()
                        else :
                            self.char = "" 
                             
                    else :
                        #print(decode(self.char))
                        #es wird bei word gezeigt
                        #es wird nur das word ausgeben keine char.
                        #if is_ble_connected:
                           # ble.send(decode(self.char))
                    
                        self.char = ""
                        
#                 #send(decode(self.char))
#                 self.char = ""
           
            if ((self.state_key_dit() == self.LOW) or (self.state_key_dah() == self.LOW) or (self.keyerControl & 0x03)):
                self.update_PaddleLatch()
                self.keyerState = self.CHK_DIT
                w_ideal.update() # update clear display time
                
                
        elif self.keyerState == self.CHK_DIT:
            #See if the dit paddle was pressed
            
            if (self.keyerControl & self.DIT_L):
                self.keyerControl |= self.DIT_PROC
                self.ktimer = cw_time.dit_time()
                self.keyerState = self.KEYED_PREP
                self.in_char = True 
                self.in_word = True
                self.char += "."
            else:
                self.keyerState = self.CHK_DAH;
                
        
        elif self.keyerState == self.CHK_DAH:
            #See if dah paddle was pressed
            
            if (self.keyerControl & self.DAH_L):
                self.ktimer = cw_time.dit_time()*3
                self.keyerState = self.KEYED_PREP
                self.in_char = True 
                self.in_word = True
                self.char += "-"
            else:
                self.keyerState = self.IDLE;
  
        elif self.keyerState == self.KEYED_PREP:
            #print("Prep")
            #Assert key down, start timing, state shared for dit or dah
            #digitalWrite(ledPin, HIGH);         // turn the LED on
            self.Key_state = self.HIGH
            cw(True)
            
            self.ktimer += utime.ticks_ms()                 # set ktimer to interval end time
            self.keyerControl &= ~(self.DIT_L + self.DAH_L)  # clear both paddle latch bits
            self.keyerState = self.KEYED                 # next state
        
        elif self.keyerState == self.KEYED:
            if (utime.ticks_ms() > self.ktimer): #are we at end of key down?
                self.Key_sate = 0
                cw(False)
                
                self.ktimer = utime.ticks_ms()+ cw_time.dit_time()  #inter-elemet time
                self.keyerState = self.INTER_ELEMENT #next state
            else:
                if (self.keyerControl & self.iambic_mode):
                    self.update_PaddleLatch()           # early paddle latch in Iambic B mode
        

                
        elif self.keyerState == self.INTER_ELEMENT:
            self.update_PaddleLatch() #latch paddle state
            if (utime.ticks_ms() > self.ktimer):         #are we at end of inter-space ?
                self.ktimer_end = utime.ticks_ms()
                if (self.keyerControl & self.DIT_PROC): # was it a dir or dah?
                    self.keyerControl &= ~(self.DIT_L + self.DIT_PROC) #clear two bits
                    self.keyerState = self.CHK_DAH  #dit done, check for dah
                    #print(utime.ticks_ms(),self.ktimer_end)
                else:
                    self.keyerControl &= ~(self.DAH_L) #clear dah latch
                    self.keyerState = self.IDLE        #go idle
            
            


# transmit pattern
def play(pattern):
    #print("play")
    for sound in pattern:
        if sound == '.':
            cw(True)
            #print(uutime.ticks_ms()())
            utime.sleep(cw_time.dit_time()/1000)
            #print(uutime.ticks_ms())
            cw(False)
            utime.sleep(cw_time.dit_time()/1000)
        elif sound == '-':
            cw(True)
            utime.sleep(3*cw_time.dit_time()/1000)
            cw(False)
            utime.sleep(cw_time.dit_time()/1000)
        elif sound == ' ':
            utime.sleep(4*cw_time.dit_time()/1000)
    utime.sleep(2*cw_time.dit_time()/1000)

def text2cw(str):
    for c in str:
        #print(".")
        if cb.button_press() == 0 :
            print("break")
            return
        else:
            play(encode(c))
         
#----------------------------------------

# Setup Hardware pin on esp32

 
onboard_led      = 2 
extern_led_pin   = 23 
tx_opt_pin       = 4 
cw_sound_pin     = 12

touchPad_dit_pin = 32
touchPad_dah_pin = 33

touchPad_command_pin  = 27
touchPad_wpm_pin      = 14
 
#----------------------------------------

i2c = machine.I2C(1, scl = machine.Pin(18), sda = machine.Pin(19), freq = 400000)  #esp32

oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
oled.rotate(0)


oled.text('start DL2DBG', 0, 0)
oled.show()

#paddle instance
print("keyer")


# user class

w_ideal = watch_ideal()


 
txopt   = tx_opt(tx_opt_pin)
cwt = cw_sound(cw_sound_pin)

cw_time = cw_timing(18) # classe "cwtiming" are use, def wpm18 or defition from json  file



cb      = command_button(touchPad_command_pin,touchPad_wpm_pin,onboard_led,extern_led_pin)
iambic  = Iambic(touchPad_dit_pin,touchPad_dah_pin)

text2cw("r") #ready

#-------- 
while True:
      iambic.cycle()
    #text2cw("v")
    
f