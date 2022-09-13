#coding=utf-8
#此代码版本
#CVE分两种，一种依据patch路径可以找到vuln，一种是依据patch描述路径，即vuln_not_exist，
# 结果通通记录在了py2_result_data.txt中,即4.25信工所测试结果
#之后，将In的和没有发现In的CVE，自己之后分离开了，即In_CVE_result
import Repository
import IsCVEInWholeProject
import os
import re
import GetModuleDiffIn
import VersionNumberAndExistTime
import xlrd
import xlwt
from xlutils.copy import copy

global cve_name
ct=0

result_file_name = 'py2_result_data.txt'
result_file_name2 = 'py2_suspected_result_data.txt'

workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('result_data')
worksheet.write(0,0,"CVE_number")
worksheet.write(0,1,"Patch_file")
worksheet.write(0,2,"Project_file")
worksheet.write(0,3,"Level")
worksheet = workbook.add_sheet('suspected_result_data')
worksheet.write(0,0,"CVE_number")
worksheet.write(0,1,"Patch_file")
worksheet.write(0,2,"Project_file")
worksheet.write(0,3,"Level")
workbook.save('Result.xls')

with open(result_file_name, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
    f.write("This is result.\n")
with open(result_file_name2, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
    f.write("These cve may be exist.\n")


def is_diff_segment_in_files(cve_dir_path,diff_segment, diff_segment_index, project_dir_path, diff_file_path):
    for file_path in Repository.get_all_file_path_list(project_dir_path):    #得到linux kernel二级文件夹下所有文件路径（递归）
        if VersionNumberAndExistTime.is_diff_segment_in_file(diff_segment, diff_segment_index, file_path,
                                                             diff_file_path)==1:
            print('\rIn ' + file_path)
            with open(result_file_name, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
                f.write(diff_file_path+os.path.basename(diff_file_path)+'\r   In ' + file_path+'\n')
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
            table.write(row, 1, os.path.basename(diff_file_path).replace('~!@#', '/'))
            table.write(row, 2, file_path)
            table.write(row, 3, score)
            excel.save("Result.xls")  # xlwt对象的保存方法，这时便覆盖掉了原来的excel
            return True
        if VersionNumberAndExistTime.is_diff_segment_in_file(diff_segment, diff_segment_index, file_path,
                                                             diff_file_path)==2:
            print('\r Probably In ' + file_path)
            with open(result_file_name2, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
                f.write(diff_file_path+os.path.basename(diff_file_path) + '\r   Probably In ' + file_path + '\n')
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
            table.write(row, 1, os.path.basename(diff_file_path).replace('~!@#', '/'))
            table.write(row, 2, file_path)
            table.write(row, 3, score)
            excel.save("Result.xls")  # xlwt对象的保存方法，这时便覆盖掉了原来的excel
            return True
    return False

def is_diff_segment_in_files1(cve_dir_path,diff_segment, diff_segment_index, project_dir_path, diff_file_path):

    for file_path in Repository.get_all_file_path_list(project_dir_path):    #得到linux kernel二级文件夹下所有文件路径（递归）
        if VersionNumberAndExistTime.is_diff_segment_in_file(diff_segment, diff_segment_index, file_path,
                                                             diff_file_path)==1:
            global ct
            ct += 1
            print(ct)
            return ct, file_path

        if VersionNumberAndExistTime.is_diff_segment_in_file(diff_segment, diff_segment_index, file_path,
                                                             diff_file_path)==2:

            return ct,file_path
    return ct,file_path

def is_diff_segment_in_files2(cve_dir_path,diff_segment, diff_segment_index, project_dir_path, diff_file_path):
    for file_path in Repository.get_all_file_path_list(project_dir_path):    #得到linux kernel二级文件夹下所有文件路径（递归）
        if VersionNumberAndExistTime.is_diff_segment_in_file(diff_segment, diff_segment_index, file_path,
                                                             diff_file_path)==1:
            print('\r In ' + file_path)
            with open(result_file_name2, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
                f.write(diff_file_path + os.path.basename(diff_file_path) + '\r   In ' + file_path + '\n')
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
            table.write(row, 1, os.path.basename(diff_file_path).replace('~!@#', '/'))
            table.write(row, 2, file_path)
            table.write(row, 3, score)
            excel.save("Result.xls")  # xlwt对象的保存方法，这时便覆盖掉了原来的excel
            return True

        if VersionNumberAndExistTime.is_diff_segment_in_file(diff_segment, diff_segment_index, file_path,
                                                             diff_file_path)==2:
            print('\r Probably In ' + file_path)
            with open(result_file_name2, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
                f.write(diff_file_path+os.path.basename(diff_file_path) + '\r   Probably In ' + file_path + '\n')
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
            table.write(row, 1, os.path.basename(diff_file_path).replace('~!@#', '/'))
            table.write(row, 2, file_path)
            table.write(row, 3, score)
            excel.save("Result.xls")  # xlwt对象的保存方法，这时便覆盖掉了原来的excel
            return True
    return False

def is_diff_segment_in_files3(cve_dir_path,diff_segment, diff_segment_index, project_dir_path, diff_file_path):
    for file_path in Repository.get_all_file_path_list(project_dir_path):    #得到linux kernel二级文件夹下所有文件路径（递归）
        if VersionNumberAndExistTime.is_diff_segment_in_file(diff_segment, diff_segment_index, file_path,
                                                             diff_file_path)==1:
            print('\r Probably In ' + file_path)
            with open(result_file_name2, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
                f.write(diff_file_path + os.path.basename(diff_file_path) + '\r   Probably In ' + file_path + '\n')
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
            table.write(row, 1, os.path.basename(diff_file_path).replace('~!@#', '/'))
            table.write(row, 2, file_path)
            table.write(row, 3, score)
            excel.save("Result.xls")  # xlwt对象的保存方法，这时便覆盖掉了原来的excel
            return True

        if VersionNumberAndExistTime.is_diff_segment_in_file(diff_segment, diff_segment_index, file_path,
                                                             diff_file_path)==2:
            print('\r Probably In ' + file_path)
            with open(result_file_name2, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
                f.write(diff_file_path+os.path.basename(diff_file_path) + '\r   Probably In ' + file_path + '\n')
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
            table.write(row, 1, os.path.basename(diff_file_path).replace('~!@#', '/'))
            table.write(row, 2, file_path)
            table.write(row, 3, score)
            excel.save("Result.xls")  # xlwt对象的保存方法，这时便覆盖掉了原来的excel
            return True
    return False

def is_diff_in_project_2(cve_dir_path,diff_file_path, project_dir_path):#单文件
    print(os.path.basename(diff_file_path))
    count = len(GetModuleDiffIn.get_diff_segment_list(diff_file_path))
    print(count)
    if count==1:          #单@@
        for diff_segment_index, diff_segment in enumerate(GetModuleDiffIn.get_diff_segment_list(diff_file_path)):
            if not is_diff_segment_in_files2(cve_dir_path,diff_segment, diff_segment_index, project_dir_path, diff_file_path):
                return False
        return True
    else:                #多@@

        global ct
        ct = 0
        for diff_segment_index, diff_segment in enumerate(GetModuleDiffIn.get_diff_segment_list(diff_file_path)):
            res,file_path=is_diff_segment_in_files1(cve_dir_path, diff_segment, diff_segment_index, project_dir_path, diff_file_path)
        print("res",res)
        if res==count:      #所有@@匹配

            print('\r In ' + file_path)
            with open(result_file_name, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
                f.write(diff_file_path + os.path.basename(diff_file_path) + '\r   In ' + file_path + '\n')
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
            table.write(row, 1, os.path.basename(diff_file_path).replace('~!@#', '/'))
            table.write(row, 2, file_path)
            table.write(row, 3, score)
            excel.save("Result.xls")  # xlwt对象的保存方法，这时便覆盖掉了原来的excel
            return True

        elif res!=0:           #部分@@匹配
            #print("=========")
            print('\r Probably In ' + file_path)
            with open(result_file_name2, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
                f.write(diff_file_path + os.path.basename(diff_file_path) + '\r   Probably In ' + file_path + '\n')
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
            table.write(row, 1, os.path.basename(diff_file_path).replace('~!@#', '/'))
            table.write(row, 2, file_path)
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
                print('\r' + diff_file_path.split('~!@#')[-1] + ' Not In ' + file_path)
                #print('\r' + diff_file_path.split('~!@#')[-1] + ' Not In ' + file_path, end='')
                break
        else:
            print('\r' + diff_file_path.split('~!@#')[-1] + ' In ' + file_path)
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
                    vuln_relative_path = diff_file_name.replace('~!@#', '/')
                    vuln_dir_path = os.path.join(project_dir_path, os.path.dirname(vuln_relative_path))
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
                    vuln_relative_path = diff_file_name.replace('~!@#', '/')
                    vuln_dir_path = os.path.join(project_dir_path, os.path.dirname(vuln_relative_path))
                    print(vuln_dir_path)
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




if __name__ == '__main__':

    cve_name = r'/home/nfs/Linux Kernel Patch'
    path_list=os.listdir(cve_name)
    path_list.sort()

    for file_name in os.listdir(cve_name):
	for file_name in path_list:
            if os.path.isdir(os.path.join(cve_name, file_name)):
                cve_dir_path = os.path.join(cve_name, file_name)
                is_cve_in_project(cve_dir_path, r'/home/nfs/linux-3.8.0')

''' 
    is_cve_in_project(r'E:\\Linux Kernel Patch\CVE-2007-2480', r'E:\\linux-3.8\\linux-3.8')    
'''






