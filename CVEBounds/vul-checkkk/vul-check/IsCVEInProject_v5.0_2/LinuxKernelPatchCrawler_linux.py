# coding=UTF-8
# Author: 14281055 Liheng Chen CIT BJTU
# File Name: LinuxKernelPatchCrawler.py


import re
import os
import bs4
import Repository
import random
import shutil
from io import StringIO
from bs4 import BeautifulSoup
from distutils.filelist import findall
import requests


def save_patch_in_git_kernel_org(hyperlink, save_dir):
    Repository.clean_dir(save_dir)
    text = Repository.requests_get_text(hyperlink, timeout=10,
                                        headers={'User-Agent': random.choice(Repository.user_agent_list)})
    if text:
        soup = bs4.BeautifulSoup(text.replace('<br/>', '\n').replace('<br>', '\n'), 'lxml')
        for tag_table in soup.select('div#cgit div.content table.diff'):
            if tag_table['summary'] == 'diff':
                vuln_file_name = ''
                has_vuln_file_name = False
                for tag_div in tag_table.select('div'):
                    if 'head' in tag_div['class']:
                        vuln_file_name_list = []
                        bm_and_am_code_hyperlink_list = []
                        for tag_a in tag_div.select('a'):
                            vuln_file_name_list.append(tag_a.get_text().strip())
                            bm_and_am_code_hyperlink_list.append("https://git.kernel.org" + tag_a['href'])
                        if len(vuln_file_name_list) != 2 or len(bm_and_am_code_hyperlink_list) != 2:
                            has_vuln_file_name = False
                            continue
                        vuln_file_name = vuln_file_name_list[0].replace('/', '#~')
                        has_vuln_file_name = True
                        Repository.append_file_with_eol(os.path.join(save_dir, vuln_file_name),
                                                        tag_div.get_text())
                        if not Repository.save_tag_code_from_html(
                                bm_and_am_code_hyperlink_list[0],
                                os.path.join(save_dir, '(BM)' + vuln_file_name)
                        ):
                            print('\r\033[1;31mFail:(BM)' + vuln_file_name + '\033[0m')
                            return False
                        if not Repository.save_tag_code_from_html(
                                bm_and_am_code_hyperlink_list[1],
                                os.path.join(save_dir, '(AM)' + vuln_file_name)
                        ):
                            print('\r\033[1;31mFail:(AM)' + vuln_file_name + '\033[0m')
                            return False
                    elif has_vuln_file_name:
                        Repository.append_file_with_eol(os.path.join(save_dir, vuln_file_name),
                                                        tag_div.get_text())
            Repository.append_file_with_eol(os.path.join(save_dir, 'Source.txt'),
                                            'git.kernel.org')
            return True
    return False


def save_patch_in_patchwork_kernel_org(hyperlink, save_dir):
    Repository.clean_dir(save_dir)
    content = Repository.requests_get_content(hyperlink, timeout=10,
                                              headers={
                                                  'User-Agent': random.choice(Repository.user_agent_list)})
    if content:
        soup = bs4.BeautifulSoup(content, 'lxml')
        has_vuln_file_name = False
        vuln_file_name = ''
        for tag_span in soup.select('div#content div.patch pre.content span'):
            if 'p_header' in tag_span['class']:
                match = re.match('diff\s+--git\s+a/(.*?)\s+b/(.*)', tag_span.get_text().strip(), re.I)
                if match:
                    vuln_file_name = match.group(1).replace('/', '#~')
                    has_vuln_file_name = True
                    Repository.append_file_with_eol(os.path.join(save_dir, vuln_file_name),
                                                    tag_span.get_text())
                elif has_vuln_file_name:
                    Repository.append_file_with_eol(os.path.join(save_dir, vuln_file_name),
                                                    tag_span.get_text())
            elif has_vuln_file_name:
                Repository.append_file_with_eol(os.path.join(save_dir, vuln_file_name),
                                                tag_span.get_text())
        Repository.append_file_with_eol(os.path.join(save_dir, 'Source.txt'),
                                        'patchwork.kernel.org')
        return True
    return False


def save_bm_code_in_github_com(hyperlink, save_path):
    if os.path.exists(save_path):
        os.remove(save_path)
    content = Repository.requests_get_content(hyperlink, timeout=10,
                                              headers={
                                                  'User-Agent': random.choice(Repository.user_agent_list)})
    if content:
        soup = bs4.BeautifulSoup(content, 'lxml')
        for tag_td in soup.select(
                'table.highlight.tab-size.js-file-line-container td.blob-code.blob-code-inner.js-file-line'):
            Repository.append_file_with_eol(save_path, tag_td.get_text())
        return True
    return False


