
import sys
import os
import xlrd
from xlutils.copy import copy
import Repository
import readExcelDate


def get_targetMINPubTime(edition_num,edition_path):
    rexcel = xlrd.open_workbook(edition_path)
    table = rexcel.sheets()[0]
    nrows = table.nrows
    pub_timeList = []
    for row in range(1,nrows):
        # print(table.cell(row,0).value)
        source_target = table.cell(row, 0).value
        if source_target is not None:
            if  str(source_target).startswith(str(edition_num)) :
                pub_time = readExcelDate.numTodate(row,1,edition_path)
                pub_timeList.append(pub_time)
    return min(pub_timeList)

def get_targetPubTime(edition_num,edition_path):
    rexcel = xlrd.open_workbook(edition_path)
    table = rexcel.sheets()[0]
    nrows = table.nrows
    for row in range(1,nrows):
        # print(table.cell(row,0).value)
        source_target = table.cell(row, 0).value
        if source_target == edition_num:
            pub_time = readExcelDate.numTodate(row,1,edition_path)
            return  pub_time

def updateSheetOne(writeTable,result_path,kernelPub_time,kernel_edition_num,pub_path,allverion_path):
    rexcel = xlrd.open_workbook(result_path)  # 用wlrd提供的方法读取一个excel文件
    # 获取sheet0的行列
    readTable = rexcel.sheets()[1]
    nrows = readTable.nrows
    ncols = readTable.ncols

    # 找到对应的cve编号
    for row in range(1, nrows):
        # print(table.cell(row,0).value)
        cve_num = readTable.cell(row, 0).value.split('/')[-1]
        # 找到当前CVE的发布时间和影响版本号
        cve_edition = get_cve_edition(allverion_path, cve_num)
        cve_pubtime = curCve_pubtime(pub_path, cve_num)
        print('cve：%s,edition:%s,pubtime:%s' % (cve_num, cve_edition, cve_pubtime))
        if cve_pubtime == None:
            cve_pubtime = ''
        elif cve_edition == None:
            cve_edition = ''
        # 条件是cve发布时间大于内核发布时间且影响版本号大于被测内核版本号
        if cve_pubtime >= kernelPub_time and cve_edition >= kernel_edition_num:
            print('||-----cve：%s,edition:%s,pubtime:%s' % (cve_num, cve_edition, cve_pubtime))
            writeTable.write(row, ncols, 'p')
        # 个别没有发布时间
        elif cve_edition >= kernel_edition_num:
            print('||-----cve：%s,edition:%s,pubtime:%s' % (cve_num, cve_edition, cve_pubtime))
            writeTable.write(row, ncols, 'noTimeP')
        # 个别没有发布版本？应该不会
        elif cve_pubtime >= kernelPub_time:
            print('||-----cve：%s,edition:%s,pubtime:%s' % (cve_num, cve_edition, cve_pubtime))
            writeTable.write(row, ncols, 'noVersionP')


def updateSheetZero(result_path,kernelPub_time,kernel_edition_num,pub_path,allverion_path):
    rexcel = xlrd.open_workbook(result_path)  # 用wlrd提供的方法读取一个excel文件
    #获取sheet0的行列
    readTable = rexcel.sheets()[0]
    nrows = readTable.nrows
    ncols = readTable.ncols

    excel = copy(rexcel)
    writeTable = excel.get_sheet(0)
    writeTable.write(0, ncols, 'Required')


    #找到对应的cve编号
    for row in range(1,nrows):
        # print(table.cell(row,0).value)
        cve_num = readTable.cell(row, 0).value.split('/')[-1]
        #找到当前CVE的发布时间和影响版本号
        cve_edition = get_cve_edition(allverion_path,cve_num)
        cve_pubtime = curCve_pubtime(pub_path,cve_num)
        print('cve：%s,edition:%s,pubtime:%s' % (cve_num,cve_edition,cve_pubtime))
        if cve_pubtime == None:
            cve_pubtime = ''
        elif cve_edition== None:
            cve_edition=''
        #条件是cve发布时间大于内核发布时间且影响版本号大于被测内核版本号
        if cve_pubtime >= kernelPub_time and cve_edition >= kernel_edition_num:
            print('||-----cve：%s,edition:%s,pubtime:%s' % (cve_num, cve_edition, cve_pubtime))
            writeTable.write(row,ncols,'p')
        #个别没有发布时间
        elif  cve_edition >= kernel_edition_num:
            print('||-----cve：%s,edition:%s,pubtime:%s' % (cve_num, cve_edition, cve_pubtime))
            writeTable.write(row, ncols, 'noTimeP')
        # 个别没有发布版本？应该不会
        elif cve_pubtime >= kernelPub_time:
            print('||-----cve：%s,edition:%s,pubtime:%s' % (cve_num, cve_edition, cve_pubtime))
            writeTable.write(row, ncols, 'noVersionP')
    writeTable = excel.get_sheet(1)
    updateSheetOne(writeTable,result_path, kernelPub_time, kernel_edition_num, pub_path, allverion_path)

    excel.save(r'D:\北交\漏洞\测试代码\Result2.xls')


def curCve_pubtime(pub_path,cve_num):
    pubList=os.listdir(pub_path)
    cve_num = cve_num + '.txt'
    if cve_num in pubList:
        cve_pubtime = Repository.get_file_line_list(os.path.join(pub_path,cve_num))[0]
        return cve_pubtime

def get_cve_edition(allverion_path,cve_num):
    versionList = os.listdir(allverion_path)
    cve_num = cve_num + '.txt'
    if cve_num in versionList:
        cve_edition = Repository.get_file_line_list(os.path.join(allverion_path, cve_num))[-1]
        return cve_edition.split(' ')[-1]



def prompt():
    print('''用户输入参数为：结果文件位置 被测版本号''')
    sys.exit(0)


if __name__ == '__main__':


    # try:
    #     #相对路径
    #     result_path = sys.argv[1]
    #     if '/' not in result_path:
    #         prompt()
    #     # 启动命令，new或者cont
    #     edition_num = sys.argv[2]
    # except IndexError:
    #     prompt()
    result_path = r'D:\北交\漏洞\测试代码\Result.xls'
    edition_path = r'D:\北交\漏洞\测试代码\Linux Kernel Release Time.xls'
    pub_path = r'D:\北交\漏洞\patch\all_cve_version\publish_date'
    allverion_path = r'D:\北交\漏洞\patch\all_cve_version'
    kernel_edition_num ='4.19.90'

    #拿到被测版本号的时间
    kernelPub_time = get_targetPubTime(kernel_edition_num,edition_path)
    if kernelPub_time == None:
        print('此版本没有发布，请重新确认')
    else:
        #进行目标excel的标记
        updateSheetZero(result_path,kernelPub_time,kernel_edition_num,pub_path,allverion_path)


