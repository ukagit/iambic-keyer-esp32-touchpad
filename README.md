# iambic keyer for es32 with touchPad


IAMBIC keyer in micropython esp32
* Iambic Mode A/B
* command function over keyer 
* display OLED ssd1306
* short key for command and WPM 
* send CW text from memoery text-buffer 
* Transmit by sound (internal speaker)
* Transmit by LED
* Transmit by optocoupler
* Parameters are stored in a JSON file
* bluetooth send, output text from keyer and command infos

 ---

![schematic](./keyer3.jpg)

On the photo, you can see the CW Keyer with the two paddles, DIT, and DAT.  
The OLED display, and two more buttons: Command and WPM/Text.
It is a minimalist device, based on the micropython `code`, installed on esp32 with Thonny Tool.
No `pcb` board, simply, solder connectors directly on esp32, and/or assemble it in a box.

# Start 

After turning it on, the keyer appears ready. 
The keyer is in send mode; you can input CW code using the DIT and DAH buttons. 
The characters are sent directly to TX out.
decoded and displayed as text on the OLED display.

Pressing the Command button switches to Command mode; pressing it again returns to operation mode."

# USE
## operate and command mode
### operate 
You can send MORSE code with the **DIT** **DAT** paddel.

### command
Hit the command button and use a morse letter 


### The procedure for the Command mode is as follows:


| operation mode | command  mode  |          responce          |
|:---------------|:---------------|:--------------------------:| 
| operation      |                |                            |
| Button Command |                |                            |
|                | c              |          out time          |
|                | Button Command |                            |
| operation      |                |                            |
| operation      |                |                            |
| Button Command |                |                            |
|                | o              | Sidetone toggle (on) (off) |
|                | Button Command |                            |
| operation      |                |          

### command table

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

**note** The definition of key-command is a copy from kn3g keyer, which I have been using for 5 years 

### Query parameters ?
1. Press **command button**.  
1. Send the **letter** "?" followed by the **letters** of the parameter. In response, 
the value of the parameter is sent. You remain in command mode.
1. End by pressing the **command button** 

***example*** ? v respond is 200

**Node** All commands with a question mark (?) can be queried

## Command Button

### Command for send memory text
1. Press **WPM button** once
1. **DAT** key switches to the next text from the memory.
1. **DIT** confirm your selection and starts cw sending of the text,
1. another **DIT** calls up the text again
1. **DAT** key switches to the next text from the memory.
1. Press **Command button** to exit memory text recall mode.

### Command for set WPM  words per minute
1. Press **WPM button** twice
1. **DAT** key decrease the Value
1. **DIT** key inecrise the WPM Value
1. Press **Command button** to exit WPM.
 


## Software Installation

1. Install Thonny on your PC/MAC 
2. connect to a esp32 to USB
3. copy all file to esp32
4. when everything works as intended, save the program as main.py
5. if the  json file is wrong, you can start in factorymode (hold command button while booting)

## Error (-.-.--.-?) 
If you enter a letter incorrectly or the character spacing is not correct, the character will not be recognized and a ? attached

(-.-.--.-?) is not  (-.-.) (--.-) cq

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
#### defintion in code
```
self.cq_liste =["cq cq de dl2dbg dl2dbg bk","dl2dbg","cq cq test dl2dbg","cq","uli","cq cq"]
```

## Pinout

 Hardwaresetup, pin on esp32


| function           | pin   |
:---------------|:------| 
|onboard_led   | 2     |
|extern_led_pin | 23    |
|tx_opt_pin      | 4     |
|cw_sound_pin     | 12    |
| |       |
|touchPad_dit_pin | 32    |
|touchPad_dah_pin | 33    |
||       |
|touchPad_command_pin | 27    |
|touchPad_wpm_pin     |  14   |
||       |

![schematic](./optocopler.jpg)
### optocoupler 
The transmitter is controlled via an optocoupler open collector.   
You can use a PC817 for this.

