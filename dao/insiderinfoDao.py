#-*-coding:utf-8-*-
__author__ = "Administrator"
import time
import string
import win32com.client
import pythoncom
import sys
import config
reload(sys)
sys.setdefaultencoding("utf-8")

class insiderinfoDao():
    def __init__(self):
        """
        init com
        """
        pythoncom.CoInitialize()

    def getInsiderMoney(self, db, sysdb, insiderNumber):
        d = None
        dns = r"Provider=Microsoft.Jet.OLEDB.4.0;User ID=ikmdb;Data Source=%s;Persist Security Info=False;Jet OLEDB:System database=%s" % (db, sysdb)
        sql = r'SELECT TOP 1 iif ( IsNull(TransactName), "", TransactName ) AS TransactName, iif ( IsNull(SCardType), "", SCardType ) AS SCardType, iif ( IsNull(InsiderMoney), "", InsiderMoney ) AS InsiderMoney FROM [InsiderInfo] WHERE InsiderNumber = "%s"' % insiderNumber
        conn = win32com.client.Dispatch(r"ADODB.Connection")
        conn.Open(dns)
        rs = win32com.client.Dispatch(r"ADODB.Recordset")
        rs.Open(sql, conn, 1, 3)
        while not rs.EOF:
            d = {}
            d["Name"] = str(rs("TransactName")).strip()
            d["InsiderMoney"] = string.atof(str(rs("InsiderMoney")).strip())
            d["SCardType"] = string.atoi(str(rs("SCardType")).strip())
            rs.MoveNext()
        rs.Close()
        conn.Close()
        return d

    def getMaxID(self, db, sysdb):
        maxid = 0;
        dns = r"Provider=Microsoft.Jet.OLEDB.4.0;User ID=ikmdb;Data Source=%s;Persist Security Info=False;Jet OLEDB:System database=%s" % (db, sysdb)
        sql = r'SELECT MAX(ID) AS ID FROM `InsiderInfo`;'
        conn = win32com.client.Dispatch(r"ADODB.Connection")
        conn.Open(dns)
        rs = win32com.client.Dispatch(r"ADODB.Recordset")
        rs.Open(sql, conn, 1, 3)
        while not rs.EOF:
            maxid = int(rs("ID"))
            rs.MoveNext()
        rs.Close()
        conn.Close()
        return maxid

    def getInsiderinfo(self, db, sysdb, lastid):
        list = []
        dns = r"Provider=Microsoft.Jet.OLEDB.4.0;User ID=ikmdb;Data Source=%s;Persist Security Info=False;Jet OLEDB:System database=%s" % (db, sysdb)
        sql = r'SELECT TOP 100 ID, iif ( IsNull(InsiderNumber), "", InsiderNumber ) AS InsiderNumber, iif ( IsNull(SCardType), 0, SCardType ) AS SCardType, iif ( IsNull(TransactName), "", TransactName ) AS TransactName, iif ( IsNull(TransactTime), "", TransactTime ) AS TransactTime, iif ( IsNull(InsiderMoney), 0, InsiderMoney ) AS InsiderMoney FROM [InsiderInfo] WHERE ID > {0}  ORDER BY ID'.format(str(lastid))
        conn = win32com.client.Dispatch(r"ADODB.Connection")
        conn.Open(dns)
        rs = win32com.client.Dispatch(r"ADODB.Recordset")
        rs.Open(sql, conn, 1, 3)
        while not rs.EOF:
            d = {}
            d["CurrentID"] = int(rs("ID"))
            d["InsiderNumber"] = str(rs("InsiderNumber")).strip()
            if(config.isDebug):
                d["InsiderNumber"] = '510107199007114395'
            d["SCardType"] = int(rs("SCardType"))
            d["TransactName"] = str(rs("TransactName")).strip()
            d["TransactTime"] = int(rs("TransactTime"))
            d["InsiderMoney"] = string.atof(str(rs("InsiderMoney")).strip())
            list.append(d)
            rs.MoveNext()
        rs.Close()
        conn.Close()
        return list

if __name__ == "__main__":
    doa = insiderinfoDao()
    db = r"U:\Insider.mdb"
    sysdb = r"U:\System.mdw"
    insiderNumber = r"92140202199609196521"
    d = doa.getInsiderMoney(db, sysdb, insiderNumber)
    if d:
        print(d)
    else:
        print("none")