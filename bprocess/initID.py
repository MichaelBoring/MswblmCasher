#-*-coding:utf-8-*-
__author__ = 'Administrator'
import json
import httppost.post
import config

class initID():
    def __init__(self):
        self.post = httppost.post.post()

    def getInitID(self):
        d = {}
        d["netbar"] = config.netbar
        d["token"] = config.token
        d["table"] = u"initialise"
        res = self.post.request(config.url, d)
        return res