#coding=utf-8
import re
import os
#os.path模块主要用来文件属性获取
def compare_files(bm_file,dst_file):
    bm_size=os.path.getsize(bm_file)
    dst_size = os.path.getsize(dst_file)
    print(bm_size,dst_size)

compare_files(r'D:\documents\linux kernel\linux-3.8\linux-3.8\net\ceph\auth_x.c',
              r'C:\Users\Administrator\Desktop\2014-6418.txt')





