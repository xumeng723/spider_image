# # -*- coding: utf-8 -*- 
import urllib
import re
import time
import os 
def save_img(img_url,file_name,file_path='book\img'):
    #保存图片到磁盘文件夹 file_path中，默认为当前脚本运行目录下的 book\img文件夹
    try:
        if not os.path.exists(file_path):
            print '文件夹',file_path,'不存在，重新建立'
            #os.mkdir(file_path)
            os.makedirs(file_path)
        #获得图片后缀
        #file_suffix = os.path.splitext(img_url)[1]
        #拼接图片名（包含路径）
        filename_1 = '{}{}{}'.format(file_path,os.sep,file_name)
        filename = filename_1.replace('\n','')
       #下载图片，并保存到文件夹中
        urllib.urlretrieve(img_url,filename=filename)
    except IOError as e:
        print '文件操作失败',e
    except Exception as e:
        print '错误 ：',e
def main(filename):
    f = open(filename,'r')
    for line in open(filename):
        img_url = f.readline()
        filename = img_url.split('/')[-1]
        save_img(img_url,filename)
