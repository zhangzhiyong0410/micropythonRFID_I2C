import RFIDI2CMicroPython
import time

AVAILABLEBLOCK = [1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16, 17, 18, 20, 21, 22, 24, 25, 26, 28, 29, 30, 32, 33, 34, 36, 37, 38, 40, 41, 42, 44, 45, 46, 48, 49, 50, 52, 53, 54, 56, 57, 58, 60, 61, 62]
class RfidAL:
    def __init__(self):
        self.rfid = RFIDI2CMicroPython.MRFC522()

    def scan(self,wait=3):
        self.rfid.MRFC522_init()
        startTime = time.ticks_ms()
        while True:
            if time.ticks_ms()-startTime > wait*1000:
                print("Card not found")
                break
            # Scan for cards
            (status, backData, tagType) = self.rfid.scan()
            if status == self.rfid.MI_OK:
                #print('Card detected, Type:',tagType)

                # Get UID of the card
                (status, uid, backBits) = self.rfid.transceive()
                if status == self.rfid.MI_OK:
                    uidStr = ""
                    for i in range(0,4):
                        buff = hex(uid[i]).replace("0x","")
                        if len(buff) == 1:
                            buff = "0"+buff
                        uidStr+=buff
                    return uidStr

    def read(self,blockAddr,wait=3):
        blockAddr = AVAILABLEBLOCK[blockAddr]
        self.rfid.MRFC522_init()
        startTime = time.ticks_ms()
        while True:
            if time.ticks_ms()-startTime > wait*1000:
                print("Card not found")
                break
            # Scan for cards
            (status, backData, tagType) = self.rfid.scan()
            if status == self.rfid.MI_OK:
                #print('Card detected, Type:',tagType)

                # Get UID of the card
                (status, uid, backBits) = self.rfid.transceive()
                if status == self.rfid.MI_OK:
                    #print('Card identified, UID:',hex(uid[0]),hex(uid[1]),hex(uid[2]),hex(uid[3]))

                    # Select the scanned card
                    try:
                      (status, backData, backBits) = self.rfid.select(uid)
                    except:
                      return None
                    if status == self.rfid.MI_OK:
                        #print('Card selected')

                        # Authenticate
                        mode = self.rfid.MIFARE_AUTHKEY1
                        (status, backData, backBits) = self.rfid.authenticate(
                            mode,
                            blockAddr,
                            self.rfid.MIFARE_KEY,
                            uid)
                        if (status == self.rfid.MI_OK):
                            #print('Card authenticated')

                            # Read data from card
                            (status, backData, backBits) = self.rfid.read(
                                blockAddr)
                            if (status == self.rfid.MI_OK):
                                hex_list = backData
                                asc_str=''
                                for hex_str in hex_list:
                                    asc = chr(hex_str)
                                    asc_str += asc
                                asc_str = asc_str.strip()
                                return asc_str
                            else:
                                print('Error while reading')
                            
                            # Deauthenticate
                            self.rfid.deauthenticate()
                            print('Card deauthenticated')
                        else:
                            print('Authentication error')

    def write(self,blockAddr,data,wait=3):
        blockAddr = AVAILABLEBLOCK[blockAddr]
        self.rfid.MRFC522_init()
        # Scan for cards
        dataASCLL = []
        for char in range(0,16):
            if char < len(data):
                dataASCLL.append(ord(data[char]))
            else:
                dataASCLL.append(0x20)
        startTime = time.ticks_ms()
        while True:
            if time.ticks_ms()-startTime > wait*1000:
                print("Card not found")
                break
            (status, backData, tagType) = self.rfid.scan()
            if status == self.rfid.MI_OK:
                #print('Card detected, Type:',tagType)
                # Get UID of the card
                (status, uid, backBits) = self.rfid.transceive()
                if status == self.rfid.MI_OK:
                    #print('Card identified, UID:',hex(uid[0]),hex(uid[1]),hex(uid[2]),hex(uid[3]))
                    # Select the scanned card
                    try:
                        (status, backData, backBits) = self.rfid.select(uid)
                    except:
                        return None
                    if status == self.rfid.MI_OK:
                        #print('Card selected')
                        # Authenticate
                        mode = self.rfid.MIFARE_AUTHKEY1
                        (status, backData, backBits) = self.rfid.authenticate(
                            mode,
                            blockAddr,
                            self.rfid.MIFARE_KEY,
                            uid)
                        if (status == self.rfid.MI_OK):
                            #print('Card authenticated')
                            if (status == self.rfid.MI_OK):
                                # Write new data to card
                                (status, backData, backBits) = self.rfid.write(
                                    blockAddr,
                                    dataASCLL)
                                if (status == self.rfid.MI_OK):
                                    print('written succeed')
                                    break
                                else:
                                    print('Error while writing new data')
                            else:
                                print('Error while reading old data')
                            # Deauthenticate
                            self.rfid.deauthenticate()
                            print('Card deauthenticated')
                        else:
                            print('Authentication error')