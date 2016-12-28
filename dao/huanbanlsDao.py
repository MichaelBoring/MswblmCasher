#-*-coding:utf-8-*-
__author__ = 'Administrator'
import time
import string
import win32com.client
import pythoncom
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class huanbanlsDao():
    def __init__(self):
        '''
        init com
        '''
        pythoncom.CoInitialize()

    def getHuanbanls(self, db, sysdb, lastid):
        list = []
        dns = r'Provider=Microsoft.Jet.OLEDB.4.0;User ID=ikmdb;Data Source=%s;Persist Security Info=False;Jet OLEDB:System database=%s' % (db, sysdb)
        sql = r"SELECT TOP 100 ID, iif (IsNull(OldName), '', OldName) AS OldName, iif (IsNull(OldTime), '', OldTime) AS OldTime, iif ( IsNull(OldMoney), 0, OldMoney ) AS OldMoney, iif (IsNull(CurName), '', CurName) AS CurName, iif (IsNull(CurTime), '', CurTime) AS CurTime, iif ( IsNull(InsiderMoney), 0, InsiderMoney ) AS InsiderMoney, iif ( IsNull(PayMoney), 0, PayMoney ) AS PayMoney, iif ( IsNull(SpareMoney), 0, SpareMoney ) AS SpareMoney FROM [HuanBanLS] WHERE ID > {0} ORDER BY ID".format(str(lastid))
        conn = win32com.client.Dispatch(r'ADODB.Connection')
        conn.Open(dns)
        rs = win32com.client.Dispatch(r'ADODB.Recordset')
        rs.Open(sql, conn, 1, 3)
        while not rs.EOF:
            d = {}
            d['CurrentID'] = int(rs('ID'))
            d['OldName'] = str(rs('OldName')).strip()
            d['OldTime'] = str(rs('OldTime')).strip()
            d['OldMoney'] = string.atof(str(rs('OldMoney')).strip())
            d['CurName'] = str(rs('CurName')).strip()
            d['CurTime'] = str(rs('CurTime')).strip()
            d['InsiderMoney'] = string.atof(str(rs('InsiderMoney')).strip())
            d['PayMoney'] = string.atof(str(rs('PayMoney')).strip())
            d['SpareMoney'] = string.atof(str(rs('SpareMoney')).strip())
            list.append(d)
            rs.MoveNext()
        rs.Close()
        conn.Close()
        return list

    def getMaxID(self):
        maxid = 0
        dns = r'Provider=Microsoft.Jet.OLEDB.4.0;User ID=ikmdb;Data Source=%s;Persist Security Info=False;Jet OLEDB:System database=%s' % (db, sysdb)
        sql = r'SELECT MAX(ID) AS ID FROM `HuanBanLS`;'
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

if __name__ == '__main__':
    doa = huanbanlsDao()
    db = r"C:\4-7\NetHouseSer.mdb"
    sysdb = r"C:\4-7\System.mdw"
    lastid = 1350
    list = doa.getHuanbanls(db, sysdb, lastid)
    if list:
        print(list)