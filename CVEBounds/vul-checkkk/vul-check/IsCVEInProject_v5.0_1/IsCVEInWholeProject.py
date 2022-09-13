# coding=utf-8
#此代码版本：
#将之前，patch描述路径不精准存在的CVE,挑选出来，存储在'vuln_path_not_data.txt'中
#这些patch描述路径不精准存在的CVE，分别在整个linux中，选取最接近的路径进行测试
#测试is_diff_in_files标准：
# is_only_non_add_diff_in_lines。对每一个diff_hunk，存在删除代码，删除代码全存在，并且增加代码不全存在
import Repository
import os
import re
import GetModuleDiffIn
import VersionNumberAndExistTime
import xlrd
import xlwt
from xlutils.copy import copy

global cve_name

whole_result_file_name = 'py2_whole_result_data.txt'
with open(whole_result_file_name, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
    f.write("This is whole result cve.\n")

no_vul_path_file_name='vuln_relative_path_not_exist_data.txt'
with open(no_vul_path_file_name, 'w') as no_vuln_f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
    no_vuln_f.write("This is no vul_path cve.\n")

def is_diff_segment_in_files(cve_dir_path,diff_segment, diff_segment_index, project_dir_path, diff_file_path):
    for file_path in Repository.get_all_file_path_list(project_dir_path):
        if VersionNumberAndExistTime.is_diff_segment_in_file(diff_segment, diff_segment_index, file_path,
                                                             diff_file_path):
            print('\r Probably In ' + file_path)
            with open(whole_result_file_name, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
                f.write(cve_dir_path+'\r   '+os.path.basename(diff_file_path) + '\r   In ' + file_path + '\n')
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


def is_diff_in_project_2(cve_dir_path,diff_file_path, project_dir_path):
    #print(os.path.basename(diff_file_path))
    for diff_segment_index, diff_segment in enumerate(GetModuleDiffIn.get_diff_segment_list(diff_file_path)):
        if not is_diff_segment_in_files(cve_dir_path,diff_segment, diff_segment_index, project_dir_path, diff_file_path):
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
                # print('\r' + diff_file_path.split('~!@#')[-1] + ' Not In ' + file_path, end='')
                break
        else:
            print('\r' + diff_file_path.split('~!@#')[-1] + ' In ' + file_path)
            return True
    return False

def match_five(file_name,project_dir_path):
    match = re.search(r'(\w+)~!@#(\w+)~!@#(\w+)~!@#(\w+)~!@#(\w+)~!@#',file_name)
    vuln_relative_path = project_dir_path + '/' + match.group(1) + '/' + match.group(2) + '/' + match.group(
        3) + '/' + match.group(4) + '/' + match.group(5)
    if os.path.exists(vuln_relative_path):
        return vuln_relative_path
    else:
        return match_four(file_name,project_dir_path)

def match_four(file_name,project_dir_path):
    match = re.search(r'(\w+)~!@#(\w+)~!@#(\w+)~!@#(\w+)~!@#', file_name)
    vuln_relative_path = project_dir_path + '/' + match.group(1) + '/' + match.group(2) + '/' + match.group(
            3) + '/' + match.group(4)
    if os.path.exists(vuln_relative_path):
        return vuln_relative_path
    else:
        return match_three(file_name,project_dir_path)

def match_three(file_name,project_dir_path):
    match = re.search(r'(\w+)~!@#(\w+)~!@#(\w+)~!@#', file_name)
    vuln_relative_path = project_dir_path + '/' + match.group(1) + '/' + match.group(2) + '/' + match.group(
                3)
    if os.path.exists(vuln_relative_path):
        return vuln_relative_path
    else:
        return match_two(file_name,project_dir_path)

def match_two(file_name,project_dir_path):
    match = re.search(r'(\w+)~!@#(\w+)~!@#', file_name)
    vuln_relative_path = project_dir_path + '/' + match.group(1) + '/' + match.group(2)
    if os.path.exists(vuln_relative_path):
        return vuln_relative_path
    else:
        return match_one(file_name,project_dir_path)

def match_one(file_name,project_dir_path):
    match = re.search(r'(\w+)~!@#', file_name)
    vuln_relative_path = project_dir_path + '/' + match.group(1)
    if os.path.exists(vuln_relative_path):
        return vuln_relative_path
    else:
        return project_dir_path



def is_cve_in_whole_project(cve_dir_path, project_dir_path):
    if Repository.is_dir_empty(cve_dir_path):
        return False
    #print (cve_dir_path)
    for file_name in os.listdir(cve_dir_path):
        if file_name != 'Source.txt' and not re.match(r'\(', file_name):
            if file_name[-1] == 'c' or file_name[-1] == 'h':
                diff_file_name = file_name
                vuln_relative_path = diff_file_name.replace('~!@#', '/')
                vuln_dir_path = os.path.join(project_dir_path, os.path.dirname(vuln_relative_path))
                if not os.path.exists(vuln_dir_path):
                    print (cve_dir_path)
                    print (vuln_dir_path + '           Vuln_dir_path Not Exist')
                    print (diff_file_name)
                    with open(no_vul_path_file_name, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
                        f.write(cve_dir_path+'\n'+vuln_dir_path + '      Vuln_dir_path Not Exist' + '\n')
                    count_list=re.findall(r'~!@#',diff_file_name)
                    count=len(count_list)
                    if count>=5:
                        vuln_path=match_four(diff_file_name,project_dir_path)
                        #print vuln_path
                    if count==4:
                        vuln_path=match_three(diff_file_name,project_dir_path)
                        #print vuln_path
                    if count==3:
                        vuln_path=match_two(diff_file_name,project_dir_path)
                        #print vuln_path
                    if count==2:
                        vuln_path=match_one(diff_file_name,project_dir_path)
                        #print vuln_path
                    if count==1:
                        vuln_path=match_one(diff_file_name,project_dir_path)
                        #print vuln_path

                    print (vuln_path+'\n')
                    if not is_diff_in_project_2(cve_dir_path,os.path.join(cve_dir_path, file_name), vuln_path):
                        return False
                    return True



if __name__ == '__main__':
    '''cve_name = r'D:\Linux Kernel Patch'
    for file_name in os.listdir(cve_name):
        if os.path.isdir(os.path.join(cve_name, file_name)):
            cve_dir_path = os.path.join(cve_name, file_name)
            is_cve_in_whole_project(cve_dir_path, r'D:\documents\linux kernel\linux-3.8\linux-3.8')'''

    cve_name = r'E:\Linux Kernel Patch'
    for file_name in os.listdir(cve_name):
        if os.path.isdir(os.path.join(cve_name, file_name)):
            cve_dir_path = os.path.join(cve_name, file_name)
            is_cve_in_whole_project(cve_dir_path, r'E:\linux-3.8\linux-3.8')

'''
    is_cve_in_whole_project(r'D:\Linux Kernel Patch\CVE-2007-3731',
                            r'D:\documents\linux kernel\linux-3.8\linux-3.8')

 is_cve_in_whole_project(r'D:\Linux Kernel Patch\CVE-2015-5283',
                      r'D:\documents\linux kernel\linux-3.8\linux-3.8')
                      
                      
    
'''

'''


    

'''

