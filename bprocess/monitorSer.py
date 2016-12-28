#-*-coding:utf-8-*-

import config
from socket import *
import threading
import json
import traceback
import httppost.post


class Monitor_ser(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.HOST = config.host
        self.PORT = config.port
        self.BUFSIZE = 1024
        self.ADDR = (self.HOST, self.PORT)
        self.udpSerSock = socket(AF_INET, SOCK_DGRAM)
        self.udpSerSock.bind(self.ADDR)
        self._post = httppost.post.post()

    def run(self):
        while True:
            try:
                dataSen = {}
                data, addr = self.udpSerSock.recvfrom(self.BUFSIZE)
                if data:
                    data = json.loads(data, encoding='utf-8')
                    heartbeat = data["Beat"]
                    computerName = data["CName"].lstrip("0")
                    if not config.dataList and config.dataList != []:
                        continue
                    total = [x["ComputerName"].lstrip("0") for x in config.dataList if x["ComputerName"] != ""]
                    if computerName in total:
                        alive = 1
                    else:

                        alive = 0
                    dataSen["State"] = alive
                    self.udpSerSock.sendto(json.dumps(dataSen, ensure_ascii=False).encode('utf-8'), addr)
                    if (data["State"] == 0 and heartbeat > data["Limit"] and alive == 0) or data["On"] == 0:
                        temp = {}
                        temp["netbar"] = config.netbar
                        temp["table"] = "monitor"
                        dl = []
                        dl.append(data)
                        temp["data"] = dl
                        if data["On"] != 0:
                            config.logger.error(data)
                        self._post.request(config.url, temp)
            except BaseException, e:
                config.logger.error(traceback.format_exc())


if __name__ == '__main__':
    Monitor_ser().run()
