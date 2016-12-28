#-*-coding:utf-8-*-
__author__ = 'Administrator'
import config
import dao.personnelinfoDao as personnelinfoDao
import dao.insiderinfoDao as insiderinfoDao
import httppost.post
import string
import time

class personnelinfo():
    def __init__(self):
        self._db = config.netHouseSerDNS
        self._insiderdb =config.insiderDNS
        self._sysdb = config.sysdb
        self._dao = personnelinfoDao.personnelinfoDao()
        self._insiderDao = insiderinfoDao.insiderinfoDao()
        self._post = httppost.post.post()

    def run(self):
        self._lastid = self.__getLastID()
        if(config.isDebug):
            self._lastid = 330240
            #self._lastid = self._lastid - 30
        list = self._dao.getPersonnelinfo(self._db, self._sysdb, self._lastid)
        if len(list) > 0:
            time.sleep(3)

        dicList = []
        for li in list:
            cardID = li["InsiderNumber"]
            d = None
            if li["Insider"] is True:
                d = self._insiderDao.getInsiderMoney(self._insiderdb, self._sysdb, cardID)
            if d is None:
                # 非会员
                d = {}
                d["Name"] = ""
                d["InsiderMoney"] = 0
            if(config.isDebug):
                print li["ComputerName"].encode("utf-8")
            if li["ComputerName"].find(u'会员充值') > -1:
                d["Type"] = 2
                del(li["Name"])
            elif len(li["BeginTime"]) == 0:
                d["Type"] = 0
                if str(li["Name"]) > 0:
                    del(d["Name"])
                else:
                    del(li["Name"])
            else:
                d["Type"] = 1
                if str(li["Name"]) > 0:
                    del(d["Name"])
                else:
                    del(li["Name"])

            # 合并字典
            item = dict(d, **li)
            if(config.isDebug):
                item["InsiderNumber"] = "510107199007114395"
            dicList.append(item)

        if len(dicList) < 1:
            return None

        data = {}
        data["netbar"] = config.netbar
        data["table"] = "personnelinfo"
        data["data"] = dicList

        ret = self._post.request(config.url, data)
        self._lastid = string.atoi(str(ret["personnelinfo"]))
        config.personnelinfoMaxID = self._lastid

    def __getLastID(self):
        if config.personnelinfoMaxID is None or config.personnelinfoMaxID == 0:
            config.personnelinfoMaxID = self._dao.getMaxID(self._db, self._sysdb)
            config.personnelinfoMaxID = config.personnelinfoMaxID
        return config.personnelinfoMaxID

if __name__ == "__main__":
    p = personnelinfo()
    p.run()