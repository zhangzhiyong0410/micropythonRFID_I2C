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
                (status, backData, backBits) = MRFC522Reader.authenticate(
                    mode,
                    blockAddr,
                    MRFC522Reader.MIFARE_KEY,
                    uid)
                if (status == MRFC522Reader.MI_OK):
                    print('Card authenticated')

                    # Read old data from card
                    (status, backData, backBits) = MRFC522Reader.read(
                        blockAddr)
                    if (status == MRFC522Reader.MI_OK):
                        print('Data ',blockAddr,' ', end = '')
                        for i in range(0,16):
                            print(backData[i]," ", end = '')
                        print('read')

                        # Write new data to card
                        data = random_data()
                        (status, backData, backBits) = MRFC522Reader.write(
                            blockAddr,
                            data)
                        if (status == MRFC522Reader.MI_OK):
                            print('Data ',blockAddr,' ', end = '')
                            for i in range(0,16):
                                print(data[i]," ", end = '')
                            print('written')

                            # Read new data from card
                            (status, backData, backBits) = MRFC522Reader.read(
                                blockAddr)
                            if (status == MRFC522Reader.MI_OK):
                                print('Data ',blockAddr,' ', end = '')
                                for i in range(0,16):
                                    print(backData[i]," ", end = '')
                                print('read')

                                continue_reading = False
                            else:
                                print('Error while reading new data')
                        else:
                            print('Error while writing new data')
                    else:
                        print('Error while reading old data')

                    # Deauthenticate
                    MRFC522Reader.deauthenticate()
                    print('Card deauthenticated')
                else:
                    print('Authentication error')