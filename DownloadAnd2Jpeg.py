import ftplib
import os
import sys
import shutil
import subprocess

debugPrint = True  # 设置为True时打印所有信息，设置为False时只打印下载完成和转图结束信息

# 定义要拷贝的文件路径和要运行的文件名
file_name = "_CopyAndRun.py"
source_file = os.path.join("F:\\Tools\\TF测试大一统ing\\improving", file_name)

# 定义本地目录主路径
local_main_path = "E:\\XJM_StarMeizu\\ReportContents\\"

# FTP 服务器信息
ftp_host = "ftp.arcsoft.com.cn"
ftp_user = "forXJMZ"
ftp_password = "4744rX74"


# 从命令行参数获取远程路径
# 获取命令行参数
args = sys.argv[1:]
relative_path = " ".join(args) # python DownloadAnd2Jpeg.py 2481 TFHDR/20240129 ，其中‘2481 TFHDR/20240129’是个整体，忽略空格影响

# 将参数合并为一个完整的远程路径
remote_path = "/" + relative_path 

# 组合本地路径
local_path = os.path.normpath(os.path.join(local_main_path, relative_path.split('魅族算法问题/')[1]))

if debugPrint:
    print("远程FTP完整路径:", remote_path)
    print("本地完整路径:", local_path)

# 连接到 FTP 服务器
ftp = ftplib.FTP(ftp_host, ftp_user, ftp_password)

# 下载远程路径下的所有内容到本地路径
def download_ftp_dir(ftp, remote_dir, local_dir):
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    ftp.cwd(remote_dir)
    items = ftp.nlst()
    for item in items:
        local_item = os.path.join(local_dir, item)
        if "." in item:  # 文件
            with open(local_item, "wb") as f:
                ftp.retrbinary("RETR " + item, f.write)
        else:  # 文件夹
            download_ftp_dir(ftp, item, local_item)

download_ftp_dir(ftp, remote_path, local_path)

# 关闭 FTP 连接
ftp.quit()

print("下载完成")


# 拷贝固定目录中文件到下载到本地的最高层目录
shutil.copy(source_file, local_path)
if debugPrint:
    print("拷贝源目录:", source_file)
    print("拷贝目的目录:", local_path)


# 切换当前工作目录到 local_path，为了后续运行服务
os.chdir(local_path)
# 运行文件
subprocess.run(["python", os.path.join(local_path, file_name)]) # 同步行为

print("转图结束")