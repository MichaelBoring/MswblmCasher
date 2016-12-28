# -*-coding:utf-8-*-
__author__ = 'Administrator'
import config
import httppost.post
import dao.huanbanlsDao
import string

class huanbanls():
    def __init__(self):
        self._dns = config.netHouseSerDNS
        self._sysdb = config.sysdb
        self._post = httppost.post.post()
        self._dao = dao.huanbanlsDao.huanbanlsDao()

    def run(self):
        self._lastID = self.__getLastID()
        list = self._dao.getHuanbanls(self._dns, self._sysdb, self._lastID)
        if len(list) < 1:
            return  None
        data = {}
        data["netbar"] = config.netbar
        data["table"] = "huanbanls"

        dl = []
        for l in list:
            dl.append(l)
        data["data"] = dl
        ret = self._post.request(config.url, data)
        self._lastID = string.atoi(str(ret["huanbanls"]))
        config.huanbanlsMaxID = self._lastID

    def __getLastID(self):
        if config.huanbanlsMaxID is None:
            config.huanbanlsMaxID = self._dao.getMaxID()
        return config.huanbanlsMaxID

if __name__ == "__main__":
    hb = huanbanls()
    hb.run()