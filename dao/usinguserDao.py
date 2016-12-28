#-*-coding:utf-8-*-
__author__ = 'Administrator'
import time
import string
import win32com.client
import pythoncom
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class usinguserDao():
    def __init__(self):
        '''
        init com
        '''
        pythoncom.CoInitialize()

    def getusinguser(self, db, sysdb):
        list = []
        dns = r'Provider=Microsoft.Jet.OLEDB.4.0;User ID=ikmdb;Data Source=%s;Persist Security Info=False;Jet OLEDB:System database=%s' % (db, sysdb)
        sql = r"SELECT iif (IsNull(Area), 0, Area) AS Area, iif (IsNull(Insider), 0, Insider) AS Insider, iif (IsNull(ComputerName), '', ComputerName) AS ComputerName, iif (IsNull(SCardType), 0, SCardType) AS SCardType FROM [UsingUser]"
        conn = win32com.client.Dispatch(r'ADODB.Connection')
        conn.Open(dns)
        rs = win32com.client.Dispatch(r'ADODB.Recordset')
        rs.Open(sql, conn, 1, 3)
        while not rs.EOF:
            d = {}
            d['Area'] = int(rs('Area'))
            d['Insider'] = int(int(rs('Insider')) != 0)
            d['SCardType'] = int(rs('SCardType'))
            d['ComputerName'] = str(rs('ComputerName')).strip()
            list.append(d)
            rs.MoveNext()
        rs.Close()
        conn.Close()
        return list

if __name__ == '__main__':
    db = r""
    sysdb = r""
    dao = usinguserDao()
    list = dao.getusinguser(db, sysdb)
    if list:
        print(list)
    else:
        print("none")