### high frequency problem
If there is a high frequency problem, an RF filter can be connected to the line. simple low pass.


## Assembly and Bill of Materials

KIS -> keep it simple

* J2 2.5mm  jack (headphone)
* optocoupler for connecting the transceiver
* button for command mode
* button for WPM (words per minute) 
* option for external command led

## Future

#### Some Ideas / options on demand?
no wishes :-)



## References
übersetzer
* MarkWoodworth xiaokey https://github.com/MarkWoodworth/xiaokey
* Iambic Morse Code Keyer Sketch Copyright (c) 2009 Steven T. Elliott https://github.com/sergev/vak-opensource/blob/master/hamradio/arduino-keyer.c

## Hardware of my keyer
Self-built in oak and brass.
all Buttons are touch.

![schematic](./keyer1.jpg)

## different hardware setup 
#### option
* OLED 
* BLE 

In the code are different class difintion. One is "aktive" the ather other is "dummy".  
You can enable or disable the class by simple comment out.

```
ble = ESP32_BLE("ESP32BLE_CW")     # BLE  enable # use Serial Terminal like "esp32 ble terminal  on iphone"
#ble = ESP32_BLE_pass("ESP32BLE_CW") # BLE  disable  an empty class definition

oe = OLED_Print() # print with oled display and BLE
#oe = BLE_Print() # now OLED,  only print and BLE 
```


## known issue
### output new line 
When BLE is on, form time to time a print("\r\n") appears,
cause is advertiser time out.

```
def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = self.ble.gap_advertise(100, bytearray('\x02\x01\x02', 'utf-8') + bytearray((len(name) + 1, 0x09),'utf-8') + name )
        self.ble.gap_advertise(100, adv_data)

        print(adv_data)
        print("\r\n")
```

#### background
Bluetooth Low Energy (BLE) advertising payloads refer to the data that is transmitted by a BLE device during the advertising process. 
In the context of BLE, advertising is a mechanism by which devices broadcast their presence to other nearby devices. 
This process allows devices to discover and establish connections with each other.
The advertising payload is a part of the advertising packet, which is the unit of data transmitted during advertising. 
The payload contains information that helps other devices understand the characteristics and purpose of the advertising device. 
The payload typically includes data such as device name, service UUIDs (Universal Unique Identifiers), manufacturer-specific data, and other relevant information.



## Bluetooth pairing 
Successfully tested with iPhone 12, MacBook, and Android Samsung.

## Bluetooth pairing fails ?
It may be that a connection is not possible
See note Android.

### Bluetooth pairing fails for Android phones with MediaTek chipset (IDFGH-5014)

Problem Description 
[(one2one copy from this Link )](https://github.com/espressif/esp-idf/issues/6800)

The ESP32 Bluetooth cannot pair with certain Android phones that use MediaTek chips that support Bluetooth 5.0. The affected phones include LG Stylo 6, LG Phoenix 5, and Alcatel 3V. Phones/tablets that do not use the MediaTek chipset for Bluetooth will pair with no issues such as the Pixel, Pixel4 (qualcom) and Hytab-plus-10wb1 (xradio).

When capturing the Bluetooth pairing packets, I noticed that there was LL_REJECT_IND_EXT opcode from the device that was common for all the affected phones which may indicate why the connection was dropped. Also tried ESP-IDF Pre-release v4.3-beta2 with different bluetooth module options but the issues still persists.

### time command
The command output can be different.  
uptime, reports the ESP32's time relative to January 1st 2000.  
Correct time because the system time was given by thonny when starting.

## Addone software
It's still tests and utility programs in the GitHub.
* i2csan.py  for HW test of the I2C display 
* touch_demo for test the touch key
* ble_test simple BLE server with output numer, test for scan, connect, und receive.

### touch_demo1

touch_demo1 help to test the touch pin.
It will output a value that changes with and without contact. 
Use this to adjust the threshold value.


---
### Version
READY for new MicroPython v1.21.0 on 2023-10-05; 

