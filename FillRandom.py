#!/usr/bin/env python3
# -*- coding: utf8 -*-

import RFIDI2CMicroPython
import random

continue_reading = True

# Create random data
def random_data(size=16):
    data = []
    for i in range(size):
        data.append(random.randint(0, 255))
    return (data)

# Create an object of the class mrfc
MRFC522Reader = RFIDI2CMicroPython.MRFC522()

MRFC522Reader.showReaderDetails()

while continue_reading:
    # Scan for cards
    (status, backData, tagType) = MRFC522Reader.scan()
    if status == MRFC522Reader.MI_OK:
        print('Card detected, Type:',tagType)

        # Get UID of the card
        (status, uid, backBits) = MRFC522Reader.transceive()
        if status == MRFC522Reader.MI_OK:
            print('Card identified, UID:',hex(uid[0]),hex(uid[1]),hex(uid[2]),hex(uid[3]))

            # Select the scanned card
            (status, backData, backBits) = MRFC522Reader.select(uid)
            if status == MRFC522Reader.MI_OK:
                print('Card selected')

                # Authenticate
                mode = MRFC522Reader.MIFARE_AUTHKEY1
                blockAddr = 8
                key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                blockAddrList = []
                for blockAddr in MRFC522Reader.MIFARE_USERDATA:
                    (status, backData, backBits) = MRFC522Reader.authenticate(
                        mode,
                        blockAddr,
                        key,
                        uid)

                    if (status == MRFC522Reader.MI_OK):
                        # Write new data to card
                        data = random_data()
                        (status, backData, backBits) = MRFC522Reader.write(
                            blockAddr,
                            data)
                        if (status == MRFC522Reader.MI_OK):
                            print('Data ',blockAddr,' ', end = '')
                            blockAddrList.append(blockAddr)
                            for i in range(0,16):
                                print(data[i]," ", end = '')
                            print()
                        else:
                            print('Error while writing new data')
                        continue_reading = False

                    else:
                        print('Authentication error')                        
            print(blockAddrList)
            # Deauthenticate
            MRFC522Reader.deauthenticate()