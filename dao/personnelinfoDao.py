#-*-coding:utf-8-*-
__author__ = "Administrator"
import time
import string
import win32com.client
import pythoncom
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class personnelinfoDao():
    def __init__(self):
        """
        init com
        """
        pythoncom.CoInitialize()

    def getMaxID(self, db, sysdb):
        maxid = 0
        dns = r'Provider=Microsoft.Jet.OLEDB.4.0;User ID=ikmdb;Data Source=%s;Persist Security Info=False;Jet OLEDB:System database=%s' % (db, sysdb)
        sql = r'SELECT MAX(ID) AS ID FROM `personnelinfo`;'
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

    def getPersonnelinfo(self, db, sysdb, lastid):
        list = []
        dns = r'Provider=Microsoft.Jet.OLEDB.4.0;User ID=ikmdb;Data Source=%s;Persist Security Info=False;Jet OLEDB:System database=%s' % (db, sysdb)
        sql = r'SELECT TOP 100 ID, iif (IsNull(NAME), "", NAME) as NAME, iif ( IsNull(Insider), "0", Insider) AS Insider, iif ( IsNull(ComputerName), "", ComputerName) AS ComputerName, iif ( IsNull(InsiderNumber), "", InsiderNumber) AS InsiderNumber, iif (IsNull(SCardType), 0, SCardType) AS SCardType, iif (IsNull(BeginTime), "", BeginTime) AS BeginTime, iif (IsNull(EndTime), "", EndTime) AS EndTime, iif (IsNull(YSMoney), 0, YSMoney) AS YSMoney, iif (IsNull(Other1), "", Other1) AS Other1, iif (IsNull(Other2), "", Other2) AS Other2 FROM [PersonnelInfo] WHERE ID > {0}  ORDER BY ID'.format(str(lastid))
        conn = win32com.client.Dispatch(r"ADODB.Connection")
        conn.Open(dns)
        rs = win32com.client.Dispatch(r"ADODB.Recordset")
        rs.Open(sql, conn, 1, 3)
        while not rs.EOF:
            d = {}
            d["CurrentID"] = int(rs("ID"))
            d["Name"] = str(rs("NAME")).strip()
            d["Insider"] = string.atoi(str(rs("Insider")).strip()) != 0
            d["ComputerName"] = str(rs("ComputerName")).strip()
            d["InsiderNumber"] = str(rs("InsiderNumber")).strip()
            d["SCardType"] = int(rs("SCardType"))
            d["BeginTime"] = str(rs("BeginTime")).strip()
            d["EndTime"] = str(rs("EndTime")).strip()
            d["YSMoney"] = string.atof(str(rs("YSMoney")).strip())
            d["EverLogin"] = str(rs("Other1")).strip()
            d["GiftMoney"] = str(rs("Other2")).strip()
            list.append(d)
            rs.MoveNext()
        rs.Close()
        conn.Close()
        return list

if __name__ == "__main__":
    dao = personnelinfoDao()
    db = r"C:\4-7\NetHouseSer.mdb"
    sysdb = r"C:\4-7\System.mdw"
    lastid=330250
    list = dao.getPersonnelinfo(db, sysdb, lastid)
    if list:
        print(list)
    else:
        print("none")