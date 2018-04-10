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
#火星坐标系转化为百度坐标系
#def gcj02tobd09(lng, lat):
    # """
    # 火星坐标系(GCJ-02)转百度坐标系(BD-09)
    # 谷歌、高德——>百度
    # :param lng:火星坐标经度
    # :param lat:火星坐标纬度
    # :return:
    # """

# 百度经纬度坐标转化为百度墨卡托坐标
def LL2MER(lon, lat):
    # EARTH_RADIS = 6378137
    # lon = float(lon)
    # lat = float(lat)
    # mercator_x = lon * (EARTH_RADIS * math.pi / 180.0)
    # mercator_y = math.log(math.tan((90.0 + lat) * math.pi / 360.0)) * EARTH_RADIS
    # return mercator_x, mercator_y
    x_pi = 3.14159265358979324 * 3000.0 / 180.0
    z = math.sqrt(lon * lon + lat * lat) + 0.00002 * math.sin(lat * x_pi)
    theta = math.atan2(lat, lon) + 0.000003 * math.cos(lon * x_pi)
    bd_lon = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    #return bd_lng, bd_lat
    LLBAND = [75, 60, 45, 30, 15, 0];
    LL2MC = [[-0.0015702102444, 111320.7020616939, 1704480524535203, -10338987376042340, 26112667856603880,
              -35149669176653700, 26595700718403920, -10725012454188240, 1800819912950474, 82.5],
             [0.0008277824516172526, 111320.7020463578, 647795574.6671607, -4082003173.641316, 10774905663.51142,
              -15171875531.51559, 12053065338.62167, -5124939663.577472, 913311935.9512032, 67.5],
             [0.00337398766765, 111320.7020202162, 4481351.045890365, -23393751.19931662, 79682215.47186455,
              -115964993.2797253, 97236711.15602145, -43661946.33752821, 8477230.501135234, 52.5],
             [0.00220636496208, 111320.7020209128, 51751.86112841131, 3796837.749470245, 992013.7397791013,
              -1221952.21711287, 1340652.697009075, -620943.6990984312, 144416.9293806241, 37.5],
             [-0.0003441963504368392, 111320.7020576856, 278.2353980772752, 2485758.690035394, 6070.750963243378,
              54821.18345352118, 9540.606633304236, -2710.55326746645, 1405.483844121726, 22.5],
             [-0.0003218135878613132, 111320.7020701615, 0.00369383431289, 823725.6402795718, 0.46104986909093,
              2351.343141331292, 1.58060784298199, 8.77738589078284, 0.37238884252424, 7.45]];
    cE = None
    for i in range(len(LLBAND)):
        if lat >= LLBAND[i]:
            cE = LL2MC[i]
            break
    if cE is None:
        return False, -1, -1
    #new_x, new_y = bdconverter(lon,lat, cE);
    #return new_x, new_y
    lon = float(bd_lon)
    lat = float(bd_lat)
    xTemp = float(cE[0]) + float(cE[1]) * math.fabs(bd_lon)
    cC = math.fabs(bd_lat) / cE[9]
    yTemp = cE[2] + cE[3] * cC + cE[4] * cC * cC + cE[5] * cC * cC * cC + cE[6] * cC * cC * cC * cC + cE[7] * cC * cC * cC * cC * cC + cE[8] * cC * cC * cC * cC * cC * cC
    xTemp = xTemp * -1 if lon < 0 else xTemp
    yTemp = yTemp * -1 if lat < 0 else yTemp
    return xTemp, yTemp
#def bdconverter(x, y, cE):


# 根据墨卡托坐标得到svid
def get_svid(MER):
    #url = 'http://sv.map.qq.com/xf?x={0}&y={1}&r=600&output=json'
    #url='http://pcsv0.map.bdimg.com/?udt=20171116&qt=qsdata&x={0}&y={1}&l=18.423999999999996&action=0&mode=day&t=1511506251379&fn=jsonp.p30397738'
    #url = 'http://pcsv0.map.bdimg.com/?udt=20171116&qt=qsdata&x={0}&y={1}&l=16.101312034168945&action=0&mode=day&t=1511512505511&fn=jsonp.p11622378'
    url = 'http://pcsv0.map.bdimg.com/?udt=20171116&qt=qsdata&x={0}&y={1}&l=13.311316563675629&action=0&mode=day&t=1511769145251&fn=jsonp.p40111812'
    json_url = url.format(MER[0],MER[1])
    try:
        res = urllib2.urlopen(json_url).read()
        a_res = json.loads(res.decode('gbk'))
        return a_res["detail"]["svid"]
    except Exception, e:
        raise Exception('ERROR JSON URL')

# 根据svid下载图片
def grab_img(svid, out_dir,name_base):
    #name = num+"_"+cate+"_"+long+"_"+lati
    #url = 'http://pcsv2.map.bdimg.com/?qt=pdata&sid=09002200011601190602171492K&pos=2_6&z=4&udt=20171116'
    #url = "http://sv1.map.qq.com/tile?svid={0}&x={1}&y={2}&from=web&level=1"
    url = "http://pcsv1.map.bdimg.com/?qt=pdata&sid={0}&pos={1}_{2}&z=4&udt=20171116"
    img_split = []
    for x in range(4, 13):
        for y in range(1, 6):
            img_url = url.format(svid, x, y)
            print img_url
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


#下载腾讯街景图片
#  参数:
#      LL：经纬度
#      output_dir: 存储下载图片的路径
def main(LL,output_dir,name_base):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    MER = LL2MER(LL[0], LL[1])
    svid = get_svid(MER)
    #name_base = str(num) + "_" + str(cate) + "_" + str(long) + "_" + str(lati)
    grab_img(svid, output_dir,name_base)

if __name__ == "__main__":
    fp = open("spider_bd_map.txt", "r")
    #LL = [116.721321,39.860142]
    for line in fp.readlines():
        zu = line.split(',')
        #LL = [116.721321,39.860142]
        #LL = [zu[-2],zu[-1]]
        LL = [zu[0],zu[1]]
        #num = zu[0]
        #cate = zu[2]
        long = zu[0]
        lati = zu[1]
        name_base = str(long) + "_" + str(lati)
        output_dir = 'output_image'
        main(LL,output_dir,name_base)
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