#-*-coding:utf-8-*-
__author__ = 'Administrator'
import config
import httppost.post as post
import string
import dao.insiderinfoDao

class insiderinfo():
    def __init__(self):
        self._db = config.insiderDNS
        self._sysdb = config.sysdb
        self._dao = dao.insiderinfoDao.insiderinfoDao()
        self._post = post.post()

    def run(self):
        self._lastID = self.__getLastID()
        list = self._dao.getInsiderinfo(self._db, self._sysdb, self._lastID)
        if len(list) < 1:
            return None
        data = {}
        data["netbar"] = config.netbar
        data["table"] = "insiderinfo"
        data["data"] = list
        ret = self._post.request(config.url, data)
        self._lastID = string.atoi(str(ret["insiderinfo"]))
        config.insiderinfoMaxID = self._lastID

    def __getLastID(self):
        if config.insiderinfoMaxID is None:
            config.insiderinfoMaxID = self._dao.getMaxID(self._db, self._sysdb)
        return config.insiderinfoMaxID

if __name__ == "__main__":
    ins = insiderinfo()
    ins.run()