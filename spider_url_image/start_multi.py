import spider_from_url_multi
from multiprocessing import Pool
import multiprocessing
import os
#multiprocessing.freeze_support()
process_num = 10
ps = Pool(process_num)
# 1.txt 2.txt
if __name__ == '__main__':
    for i in xrange(10):
        #multiprocessing.freeze_support()
        ps.apply_async(spider_from_url_multi.main,args=('img_'+str(i+1)+'.txt',))
    ps.close()
    ps.join()

