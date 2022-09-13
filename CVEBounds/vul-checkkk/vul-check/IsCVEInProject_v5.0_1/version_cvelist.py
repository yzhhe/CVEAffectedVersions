# coding:utf-8
import os
import re
from bs4 import BeautifulSoup
from distutils.filelist import findall
import requests

#CVE对应版本号


# 获取网页内容
'''
def cat_code(url, list, file_name):
    r = requests.get(url)
    data = r.text
    # 利用正则查找所有连接
    link_list = re.findall(
        r"(https?:\/\/git\.kernel\.org\/cgit\/linux\/kernel\/git\/torvalds\/linux\.git\/commit\/\?id=[0-9]+[a-zA-Z]+[0-9a-zA-Z]*)",
        data)  # 数字开头连接
    # print link_list[0]
    # print link_list
    if len(link_list) < 1:
        link_list = re.findall(
            r"(https?:\/\/git\.kernel\.org\/cgit\/linux\/kernel\/git\/torvalds\/linux\.git\/commit\/\?id=[a-zA-Z]+[0-9]+[0-9a-zA-Z]*)",
            data)  # 字母开头连接
        if len(link_list) < 1:
            print ("无链接！")
        else:
            list1 = []
            list2 = []
            list3 = []
            list4 = []
            print (link_list[0])
            content = requests.get(link_list[0]).content
            soup = BeautifulSoup(content, "html.parser")
            for tag in soup.find_all('td', class_='upd'):
                for c_name in tag.find_all('a'):
                    print (c_name.get_text())
                    list1.append(c_name.get_text())  # 漏洞文件名字
            for tag in soup.find_all('table', class_='diff'):
                for cve_code in tag.find_all('div'):
                    print (cve_code.get_text())  # 漏洞代码
                    list1.append(cve_code.get_text())

            for tag in soup.find_all('div', class_='head'):
                for pre_c_file in tag.find_all('a'):
                    print (pre_c_file['href'])
                    list2.append(pre_c_file['href'])

            content = requests.get("https://git.kernel.org" + list2[0]).content  # 获取修改之前文件代码
            soup = BeautifulSoup(content, "html.parser")
            for pre in soup.find_all('code'):
                print (pre.get_text())
                list3.append(pre.get_text())
                # for pre_code in pre.find_all('span'):
                # print pre_code.get_text()
                # list3.append(pre_code.get_text())

            content = requests.get("https://git.kernel.org" + list2[1]).content  # 获取修改之后文件代码
            soup = BeautifulSoup(content, "html.parser")
            for post in soup.find_all('code'):
                print (post.get_text())
                list4.append(post.get_text())
                # for post_code in post.find_all('span'):
                # print post_code.get_text()
                # list4.append(post_code.get_text())
            dir = 'D:\\CVE\\' + list[file_name]
            print (dir)
            if os.path.isfile(dir):
                #os.remove(dir)
                return 0
            else:
                os.makedirs(dir)  # 创建以cve编号为文件夹名的文件夹
                fileObject = open(dir + '\\CVE_Patch.txt', 'a')
            for cve_info1 in list1:  # 存入patch信息
                fileObject.write(cve_info1)
                fileObject.write('\n')
            fileObject.close()

            fileObject = open(dir + '\\CVE_Precode.txt', 'a')
            for cve_pre in list3:  # 存入修改前代码
                fileObject.write(cve_pre)
                fileObject.write('\n')
            fileObject.close()

            fileObject = open(dir + '\\CVE_Postcode.txt', 'a')
            for cve_post in list4:  # 存入修改后代码
                fileObject.write(cve_post)
                fileObject.write('\n')
            fileObject.close()
    else:
        list1 = []
        list2 = []
        list3 = []
        list4 = []
        print (link_list[0])
        content = requests.get(link_list[0]).content
        soup = BeautifulSoup(content, "html.parser")
        for tag in soup.find_all('td', class_='upd'):
            for c_name in tag.find_all('a'):
                print (c_name.get_text())
                list1.append(c_name.get_text())  # 漏洞文件名字
        for tag in soup.find_all('table', class_='diff'):
            for cve_code in tag.find_all('div'):
                print (cve_code.get_text())  # 漏洞代码
                list1.append(cve_code.get_text())

        for tag in soup.find_all('div', class_='head'):
            for pre_c_file in tag.find_all('a'):
                print (pre_c_file['href'])
                list2.append(pre_c_file['href'])

        content = requests.get("https://git.kernel.org" + list2[0]).content  # 获取修改之前文件代码
        soup = BeautifulSoup(content, "html.parser")
        for pre in soup.find_all('code'):
            print (pre.get_text())
            list3.append(pre.get_text())
            # for pre_code in pre.find_all('span'):
            # print pre_code.get_text()
            # list3.append(pre_code.get_text())

        content = requests.get("https://git.kernel.org" + list2[1]).content  # 获取修改之后文件代码
        soup = BeautifulSoup(content, "html.parser")
        for post in soup.find_all('code'):
            print (post.get_text())
            list4.append(post.get_text())
            # for post_code in post.find_all('span'):
            # print post_code.get_text()
            # list4.append(post_code.get_text())

        dir = 'D:\\CVE\\' + list[file_name]
        print (dir)
        if os.path.exists(dir):
            #os.remove(dir)
            print 'ok'
            return False
        else:
            os.makedirs(dir)  # 创建以cve编号为文件夹名的文件夹
            fileObject = open(dir + '\\CVE_Patch.txt', 'a')
        for cve_info1 in list1:  # 存入patch信息
            fileObject.write(cve_info1)
            fileObject.write('\n')
        fileObject.close()

        fileObject = open(dir + '\\CVE_Precode.txt', 'a')
        for cve_pre in list3:  # 存入修改前代码
            fileObject.write(cve_pre)
            fileObject.write('\n')
        fileObject.close()

        fileObject = open(dir + '\\CVE_Postcode.txt', 'a')
        for cve_post in list4:  # 存入修改后代码
            fileObject.write(cve_post)
            fileObject.write('\n')
        fileObject.close()
'''

