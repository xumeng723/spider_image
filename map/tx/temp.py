import spider_tx_map

import sys
import os
from multiprocessing import Pool
from multiprocessing import Manager
datadir = 'E:\\didi\\merge\\dir_txt'
#datadir = sys.argv[1]
process_num = 10

	
if len(sys.argv)==2:
	if not datadir[-1:]=='/':
		datadir=datadir+'/'

if len(sys.argv)==3:
	if not datadir[-1:]=='/':
		datadir=datadir+'/'
	process_num = int(sys.argv[2])

ps=Pool(process_num)
list_all = os.listdir(datadir)
for i,fileList in enumerate(list_all):
	if not fileList.split('_')[0] =='track':
		continue
	print fileList
	base_name = 'img_'
	img_list_name = base_name +str(i)+'.txt'

	ps.apply_async(spider_tx_map.main, args = (fileList,))
ps.close()
ps.join()

