#coding=utf-8
import  random
import Repository
import IsCVEInWholeProject
import shutil
import os
import re
import GetModuleDiffIn
import VersionNumberAndExistTime
import xlrd
import xlwt
import sys
sys.setrecursionlimit(1000000)
from xlutils.copy import copy

global cve_name
ct=0


result_file_name = 'py2_result_data.txt'
result_file_name2 = 'py2_suspected_result_data.txt'



with open(result_file_name, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
    f.write("This is result.\n")
with open(result_file_name2, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
    f.write("These cve may be exist.\n")


def is_diff_segment_in_files(cve_dir_path,diff_segment, diff_segment_index, project_dir_path, diff_file_path):
    #for file_path in Repository.get_all_file_path_list(project_dir_path):    #得到linux kernel二级文件夹下所有文件路径（递归）
    res=VersionNumberAndExistTime.is_diff_segment_in_file(diff_segment, diff_segment_index, project_dir_path,
                                                             diff_file_path)

    if res==1:
        print('\rIn ' + project_dir_path)
        with open(result_file_name, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
            f.write(diff_file_path+os.path.basename(diff_file_path)+'\r   In ' + project_dir_path+'\n')
        f.close()
        with open(cve_dir_path+"/"+"score.txt") as f:
            score=f.readlines()
        f.close()
        rexcel = xlrd.open_workbook("Result.xls")  # 用wlrd提供的方法读取一个excel文件
        rows = rexcel.sheets()[0].nrows  # 用wlrd提供的方法获得现在已有的行数
        excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
        table = excel.get_sheet(0)  # 用xlwt对象的方法获得要操作的sheet
        row = rows
        table.write(row, 0, cve_dir_path)  # xlwt对象的写方法，参数分别是行、列、值
        table.write(row, 1, os.path.basename(diff_file_path).replace('#~', '/'))
        table.write(row, 2, project_dir_path)
        table.write(row, 3, score)
        excel.save("Result.xls")  # xlwt对象的保存方法，这时便覆盖掉了原来的excel
        return True
    if res==2:
        print('\r Probably In ' + project_dir_path)
        with open(result_file_name2, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
            f.write(diff_file_path+os.path.basename(diff_file_path) + '\r   Probably In ' + project_dir_path + '\n')
        f.close()
        with open(cve_dir_path+"/"+"score.txt",'r') as f:
            score=f.readlines()
        f.close()
        rexcel = xlrd.open_workbook("Result.xls")  # 用wlrd提供的方法读取一个excel文件
        rows = rexcel.sheets()[1].nrows  # 用wlrd提供的方法获得现在已有的行数
        excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
        table = excel.get_sheet(1)  # 用xlwt对象的方法获得要操作的sheet
        row = rows
        table.write(row, 0, cve_dir_path)  # xlwt对象的写方法，参数分别是行、列、值
        table.write(row, 1, os.path.basename(diff_file_path).replace('#~', '/'))
        table.write(row, 2, project_dir_path)
        table.write(row, 3, score)
        excel.save("Result.xls")  # xlwt对象的保存方法，这时便覆盖掉了原来的excel
        return True
    return False

def is_diff_segment_in_files1(cve_dir_path,diff_segment, diff_segment_index, project_dir_path, diff_file_path):

    #for file_path in Repository.get_all_file_path_list(project_dir_path):    #得到linux kernel二级文件夹下所有文件路径（递归）
    res=VersionNumberAndExistTime.is_diff_segment_in_file(diff_segment, diff_segment_index, project_dir_path,
                                                             diff_file_path)
    global ct
    if res==1:

        ct += 1
        print(ct)
        return ct, project_dir_path

    if res==2:
        return ct, project_dir_path

    return ct,project_dir_path

def is_diff_segment_in_files2(cve_dir_path,diff_segment, diff_segment_index, project_dir_path, diff_file_path):
    #for file_path in Repository.get_all_file_path_list(project_dir_path):    #得到linux kernel二级文件夹下所有文件路径（递归）
    res=VersionNumberAndExistTime.is_diff_segment_in_file(diff_segment, diff_segment_index, project_dir_path,diff_file_path)
    if res==1:
        print('\r In ' + project_dir_path)
        with open(result_file_name2, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
            f.write(diff_file_path + os.path.basename(diff_file_path) + '\r   In ' + project_dir_path + '\n')
        f.close()
        with open(cve_dir_path+"/"+"score.txt",'r') as f:
            score=f.readlines()
        f.close()
        rexcel = xlrd.open_workbook("Result.xls")  # 用wlrd提供的方法读取一个excel文件
        rows = rexcel.sheets()[0].nrows  # 用wlrd提供的方法获得现在已有的行数
        excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
        table = excel.get_sheet(0)  # 用xlwt对象的方法获得要操作的sheet
        row = rows
        table.write(row, 0, cve_dir_path)  # xlwt对象的写方法，参数分别是行、列、值
        table.write(row, 1, os.path.basename(diff_file_path).replace('#~', '/'))
        table.write(row, 2, project_dir_path)
        table.write(row, 3, score)
        excel.save("Result.xls")  # xlwt对象的保存方法，这时便覆盖掉了原来的excel
        return True

    if res==2:
        print('\r Probably In ' + diff_file_path)
        with open(result_file_name2, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
            f.write(diff_file_path+os.path.basename(diff_file_path) + '\r   Probably In ' + project_dir_path + '\n')
        f.close()
        with open(cve_dir_path+"/"+"score.txt",'r') as f:
            score=f.readlines()
        f.close()
        rexcel = xlrd.open_workbook("Result.xls")  # 用wlrd提供的方法读取一个excel文件
        rows = rexcel.sheets()[1].nrows  # 用wlrd提供的方法获得现在已有的行数
        excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
        table = excel.get_sheet(1)  # 用xlwt对象的方法获得要操作的sheet
        row = rows
        table.write(row, 0, cve_dir_path)  # xlwt对象的写方法，参数分别是行、列、值
        table.write(row, 1, os.path.basename(diff_file_path).replace('#~', '/'))
        table.write(row, 2, project_dir_path)
        table.write(row, 3, score)
        excel.save("Result.xls")  # xlwt对象的保存方法，这时便覆盖掉了原来的excel
        return True
    return False

def is_diff_segment_in_files3(cve_dir_path,diff_segment, diff_segment_index, project_dir_path, diff_file_path):
    #for file_path in Repository.get_all_file_path_list(project_dir_path):    #得到linux kernel二级文件夹下所有文件路径（递归）
    res=VersionNumberAndExistTime.is_diff_segment_in_file(diff_segment, diff_segment_index, project_dir_path,diff_file_path)

    if res==1:
        print('\r Probably In ' + project_dir_path)
        with open(result_file_name2, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
            f.write(diff_file_path + os.path.basename(diff_file_path) + '\r   Probably In ' + project_dir_path + '\n')
        f.close()
        with open(cve_dir_path + "/" + "score.txt", 'r') as f:
            score = f.readlines()
        f.close()
        rexcel = xlrd.open_workbook("Result.xls")  # 用wlrd提供的方法读取一个excel文件
        rows = rexcel.sheets()[1].nrows  # 用wlrd提供的方法获得现在已有的行数
        excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
        table = excel.get_sheet(1)  # 用xlwt对象的方法获得要操作的sheet
        row = rows
        table.write(row, 0, cve_dir_path)  # xlwt对象的写方法，参数分别是行、列、值
        table.write(row, 1, os.path.basename(diff_file_path).replace('#~', '/'))
        table.write(row, 2, project_dir_path)
        table.write(row, 3, score)
        excel.save("Result.xls")  # xlwt对象的保存方法，这时便覆盖掉了原来的excel
        return True

    if res==2:
        print('\r Probably In ' + project_dir_path)
        with open(result_file_name2, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
            f.write(diff_file_path+os.path.basename(diff_file_path) + '\r   Probably In ' + project_dir_path + '\n')
        f.close()
        with open(cve_dir_path+"/"+"score.txt",'r') as f:
            score=f.readlines()
        f.close()
        rexcel = xlrd.open_workbook("Result.xls")  # 用wlrd提供的方法读取一个excel文件
        rows = rexcel.sheets()[1].nrows  # 用wlrd提供的方法获得现在已有的行数
        excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
        table = excel.get_sheet(1)  # 用xlwt对象的方法获得要操作的sheet
        row = rows
        table.write(row, 0, cve_dir_path)  # xlwt对象的写方法，参数分别是行、列、值
        table.write(row, 1, os.path.basename(diff_file_path).replace('#~', '/'))
        table.write(row, 2, project_dir_path)
        table.write(row, 3, score)
        excel.save("Result.xls")  # xlwt对象的保存方法，这时便覆盖掉了原来的excel
        return True
    return False

def is_diff_in_project_2(cve_dir_path,diff_file_path, project_dir_path):#单文件
    print(os.path.basename(diff_file_path))
    diff_list=[]
    diff_list=GetModuleDiffIn.get_diff_segment_list(diff_file_path)[:]
    #count = len(GetModuleDiffIn.get_diff_segment_list(diff_file_path))
    count=len(diff_list)
    print(count)
    if count==1:          #单@@
        for diff_segment_index, diff_segment in enumerate(diff_list):
            if not is_diff_segment_in_files2(cve_dir_path,diff_segment, diff_segment_index, project_dir_path, diff_file_path):
                return False
        return True
    else:                #多@@
        global ct
        ct = 0
        res = 0
        for diff_segment_index, diff_segment in enumerate(diff_list):
            res,file_path=is_diff_segment_in_files1(cve_dir_path, diff_segment, diff_segment_index, project_dir_path, diff_file_path)
        # print("res",res)
        if res==count:      #所有@@匹配

            print('\r In ' + project_dir_path)
            with open(result_file_name, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
                f.write(diff_file_path + os.path.basename(diff_file_path) + '\r   In ' + project_dir_path + '\n')
            f.close()
            with open(cve_dir_path+"/"+"score.txt") as f:
                score=f.readlines()
            f.close()
            rexcel = xlrd.open_workbook("Result.xls")  # 用wlrd提供的方法读取一个excel文件
            rows = rexcel.sheets()[0].nrows  # 用wlrd提供的方法获得现在已有的行数
            excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
            table = excel.get_sheet(0)  # 用xlwt对象的方法获得要操作的sheet
            row = rows
            table.write(row, 0, cve_dir_path)  # xlwt对象的写方法，参数分别是行、列、值
            table.write(row, 1, os.path.basename(diff_file_path).replace('#~', '/'))
            table.write(row, 2, project_dir_path)
            table.write(row, 3, score)
            excel.save("Result.xls")  # xlwt对象的保存方法，这时便覆盖掉了原来的excel
            return True

        elif res!=0:           #部分@@匹配
            #print("=========")
            print('\r Probably In ' + project_dir_path)
            with open(result_file_name2, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
                f.write(diff_file_path + os.path.basename(diff_file_path) + '\r   Probably In ' + project_dir_path + '\n')
            f.close() #file_name2的文件
            with open(cve_dir_path+"/"+"score.txt",'r') as f:
                score=f.readlines()
            f.close()
            rexcel = xlrd.open_workbook("Result.xls")  # 用wlrd提供的方法读取一个excel文件
            rows = rexcel.sheets()[1].nrows  # 用wlrd提供的方法获得现在已有的行数
            excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
            table = excel.get_sheet(1)  # 用xlwt对象的方法获得要操作的sheet
            row = rows
            table.write(row, 0, cve_dir_path)  # xlwt对象的写方法，参数分别是行、列、值
            table.write(row, 1, os.path.basename(diff_file_path).replace('#~', '/'))
            table.write(row, 2, project_dir_path)
            table.write(row, 3, score)
            excel.save("Result.xls")  # xlwt对象的保存方法，这时便覆盖掉了原来的excel
            return True
        return False


def is_diff_in_project_3(cve_dir_path,diff_file_path, project_dir_path): #多文件
    print(os.path.basename(diff_file_path))

    for diff_segment_index, diff_segment in enumerate(GetModuleDiffIn.get_diff_segment_list(diff_file_path)):
        if not is_diff_segment_in_files3(cve_dir_path,diff_segment, diff_segment_index, project_dir_path, diff_file_path):
            return False
    return True




def is_diff_in_project(diff_file_path, project_dir_path):
    global result_file_name
    for file_path in Repository.get_all_file_path_list(project_dir_path):
        for diff_segment_index, diff_segment in enumerate(
                GetModuleDiffIn.get_diff_segment_list(diff_file_path)):
            if not VersionNumberAndExistTime.is_diff_segment_in_file(diff_segment, diff_segment_index,
                                                                     file_path,
                                                                     diff_file_path):
                print('\r' + diff_file_path.split('#~')[-1] + ' Not In ' + file_path)
                #print('\r' + diff_file_path.split('#~')[-1] + ' Not In ' + file_path, end='')
                break
        else:
            print('\r' + diff_file_path.split('#~')[-1] + ' In ' + file_path)
            return True
    return False


def is_cve_in_project(cve_dir_path, project_dir_path):
    if Repository.is_dir_empty(cve_dir_path):
        return False
    print (cve_dir_path)

    file_count=0
    for file_name in os.listdir(cve_dir_path):
        #print(file_name)
        if file_name != 'Source.txt' and not re.match(r'\(', file_name):
            #print(file_name)
            if file_name[-1]=='c' or file_name[-1]=='h':
                file_count+=1

    if file_count==1: #单文件
        for file_name in os.listdir(cve_dir_path):
            #print(file_name)
            if file_name != 'Source.txt' and not re.match(r'\(', file_name):
                #print(file_name)
                if file_name[-1]=='c' or file_name[-1]=='h':
                    diff_file_name = file_name
                    vuln_relative_path = diff_file_name.replace('#~', '/')
                    vuln_dir_path = os.path.join(project_dir_path, os.path.join(vuln_relative_path))
                    print(file_name)
                    print(vuln_dir_path)
                    if os.path.exists(vuln_dir_path):          #路径存在
                        if not is_diff_in_project_2(cve_dir_path,os.path.join(cve_dir_path, file_name), vuln_dir_path):
                            return False
                        return True
                    else:                                      #路径不存在
                        print (vuln_dir_path +'\n'+'Vuln_dir_path Not Exist')
                        #IsCVEInWholeProject.is_cve_in_whole_project(cve_dir_path, project_dir_path)
                        #with open(result_file_name, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
                            #f.write(vuln_dir_path +'\n'+'Vuln_dir_path Not Exist' + '\n')


    else:    #多文件
        for file_name in os.listdir(cve_dir_path):
            #print(file_name)
            if file_name != 'Source.txt' and not re.match(r'\(', file_name):
                #print(file_name)
                if file_name[-1]=='c' or file_name[-1]=='h':
                    diff_file_name = file_name
                    vuln_relative_path = diff_file_name.replace('#~', '/')
                    print( vuln_relative_path)
                    vuln_dir_path = os.path.join(project_dir_path, os.path.join(vuln_relative_path))
                    print(vuln_dir_path)
                    print(file_name)
                    if os.path.exists(vuln_dir_path):          #路径存在
                        if not is_diff_in_project_3(cve_dir_path,os.path.join(cve_dir_path, file_name), vuln_dir_path):
                            return False
                        else:
                            return True
                    else:                                      #路径不存在
                        print (vuln_dir_path +'\n'+'Vuln_dir_path Not Exist')
                        #IsCVEInWholeProject.is_cve_in_whole_project(cve_dir_path, project_dir_path)
                        #with open(result_file_name, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
                            #f.write(vuln_dir_path +'\n'+'Vuln_dir_path Not Exist' + '\n')


def fisrt_newExcel():
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('result_data')
    worksheet.write(0, 0, "CVE_number")
    worksheet.write(0, 1, "Patch_file")
    worksheet.write(0, 2, "Project_file")
    worksheet.write(0, 3, "Level")
    worksheet = workbook.add_sheet('suspected_result_data')
    worksheet.write(0, 0, "CVE_number")
    worksheet.write(0, 1, "Patch_file")
    worksheet.write(0, 2, "Project_file")
    worksheet.write(0, 3, "Level")
    workbook.save('Result.xls')


if __name__ == '__main__':
    #is_cve_in_project(r'/home/nfs/Linux Kernel Patch_v2.0/CVE-2010-2803', r'/home/nfs/linux-3.8.0')

    try:
        b = sys.argv[1]
    except:
        print('如果第一次运行，参数为fisrt,否则为wrong')
        sys.exit(0)
    print(b)
    cve_name = r'/home/ming/Linux Kernel Patch_v2.0'
    path_list=os.listdir(cve_name)
    path_list.sort()
    # print(path_list)
    if str(b) == 'new':
        fisrt_newExcel()
        #for file_name in os.listdir(cve_name):
        for index,file_name in enumerate(path_list):
            if os.path.isdir(os.path.join(cve_name, file_name)):
                cve_dir_path = os.path.join(cve_name, file_name)
                year = int(file_name.split('-')[1])
                num = int(file_name.split('-')[2])
                if year >= 2019 :
                        # print("已进行%.2f" % ((index / len(path_list))*100) + '%')
                        is_cve_in_project(cve_dir_path, r'/home/ming/linux-4.19.90')
    elif str(b) == 'cont':
        cve_num = input('请输入要测试的CVE编号继续测试：')
        index_num = path_list.index(cve_num)
        print(path_list[index_num:])
        for index,file_name in enumerate(path_list[index_num:]):
            if os.path.isdir(os.path.join(cve_name, file_name)):
                cve_dir_path = os.path.join(cve_name, file_name)
                year = int(file_name.split('-')[1])
                num = int(file_name.split('-')[2])
                if year >= 2019 :
                        # print(file_name)
                        # print("已进行%.2f" % ((index / len(path_list))*100) + '%')
                        is_cve_in_project(cve_dir_path, r'/home/ming/linux-4.19.90')

