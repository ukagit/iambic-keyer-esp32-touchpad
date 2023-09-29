from machine import   Pin

from machine import TouchPad 
from time import sleep

touch0=TouchPad(Pin(33))
touch4=TouchPad(Pin(32))

touch2=TouchPad(Pin(14))
touch3=TouchPad(Pin(27))

while True:
    #print("a",touch0.read())
    #print("b",touch4.read())
    
    try:
        touch_val = touch0.read()
    # ggf. Fehler abfangen
    except ValueError:
        print("ValueError while reading touch_pin")
    
    print("1",touch_val)
    
    try:
        touch_val4 = touch4.read()
    # ggf. Fehler abfangen
    except ValueError:
        print("ValueError while reading touch_pin")
    
    print("4",touch_val4)
    
    try:
        touch_val2 = touch2.read()
    # ggf. Fehler abfangen
    except ValueError:
        print("ValueError while reading touch_pin")
    
    print("2",touch_val2)
    
    try:
        touch_val3 = touch3.read()
    # ggf. Fehler abfangen
    except ValueError:
        print("ValueError while reading touch_pin")
    
    print("3",touch_val3)
    
    sleep(0.5)
    
   