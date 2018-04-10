# _*_ coding: utf-8 _*_
__author__ = 'Administrator'

import urllib2
import threading
from optparse import OptionParser
from bs4 import BeautifulSoup
import sys
import re
import urlparse
import Queue
import hashlib


def download(url, name):
    #path = "C:\\Users\\Administrator\\Desktop\\GPS"
    # url = "http://pic2.sc.chinaz.com/files/pic/pic9/201309/apic520.jpg"
    # url = "https://maps.googleapis.com/maps/api/streetview?size=600x300&location=46.414382,10.013988&heading=151.78&pitch=-0.76&key="#你的KEY"

    # 保存文件时候注意类型要匹配，如要保存的图片为jpg，则打开的文件的名称必须是jpg格式，否则会产生无效图片
    conn = urllib2.urlopen(url)
    f = open(name, 'wb')
    f.write(conn.read())
    f.close()
    print('Pic Saved!')


#fp = open("E:\\Desktop\\GPS\\spider_google.txt", "r")
fp = open("spider_bd_map.txt","r")

for line in fp.readlines():
    #line = (lambda x: x[11:-11])(line)
    line=line.strip('\n')
    zu = line.split(',')
    jin = zu[0]
    wei = zu[1]
    #heading = zu[2]
    img_name = "E:\\didi\\map\\bd\\out_image\\" + jin + "_" + wei +".JPG"
    #url = "https://maps.googleapis.com/maps/api/streetview?size=600x300&location=46.414382,10.013988&heading=151.78&pitch=-0.76&key="  # 你的KEY"
    url = "http://api.map.baidu.com/panorama/v2?ak=9FcRfTXGEkpiBMrkjV7d2BGOVBXcaAoo&width=1024&height=512&location="+jin+","+wei+"&fov=180"  # 你的KEY"
    # print zu
    print img_name
    # print url
    download(url, img_name)

fp.close()