def save_patch_in_github_com(hyperlink, save_dir):
    Repository.clean_dir(save_dir)
    content = Repository.requests_get_content(hyperlink, timeout=10,
                                              headers={
                                                  'User-Agent': random.choice(Repository.user_agent_list)})
    if content:
        soup = bs4.BeautifulSoup(content, 'lxml')
        for tag_div_diff in soup.select(
                'div.js-diff-progressive-container '
                'div.file.js-file.js-details-container.Details.show-inline-notes'):
            vuln_file_name = ''
            for tag_a in tag_div_diff.select('div.file-header.js-file-header div.file-info a.link-gray-dark'):
                vuln_file_name = tag_a.get_text().strip().replace('/', '#~')
            for tag_a in tag_div_diff.select('div.file-actions a.btn.btn-sm.tooltipped.tooltipped-nw'):
                bm_code_hyperlink = 'https://github.com' + tag_a['href']
                if not save_bm_code_in_github_com(bm_code_hyperlink,
                                                  os.path.join(save_dir, '(BM)' + vuln_file_name)):
                    print('\r\033[1;31mFail:(BM)' + vuln_file_name + '\033[0m')
                    return False
            for tag_table in tag_div_diff.select(
                    'div.js-file-content.Details-content--shown table.diff-table.tab-size'):
                Repository.append_file_with_eol(os.path.join(save_dir, vuln_file_name),
                                                re.sub(r'\n+', r'\n', tag_table.get_text()))
        Repository.append_file_with_eol(os.path.join(save_dir, 'Source.txt'),
                                        'github.com')
        return True
    return False


def save_patch(cve_info_url, cve_id, save_root):
    # 判断CVE编号漏洞文件夹是否存在
    save_dir = os.path.join(save_root, cve_id)
    if os.path.exists(save_dir):
        return True
    else:
        os.makedirs(save_dir)

    content = Repository.requests_get_content(cve_info_url, timeout=10,
                                              headers={
                                                  'User-Agent': random.choice(Repository.user_agent_list)})
    if content:
        url_soup = bs4.BeautifulSoup(content, "lxml")
        temp = url_soup.select("span[data-testid=vuln-cvssv3-base-score]")
        str1 = ' '.join(map(lambda _: ' '.join(_.contents), temp))

        # print(str1)
        # print(os.path.join(save_dir, 'Score.txt'))
        # with open(os.path.join(save_dir, 'Score.txt'),'a') as f:
        #     f.write(str1+'\n')
        # print(open(os.path.join(save_dir, 'Score.txt'), 'r').read())
        reference_dict_list = Repository.get_reference_dict_list(url_soup)
        has_patch = False
        for reference_dict in reference_dict_list:
            reference_hyperlink = reference_dict['Hyperlink']
            if re.match(r'https?://git\.kernel\.org', reference_hyperlink, re.I):
                has_patch = True
                if save_patch_in_git_kernel_org(reference_hyperlink, save_dir):
                    return True
                else:
                    continue
            elif re.match(r'https?://patchwork\.kernel\.org', reference_hyperlink, re.I):
                has_patch = True
                if save_patch_in_patchwork_kernel_org(reference_hyperlink, save_dir):
                    return True
                else:
                    continue
            elif re.match(r'https?://github\.com', reference_hyperlink, re.I):
                has_patch = True
                if save_patch_in_github_com(reference_hyperlink, save_dir):
                    return True
                else:
                    continue
        if not has_patch:
            return True
    shutil.rmtree(save_dir)
    open(os.path.join(save_dir, 'Score.txt'),'a').write(str1+'\n')
    return False


def save_linux_kernel_patch(save_root):
    key_word = "linux+kernel"

    cve_count = Repository.get_cve_count(key_word)
    if not cve_count or cve_count <= 0:
        return False
    count = 1
    # 构造查询结果的网页链接
    for start_index in range(0, cve_count, 20):
        search_result_url = 'https://nvd.nist.gov/vuln/search/results' \
                            '?form_type=Basic&results_type=overview' \
                            '&query=' + key_word + '&search_type=all&startIndex=' + str(start_index)
        print("\rConnect:" + search_result_url, end='')

        # 捕获一页中的漏洞的CVE编号
        cve_id_list = Repository.get_cve_id_list(search_result_url)
        if not cve_id_list:
            count += 20
            print("\r\033[1;31mNo CVEs:" + search_result_url + '\033[0m')
            continue

        # 捕获每一个CVE的补丁代码
        for cve_id in cve_id_list:
            # cve_id = 'CVE-2016-3841'

            if cve_id in os.listdir(save_root):
                return True
            cve_info_url = ("https://nvd.nist.gov/vuln/detail/" + cve_id)
            print("\rConnect:" + cve_info_url + '\tCount:' + str(count) + '\tRate:' + str(
                int(count / cve_count * 100)) + '%', end='')
            if not save_patch(cve_info_url, cve_id, save_root):
                print('\r\033[1;31mFail:' + cve_id + '\033[0m')
            count += 1
    return True

import sys

def prompt():
    print('''请输入Python LinuxKernelPatchCrawler_linux.py CVE漏洞库绝对路径''')
    sys.exit(0)


if __name__ == "__main__":
    try:
        downloadPath = sys.argv[1]
        print(downloadPath)
        if '/' not in downloadPath:
            prompt()
        save_linux_kernel_patch(downloadPath)
    except IndexError:
            prompt()
