#图片处理pillow模块的应用，
#参考3个网址：
http://www.w2bc.com/article/122079
http://python.jobbole.com/84956/
http://www.cnblogs.com/way_testlife/archive/2011/04/17/2019013.html

from PIL import Image
#打开图片
im = Image.open(path)

#图片截取imf
img.crop((x1, x2, x3, x4))
crop函数带的参数为(起始点的横坐标，起始点的纵坐标，宽度，高度）
