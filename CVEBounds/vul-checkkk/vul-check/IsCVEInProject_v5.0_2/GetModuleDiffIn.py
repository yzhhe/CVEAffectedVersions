#coding=utf-8
# Author: 14281055 Liheng Chen CIT BJTU
# File Name:
import Repository
import re
import os


def match_line(module_info_list, line):
    line = Repository.separate_word_and_nonword(line)
    if module_info_list[0] == 'struct':
        return True if re.search(r'\bstruct ' + re.escape(module_info_list[1]) + ' {', line) else False
    elif module_info_list[0] == 'function':
        return True if re.search(
            r'\b' + re.escape(module_info_list[1]) + ' ' + re.escape(module_info_list[2]) + r' \(',
            line) else False
    return None


def match_lines(module_info_list, line_list, default_line_index_range=30):
    if match_line(module_info_list, line_list[0]):
        return True
    line_index_range = default_line_index_range if len(line_list) > default_line_index_range else len(
        line_list)
    lines = Repository.line_list_to_lines(line_list[:line_index_range])
    first_line_end_index = Repository.get_first_line_end_index_in_lines(line_list[0], lines)
    if module_info_list[0] == 'struct':
        match = re.search(r'\bstruct ' + re.escape(module_info_list[1]) + ' {', lines)
        if match:
            tag_end_index = match.start() + 5  # length of 'struct' is 6
            if tag_end_index <= first_line_end_index:
                return True
        return False
    elif module_info_list[0] == 'function':
        match = re.search(
            r'\b' + re.escape(module_info_list[1]) + ' (?:\* )*' + re.escape(
                module_info_list[2]) + r' \([^)]*\) {',
            lines)
        if match:
            tag_end_index = match.start() + len(module_info_list[1]) - 1
            if tag_end_index <= first_line_end_index:
                return True
        return False
    return None


def get_module_info_list(line_list):
    lines = Repository.line_list_to_lines(line_list)
    first_line_end_index = Repository.get_first_line_end_index_in_lines(line_list[0], lines)
    match = re.search(r'\bstruct (\w+) {', lines)
    if match:
        tag_end_index = match.start() + 5  # length of 'struct' is 6
        if tag_end_index <= first_line_end_index:
            return ['struct', match.group(1)]

    match = re.search(r'(?!if|while)(\w+) (?:\* )*(?!if|while)(\w+) \([^)]*\) {', lines)
    if match:
        tag_end_index = match.start() + len(match.group(1)) - 1
        if tag_end_index <= first_line_end_index:
            return ['function', match.group(1), match.group(2)]
    return None


def read_module_and_scope_list(module_file_path):
    #将(module)bm_file_path转化为数组
    module_file_line_list = Repository.get_file_line_list(module_file_path)
    module_and_scope_list = []
    if module_file_line_list:
        for line in module_file_line_list:
            module_and_scope = line.strip().split('\t')
            # print('总体是%s'%(module_and_scope))
            # print('值是%s'%(module_and_scope[-1]))
            # print('类型是%s和%s'%(type(module_and_scope[-1]),type(module_and_scope[-2])))
            # print('结果为%s和%s'%(module_and_scope[-1] == 'None',module_and_scope[-2] == 'None'))
            if module_and_scope[-1] != 'None' and module_and_scope[-2] != 'None':
                module_and_scope[-2] = int(module_and_scope[-2])
                #若为'None'怎么办
                module_and_scope[-1] = int(module_and_scope[-1])
                module_and_scope_list.append(module_and_scope)
    return module_and_scope_list


def get_module_info_list_list(dst_file_path, default_line_list_range=30):
    dst_file_line_list = Repository.get_file_line_list(dst_file_path)
    module_info_list_list = []
    for line_index, line in enumerate(dst_file_line_list):
        line_list_range = default_line_list_range if len(
            dst_file_line_list) - line_index > default_line_list_range else len(
            dst_file_line_list) - line_index
        module = get_module_info_list(dst_file_line_list[line_index:line_index + line_list_range])
        if module:
            module_info_list_list.append(module)
    return module_info_list_list