def cat_cve_num(r):
    soup = BeautifulSoup(requests.get(r).content, "html.parser")
    version_list = list(filter(lambda x: x.startswith('CVE'),
                               [cve.get_text()
                                for tag in soup.find_all('tr', class_='srrowns')
                                for tag1 in tag.find_all('td')
                                for cve in tag1.find_all('a')]))
    print(version_list)


    for i in range(0,len(version_list)):
        ver = re.findall(r"\d*\.?\d*\.?\d*",version_list[i])
        for j in range(0, len(ver)):
            if ver[j] != '':
                version=ver[j]
                print(version)
                r="https://nvd.nist.gov/vuln/search/results?form_type=Advanced&cves=on&cpe_version=cpe%3a%2fo%3alinux%3alinux_kernel%3a"+version
                content = requests.get(r).content
                soup = BeautifulSoup(content, "html.parser")
                for tag1 in soup.find_all('div', class_='col-sm-12 col-lg-3'):
                    for page in tag1.find_all('strong'):
                        #print(page.get_text())
                        page1 = int(page.get_text().replace(',', '')) / 20
                        print(int(page1))
                        break

                    for i in range(0, int(page1)+1):
                        content = requests.get(r + "&startIndex=" + str(i * 20)).content
                        soup = BeautifulSoup(content, "html.parser")
                        tag1=soup.find('tbody')

                        for tag2 in tag1.find_all('th'):
                            cvelist = tag2.get_text()
                            cvelist = cvelist.strip('\n')
                            print(cvelist)
                            with open("E:\研究生\实验室\漏洞相关\IsCVEInProject_v5.0\ew results\\linux kernel %s.txt" % version,"a") as f:
                                f.write(cvelist)
                                f.write('\n')

                                    # for i in range(0,100):




if __name__ == "__main__":
    k1 = int(input('开始页码:'))
    k2 = int(input('结束页码:'))
    for k3 in range(k1, k2 + 1):
        num = (k3 - 1) * 50
        # cat_cve_num()
        r = "https://www.cvedetails.com/vulnerability-list/vendor_id-33/product_id-47/Linux-Linux-Kernel.html" + str(
            num)
        print(r)
        cat_cve_num(r)
