import os, os.path
import pandas as pd
import numpy as np
import datetime
import pytesseract
from PIL import Image
import threading
from progressbar import *
import sys
import time
import os

#os.getcwd() = ~/ipython

date_index = pd.date_range(start='20110130', end = '20170225',  freq= 'W-FRI')
#以爬取到的股票名单作为列名
name_list = os.listdir('./BaiduIndex/')
df = pd.DataFrame(index=date_index, columns=name_list)
diff_list = [0, 1, 3, 4, 5, 7, 8, 9, 10, 12, 13, 14, 16, 17, 18, 20, 21, 23, 24, 25, 27, 28, 29, 30, 32, 33, 34, 36, 37, 38, 40, 41, 42, 44, 45, 47, 48, 49, 50, 52, 53, 54, 56, 57, 58, 60, 61, 62, 64, 65, 66, 68, 69, 70, 71, 73, 74, 76, 77, 78, 80, 81, 82, 84, 85, 86, 88, 89, 90, 91, 93, 94, 95, 97, 98, 100, 101, 102, 104, 105, 106, 108, 109, 110, 111, 113, 114, 115, 117, 118, 119, 121, 122, 124, 125, 126, 127, 129, 130, 131, 133, 134, 135, 137, 138, 139, 141, 142, 143, 145, 146, 147, 149, 150, 151, 153, 154, 155, 157, 158, 159, 161, 162, 163, 165, 166, 167, 168, 170, 171, 172, 174, 175, 177, 178, 179, 181, 182, 183, 185, 186, 187, 188, 190, 191, 192, 194, 195, 196, 198, 199, 201, 202, 203, 205, 206, 207, 208, 210, 211, 212, 214, 215, 216, 218, 219, 220, 222, 223, 224, 226, 227, 228, 229, 231, 232, 234, 235, 236, 238, 239, 240, 242, 243, 244, 246, 247, 248, 249, 251, 252, 254, 255, 256, 258, 259, 260, 262, 263, 264, 266, 267, 268, 269, 271, 272, 273, 275, 276, 278, 279, 280, 282, 283, 284, 285, 287, 288, 289, 291, 292, 293, 295, 296, 297, 299, 300, 302, 303, 304, 305, 307, 308, 309, 311, 312, 313, 315, 316, 317, 319, 320, 321, 323, 324, 325, 327, 328, 329, 331, 332, 333, 335, 336, 337, 339, 340, 341, 343, 344, 345, 346, 348, 349, 350, 352, 353, 355, 356, 357, 359, 360, 361, 363, 364, 365, 366, 368, 369, 370, 372, 373, 374, 376, 377, 379, 380, 381, 382, 384, 385, 386, 388, 389, 390, 392, 393, 394, 396, 397, 398, 400, 401, 402, 404, 405, 406, 408, 409, 410, 412, 413, 414, 416, 417, 418, 420]
signal = 'start'
print '输出信息看“BaiduInde1.0.log”'
f = os.open('BaiduIndex1.0.log', os.O_CREAT|os.O_RDWR)
def iden():
    global signal
    count = 0
    for i in range(0, len(name_list)):
        start = datetime.datetime.now()
        name = name_list[i]
        os.write(f, '%d:开始识别 %s\n' % (count + 1, name))
        jpg_dir = os.path.join('/home/mr_zerow/ipython /BaiduIndex', '%s' % name)
        L = []
        date_num = 0 #日期计时器
        for n in diff_list:
            try:
                jpg_path = os.path.join(jpg_dir, '%d.jpg' % n)
                img = Image.open(jpg_path)
                code = pytesseract.image_to_string(img)
                (x, y) = img.size
                box = (0, 10, x, y)
                jpg = img.crop(box)
                (x, y) = jpg.size
                png = jpg.resize((2* x, 2* y), Image.ANTIALIAS)  #边缘模糊很重要

                code = pytesseract.image_to_string(png,lang='myindex', config='-psm 7' )
                if len(code) == 1  and x >= 10:
                    code = np.nan
                    date = datetime.datetime.strftime(date_index[date_num], '%Y-%m-%d')
                    os.write(f, '%s : %s \n图片空白，终极算法识别错误，填为空值\n' % (date, name))
            #日期计时器
                date_num += 1
                L.append(code)
            except:
                date = datetime.datetime.strftime(date_index[date_num], '%Y-%m-%d')
                os.write(f, '%s : %s \n错误发生，因为图片不存在，缺失值!\n'% (date, name))
                date_num += 1
                L.append(np.nan)
                continue
                    
        
        #空序列，加入不同时间数据
        count += 1 
        diff_data = []
        for i in range(0, 317):
            diff_data.append(L[i])
        df[name] = diff_data
        end = datetime.datetime.now()
        delta = end - start
        os.write(f, '%d:%s 已识别\n' % (count,name))
        os.write(f, '费时 %d秒\n' % delta.seconds)
    signal = 'end'
    os.fsync(f)
    return signal
        
def func():
    while signal != 'end':
        widgets = ['Progress: ', Percentage(), ' ', Bar(marker=RotatingMarker('>-=')),
           ' ', ETA(), ' ', FileTransferSpeed()]
        pbar = ProgressBar(widgets=widgets, maxval=900).start()
        for i in range(901):
          # do something
            if signal == 'end':
                break
            else:
                pbar.update(i)
                time.sleep(1)
        pbar.finish()
        os.fsync(f)
        
threads = []
t1 = threading.Thread(target=iden)
threads.append(t1)
t2 = threading.Thread(target=func)
threads.append(t2)

for t in threads:
    t.setDaemon(True)
    t.start()
