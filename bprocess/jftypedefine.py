#-*-coding:utf-8-*-
__author__ = 'Administrator'
import config
import dao.jftypedefineDao
import httppost.post
import string

class jftypedefine():
    def __init__(self):
        self._db = config.netHouseSerDNS
        self._sysdb = config.sysdb
        self._post = httppost.post.post()
        self._dao = dao.jftypedefineDao.jftypedefineDao()

    def run(self):
        list = self._dao.getJftypedefine(self._db, self._sysdb)
        data = {}
        data["netbar"] = config.netbar
        data["table"] = "jftypedefine"
        data["data"] = list
        self._post.request(config.url, data)

if __name__ == "__main__":
    jf = jftypedefine()
    jf.run()