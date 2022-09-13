# File Name: Repository.py


import http.client
import os
import random
import re
import shutil
import socket
import ssl
import time
import urllib.error
import urllib.request
# import winsound

import bs4
import numpy
import requests
import xlrd
import xlsxwriter
import xlwt
from xlutils.copy import copy

unknown = -1
true = 1
false = 0

user_agent_list = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322"
    "; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.5"
    "0727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR"
    " 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3"
    ".5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SL"
    "CC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .N"
    "ET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50"
    "727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko,"
    " Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) "
    "Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/"
    "2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kap"
    "iko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazeha"
    "kase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0"
    ".963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) "
    "Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

c_keyword_list = [
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum',
    'extern', 'float', 'for', 'goto', 'if', 'int', 'long', 'register', 'return', 'short', 'signed',
    'sizeof', 'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while',
    'inline', 'restrict', '_Bool', '_Complex', '_Imaginary', '_Alignas', '_Alignof', '_Atomic',
    '_Static_assert', '_Noreturn', '_Thread_local', '_Generic'
]
java_keyword_list = [
    'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class', 'const', 'continue',
    'default', 'do', 'double', 'else', 'enum', 'extends', 'final', 'finally', 'float', 'for', 'goto', 'if',
    'implements', 'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new', 'package', 'private',
    'protected', 'public', 'return', 'strictfp', 'short', 'static', 'super', 'switch', 'synchronized',
    'this', 'throw', 'throws', 'transient', 'try', 'void', 'volatile', 'while'
]
cpp_keyword_list = [
    'asm', 'do', 'if', 'return', 'typedef', 'auto', 'double', 'inline', 'short', 'typeid', 'bool',
    'dynamic_cast', 'int', 'signed', 'typename', 'break', 'else', 'long', 'sizeof', 'union', 'case', 'enum',
    'mutable', 'static', 'unsigned', 'catch', 'explicit', 'namespace', 'static_cast', 'using', 'char',
    'export', 'new', 'struct', 'virtual', 'class', 'extern', 'operator', 'switch', 'void', 'const', 'false',
    'private', 'template', 'volatile', 'const_cast', 'float', 'protected', 'this', 'wchar_t', 'continue',
    'for', 'public', 'throw', 'while', 'default', 'friend', 'register', 'true', 'delete', 'goto',
    'reinterpret_cast', 'try', 'alignas', 'alignof', 'char16_t', 'char32_t', 'constexpr', 'decltype',
    'noexcept', 'nullptr', 'static_assert', 'thread_local'
]

python_keyword_list = [
    'False', 'def', 'if', 'raise', 'None', 'del', 'import', 'return', 'True', 'elif', 'in', 'try', 'and',
    'else', 'is', 'while', 'as', 'except', 'lambda', 'with', 'assert', 'finally', 'nonlocal', 'yield',
    'break', 'for', 'not', 'class', 'from', 'or', 'continue', 'global', 'pass',
]


def is_blank(letter):
    if re.match(r' $', letter):
        return True
    else:
        return False


def is_letter(letter):
    if re.match(r'\w$', letter):
        return True
    else:
        return False


def remove_keyword(string, keyword):
    match = re.search(re.escape(keyword) + r'\W', string)
    if match:
        if match.start() == 0:
            return remove_keyword(string[match.end() - 1:], keyword)
        elif is_letter(string[match.start() - 1]):
            return string[:match.end() - 1] + remove_keyword(string[match.end() - 1:], keyword)
        elif is_blank(string[match.start() - 1]):
            return string[:match.start() - 1] + remove_keyword(string[match.end() - 1:], keyword)
        else:
            return string[:match.start()] + remove_keyword(string[match.end() - 1:], keyword)
    else:
        match = re.search(re.escape(keyword) + r'$', string)
        if match:
            if match.start() == 0:
                return ''
            elif is_letter(string[match.start() - 1]):
                return string[:match.end()]
            elif is_blank(string[match.start() - 1]):
                return string[:match.start() - 1]
            else:
                return string[:match.start()]
        else:
            return string


