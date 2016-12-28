#-*-coding:utf-8-*-
__author__ = "Administrator"
import win32com.client
import pythoncom
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class insiderinfoDao():
    def __init__(self):
        pythoncom.CoInitialize()


    def getInsiderinfo(self, db, sysdb):
        list = []
        dns = r"Provider=Microsoft.Jet.OLEDB.4.0;User ID=ikmdb;Data Source=%s;Persist Security Info=False;Jet OLEDB:System database=%s" % (db, sysdb)
        conn = win32com.client.Dispatch(r"ADODB.Connection")
        conn.Open(dns)
        sql_statement = u"update [InsiderInfo] set SCardType = Switch(SCardType = 0, 3, SCardType = 3, 0, True, SCardType)"
        conn.Execute(sql_statement)
        conn.Close()

    def getInsiderinfo1(self, db, sysdb):
        dns = r"Provider=Microsoft.Jet.OLEDB.4.0;User ID=ikmdb;Data Source=%s;Persist Security Info=False;Jet OLEDB:System database=%s" % (db, sysdb)
        sql = r'SELECT count(*) AS s FROM InsiderInfo WHERE SCardType = 0'
        # , iif(IsNull(SCardType), 0, SCardType)
        # AS
        # SCardType
        conn = win32com.client.Dispatch(r"ADODB.Connection")
        conn.Open(dns)
        rs = win32com.client.Dispatch(r"ADODB.Recordset")
        rs.Open(sql, conn, 1, 3)
        while not rs.EOF:
            print rs("s")
            rs.MoveNext()
        rs.Close()
        conn.Close()
        return list

if __name__ == "__main__":
    doa = insiderinfoDao()
    db = r"C:/1/Insider.mdb"
    sysdb = r"C:/1/System.mdw"
    d = doa.getInsiderinfo1(db, sysdb)
