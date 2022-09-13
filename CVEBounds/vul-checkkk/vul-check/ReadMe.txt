IsCVEInProject_v5.0_1 是无版本限制：（Linux环境下运行）
命令：Python isCVEInProject_unlimited.py 源代码绝对路径 被测系统根目录  new
Python isCVEInProject_unlimited.py 源代码绝对路径 被测系统根目录  cont cve编号

 python IsCVEInProject_unlimited.py /home/greatwall/vul-check/linux-4.14.76 /home/greatwall/vul-check new

IsCVEInProject_v5.0_2 是有版本限制，Linux kernel 需要用到all_cve_version以及Linux Kernel Release Time.xls
启动命令：Python IsCVEInProject_limited.py 源代码绝对路径 被测系统根目录 测试的版本编号前两位 new
          Python IsCVEInProject_limited.py 源代码绝对路径 被测系统根目录 测试的版本编号前两位 cont cve编号

更新Patch方法：（Windows环境下运行）
①如果是Linux kernel，修改main函数的保存路径，然后直接运行LinuxKernelPatchCrawler.py，就可以更新linux的Patch，测试方法不变。
②如果是应用工具的Patch更新，i、如果是全部的应用层工具更新，则直接启动NVDVulnInfoCrawler2.py的main方法
更新APP文件，而后点击相应的应用层爬虫即可。比如OpenSSLPatchCrawler.py。ii、如果只想更新一个引用层，
则使用NVDVulnInfoCrawler2.py的main2方法。需要修改一下371行。将main注释掉，换成main2。同时注意修改OSSList_single.xls
将Name换成你需要更新的工具名，Number就是要生成的文件名，可以将APP-*后面的数字换掉。然后运行NVDVulnInfoCrawler2.py，
之后再运行对应的爬虫就行了。

如果有提示路径不对的，则更换为你的根路径。