def print_module_and_scope(file_path):
    for module_info_list in get_module_info_list_list(file_path):
        scope_tuple = get_module_scope_tuple(module_info_list, file_path)
        if scope_tuple:
            print('\t'.join(module_info_list) + '\t' + str(scope_tuple[0]) + '\t' + str(scope_tuple[1]))
        else:
            print('\t'.join(module_info_list))


def write_module_and_scope(module_file_path, module_and_scope=None, flag=False):
    if flag:
        line = '\t'.join(module_and_scope[:-2]) + '\t' + str(module_and_scope[-2]) + '\t' + str(
            module_and_scope[-1])
        Repository.append_file_with_eol(module_file_path, line)
    else:
        Repository.append_file_with_eol(module_file_path, ' ')


def read_diff_module_and_scope(module_diff_file_path, diff_index):
    #print ('diff_index')
    #print(diff_index)
    lines = Repository.get_file_line_list(module_diff_file_path)
    #print ('len lines')
    #print len(lines)
    line = Repository.get_file_line_list(module_diff_file_path)[diff_index]
    if line.strip() == '':
        return []
    else:
        module_and_scope = line.strip().split('\t')
        module_and_scope[-2] = int(module_and_scope[-2])
        module_and_scope[-1] = int(module_and_scope[-1])
        #print(module_and_scope)
        return module_and_scope


def bm_file_to_module_bm_file(bm_file_path):
    module_bm_file_path = os.path.join(os.path.dirname(bm_file_path),
                                       '(Module)' + os.path.basename(bm_file_path))
    # 在这里定义并创建(Module)+bm_file_path 文件
    if not os.path.exists(module_bm_file_path):
        for module_info_list in get_module_info_list_list(bm_file_path):
            scope_tuple = get_module_scope_tuple(module_info_list, bm_file_path)
            if scope_tuple:
                module_info_list.extend(scope_tuple)
            else:
                module_info_list.extend(['None', 'None'])
            write_module_and_scope(module_bm_file_path, module_info_list, True)
            #将存在于bm_file_path的module_info_list的scope_tuple，存入(Module)+bm_file_path 文件


def diff_file_to_module_diff_file(diff_file_path):
    module_diff_file_path = os.path.join(os.path.dirname(diff_file_path),
                                         '(Module)' + os.path.basename(diff_file_path))
    #在这里定义并创建(Module)+diff_file_path 文件
    if not os.path.exists(module_diff_file_path):
        bm_file_path = os.path.join(os.path.dirname(diff_file_path),
                                    '(BM)' + os.path.basename(diff_file_path))
        bm_file_line_list = Repository.get_file_line_list(bm_file_path)

        bm_file_to_module_bm_file(bm_file_path)
        for diff_segment in get_diff_segment_list(diff_file_path):
            for module_and_scope in read_module_and_scope_list(os.path.join(os.path.dirname(bm_file_path),
                                                                            '(Module)' + os.path.basename(
                                                                                bm_file_path))):
                if module_and_scope[-2] != 'None' and module_and_scope[-1] != 'None' \
                        and Repository.is_lines_in_lines(diff_segment[4], bm_file_line_list[
                                                                          module_and_scope[-2]:
                                                                          module_and_scope[
                                                                              -1] + 1]):
                    #bm_file_module scope存在，并且diff_segment原代码在此scope中对应存在
                    write_module_and_scope(module_diff_file_path, module_and_scope, True)
                    #创建(Module)diff_file_path ,是diff_segment 在bm_file中的module_and_scope
                    break
            else:
                write_module_and_scope(module_diff_file_path)
                #创建(Module)diff_file_path，若找不到scope，flag=flase,则添加行为''+'\n'


def is_only_non_add_diff_in_lines(diff, dst_line_list):#diff[1]存删除代码 diff[2]存增加代码 diff[3]other代码
    res0 = Repository.is_lines_in_lines(diff[0], dst_line_list)
    res1=Repository.is_lines_in_lines(diff[1], dst_line_list)
    res2=Repository.is_lines_in_lines(diff[2], dst_line_list)
    res3=Repository.is_lines_in_lines(diff[3], dst_line_list)

    #if res1 and not res2 and res3:
        #print(Repository.is_lines_in_lines(diff[2], dst_line_list))
        #return True
    #print(diff[0])
    #print("res",res0)
    if res1 and res3 and not res2:
        return True
        
    else:
        if res1 and not res2:
            return 2
        return False

