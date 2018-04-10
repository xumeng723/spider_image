# coding=utf-8
import urllib2
import json
import math
import os
import numpy as np
import cv2

def concat_img(img_list, height, width):
    try:
        if len(img_list) < height*width:
            return False, 0

        shape_width = img_list[0].shape[1]
        shape_height = img_list[0].shape[0]

        result = np.zeros((shape_height * height, shape_width * width, 3))

        for w in xrange(width):
            for h in xrange(height):
                start_h = h * shape_height
                end_h = (h + 1) * shape_height

                start_w = w * shape_width
                end_w = (w + 1) * shape_width

                result[start_h:end_h, start_w:end_w, :] = img_list[w * height + h]

        return True, result
    except Exception, e:
        print "ERROR CONCAT"
        return False, 0


# 经纬度坐标转化为墨卡托坐标
def LL2MER(lon, lat):
    EARTH_RADIS = 6378137
    lon = float(lon)
    lat = float(lat)
    mercator_x = lon * (EARTH_RADIS * math.pi / 180.0)
    mercator_y = math.log(math.tan((90.0 + lat) * math.pi / 360.0)) * EARTH_RADIS
    #print mercator_x, mercator_y
    return mercator_x, mercator_y

# 根据墨卡托坐标得到svid
def get_svid(new_MER):
    url = 'http://sv.map.qq.com/xf?x={0}&y={1}&r=600&output=json'
    json_url = url.format(new_MER[0],new_MER[1])
    try:
        res = urllib2.urlopen(json_url).read()
        a_res = json.loads(res.decode('gbk'))
        return a_res["detail"]["svid"]
    except Exception, e:
        raise Exception('ERROR JSON URL')
#更新墨卡托坐标（加入4m扰动）
def update_MER(MER,angle):
	rad = math.radians(angle)
	#print rad 
	#print math.sin(rad)
	#print math.cos(rad)
	#print MER[0]
	#print MER[1]
	real_mercator_x = MER[0]+4*(math.sin(rad))
	real_mercator_y = MER[1]+4*(math.cos(rad))
	#print  real_mercator_x,real_mercator_y
	return real_mercator_x,real_mercator_y

# 根据svid下载图片
def grab_img(svid, out_dir,name_base):
    #name = num+"_"+cate+"_"+long+"_"+lati
    url = "http://sv1.map.qq.com/tile?svid={0}&x={1}&y={2}&from=web&level=1"
    img_split = []
    for x in range(4, 13):
        for y in range(1, 6):
            img_url = url.format(svid, x, y)
            #print img_url
            data = urllib2.urlopen(img_url, timeout=120).read()
            mat = cv2.imdecode(np.asarray(bytearray(data), dtype=np.uint8), 1)
            try:
                if len(data) < 1000:
                    print 'ERROR DATA_LEN'
                    continue
                else:
                    img_split.append(mat)
            except Exception, e:
                print "ERROR JSON URL"
                continue
    key, concated_img = concat_img(img_split, 5, 8)
    if key:

        # file_name = "{0}.jpg".format(svid)
        file_name = "{0}.jpg".format(name_base)
        #file_name = name +".jpg"
        #file_name = "{0}_{1}_{2}_{3}.jpg".format(num, cate, long, lati )
        cv2.imwrite(os.path.join(out_dir,file_name), concated_img)
        print file_name


# 下载腾讯街景图片
#   参数:
#       LL：经纬度
#       output_dir: 存储下载图片的路径
def main(LL,output_dir,name_base,angle):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    MER = LL2MER(LL[0], LL[1])
    new_MER = update_MER(MER,angle)
    #svid = get_svid(MER)
    svid = get_svid(new_MER)
    #name_base = str(num) + "_" + str(cate) + "_" + str(long) + "_" + str(lati)
    grab_img(svid, output_dir,name_base)

if __name__ == "__main__":
    fp = open("img_1.txt", "r")
    #LL = [116.721321,39.860142]
    for line in fp.readlines():
        line = line.strip('\r\n')
        zu = line.split(' ')
        #LL = [116.721321,39.860142]
        LL = [zu[-2],zu[-1]]
        num = zu[0]
        cate = zu[2]
        angle = float(zu[3])
        long = zu[-2]
        lati = zu[-1]
        name_base = str(num) + "_" + str(cate) + "_" + str(long) + "_" + str(lati)
        output_dir = 'output_image'
        main(LL,output_dir,name_base,angle)
    #output_dir = 'output_image'
    #main(LL,output_dir)


# def func(LL,output_dir,name_base):
#     if not os.path.exists(output_dir):
#         os.mkdir(output_dir)
#     MER = LL2MER(LL[0], LL[1])
#     svid = get_svid(MER)
#     #name_base = str(num) + "_" + str(cate) + "_" + str(long) + "_" + str(lati)
#     grab_img(svid, output_dir,name_base)

# def main(file_name):
#     fp = open(file_name, "r")
#     for line in fp.readlines():
#         zu = line.split(' ')
#         #LL = [116.721321,39.860142]
#         LL = [zu[-2],zu[-1]]
#         num = zu[0]
#         cate = zu[2]
#         long = zu[-2]
#         lati = zu[-1]
#         name_base = str(num) + "_" + str(cate) + "_" + str(long) + "_" + str(lati)
#         output_dir = 'output_image'
#         func(LL,output_dir,name_base)