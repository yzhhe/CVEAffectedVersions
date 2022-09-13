#! -*- coding utf-8 -*-
# ! @Time  :2019/7/4 15:46
# ! Author :Frank Zhang
# ! @File  :ReadExcelDemo.py
# ！SoftWare PyChart 5.0.3
# ! Python Version 3.7
import xlrd
import time
from datetime import datetime
from xlrd import xldate_as_tuple
import  os

def numTodate(iRow,iCol,sFile):
    if not os.path.exists(sFile):
        print('文件路径不存在')
        return
    wb = xlrd.open_workbook(sFile)
    sheet1 = wb.sheet_by_index(0)

    sCell = sheet1.cell_value(iRow, iCol)

    # Python读Excel，返回的单元格内容的类型有5种：
    # ctype： 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
    ctype = sheet1.cell(iRow, iCol).ctype

    # ctype =3,为日期
    if ctype == 3:
        date = datetime(*xldate_as_tuple(sCell, 0))
        cell = date.strftime('%Y-%m-%d')  # ('%Y/%m/%d %H:%M:%S')
        # print(cell)
        return cell

    # ctype =1，为字符串
    elif ctype == 1:
        if isVaildDate(sCell):
            t1 = time.strptime(sCell, "%Y-%m-%d")
            sDate = changeStrToDate(t1, "yyyy-mm-dd")
            # print(sDate)
            return sDate
    else:
        pass


def formatDay(sDay, sFormat):
    sYear = str(sDay.year)
    sMonth = str(sDay.month)
    sDay = str(sDay.day)

    if sFormat == "yyyy-mm-dd":
        sFormatDay = sYear + "-" + sMonth.zfill(2) + "-" + sDay.zfill(2)
    elif sFormat == "yyyy/mm/dd":
        sFormatDay = sYear + "/" + sMonth.zfill(2) + "/" + sDay.zfill(2)
    else:
        sFormatDay = sYear + "-" + sMonth + "-" + sDay

    return sFormatDay


"""
功能：判断是否为日期
"""


def isVaildDate(sDate):
    try:
        if ":" in sDate:
            time.strptime(sDate, "%Y-%m-%d %H:%M:%S")
        else:
            time.strptime(sDate, "%Y-%m-%d")
        return True
    except:
        return False


"""
   功能：把字符串格式的日期转换为格式化的日期，如把2019-7-1转换为2019-07-01
"""


def changeStrToDate(sDate, sFormat):
    sYear = str(sDate.tm_year)
    sMonth = str(sDate.tm_mon)
    sDay = str(sDate.tm_mday)

    if sFormat == "yyyy-mm-dd":
        sFormatDay = sYear + "-" + sMonth.zfill(2) + "-" + sDay.zfill(2)
    elif sFormat == "yyyy/mm/dd":
        sFormatDay = sYear + "/" + sMonth.zfill(2) + "/" + sDay.zfill(2)
    else:
        sFormatDay = sYear + "-" + sMonth + "-" + sDay

    return sFormatDay


# if __name__ == "__main__":
#     numTodate(1,1,r'D:\北交\漏洞\测试代码\Linux Kernel Release Time.xls')