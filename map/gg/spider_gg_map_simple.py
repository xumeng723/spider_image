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
    conn = urllib2.urlopen(url)
    f = open(name, 'wb')
    f.write(conn.read())
    f.close()
    print('Pic Saved!')


fp = open("E:\\didi\\map\\gg\\spider_gg_map.txt", "r")

for line in fp.readlines():
    #line = (lambda x: x[11:-11])(line)
    #line = line.split('\n')[0]
    line=line.strip('\n')
    zu = line.split(',')
    jin = zu[0]
    wei = zu[1]
    #heading = zu[2]
    name = "E:\\didi\\map\\gg\\out_image\\" + jin + "_" + wei +".JPG"
    #url = "https://maps.googleapis.com/maps/api/streetview?size=600x300&location=46.414382,10.013988&heading=151.78&pitch=-0.76&key="  # 你的KEY"
    url = "https://maps.googleapis.com/maps/api/streetview?size=936x537&location=" + jin + "," + wei + "&heading=270&pitch=-004&key="  # 你的KEY"
    # print zu
    print name
    # print url
    download(url, name)

fp.close()