#-*-coding:utf-8-*-
__author__ = 'Administrator'

import win32serviceutil
import win32service
import win32event
import traceback
import logging
import mainProcess
import config
import time

class MswblmService(win32serviceutil.ServiceFramework):
    _svc_name_ = "mswblm"
    _svc_display_name_ = "mswblm"
    _svc_description_ = "mswblm Service"

    def __init__(self, args):
        try:
            win32serviceutil.ServiceFramework.__init__(self, args)
            self.logger = self._getLogger()
            self._config()
            self.isAlive = True
            self.process = mainProcess.MainProcess()
        except BaseException, e:
            self.logger.error(traceback.format_exc())

    def SvcDoRun(self):
        try:
            self.logger.debug("svc do run....")
            ret = self.process.Init()
            if ret is None:
                self.logger.debug(u"获取初始化参数失败")
                self.isAlive = False

            while self.isAlive:
                try:
                    self.process.Run()
                except BaseException, e:
                    self.logger.error(traceback.format_exc())
                finally:
                    time.sleep(0.8)
        except BaseException, e:
            self.logger.error(e)

    def SvcStop(self):
        self.logger.debug("svc do stop....")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.isAlive = False

    def _config(self):
        import ConfigParser
        config.logger = self.logger
        configer = ConfigParser.ConfigParser()
        configer.read(r"C:\WINDOWS\mswblm.ini")
        dbfile = configer.get("mswblm", "AccessPath").decode('gbk').encode('utf-8')
        systemfile = configer.get("mswblm", "SystemPath").decode('gbk').encode('utf-8')
        #netbar = configer.get("mswblm", "NetBar").decode('gbk').encode('utf-8')
        netbarid = configer.get("mswblm", "NetBarID").decode('gbk').encode('utf-8')
        token = configer.get("mswblm", "Token").decode('gbk').encode('utf-8')
        if configer.has_option("mswblm", "Gold"):
            config.gold = configer.getint("mswblm", "Gold")
        if configer.has_option("mswblm", "Gold"):
            config.platnum = configer.getint("mswblm", "Platnum")
        if configer.has_option("mswblm", "Gold"):
            config.diamond = configer.getint("mswblm", "Diamond")
        if configer.has_option("mswblm", "CashSpeaker"):
            config.cashSpeaker = configer.getint("mswblm", "CashSpeaker")
        if configer.has_option("mswblm", "Except"):
            config._except = map(int, configer.get("mswblm", "Except").decode('gbk').encode('utf-8').split(','))
        if configer.has_option("mswblm", "SwitchCash"):
            config.switch_cash = configer.getint("mswblm", "SwitchCash")
        if configer.has_option("mswblm", "SwitchOffline"):
            config.switch_offline = configer.getint("mswblm", "SwitchOffline")
        if configer.has_option("mswblm", "SwitchOnline"):
            config.switch_online = configer.getint("mswblm", "SwitchOnline")
        if configer.has_option("mswblm", "Ip"):
            config.host = configer.get("mswblm", "Ip").decode('gbk').encode('utf-8')
        if configer.has_option("mswblm", "Port"):
            config.port = configer.getint("mswblm", "Port")
        #isdebug = configer.get("mswblm", "Debug")
        #if isdebug is not None:
        #    isdebug = string.atoi(configer.get("mswblm", "Debug").decode('gbk').encode('utf-8'))
        #    cid = configer.get("mswblm", "ID").decode('gbk').encode('utf-8')
        #    config.isdebug = isdebug
        #    config.ID = cid

        config.netHouseSerDNS = u"{0}/NetHouseSer.mdb".format(dbfile)
        config.insiderDNS = u"{0}/Insider.mdb".format(dbfile)
        config.logInfoDNS = u"{0}/Loginfo.mdb".format(dbfile)
        config.sysdb = u"{0}/System.mdw".format(systemfile)
        if configer.has_option("mswblm", "Src"):
            config.src = configer.get("mswblm", "Src").decode('gbk').encode('utf-8')
        config.token = token
        config.netbar = netbarid

    def _getLogger(self):
        # import logging
        import os
        import inspect
        logger = logging.getLogger('[mswblmppy]')
        this_file = inspect.getfile(inspect.currentframe())
        dirpath = os.path.abspath(os.path.dirname(this_file))
        handler = logging.FileHandler(os.path.join(dirpath, "mswblmppy.log"))
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger