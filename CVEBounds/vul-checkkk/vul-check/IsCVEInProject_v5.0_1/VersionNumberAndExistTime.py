#coding=utf-8

import xlrd
import os
import re
import datetime
import Repository
import GetModuleDiffIn


def get_linux_kernel_release_time_tuple(version_number, linux_kernel_release_time_file_path):
    r_workbook = xlrd.open_workbook(linux_kernel_release_time_file_path)
    r_sheet = r_workbook.sheets()[0]
    if r_sheet.nrows <= 1:
        return ()
    proximate_version_number = r_sheet.cell(1, 0).value
    proximate_version_number_row_index = 1
    for row_index in range(1, r_sheet.nrows):
        cell_version_number = r_sheet.cell(row_index, 0).value
        if not Repository.is_version_number(cell_version_number):
            continue
        if Repository.version_number_compare(cell_version_number, version_number) == 0:
            proximate_version_number_row_index = row_index
            break
        if Repository.version_number_compare(cell_version_number, version_number) < 0 < \
                Repository.version_number_compare(cell_version_number, proximate_version_number):
            proximate_version_number = cell_version_number
            proximate_version_number_row_index = row_index
    return xlrd.xldate_as_tuple(r_sheet.cell(proximate_version_number_row_index, 1).value, 0)[0:3]


def is_diff_segment_in_file(diff_segment, diff_segment_index, dst_file_path, diff_file_path):
    #bm_file_path,存储于diff_file_path文件夹里面，文件名为(BM)+diff_file_path
    bm_file_path = os.path.join(os.path.dirname(diff_file_path),
                                '(BM)' + os.path.basename(diff_file_path))
    if os.path.splitext(diff_file_path)[1] in ('.c', '.h') and os.path.exists(bm_file_path):
        #如果bm_file_path存在的话
        GetModuleDiffIn.diff_file_to_module_diff_file(diff_file_path)
        #创建(Module)diff_file_path 文件
        module_diff_file_path = os.path.join(os.path.dirname(diff_file_path),
                                             '(Module)' + os.path.basename(diff_file_path))
        diff_module_and_scope = GetModuleDiffIn.read_diff_module_and_scope(module_diff_file_path,
                                                                           diff_segment_index)
        #从(Module)diff_file_path 文件,得到diff_segment的scope 几行到几行
        if diff_module_and_scope:
            scope_tuple = GetModuleDiffIn.get_module_scope_tuple(diff_module_and_scope[:-2], dst_file_path)           #去掉函数名后面的范围，linux kernel漏洞二级目录下的所有路径
            if scope_tuple:
                print("-----",scope_tuple[0])
                return GetModuleDiffIn.is_only_non_add_diff_in_lines(
                    diff_segment,
                    Repository.get_file_line_list(dst_file_path)[scope_tuple[0]:scope_tuple[1] + 1]
                )
            else:
                return False
    return GetModuleDiffIn.is_only_non_add_diff_in_lines(diff_segment,
                                                         Repository.get_file_line_list(dst_file_path))


def is_one_vuln_in_linux_kernel_accurate(diff_file_name, patch_dir, kernel_dir):
    vuln_relative_path = diff_file_name.replace('#~', '/')
    vuln_dir_path = os.path.join(kernel_dir, os.path.dirname(vuln_relative_path))
    if os.path.exists(vuln_dir_path):
        for file_name in os.listdir(vuln_dir_path):
            if os.path.isdir(os.path.join(vuln_dir_path, file_name)):
                continue
            elif re.match(
                    re.escape(os.path.splitext(os.path.basename(vuln_relative_path))[0])
                    + r'(_[1-5])?'
                    + re.escape(os.path.splitext(os.path.basename(vuln_relative_path))[1]),
                    file_name, re.I):
                for diff_segment_index, diff_segment in enumerate(
                        GetModuleDiffIn.get_diff_segment_list(os.path.join(patch_dir, diff_file_name))):
                    if not is_diff_segment_in_file(diff_segment, diff_segment_index,
                                                   os.path.join(vuln_dir_path, file_name),
                                                   os.path.join(patch_dir, diff_file_name)):
                        break
                else:
                    return True
    return False


# def is_one_vuln_in_linux_kernel(patch_name, patch_dir, kernel_dir):
#     patch_relative_path = patch_name.replace('~！@#', '/')
#     patch_relative_path_dir_name = os.path.dirname(patch_relative_path)
#     patch_relative_path_base_name = os.path.basename(patch_relative_path)
#     vuln_path_dir_name = os.path.join(kernel_dir, patch_relative_path_dir_name)
#     if not os.path.exists(vuln_path_dir_name):
#         return False
#     for file_name in os.listdir(vuln_path_dir_name):
#         if os.path.isdir(os.path.join(vuln_path_dir_name, file_name)):
#             continue
#         if os.path.splitext(patch_relative_path_base_name)[0] in file_name:
#             with open(os.path.join(patch_dir, patch_name), 'r') as patch_file:
#                 for line in patch_file.readlines():
#                     match = re.match(r'-([^-].*)', line)
#                     if match and not Repository.is_string_in_file(
#                             match.group(1).strip(),
#                             os.path.join(vuln_path_dir_name, file_name)
#                     ):
#                         break
#                 else:
#                     return True
#     return False

def is_one_vuln_in_linux_kernel_path(diff_file_name, kernel_dir):
    vuln_relative_path = diff_file_name.replace('#~', '/')
    vuln_dir_path = os.path.join(kernel_dir, os.path.dirname(vuln_relative_path))

    if os.path.exists(vuln_dir_path):
        for file_name in os.listdir(vuln_dir_path):
            if os.path.isdir(os.path.join(vuln_dir_path, file_name)):
                continue
            elif re.match(
                    re.escape(os.path.splitext(os.path.basename(vuln_relative_path))[0])
                    + r'(_[1-5])?'
                    + re.escape(os.path.splitext(os.path.basename(vuln_relative_path))[1]),
                    file_name, re.I):
                return True
    return False


def is_vuln_in_linux_kernel_path(patch_dir, kernel_dir):
    for file_name in os.listdir(patch_dir):
        if file_name != 'Source.txt' and not re.match(r'\(', file_name):
            if not is_one_vuln_in_linux_kernel_path(file_name, kernel_dir):
                return False
    return True


def is_vuln_in_linux_kernel(patch_dir, kernel_dir):
    if Repository.is_dir_empty(patch_dir) or not is_vuln_in_linux_kernel_path(patch_dir, kernel_dir):
        return False
    for file_name in os.listdir(patch_dir):
        if file_name != 'Source.txt' and not re.match(r'\(', file_name):
            if not is_one_vuln_in_linux_kernel_accurate(file_name, patch_dir, kernel_dir):
                return False
    return True


def print_current_search(kernel_name, rate_str):
    print(rate_str + '\tSearch:Linux-' + get_version_number(kernel_name))


def get_version_number(kernel_name):
    match = re.match(r'linux-(\d+(\.\d+)*)', kernel_name, re.I)
    if match:
        return match.group(1)
    else:
        return None


def get_oldest_version_number_binary_search(patch_dir, kernel_root, rate_str):
    kernel_name_list = sorted(os.listdir(kernel_root),
                              key=Repository.cmp_to_key(Repository.kernel_name_compare))
    low_index = 0
    high_index = len(kernel_name_list) - 1
    last_exist_index = None
    while True:
        if low_index == high_index:
            print_current_search(kernel_name_list[low_index], rate_str)
            if (last_exist_index and low_index == last_exist_index) \
                    or is_vuln_in_linux_kernel(patch_dir, kernel_name_list[low_index]):
                return get_version_number(kernel_name_list[low_index])
            else:
                return None
        middle_index = int((low_index + high_index)/2)
        print_current_search(kernel_name_list[middle_index], rate_str)
        if (last_exist_index and middle_index == last_exist_index) \
                or is_vuln_in_linux_kernel(patch_dir,
                                           get_kernel_dir(kernel_root, kernel_name_list[middle_index])):
            last_exist_index = middle_index
            high_index = middle_index
        else:
            low_index = middle_index + 1


def get_kernel_dir(kernel_root, kernel_name):
    match = re.match(r'linux-(\d+(\.\d+)*)', kernel_name, re.I)
    if match:
        version_number = match.group(1)
        if Repository.version_number_compare(version_number, '2.6.12') < 0:
            return os.path.join(kernel_root, kernel_name)
        else:
            kernel_middle_dir = os.path.join(kernel_root, kernel_name)
            for file_name in os.listdir(kernel_middle_dir):
                file_path = os.path.join(kernel_middle_dir, file_name)
                if os.path.isdir(file_path):
                    return file_path
    return None


def get_oldest_version_number(patch_dir, kernel_root, rate_str):
    kernel_name_list = sorted(os.listdir(kernel_root),
                              key=Repository.cmp_to_key(Repository.kernel_name_compare))
    for kernel_name in kernel_name_list:
        match = re.match(r'linux-(\d+(\.\d+)*)', kernel_name, re.I)
        if match:
            version_number = match.group(1)
            kernel_dir = get_kernel_dir(kernel_root, kernel_name)
            if kernel_dir:
                print(rate_str + '\tSearch:Linux-' + version_number)
                if is_vuln_in_linux_kernel(patch_dir, kernel_dir):
                    return version_number
    return None


def get_version_number_and_exist_time_tuple(patch_dir, kernel_root,
                                            linux_kernel_release_time_file_path, rate_str='\r'):
    if os.path.exists(patch_dir):
        oldest_kernel_version_number = get_oldest_version_number(patch_dir, kernel_root, rate_str)
        if oldest_kernel_version_number:
            release_time_tuple = get_linux_kernel_release_time_tuple(
                oldest_kernel_version_number,
                linux_kernel_release_time_file_path
            )
            return oldest_kernel_version_number, release_time_tuple
    return ()


def save_vuln_version_number_and_exist_time(save_path, excel_path, patch_root, kernel_root,
                                            linux_kernel_release_time_file_path, start_row_index):
    r_workbook = xlrd.open_workbook(excel_path)
    r_sheet = r_workbook.sheets()[0]
    Repository.init_workbook(save_path,
                             ['CVE Number', 'Linux Kernel Version Number', 'Vulnerability Exist Time'],
                             width=1.5)

    for row_index in range(start_row_index, r_sheet.nrows):
        cve_id = str(r_sheet.cell(row_index, 0).value).strip()
        rate_str = '\rRow Index:' + str(row_index) + '\t' + cve_id
        print(rate_str)
        info_tuple = get_version_number_and_exist_time_tuple(os.path.join(patch_root, cve_id.upper()),
                                                             kernel_root,
                                                             linux_kernel_release_time_file_path,
                                                             rate_str)
        if info_tuple:
            version_number = info_tuple[0]
            if info_tuple[1]:
                release_time = datetime.datetime(*info_tuple[1])
            else:
                release_time = None
        else:
            version_number = None
            release_time = None
        Repository.write_workbook(save_path,
                                  {'CVE Number': cve_id, 'Linux Kernel Version Number': version_number,
                                   'Vulnerability Exist Time': release_time}, row_index - 1,
                                  style_list=[None, None, Repository.set_date_style()])


if __name__ == '__main__':
    save_vuln_version_number_and_exist_time(
        r'C:\Users\79196\Downloads\NVD\CVE Oldest Version Number.xls',
        r'C:\Users\79196\Downloads\NVD\Linux Kernel Character Factor.xls',
        r'C:\Users\79196\Downloads\NVD\Linux Kernel Patch',
        r'D:\Linux Kernel\Main',
        r'C:\Users\79196\Downloads\NVD\Linux Kernel Release Time.xls',
        start_row_index=26,
    )
