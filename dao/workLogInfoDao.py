#-*-coding:utf-8-*-
__author__ = 'Administrator'
import time
import string
import win32com.client
import pythoncom
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# Microsoft.Jet.OLEDB.4.0

class workLogInfoDao():
    def __init__(self):
        '''
        init com
        '''
        pythoncom.CoInitialize()

    def getMaxID(self, db, sysdb):
        maxid = 0;
        dns = r'Provider=Microsoft.Jet.OLEDB.4.0;User ID=ikmdb;Data Source=%s;Persist Security Info=False;Jet OLEDB:System database=%s' % (db, sysdb)
        sql = r"SELECT Max(ID) AS ID FROM WorkLogInfo;"
        conn = win32com.client.Dispatch(r'ADODB.Connection')
        conn.Open(dns)
        rs = win32com.client.Dispatch(r'ADODB.Recordset')
        rs.Open(sql, conn, 1, 3)
        while not rs.EOF:
            maxid = int(rs('ID'))
            rs.MoveNext()
        rs.Close()
        conn.Close()
        return maxid

    def getLogs(self, db, sysdb, lastid):
        list = []
        dns = r'Provider=Microsoft.Jet.OLEDB.4.0;User ID=ikmdb;Data Source=%s;Persist Security Info=False;Jet OLEDB:System database=%s' % (db, sysdb)
        sql = r"SELECT TOP 100 ID, iif (IsNull(ComputerName), '', ComputerName) AS ComputerName, iif (IsNull(sCommand), '', sCommand) AS sCommand, iif (IsNull(SCardNumber), '', SCardNumber) AS SCardNumber, iif (IsNull(sNote), '', sNote) AS sNote FROM WorkLogInfo WHERE ID>{0} ORDER BY ID".format(str(lastid))
        conn = win32com.client.Dispatch(r'ADODB.Connection')
        conn.Open(dns)
        rs = win32com.client.Dispatch(r'ADODB.Recordset')
        rs.Open(sql, conn, 1, 3)
        while not rs.EOF:
            d = {}
            d['ID'] = int(rs('ID'))
            d['sCommand'] = str(rs('sCommand')).strip()
            d['ComputerName'] = str(rs('ComputerName')).strip()
            d['SCardNumber'] = str(rs('SCardNumber')).strip()
            d['sNote'] = str(rs('sNote')).strip()
            list.append(d)
            rs.MoveNext()
        rs.Close()
        conn.Close()
        return list