def get_module_scope_tuple(module_info_list, dst_file_path, line_offset=0):
    dst_file_line_list = Repository.get_file_line_list(dst_file_path)
    for line_index in range(len(dst_file_line_list[line_offset:])):
        if match_lines(module_info_list, dst_file_line_list[line_offset + line_index:]):   #匹配函数名？
            start_line_index = line_offset + line_index                     #patch第一行，相对于函数名的第一行漏洞代码位置
            break
    else:
        return ()
    remain_lines = Repository.line_list_to_lines(dst_file_line_list[start_line_index:])
    remain_line_end_char_index_dict = Repository.get_line_end_char_index_dict_with_lines(
        dst_file_line_list[start_line_index:],
        remain_lines)
    opening_brace_number = 0
    closing_brace_number = 0
    match = re.search(re.escape(module_info_list[-1]) + '.*?{', remain_lines)
    if match:
        # opening_brace_liF{ne_index = Repository.get_line_index(remain_line_end_char_index_dict,
        #                                                      match.end() - 1) + start_line_index
        opening_brace_number += 1
    else:
        return ()
    closing_brace_line_index = len(dst_file_line_list)
    for char_index, character in enumerate(remain_lines[match.end():]):
        if character == '{':
            opening_brace_number += 1
        elif character == '}':
            closing_brace_number += 1
            if opening_brace_number == closing_brace_number:
                closing_brace_line_index = Repository.get_line_index(
                    remain_line_end_char_index_dict,
                    char_index + match.end()
                ) + start_line_index
                break
    return start_line_index, closing_brace_line_index


def get_diff_segment_list(diff_file_path):
    diff_file_line_list = Repository.get_file_line_list(diff_file_path)
    diff_segment_list = []
    diff_segment = []
    diff_segment_delete_list = []
    diff_segment_add_list = []
    diff_segment_other_list = []
    diff_segment_non_add_list = []
    has_diff_segment_head = False
    for diff_file_line in diff_file_line_list:
        match = re.search(r'@@.*?@@(.*)', diff_file_line)
        if match:
            if diff_segment:
                diff_segment.append(diff_segment_delete_list)
                diff_segment.append(diff_segment_add_list)
                diff_segment.append(diff_segment_other_list)
                diff_segment.append(diff_segment_non_add_list)
                diff_segment_list.append(diff_segment)
                diff_segment_delete_list = []
                diff_segment_add_list = []
                diff_segment_other_list = []
                diff_segment_non_add_list = []
                diff_segment = []
            diff_segment_head = match.group(1).strip()
            diff_segment.append(diff_segment_head)
            has_diff_segment_head = True
        else:
            if has_diff_segment_head and diff_file_line.strip() != '':
                match = re.match(r'\+(.*)', diff_file_line)
                if match:
                    diff_segment_add_list.append(match.group(1).strip())
                elif re.match(r'[^-+]', diff_file_line):  #没有+-号的行
                    diff_segment_other_list.append(diff_file_line.strip())
                    diff_segment_non_add_list.append(diff_file_line.strip())
                else:
                    match = re.match(r'-(.*)', diff_file_line)
                    if match:
                        diff_segment_delete_list.append(match.group(1).strip())
                        diff_segment_non_add_list.append(match.group(1).strip())
    if diff_segment:
        diff_segment.append(diff_segment_delete_list)
        diff_segment.append(diff_segment_add_list)
        diff_segment.append(diff_segment_other_list)
        diff_segment.append(diff_segment_non_add_list)
        diff_segment_list.append(diff_segment)
        #print(diff_segment[3][0])
    return diff_segment_list


if __name__ == '__main__':
    str2 = ['function', 'f', 'IS_ENABLED', 'None', 'None']
    print(str2[-2] is 'None')