def remove_given_keyword_list(string, keyword_list):
    for keyword in keyword_list:
        string = remove_keyword(string, keyword)
    return string


def remove_all_keyword(string):
    string = remove_given_keyword_list(string, c_keyword_list)
    string = remove_given_keyword_list(string, cpp_keyword_list)
    string = remove_given_keyword_list(string, java_keyword_list)
    string = remove_given_keyword_list(string, python_keyword_list)
    return string


def is_substring(src_str_list, dst_str, case_ignore=True):
    for src_str in src_str_list:
        if case_ignore:
            if re.search(re.escape(src_str), dst_str, re.I):
                return True
        else:
            if re.search(re.escape(src_str), dst_str):
                return True
    return False


class PercentBar(object):
    def __init__(self, name):
        super(PercentBar, self).__init__()
        self.template = "\rDownload:\033[4;34m%s\033[0m\t\033[1;34m%.2f%%\033[0m"
        self.name = name

    def refresh(self, chunk_number, chunk_size, total_size):
        print(self.template % (self.name, chunk_number * chunk_size / total_size * 100), end='')


def requests_get_content(url, **kwarg):
    response = requests_get(url, **kwarg)
    if response:
        content = response.content
        response.close()
        return content
    else:
        return None


def requests_get_text(url, **kwarg):
    response = requests_get(url, **kwarg)
    if response:
        text = response.text
        response.close()
        return text
    else:
        return None


def requests_get(url, try_times=5, sleep_time=10, **kwarg):
    try_times_count = try_times
    while try_times_count > 0:
        try:
            # 屏蔽warning信息
            requests.packages.urllib3.disable_warnings()
            response = requests.get(url, **kwarg)
            response.raise_for_status()
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError, ssl.SSLError,
                requests.exceptions.HTTPError, requests.exceptions.InvalidSchema,
                requests.exceptions.MissingSchema):
            try_times_count -= 1
            time.sleep(sleep_time)
        else:
            break
    else:
        # print('\r\033[1;31mFail(' + str(try_times) + " Times):" + url + '\033[0m')
        return None
    return response


def download_file(hyperlink, save_path):
    if not os.path.exists(save_path):
        content = requests_get_content(hyperlink, timeout=10,
                                       headers={'User-Agent': random.choice(user_agent_list)})
        if content:
            with open(save_path, 'wb') as file:
                file.write(content)
            return True
        else:
            print('\rFail:' + os.path.basename(save_path))
            return False
    return True


def download_file_in_chunk(hyperlink, save_path):
    if not os.path.exists(save_path):
        response = requests_get(hyperlink, stream=True)
        if response:
            content_size = 0
            chunk_size = 1024
            total_size = int(response.headers['content-length'])
            percent_bar = PercentBar(os.path.basename(save_path))
            with open(save_path, "wb") as file:
                try:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        file.write(chunk)
                        content_size += len(chunk)
                        percent_bar.refresh(content_size / chunk_size, chunk_size, total_size)
                except ssl.SSLError as e:
                    # winsound.Beep(600, 1000)
                    print('\r\033[1;31m' + str(e) + ':' + save_path + '\033[0m')
                    file.close()
                    response.close()
                    if os.path.exists(save_path):
                        os.remove(save_path)
                    return False
            if content_size != total_size:
                # winsound.Beep(600, 1000)
                print('\r\033[1;31mContentTooShort:' + os.path.basename(save_path) + '\033[0m')
                file.close()
                response.close()
                if os.path.exists(save_path):
                    os.remove(save_path)
                return False
            response.close()
            return True
        print('\r\033[1;31mFail:' + os.path.basename(save_path) + '\033[0m')
        return False
    return True


def urllib_urlretrieve(hyperlink, save_path):
    if not os.path.exists(save_path):
        try:
            percent_bar = PercentBar(os.path.basename(save_path))
            urllib.request.urlretrieve(hyperlink, save_path, percent_bar.refresh)
        except (
                urllib.error.ContentTooShortError, urllib.error.URLError,
                http.client.RemoteDisconnected) as e:
            print('\r\033[1;31m' + str(e) + ':' + save_path + '\033[0m')
            if os.path.exists(save_path):
                os.remove(save_path)
            return False
    return True


