from machine import Pin, Timer, SoftI2C
from time import sleep_ms
import ubluetooth
import time


class ESP32_BLE():
    def __init__(self, name):
        # Create internal objects for the onboard LED
        # blinking when no BLE device is connected
        # stable ON when connected
        self.led = Pin(2, Pin.OUT)
        self.timer1 = Timer(0)
        
        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()

    def connected(self):
        global is_ble_connected
        is_ble_connected = True
        self.led.value(1)
        self.timer1.deinit()

    def disconnected(self):
        global is_ble_connected
        is_ble_connected = False
        self.timer1.init(period=100, mode=Timer.PERIODIC, callback=lambda t: self.led.value(not self.led.value()))

    def ble_irq(self, event, data):
        global ble_msg
        
        if event == 1: #_IRQ_CENTRAL_CONNECT:
                       # A central has connected to this peripheral
            self.connected()
            print("connect")

        elif event == 2: #_IRQ_CENTRAL_DISCONNECT:
                         # A central has disconnected from this peripheral.
            self.advertiser()
            self.disconnected()
            print("disconnectec")
        
        elif event == 3: #_IRQ_GATTS_WRITE:
                         # A client has written to this characteristic or descriptor.          
            buffer = self.ble.gatts_read(self.rx)
            ble_msg = buffer.decode('UTF-8').strip()
            print("read")
            print(ble_msg)
            
    def register(self):        
        # Nordic UART Service (NUS)
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
            
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)
            
        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART, )
        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        if is_ble_connected:
            self.ble.gatts_notify(0, self.tx, data + '\n')

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = self.ble.gap_advertise(100, bytearray('\x02\x01\x02', 'utf-8') + bytearray((len(name) + 1, 0x09),'utf-8') + name )
        self.ble.gap_advertise(100, adv_data)
   

#    def advertiser(self):
#        name = bytes(self.name, 'UTF-8')
#        adv_data = bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name
#        self.ble.gap_advertise(100, adv_data)
        print(adv_data)
        print("\r\n")
                # adv_data
                # raw: 0x02010209094553503332424C45
                # b'\x02\x01\x02\t\tESP32BLE'
                #
                # 0x02 - General discoverable mode
                # 0x01 - AD Type = 0x01
                # 0x02 - value = 0x02
                
                # https://jimmywongiot.com/2019/08/13/advertising-payload-format-on-ble/
                # https://docs.silabs.com/bluetooth/latest/general/adv-and-scanning/bluetooth-adv-data-basics
#ble = ESP32_BLE("ESP32BLE_CW")#ble = ESP32_BLE("ESP32BLE_CW")
    

print("start")
ble = ESP32_BLE("ESP32BLE_TestA")
while 1:
    for i in range(1,100):
        print(i)
        ble.send(str(i))
        time.sleep(1)


