#!/usr/bin/env python

from socket import *
import time
import os
import json
import time
import traceback
HOST = 'localhost'
PORT = 21567
BUFSIZE = 1024
heartbeat = 0
ADDR = (HOST, PORT)
data = {}
data["CName"] = os.getenv('computername').lstrip("0")
data["State"] = -1

udpCliSock = socket(AF_INET, SOCK_DGRAM)
udpCliSock.setblocking(True)


while True:
    try:
        heartbeat += 1
        data["Beat"] = heartbeat
        data["Time"] = int(time.time())
        dataSen = json.dumps(data, ensure_ascii=False).encode('utf-8')
        udpCliSock.sendto(dataSen,ADDR)
        print time.time()
        # udpCliSock.settimeout(1)
        dataRec,addr = udpCliSock.recvfrom(BUFSIZE)
        print time.time()
        dataRec = json.loads(dataRec, encoding='utf-8')
        print dataRec
        if dataRec:
            if data["State"] != dataRec["State"]:
                data["State"] = dataRec["State"]
                data["Beat"] = heartbeat = 0

    except BaseException, e:
        data["State"] = -1
        data["Beat"] = heartbeat = 0
        traceback.print_exc()
    finally:
        print data
        # if heartbeat > 5:
        #     time.sleep(heartbeat * 6)
        # else:
        time.sleep(6)
udpCliSock.close()