def urllib_request_urlopen_text(url, headers=None, try_times=5, sleep_time=10, timeout=10):
    if headers is None:
        headers = {}
    try_times_count = try_times
    while try_times_count > 0:
        try:
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request, timeout=timeout)
            text = response.read()
            text = text.decode()
            response.close()
        except (ValueError, urllib.error.URLError, socket.timeout):
            try_times_count -= 1
            time.sleep(sleep_time)
        else:
            break
    else:
        # print('\r\033[1;31mFail(' + str(try_times) + " Times):" + url + '\033[0m')
        return None
    return text


def urllib_request_urlopen(url, headers=None, try_times=5, sleep_time=10, timeout=10):
    if headers is None:
        headers = {}
    try_times_count = try_times
    while try_times_count > 0:
        try:
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request, timeout=timeout)
        except (ValueError, urllib.error.URLError, socket.timeout):
            try_times_count -= 1
            time.sleep(sleep_time)
        else:
            break
    else:
        # print('\r\033[1;31mFail(' + str(try_times) + " Times):" + url + '\033[0m')
        return None
    return response


def append_file_with_eol(save_path, string, encoding=None):
    with open(save_path, 'a', encoding=encoding, errors='ignore') as file:
        file.write(string + '\n')


def separate_word_and_nonword(string):
    return remove_redundant_blank(separate_word_and_nonword_recursion(string))


def separate_word_and_nonword_recursion(string):
    match = re.search(r'[^\w\s]', string)
    if match:
        string = string[:match.start()] + ' ' + match.group() + ' ' + separate_word_and_nonword_recursion(
            string[match.end():])
    return string


def remove_redundant_blank(string):
    return ' '.join(string.split())


def save_tag_code_from_html(hyperlink, save_path):
    if os.path.exists(save_path):
        os.remove(save_path)
    # 获取修改之前文件代码
    text = urllib_request_urlopen_text(hyperlink,
                                       headers={'User-Agent': random.choice(user_agent_list)})
    if text:
        soup = bs4.BeautifulSoup(text, 'lxml')
        for tag_code in soup.select('code'):
            append_file_with_eol(save_path, tag_code.get_text())
        return True
    return False


def month_to_number(month):
    month_abbreviation_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                               'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    for key in month_abbreviation_dict.keys():
        if re.match(re.escape(key), month, re.I):
            return month_abbreviation_dict[key]
    return None


def has_none_in_tuple(a_tuple):
    for element in a_tuple:
        if element is None:
            return True
    return False


def is_version_number(version_number):
    version_number = version_number.strip().replace(' ', '')
    return True if re.match(r'\d+(\.\d+)*$', version_number) else False


def set_font(name='Arial', color_index=0, bold=False):
    font = xlwt.Font()
    font.name = name
    font.colour_index = color_index
    font.bold = bold
    font.height = 220

    style = xlwt.XFStyle()
    style.font = font

    return style


def set_date_style(flag=True, name='Arial', color_index=0, bold=False, date_format='yyyy年mm月'):
    style = set_font(name=name, color_index=color_index, bold=bold)
    if flag:
        style.num_format_str = date_format
    return style


def write_workbook_key_value(save_path, dictionary, start_row_index, style_list=None):
    if style_list is None:
        style_list = [None, None]
    r_workbook = xlrd.open_workbook(save_path, formatting_info=True)
    w_workbook = copy(r_workbook)
    w_sheet = w_workbook.get_sheet(0)

    for key in dictionary.keys():
        if style_list[0]:
            w_sheet.write(start_row_index, 0, key, style_list[0])
        else:
            w_sheet.write(start_row_index, 0, key)
        if style_list[1]:
            w_sheet.write(start_row_index, 1, dictionary[key], style_list[1])
        else:
            w_sheet.write(start_row_index, 1, dictionary[key])
        start_row_index += 1
    w_workbook.save(save_path)


