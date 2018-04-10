# # -*- coding: utf-8 -*- 
import urllib
import re
import time
import os 

# #显示下载进度  
# def schedule(a,b,c):  
#     ''' 
#     a:已经下载的数据块 
#     b:数据块的大小 
#     c:远程文件的大小 
#    '''  
#     per = 100.0 * a * b / c  
#     if per > 100 :  
#         per = 100  
#     print '%.2f%%' % per 

# def getHtml(url):
# 	f = open('./picture_list.txt', 'r')
# 	for line in open('picture_list.txt'):
# 		html = f.readline()
# 		return html
# def save_img(img_url,file_name,file_path='.\img'):
#     #保存图片到磁盘文件夹 file_path中，默认为当前脚本运行目录下的 book\img文件夹
#     try:
#         if not os.path.exists(file_path):
#             print '文件夹',file_path,'不存在，重新建立'
#             #os.mkdir(file_path)
#             os.makedirs(file_path)
#         #获得图片后缀
#         file_suffix = os.path.splitext(img_url)[1]
#         #拼接图片名（包含路径）
#         filename = '{}{}{}{}'.format(file_path,os.sep,file_name,file_suffix)
#        #下载图片，并保存到文件夹中
#         urllib.urlretrieve(img_url,filename=filename)
#     except IOError as e:
#         print '文件操作失败',e
#     except Exception as e:
#         print '错误 ：',e


# def downloadImg(html):  
#     #reg = r'src="(.+?\.jpg)" pic_ext'  
#     #imgre = re.compile(reg)  
#     imglist = re.findall(imgre, html)  
#     #定义文件夹的名字  
#     t = time.localtime(time.time())  
#     foldername = str(t.__getattribute__("tm_year"))+"-"+str(t.__getattribute__("tm_mon"))+"-"+str(t.__getattribute__("tm_mday"))  
#     picpath = 'D:\\ImageDownload\\%s' % (foldername) #下载到的本地目录  
      
#     if not os.path.exists(picpath):   #路径不存在时创建一个  
#         os.makedirs(picpath)     
#     x = 0  
#     for imgurl in imglist:  
#         target = picpath+'\\%s.jpg' % x  
#         print 'Downloading image to location: ' + target + '\nurl=' + imgurl  
#         image = urllib.urlretrieve(imgurl, target, schedule)  
#         x += 1  
#     return image;
#     save_img(img_url,'jianshu')
# if __name__ == '__main__':  
#     t = time.localtime(time.time())  
#     foldername = str(t.__getattribute__("tm_year"))+"-"+str(t.__getattribute__("tm_mon"))+"-"+str(t.__getattribute__("tm_mday"))  
#     file_path = '.\\ImageDownload\\%s' % (foldername) #下载到的本地目录    
#     #html = getHtml("http://tieba.baidu.com/p/2460150866")  
#     #file_path = ./picture
#   		with open('./picture_list.txt', 'r') as f:
# 			for line in open('picture_list.txt'):
# 				html = f.readline()
# 				save_img(img_url,' ',file_path=file_path)
#     #downloadImg(html)  
#     print "Download has finished." 

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

if __name__ == '__main__':
    #img_url = 'https://img-hxy021.didistatic.com/static/godeyes/20171108080004_377728973527932928_21_891316.jpg'
    f= open('./picture_list.txt', 'r')
    for line in open('picture_list.txt'):
    	img_url = f.readline()
# 				html = f.readline()
    	filename = img_url.split('/')[-1]
    	#if filename[len(filename)-1] == '?':
    	#	print "wrong" 
    	#filename = filename_1.replace('?','')
    	#filename = filename_1.split('.jpg?')[0]
    	#filename = filename_1.split('')[0]
    	save_img(img_url,filename)

# if __name__ == '__main__':
#     file_path = 'I:'+os.sep + 'myimg'
#     img_url = 'http://upload.jianshu.io/admin_banners/web_images/2474/259a36ccbca577c3064c68ab3c0f1834d77456d7.png'
#     save_img(img_url,'jianshu',file_path=file_path)

