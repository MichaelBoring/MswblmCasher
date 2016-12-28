#-*-coding:utf-8-*-
__author__ = 'Administrator'
import config
import logging
import bprocess.initID
import bprocess.insiderinfo
import bprocess.huanbanls
import bprocess.jftypedefine
import bprocess.personnelinfo
import bprocess.usinguser
import string

class MainProcess():
    def __init__(self):
        self.personnelinfo = bprocess.personnelinfo.personnelinfo()
        self.insiderinfo = bprocess.insiderinfo.insiderinfo()
        self.huanbanls = bprocess.huanbanls.huanbanls()
        self.usinguser = bprocess.usinguser.usinguser()

    def Init(self):
        init = bprocess.initID.initID()
        ini = init.getInitID()
        if ini["token"] == 0:
            return None
        if ini["personnelinfo"] is not None:
            config.personnelinfoMaxID = string.atoi(str(ini["personnelinfo"]))
        if ini["insiderinfo"] is not None:
            config.insiderinfoMaxID = string.atoi(str(ini["insiderinfo"]))
        if ini["huanbanls"] is not None:
            config.huanbanlsMaxID = string.atoi(str(ini["huanbanls"]))

        self.__onstart__()
        return 1

    def Run(self):
        #4.workloginfo(Loginfo)&&usinguser(NethouseSer)
        self.usinguser.run()

        # 1. personnelinfo(NethouseSer)
        self.personnelinfo.run()

        #2.insiderinfo(Insider)
        self.insiderinfo.run()

        #3.huanbanls(NethouseSer)
        self.huanbanls.run()


    def __onstart__(self):
        jf = bprocess.jftypedefine.jftypedefine()
        jf.run()
        self.usinguser.onlyone()