def write_workbook(save_path, dictionary, row_index, sheet_name=None, sheet_index=0, style_list=None):
    if style_list is None:
        style_list = [None] * len(dictionary)
    r_workbook = xlrd.open_workbook(save_path, formatting_info=True)
    w_workbook = copy(r_workbook)
    if sheet_name:
        r_sheet = r_workbook.sheet_by_name(sheet_name)
        w_sheet = w_workbook.get_sheet(sheet_name)
    else:
        r_sheet = r_workbook.sheets()[sheet_index]
        w_sheet = w_workbook.get_sheet(sheet_index)
    for col_index in range(0, r_sheet.ncols):
        key = str(r_sheet.cell(0, col_index).value).strip()
        if key in dictionary.keys():
            if dictionary[key] is not None:
                if style_list[col_index]:
                    w_sheet.write(row_index, col_index, dictionary[key], style_list[col_index])
                else:
                    w_sheet.write(row_index, col_index, dictionary[key])
        else:
            w_sheet.write(row_index, col_index, 'Error', set_font(color_index=2))
    w_workbook.save(save_path)


def is_zero(string):
    return True if re.match(r'0+$', string) else False


def get_subversion_number(version_number):
    version_number = version_number.strip().replace(' ', '')
    if not is_version_number(version_number) or version_number is '':
        return None
    if re.match(r'\d+$', version_number):
        return ''
    return re.match(r'\d+\.(.*)$', version_number).group(1)


def version_number_compare(version_number1, version_number2):
    if not is_version_number(version_number1) or not is_version_number(version_number2):
        # print("\033[1;31mVersion number should like 'X.Y.Z...'\033[0m")
        return None
    subversion_number1 = version_number1.strip().replace(' ', '')
    subversion_number2 = version_number2.strip().replace(' ', '')
    while True:
        if (subversion_number1 is '' or is_zero(subversion_number1)) and \
                (subversion_number2 is '' or is_zero(subversion_number2)):
            return 0
        elif subversion_number1 is '' or is_zero(subversion_number1):
            return -1
        elif subversion_number2 is '' or is_zero(subversion_number2):
            return 1
        x1 = int(re.match(r'\d+', subversion_number1).group())
        x2 = int(re.match(r'\d+', subversion_number2).group())
        if x1 < x2:
            return -1
        elif x1 > x2:
            return 1

        subversion_number1 = get_subversion_number(subversion_number1)
        subversion_number2 = get_subversion_number(subversion_number2)
        if subversion_number1 is None or subversion_number2 is None:
            return None


def get_oldest_version_number(version_number_list):
    if not version_number_list:
        return None
    oldest_version_number = version_number_list[0]
    for version_number in version_number_list[1:]:
        if not is_version_number(version_number):
            continue
        if not is_version_number(oldest_version_number):
            oldest_version_number = version_number
            continue
        if version_number_compare(oldest_version_number, version_number) > 0:
            oldest_version_number = version_number
    return oldest_version_number


def is_string_in_file(string, file_path, encoding=None):
    try:
        with open(file_path, 'r', encoding=encoding, errors='ignore') as file:
            if string in file.read():
                return True
            else:
                return False
    except PermissionError as e:
        print('\r\033[1;31m' + str(e) + '\033[0m')
        # winsound.Beep(600, 1000)
        return False


def line_rough_cmp(src_line, dst_line):
    src_line = separate_word_and_nonword(src_line)
    dst_line = separate_word_and_nonword(dst_line)
    return src_line in dst_line or dst_line in src_line or src_line == dst_line


def line_cmp(src_line, dst_line):
    src_line = separate_word_and_nonword(src_line)
    dst_line = separate_word_and_nonword(dst_line)
    return src_line == dst_line


def is_line_in_lines(src_line, dst_line_list):
    for line_index, dst_line in enumerate(dst_line_list):
        if line_cmp(src_line.strip(), dst_line.strip()):
            return line_index
    return None


