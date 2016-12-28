#!/usr/bin/env python
#-*-coding:utf-8-*-
__author__ = 'Administrator'
import mp3play
import time
import traceback
import threading
import config
import dao.usinguserDao
import dao.insiderinfoDao as insiderinfoDao
import pymedia.muxer as muxer
import pymedia.audio.acodec as acodec
import pymedia.audio.sound as sound
import string
import win32com.client
import pythoncom
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class PlaySound(threading.Thread):
    def __init__(self, t_name, queue = config.queue):
        pythoncom.CoInitialize()
        threading.Thread.__init__(self, name = t_name)
        self.queue = queue
        self._netDB = config.netHouseSerDNS
        self._sysdb = config.sysdb
        self._usingDao = dao.usinguserDao.usinguserDao()
        self.num = -1
        self._insiderdb = config.insiderDNS
        self._insiderinfoDao = insiderinfoDao.insiderinfoDao()
        self.block = -1
        self.liveness = 0


    def run(self):
        while True:
            try:
                if self.liveness > 150:
                    self.liveness = 20
                if self.queue.qsize() > 5:
                    self.liveness = 0
                    self.block = time.time() - 60
                    while self.queue.qsize() > 1:
                        self.queue.get()
                else:
                    record = self.queue.get()
                    self.analysis(record)
            except BaseException:
                config.logger.error(traceback.format_exc())
            finally:
                time.sleep(1)



    def analysis(self, record):
        voice = []
        if record['type'] == 'online':
            if config.switch_online == 0:
                return None
            voice = self.analysis_online(record)
            type = 1
        elif record['type'] == 'offline':
            if config.switch_offline == 0:
                return None
            cur = int(time.strftime('%H'))

            total = [x['ComputerName'] for x in config.dataList if x['ComputerName'] != '']
            if cur in config._except:
                pass
            elif record['ComputerName'] in total:
                pass
            else:
                type = 1
                if self.num == -1:
                    voice = self.analysis_offline(record)
                elif abs(int(record['ComputerName']) - self.num) < 2 and time.time() - self.block < 40:
                    self.liveness += 25
                    return None
                elif abs(int(record['ComputerName']) - self.num) < 3 and time.time() - self.block < 20:
                    self.liveness += 25
                    return None
                elif time.time() - self.block < 50 + self.liveness / 5:
                    self.liveness += 1
                    self.queue.put(record)
                    return None
                elif self.liveness >= 0:
                    self.liveness -= 15
                    if self.liveness < 0:
                        self.liveness = 0

                voice = self.analysis_offline(record)
                self.num = int(record['ComputerName'])
                self.block = time.time()
        if record['type'] == 'cash':
            self.playCash(record)
        if voice:
            self.play(voice, type)


    def analysis_recharge(self):
        pass


    def analysis_online(self, record):
        voice = []
        voice.append('pre')
        level = record['sNote'].split('，')[0]
        voice.append(level)
        voice.append(u'在')
        record['ComputerName'] = int(record['ComputerName'])
        self.analysis_number(str(record['ComputerName']), voice)
        voice.append('123')
        voice.append(u'online')
        return voice


    def analysis_online_new(self, record):
        voice = []
        voice.append('pre')
        level = record['sNote'].split('，')[0]
        voice.append(level)
        record['ComputerName'] = int(record['ComputerName'])
        voice.append('on{0}'.format(str(record['ComputerName'])))
        return voice


    def analysis_offline(self, record):
        voice = []
        voice.append('offline')
        voice.append(u'clean')
        record['ComputerName'] = int(record['ComputerName'])
        self.analysis_number(str(record['ComputerName']), voice)
        voice.append('123')
        time.sleep(2)
        return voice


    def analysis_offline_new(self, record):
        voice = []
        voice.append('offline')
        record['ComputerName'] = int(record['ComputerName'])
        voice.append('off{0}'.format(str(record['ComputerName'])))
        time.sleep(1)
        return voice


    def analysis_cash(self, record):
        voice = []
        level = record['sNote'].split('，')[0]
        if level == u'初级会员':
            level = 'l1'
        if level == u'黄金VIP':
            level = 'l2'
        elif level == u'铂金VIP':
            level = 'l3'
        elif level == u'钻石VIP':
            level = 'l4'
        elif level == u'管理员卡':
            level = 'l0'
            voice.append(level)
            return voice
        voice.append(level)
        voice.append(u'余额')
        record['InsiderMoney'] = int(record['InsiderMoney'])
        self.analysis_number(str(record['InsiderMoney']), voice)
        voice.append(u'元')
        return voice


    def analysis_number(self, cash, voice):
        unit = u'十百千万'
        length = len(cash)
        lengthTemp = len(cash)
        cash = cash.rstrip('0')
        lengthStrip = len(cash)
        if cash >= 0:
            for index in range(lengthStrip):
                length -= 1
                if index < lengthStrip - 1 and cash[index:index + 2] == '00':
                    continue
                if lengthTemp != 2 or index != 0 or cash[index] != '1':
                    voice.append(cash[index])
                if length != 0 and cash[index] != '0':
                    voice.append(unit[length - 1])


    def play(self, voice, type = 1):
        suffix = '.wav'
        prefix = config.src
        for temp in voice:
            temp = prefix + temp + suffix
            clip = mp3play.load(temp.encode('gbk'))
            if type:
                clip.play()
                while clip.isplaying():
                    time.sleep(0.1)
                clip.stop()
                continue


    def playCash(self, temp):
        try:
            d = None
            dns = 'Provider=Microsoft.Jet.OLEDB.4.0;User ID=ikmdb;Data Source=%s;Persist Security Info=False;Jet OLEDB:System database=%s' % (self._insiderdb, self._sysdb)
            sql = 'SELECT TOP 1 iif ( IsNull(SCardType), "", SCardType ) AS SCardType, iif ( IsNull(InsiderMoney), "", InsiderMoney ) AS InsiderMoney FROM [InsiderInfo] WHERE InsiderNumber = "%s"' % temp['InsiderNumber']
            conn = win32com.client.Dispatch(r'ADODB.Connection')
            conn.Open(dns)
            rs = win32com.client.Dispatch('ADODB.Recordset')
            rs.Open(sql, conn, 1, 3)
            while not rs.EOF:
                d = { }
                d['InsiderMoney'] = string.atof(str(rs('InsiderMoney')).strip())
                d['SCardType'] = string.atoi(str(rs('SCardType')).strip())
                rs.MoveNext()
            rs.Close()
            conn.Close()
            if d:
                d['type'] = 'cash'
                d['level'] = config.memtype[d['SCardType']] + 'CASH'
                temp = d
            else:
                return None
            tt = []
            if self.queue.qsize() == 0:
                tt.append(temp['level'])
            if int(temp['InsiderMoney']) > config.switch_money:
                tt.append(str(int(temp['InsiderMoney'])))
            suffix = '.mp3'
            prefix = config.src
            for tem in tt:
                f = open((prefix + tem + suffix).encode('gbk'), 'rb')
                data = f.read()
                dm = muxer.Demuxer('mp3')
                frames = dm.parse(data)
                dec = acodec.Decoder(dm.streams[0])
                r = dec.decode(data)
                snd = sound.Output(r.sample_rate, r.channels, 32, config.cashSpeaker)
                snd.play(r.data)
                while snd.isPlaying():
                    time.sleep(0.1)
        except BaseException:
            config.logger.error(traceback.format_exc())



if __name__ == '__main__':
    cash = "115"
    unit = u'十百千万'
    length = len(cash)
    lengthTemp = len(cash)
    cash = cash.rstrip('0')
    lengthStrip = len(cash)
    voice = []
    if cash >= 0:
        for index in range(lengthStrip):
            length -= 1
            if index < lengthStrip - 1 and cash[index:index + 2] == '00':
                print 'aaa'
                continue
            if lengthTemp != 2 or index != 0 or cash[index] != '1':
                print cash[index]
                voice.append(cash[index])
            if length != 0 and cash[index] != '0':
                print unit[length - 1]
                voice.append(unit[length - 1])