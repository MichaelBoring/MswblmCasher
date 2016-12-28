#!/usr/bin/env python
# encoding: utf-8
__author__ = 'Administrator'
import config
import httppost.post
import dao.workLogInfoDao
import dao.usinguserDao
import dao.insiderinfoDao
import bprocess.playSound
import bprocess.monitorSer
import bprocess.screenShot
import time


class usinguser:

    def __init__(self):
        self._sysdb = config.sysdb
        self._logDB = config.logInfoDNS
        self._netDB = config.netHouseSerDNS
        self._post = httppost.post.post()
        self.block = time.time()
        self.dataList = []
        self._logDao = dao.workLogInfoDao.workLogInfoDao()
        self._usingDao = dao.usinguserDao.usinguserDao()
        self._insiderDao = dao.insiderinfoDao.insiderinfoDao()
        self._insiderdb = config.insiderDNS
        self._lastID = self._logDao.getMaxID(self._logDB, self._sysdb)
        self._tem = bprocess.playSound.PlaySound('playSound', config.queue)
        self._tem.setDaemon(True)
        self._tem.start()
        self._tem2 = bprocess.monitorSer.Monitor_ser()
        self._tem2.setDaemon(True)
        self._tem2.start()
        if config.switch_cash != -1:
            self._tem1 = bprocess.playSound.PlaySound('playAudio', config.cash)
            self._tem1.setDaemon(True)
            self._tem1.start()
            self._tem3 = bprocess.screenShot.ScreenShot('screenShot', config.cash)
            self._tem3.setDaemon(True)
            self._tem3.start()


    def run(self):
        tempList = self._usingDao.getusinguser(self._netDB, self._sysdb)
        temptotal = [x["ComputerName"].lstrip("0") for x in tempList if x["ComputerName"] != ""]
        total = [x["ComputerName"].lstrip("0") for x in config.dataList if x["ComputerName"] != ""]

        if (len(set(temptotal) ^ set(total)) != 0) or ((time.time() - self.block) > 60 * 5):
            self.onlyone()

        list = self._logDao.getLogs(self._logDB, self._sysdb, self._lastID)
        if len(list) < 1:
            return None

        self._lastID = list[-1]['ID']

        item = [x for x in list if x['sCommand'].find(u'修改会员金额或者时间') > -1]
        if len(item) > 0:
            self._usinguser_modifyMoney(item)

        jfcheck = {}
        for jftemp in config.jftype.keys():
            jfcheck[jftemp] = 0
        for x in self.dataList:
            type = x['SCardType']
            if config.memtype.has_key(x['SCardType']):
                jfcheck[config.memtype[x['SCardType']]] += 1

        if config.switch_online != -1:
            item = [x for x in list if (x['sCommand'].find(u'客户端登录') > -1 or x['sCommand'].find(u'刷卡计费') > -1) and x['ComputerName'] != '']
            if len(item) > 0:
                for temp in item:
                    level = temp['sNote'].split('，')[0]
                    temp['type'] = 'online'
                    if level == u'黄金VIP' and jfcheck[level] < config.gold:
                        config.queue.put(temp)
                    if level == u'铂金VIP' and jfcheck[level] < config.platnum:
                        config.queue.put(temp)
                    if level == u'钻石VIP' and jfcheck[level] < config.diamond:
                        config.queue.put(temp)
                    if level == u'管理员卡':
                        config.queue.put(temp)

        if config.switch_offline != -1:
            item = [x for x in list if (x['sCommand'].find(u'结帐') > -1  or x['sCommand'].find(u'会员卡存金额用完') > -1 or x['sCommand'].find(u'限时时间到') > -1) and x['ComputerName'] != '']
            if len(item) > 0:
                for temp in item:
                    if temp['ComputerName']:
                        temp['type'] = 'offline'
                        config.queue.put(temp)


    def onlyone(self):
        temp = self._usingDao.getusinguser(self._netDB, self._sysdb)
        totalList = [x for x in temp if x['Area'] > -1]
        tempList = [x for x in totalList if x['Insider'] == 0]

        online = []
        # for on in totalList:
        #     if len(on['ComputerName']) > 0:
        #         online.append(on['ComputerName'])
        # print online
        online = [x['ComputerName'] for x in totalList if x['ComputerName'] != ""]
        data = {}
        data['netbar'] = config.netbar
        data['table'] = 'netbarState'
        d = {}
        d['Total'] = len(totalList)
        d['Temp'] = len(tempList)
        d['Online'] = online
        dl = []
        dl.append(d)
        data['data'] = dl
        self._post.request(config.url, data)
        config.dataList = self.dataList = temp
        self.block = time.time()


    def _usinguser_modifyMoney(self, list):
        if len(list) < 1:
            return None
        dl = []
        for l in list:
            d = { }
            d['Note'] = l['sNote']
            d['SCardNumber'] = l['SCardNumber']
            d['Command'] = 1
            dl.append(d)

        if len(dl) < 1:
            return None
        data = {}
        data['netbar'] = config.netbar
        data['table'] = 'workloginfo'
        data['data'] = dl
        self._post.request(config.url, data)


if __name__ == '__main__':
    uu = usinguser()
    uu.run()