def is_word(string):
    return True if re.match(r'\w+$', string) else False


def get_first_line_end_index_in_line_list(line_list):
    lines = line_list_to_lines(line_list)
    return get_first_line_end_index_in_lines(line_list[0], lines)


def get_first_line_end_index_in_lines(first_line, lines):
    first_line = separate_word_and_nonword(first_line)
    match = re.match(re.escape(first_line), lines)
    if match:
        return match.end() - 1
    else:
        return None


def line_list_to_lines(line_list):
    lines = ''
    for line in line_list:
        lines += separate_word_and_nonword(line) + ' '
    return lines.strip()


def get_line_end_char_index_dict_with_lines(line_list, lines):
    line_end_char_index_dict = {}
    base_offset = 0
    for line_index, line in enumerate(line_list):
        line = separate_word_and_nonword(line)
        if line == '' and line_index != 0:
            line_end_char_index_dict.update({line_index: line_end_char_index_dict[line_index - 1] + 1})
            lines = lines[1:]
            base_offset += 1
        else:
            match = re.search(re.escape(line), lines)
            line_end_char_index_dict.update({line_index: base_offset + match.end() - 1})
            lines = lines[match.end():]
            base_offset += match.end()

    return line_end_char_index_dict


def get_line_char_end_index_dict(line_list):
    lines = line_list_to_lines(line_list)
    return get_line_end_char_index_dict_with_lines(line_list, lines)


def get_line_index(line_end_char_index_dict, lines_char_index):
    for line_index in range(len(line_end_char_index_dict)):
        if lines_char_index <= line_end_char_index_dict[line_index]:
            return line_index
    return None


