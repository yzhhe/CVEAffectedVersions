import pandas as pd
import os

# #文件路径
# file_dir = r'D:\北交\漏洞\测试代码\lll'
# #构建新的表格名称
# new_filename = file_dir + '\\new_file.xls'
# #找到文件路径下的所有表格名称
# file_list = os.walk(file_dir)
# new_list = []
#
# for dir_path,dirs,files in file_list:
#     for file in files:
#         #重构文件路径
#         file_path = os.path.join(dir_path,file)
#         #将excel转换成DataFrame
#         df = pd.read_excel(file_path)
#         new_list.append(df)
#
# #多个DataFrame合并为一个
# df = pd.concat(new_list)
# #写入到一个新excel表中
# df.to_excel(new_filename,index=False)

import re
if __name__ == '__main__':
    ll = ['2018-2-2','2017-3-2','2020-12-2']
    print(min(ll))

    if  '3.1.1'.startswith('1.1'):
        print("neng ")

    s2 = 'b'
    s1 = 'aa' + s2
    print(s1)
    result = re.match(r'\d+\.\d+\.\d+','3.11')
    if result:
        print('yes')
    else:
        print('wrong')





















