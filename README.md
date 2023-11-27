# version 0.9

ich den code noch mal deutlich überarbeitet
das readme werden ich in den nächste tage noch mal nachreichen

tuka dl2dbg

 


----------------------------


## setting of different hardware

ble = ESP32_BLE("ESP32BLE_CW")     # BLE  enable # use Serial Terminal like "esp32 ble terminal  on iphone"
#ble = ESP32_BLE_pass("ESP32BLE_CW") # BLE  disable  an empty class definition

oe = OLED_Print() # print with oled display and BLE
#oe = BLE_Print() # now OLED,  only print and BLE 


----------------------------

reports the ESP32's time relative to January 1st 2000
Simple solution for uptime timer
When I used utime while Thonny was running

----------------------------
# "\r\n"
when ble is on a form time to time print("\r\n") appears
```

def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = self.ble.gap_advertise(100, bytearray('\x02\x01\x02', 'utf-8') + bytearray((len(name) + 1, 0x09),'utf-8') + name )
        self.ble.gap_advertise(100, adv_data)

        print(adv_data)
        print("\r\n")
```

background
Bluetooth Low Energy (BLE) advertising payloads refer to the data that is transmitted by a BLE device during the advertising process. 
In the context of BLE, advertising is a mechanism by which devices broadcast their presence to other nearby devices. 
This process allows devices to discover and establish connections with each other.
The advertising payload is a part of the advertising packet, which is the unit of data transmitted during advertising. 
The payload contains information that helps other devices understand the characteristics and purpose of the advertising device. 
The payload typically includes data such as device name, service UUIDs (Universal Unique Identifiers), manufacturer-specific data, and other relevant information.


# iambic keyer for es32 with touchPad
23.11.23 
READY for new MicroPython v1.21.0 on 2023-10-05; 
I update of my software, and deleted Bluetooth modules, because they no work with the new v1.21.0 version. I coud not identified the cause :-(





IAMBIC keyer in micropython esp32
* Iambic Mode A/B
* command function over keyer 
* display old ssd1306
* short key command and WPM 
* send CW text from text-buffer 
* Transmit by sound (headphone)
* Transmit by LED
* Transmit by optocoupler
*
* bluetooth print text from keyer and command infos

 

![schematic](./keyer3.jpg)
profession Version :-)


It is a minimalist device based on the micropython `code`  installed on esp32 with Thonny Tool.

No `pcb` board, simply solder connectors directly on esp32, and/or assemble it in a box

## Features
* i2csan.py  for HW test of the I2C display 
* touch_demo for test the touch key
 
Command

Hit the command button and use a morse letter. The definition is copy from kn3g keyer, which I have been using for 5 years 

* a -> Iambic Mode A# iambic keyer for es32 with touchPad
21.11.23 
READY for new MicroPython v1.21.0 on 2023-10-05; 
I update of my software, and deleted Bluetooth modules, because they no work with the new v1.21.0 version. I coud not identified the cause :-(


IAMBIC keyer in micropython esp32
* Iambic Mode A/B
* command function over keyer 
* display old ssd1306
* short key command and WPM 
* send CW text from text-buffer 
* Transmit by sound (headphone)
* Transmit by LED
* Transmit by optocoupler
*
* wifi and ntptime

 

![schematic](./keyer3.jpg)
profession Version :-)


It is a minimalist device based on the micropython `code`  installed on esp32 with Thonny Tool.

No `pcb` board, simply solder connectors directly on esp32, and/or assemble it in a box

 
Command

Hit the command button and use a morse letter. The definition is copy from kn3g keyer, which I have been using for 5 years 

* a -> Iambic Mode A
* b -> Iambic Mode B
* m -> (?) request Iambic Mode A/B

* ? -> request value of ...

* i -> (?) TX_opt enable(on) disable(off)
 
* o -> (?) Sidetone toggle (on) (off)

* f -> (?) adjust sidetone frequency
* v -> (?) adjust sidetone volume 1-100
 

* t -> tune mode, end with command mode
* s -> save parameter to  file

* c -> show time
* d -> show date

* / -> print json data file 

* x -> exit command mode

## command for send memory text 

1. Press WPM button

2. Dash key for the following memory locations (dot is issued as a receipt)

3rd point button starts memory text, (!! but adds a point at the end)

4. another point calls up the memory text again

5. Command key to exit memory text recall mode.

6. Calling up the WPM button again: the last used text memory space is made available, a period key calls up this text memory and outputs it. (with a period after)


## Software Installation

1. Install Thonny on your PC/MAC 
2. connect to a esp32 to USB
3. copy all file to esp32
4. when everything works as intended, save the program as main.py
5. if the  json file is wrong, you can start in factorymode (hold command button while booting)

## Error Info ?

If you enter a letter incorrectly or the character spacing is not correct, the character will not be recognized and a ? attached

(-.-.--.-?) is not  (-.-.) (--.-) cq

## WIFI and NTP for Clock 

esp32 wifi is aktive to get NTP requet
set your data
# user data for WIFI
ssid = "your_wifi_ssid"
pw = "your_wifi_pw"


## Configuration
Main parameters are set up in json file.
You can change the parameters in command mode of the keyer, or edit the json.txt file.  

```
"{\"threshold_key\": 200, 
\"sidetone_freq\": 700, 
\"iambic_mode\": 16, 
\"tx_enamble\": 0, 
\"sidetone_enable\": 1, 
\"sidetone_volume\": 10, 
\"wpm\": 17, 
\"txt_emable\": 0, 
\"cq_txt_liste\": [\"cq cq de dl2dbg dl2dbg bk\", \"dl2dbg\", \"cq cq test dl2dbg\", \"cq\", \"uli\", \"cq cq\"]
}"
```

```
self.cq_liste =["cq cq de dl2dbg dl2dbg bk","dl2dbg","cq cq test dl2dbg","cq","uli","cq cq"]
```

## Pinout

Setup Hardware pin on esp32
```
 
onboard_led      = 2 
extern_led_pin   = 23 
tx_opt_pin       = 4 
cw_sound_pin     = 12

touchPad_dit_pin = 32
touchPad_dah_pin = 33

touchPad_command_pin  = 27
touchPad_wpm_pin      = 14
```
![schematic](./optocopler.jpg)

## Assembly and Bill of Materials


KIS -> keep it simple

* J2 2.5mm  jack (headphone)
* optocoupler for connecting the transceiver
* button for command mode
* button for WPM (words per minute) 
* option for external command led

## Future

Some Ideas / options on demand:

*  
*  

## touch_demo1

touch_demo1 help to test the touch pin.
It will output a value that changes with and without contact. 
Use this to adjust the threshold value.

## high frequency problem
If there is a high frequency problem, an RF filter can be connected to the line. simple low pass.



## References
übersetzer
* MarkWoodworth xiaokey https://github.com/MarkWoodworth/xiaokey
* Cornell University ECE4760 RP2040 testing http://people.ece.cornell.edu/land/courses/ece4760/RP2040/index_rp2040_testing.html 
* Iambic Morse Code Keyer Sketch Copyright (c) 2009 Steven T. Elliott https://github.com/sergev/vak-opensource/blob/master/hamradio/arduino-keyer.c

## Hardware

Self-built in oak and brass.
all Buttons are touch.

![schematic](./keyer1.jpg)