if __name__ == '__main__':
    # db = r"U:/Loginfo.mdb"
    # sysdb = r"U:/System.mdw"
    # maxid = 0;
    # dns = r'Provider=Microsoft.Jet.OLEDB.4.0;User ID=ikmdb;Data Source=%s;Persist Security Info=False;Jet OLEDB:System database=%s' % (
    # db, sysdb)
    # sql = r"SELECT Max(ID) AS ID FROM WorkLogInfo;"
    # conn = win32com.client.Dispatch(r'ADODB.Connection')
    # conn.Open(dns)
    # rs = win32com.client.Dispatch(r'ADODB.Recordset')
    # rs.Open(sql, conn, 1, 3)
    # while not rs.EOF:
    #     maxid = int(rs('ID'))
    #     rs.MoveNext()
    # rs.Close()
    # conn.Close()
    # print  maxid


    db = r"U:/Loginfo.mdb"
    sysdb = r"U:/System.mdw"
    dns = r'Provider=Microsoft.Jet.OLEDB.4.0;User ID=ikmdb;Data Source=%s;Persist Security Info=False;Jet OLEDB:System database=%s' % (
    db, sysdb)
    conn = win32com.client.Dispatch(r'ADODB.Connection')
    conn.Open(dns)
    sql_statement = u"Insert INTO WorkLogInfo (SCardNumber,ComputerName,sCommand,sNote) VALUES('513821199201169013', '121', '客户端结帐', '黄金VIP，首次从客户端登陆')"
    conn.Execute(sql_statement)
    # sql_statement = u"Insert INTO WorkLogInfo (SCardNumber,ComputerName,sCommand,sNote) VALUES('513821199201169013', '160', '客户端登录', '黄金VIP，首次从客户端登陆')"
    # conn.Execute(sql_statement)
    # sql_statement = u"Insert INTO WorkLogInfo (SCardNumber,ComputerName,sCommand,sNote) VALUES('513821199201169013', '37', '客户端结帐', '黄金VIP，首次从客户端登陆')"
    # conn.Execute(sql_statement)
    sql_statement = u"Insert INTO WorkLogInfo (SCardNumber,ComputerName,sCommand,sNote) VALUES('513821199201169013', '155', '客户端结帐', '黄金VIP，首次从客户端登陆')"
    conn.Execute(sql_statement)
    # time.sleep(2)
    # sql_statement = u"Insert INTO WorkLogInfo (SCardNumber,ComputerName,sCommand,sNote) VALUES('513821199201169013', '139', '客户端结帐', '黄金VIP，首次从客户端登陆')"
    # conn.Execute(sql_statement)
    # sql_statement = u"Insert INTO WorkLogInfo (SCardNumber,ComputerName,sCommand,sNote) VALUES('513821199201169013', '50', '客户端结帐', '黄金VIP，首次从客户端登陆')"
    # conn.Execute(sql_statement)
    # time.sleep(1)
    sql_statement = u"Insert INTO WorkLogInfo (SCardNumber,ComputerName,sCommand,sNote) VALUES('513821199201169013', '232', '客户端结帐', '黄金VIP，首次从客户端登陆')"
    conn.Execute(sql_statement)
    sql_statement = u"Insert INTO WorkLogInfo (SCardNumber,ComputerName,sCommand,sNote) VALUES('513821199201169013', '234', '客户端结帐', '黄金VIP，首次从客户端登陆')"
    conn.Execute(sql_statement)
    # time.sleep(5)
    sql_statement = u"Insert INTO WorkLogInfo (SCardNumber,ComputerName,sCommand,sNote) VALUES('513821199201169013', '235', '客户端结帐', '黄金VIP，首次从客户端登陆')"
    conn.Execute(sql_statement)
    # time.sleep(5)
    #
    # sql_statement = u"Insert INTO WorkLogInfo (SCardNumber,ComputerName,sCommand,sNote) VALUES('513821199107148030', '35', '刷卡计费', '钻石VIP，首次从客户端登陆')"
    # conn.Execute(sql_statement)
    # time.sleep(3)
    # sql_statement = u"Insert INTO WorkLogInfo (SCardNumber,ComputerName,sCommand,sNote) VALUES('513821199107148030', '', '刷卡计费', '管理员卡，首次从客户端登陆')"
    # conn.Execute(sql_statement)
    # time.sleep(3)
    # sql_statement = u"Insert INTO WorkLogInfo (SCardNumber,ComputerName,sCommand,sNote) VALUES('513821199107148030', '', '刷卡计费', '黄金VIP，首次从客户端登陆')"
    # conn.Execute(sql_statement)
    # time.sleep(3)
    sql_statement = u"Insert INTO WorkLogInfo (SCardNumber,ComputerName,sCommand,sNote) VALUES('513821199107148030', '', '刷卡计费', '铂金会员，首次从客户端登陆')"
    conn.Execute(sql_statement)
    conn.Close()

    # import bprocess.playSound
    # import config
    # tem = bprocess.playSound.PlaySound('playSound')
    # tem.setDaemon(True)
    # tem.start()
    # dao = workLogInfoDao()
    # maxid = dao.getMaxID(db, sysdb)
    # lastid = maxid - 8
    # list = dao.getLogs(db, sysdb, lastid)
    # if list:
    #     for temp in list:
    #         if temp['sCommand'] == u'客户端登录':
    #             for key in temp:
    #                 print "%s:%s" % (key, temp[key])
    #             print '\n'
    #             temp['type'] = 'online'
    #             config.queue.put(temp)
    #             time.sleep(2)
    # else:
    #     print("none")
