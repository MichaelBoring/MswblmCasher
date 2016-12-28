#-*-coding:utf-8-*-
__author__ = 'Administrator'
import time
import string
import win32com.client
import pythoncom
import sys
import config
reload(sys)
sys.setdefaultencoding("utf-8")

class jftypedefineDao():
    def __init__(self):
        '''
        init com
        '''
        pythoncom.CoInitialize()

    def getJftypedefine(self, db, sysdb):
        list = []
        config.jftype = {}
        config.memtype = {}
        dns = r'Provider=Microsoft.Jet.OLEDB.4.0;User ID=ikmdb;Data Source=%s;Persist Security Info=False;Jet OLEDB:System database=%s' % (db, sysdb)
        sql = r"SELECT iif (IsNull(CardJFCode), 0, CardJFCode) AS CardJFCode, iif (IsNull(CardJFName), '', CardJFName) AS CardJFName FROM [JFTypeDefine]"
        conn = win32com.client.Dispatch(r'ADODB.Connection')
        conn.Open(dns)
        rs = win32com.client.Dispatch(r'ADODB.Recordset')
        rs.Open(sql, conn, 1, 3)
        f = {}
        while not rs.EOF:
            d = {}
            d['CardJFCode'] = int(rs('CardJFCode'))
            d['CardJFName'] = str(rs('CardJFName')).strip()
            config.jftype[d['CardJFName']] = d['CardJFCode']
            config.memtype[d['CardJFCode']] = d['CardJFName']
            f[str(rs('CardJFName')).strip()] = int(rs('CardJFCode'))
            list.append(d)
            rs.MoveNext()
        rs.Close()
        conn.Close()
        return list

if __name__ == '__main__':
    doa = jftypedefineDao()
    db = r"C:\4-7\NetHouseSer.mdb"
    sysdb = r"C:\4-7\System.mdw"
    list = doa.getJftypedefine(db, sysdb)
    if list:
        print(list)