def get_file_line_list(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', errors='ignore') as file:
            return file.readlines().copy()
    return []


def is_dir_empty(dir_path):
    return False if os.listdir(dir_path) else True


def clean_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    elif not is_dir_empty(dir_path):
        shutil.rmtree(dir_path)
        os.makedirs(dir_path)


def kernel_name_compare(kernel_name1, kernel_name2):
    match = re.match(r'linux-(\d+(\.\d+)*)', kernel_name1, re.I)
    if match:
        version_number1 = match.group(1)
    else:
        return None
    match = re.match(r'linux-(\d+(\.\d+)*)', kernel_name2, re.I)
    if match:
        version_number2 = match.group(1)
    else:
        return None
    return version_number_compare(version_number1, version_number2)


def cmp_to_key(cmp):
    class CmpKey(object):
        def __init__(self, obj):
            self.obj = obj

        def __lt__(self, other):
            return cmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return cmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return cmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return cmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return cmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return cmp(self.obj, other.obj) != 0

    return CmpKey


def binary_search(a_list, value, compare):
    low_index = 0
    high_index = len(a_list) - 1
    while low_index <= high_index:
        middle_index = int((low_index + high_index) / 2)
        middle_value = a_list[middle_index]
        if compare(middle_value, value) < 0:
            low_index = middle_index + 1
        elif compare(middle_value, value) > 0:
            high_index = middle_index - 1
        else:
            return middle_index
    return None


def combine_element_and_list(element=None, element_list=None, default_value=None):
    if element_list is None:
        element_list = []

    element_list.extend([element] if element else [])
    if element_list:
        return element_list
    elif default_value:
        return [default_value]
    else:
        return []


def init_workbook(save_path, head_list, sheet_name=None, sheet_name_list=None, width=1.5):
    sheet_name_list = combine_element_and_list(sheet_name, sheet_name_list, 'Sheet1')
    # Judge path exists or not
    if not os.path.exists(save_path):
        # Open workbook
        w_workbook = xlwt.Workbook()
        for sheet_name in sheet_name_list:
            w_sheet = w_workbook.add_sheet(sheet_name)
            cell_width = w_sheet.col(0).width
            for col_index in range(len(head_list)):
                w_sheet.write(0, col_index, head_list[col_index], set_font(bold=True))
                w_sheet.col(col_index).width = int(cell_width * width)
        w_workbook.save(save_path)


def padding(string, char='+'):
    return char.join(string.split())


def get_sheet_nrows(path, index=0):
    r_workbook = xlrd.open_workbook(path)
    return r_workbook.get_sheet(index).nrows


def get_sheet_nrows_by_name(path, name):
    r_workbook = xlrd.open_workbook(path)
    return r_workbook.sheet_by_name(name).nrows


def get_all_file_path_list(path):
    all_file_path_list = []
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isdir(file_path):
            all_file_path_list.extend(get_all_file_path_list(file_path))
        else:
            all_file_path_list.append(file_path)
    return all_file_path_list


def is_lines_in_lines(src_line_list, dst_line_list):
    if src_line_list == []:
        return False
    for src_line in src_line_list:
        for line_index, dst_line in enumerate(dst_line_list):
            if line_cmp(src_line.strip(), dst_line.strip()):
                match_line_index = line_index
                break
        else:
            return False
        dst_line_list = dst_line_list[match_line_index + 1:]
    return True


def add_prefix_to_file_name(dst_file_path, prefix):
    return os.path.join(os.path.dirname(dst_file_path), prefix + os.path.basename(dst_file_path))


def add_suffix_to_file_name(dst_file_path, suffix):
    return suffix.join(os.path.splitext(dst_file_path))


def copy_row(src_r_sheet, src_rowx, dst_w_sheet, dst_rowx):
    for src_colx in range(0, src_r_sheet.row_len(src_rowx)):
        dst_w_sheet.write(dst_rowx, src_colx, src_r_sheet.cell(src_rowx, src_colx).value)


def copy_specified_rows(src_r_sheet, src_start_rowx, src_colx, dst_w_sheet, dst_start_rowx, ref_list):
    for src_rowx in range(src_start_rowx, src_r_sheet.nrows):
        value = str(src_r_sheet.cell(src_rowx, src_colx).value).strip()
        if value in ref_list:
            copy_row(src_r_sheet, src_rowx, dst_w_sheet, dst_start_rowx)
            dst_start_rowx += 1


def update_count_dict(count_dict, keys):
    for key in keys:
        if key in count_dict.keys():
            count_dict[key] += 1
        else:
            count_dict.update({key: 1})


def normalization(value, value_min, value_max):
    return (value - value_min) / (value_max - value_min)


def get_dict_value(dictionary, key):
    return dictionary[key]


def get_description_in_baidubaike(key_word):
    description = ''
    if key_word is '':
        print("\033[1;31mKey word should not be empty")
        return description
    key_word = padding(key_word, '%20')

    url = 'https://baike.baidu.com/item/' + key_word
    content = requests_get_content(url, timeout=5, headers={
        'User-Agent': random.choice(user_agent_list)})
    if content:
        soup = bs4.BeautifulSoup(content, "lxml")
        for tag_div in soup.select('div.lemma-summary div'):
            description += tag_div.get_text().strip()
    return description


def get_cve_id_list(url):
    cve_id_list = []
    content = requests_get_content(url, timeout=10, headers={'User-Agent': random.choice(user_agent_list)})
    if content:
        soup = bs4.BeautifulSoup(content, 'lxml')
        for tag_a in soup.select('div#row table[data-testid=vuln-results-table] tbody tr th strong a'):
            cve_id_list.append(tag_a.get_text().strip())
    return cve_id_list


def get_cve_count(key_word):
    if key_word == '':
        return None
    key_word = padding(key_word)
    entry_url = 'https://nvd.nist.gov/vuln/search/results' \
                '?form_type=Basic&results_type=overview' \
                '&query=' + key_word + '&search_type=all&startIndex=0'
    content = requests_get_content(entry_url, timeout=10,
                                   headers={
                                       'User-Agent': random.choice(user_agent_list)})
    if content:
        soup = bs4.BeautifulSoup(content, 'lxml')
        for tag_strong in soup.select('strong[data-testid=vuln-matching-records-count]'):
            return int(tag_strong.get_text().strip().replace(',', ''))
    return None


def clean_empty_directory(root_path):
    for file_name in os.listdir(root_path):
        file_path = os.path.join(root_path, file_name)
        if os.path.isdir(file_path) and not os.listdir(file_path):
            os.rmdir(file_path)


def get_reference_dict_list(soup):
    reference_dict_list = []
    for tag_tr in soup.select('table[data-testid=vuln-hyperlinks-table] tbody tr'):
        reference_dict = {}
        for tag_td in tag_tr.select('td'):
            tag_td_text = tag_td.get_text().strip()
            if re.match(r'vuln-hyperlinks-link-', tag_td['data-testid'], re.I):
                reference_dict.update({'Hyperlink': tag_td_text})
            elif re.match(r'vuln-hyperlinks-restype-', tag_td['data-testid'], re.I):
                reference_dict.update({'Resource': tag_td_text})
        reference_dict_list.append(reference_dict)
    return reference_dict_list


def get_all_cwe_id_list():
    url = 'https://nvd.nist.gov/vuln/categories'
    content = requests_get_content(url)
    cwe_id_list = []
    if content:
        soup = bs4.BeautifulSoup(content, 'lxml')
        for tag_td in soup.select('div#page-content div.row table[data-testid=vuln-feed-table] tbody tr td'):
            if re.match(r'CWE-\d+', tag_td.get_text().strip()) \
                    or re.match(r'NVD-CWE-Other', tag_td.get_text().strip()) \
                    or re.match(r'NVD-CWE-noinfo', tag_td.get_text().strip()):
                cwe_id_list.append(tag_td.get_text().strip())
    return cwe_id_list


def excel_to_np_array(path):
    r_workbook = xlrd.open_workbook(path)
    r_sheet = r_workbook.sheet_by_index(0)
    matrix = []
    for rowx in range(r_sheet.nrows):
        row_array = []
        for colx in range(r_sheet.ncols):
            row_array.append(r_sheet.cell_value(rowx, colx))
        matrix.append(row_array)
    return numpy.array(matrix)


def np_array_to_excel(np_array, path):
    w_workbook = xlsxwriter.Workbook(path)
    w_sheet = w_workbook.add_worksheet()
    for rowx in range(np_array.shape[0]):
        for colx in range(np_array.shape[1]):
            w_sheet.write(rowx, colx, np_array[rowx][colx])
    w_workbook.close()


def convert_to_one_hot(np_array, class_number, bounds=(0, 1)):
    one_hot_np_array = numpy.zeros([np_array.shape[0], class_number], dtype='Int32') + bounds[0]
    for rowx in range(np_array.shape[0]):
        one_hot_np_array[rowx, int(np_array[rowx])] = bounds[1]
    return one_hot_np_array


def reverse_one_hot(one_hot_np_array, bounds=(0, 1)):
    np_array = numpy.zeros([one_hot_np_array.shape[0], 1], dtype='Int32')
    for rowx in range(one_hot_np_array.shape[0]):
        np_array[rowx] = numpy.where(one_hot_np_array[rowx] == bounds[1])[0]
    return np_array


def reverse_one_hot_like(one_hot_like_np_array):
    np_array = numpy.zeros([one_hot_like_np_array.shape[0], 1], dtype='Int32')
    for rowx in range(one_hot_like_np_array.shape[0]):
        np_array[rowx] = numpy.where(one_hot_like_np_array[rowx] == one_hot_like_np_array[rowx].max())[0]
    return np_array


def save_one_hot(src_path, class_number, one_hot_path):
    np_array_to_excel(convert_to_one_hot(excel_to_np_array(src_path), class_number), one_hot_path)


def save_one_hot_reversal(one_hot_path, dst_path):
    np_array_to_excel(reverse_one_hot(excel_to_np_array(one_hot_path)), dst_path)


def save_one_hot_like_reversal(one_hot_like_path, dst_path):
    np_array_to_excel(reverse_one_hot_like(excel_to_np_array(one_hot_like_path)), dst_path)
