# 用Python去番剧水印

如题，一些良心番看番送壁纸，但右上角有水印。于是弹幕里充斥着“万恶的水印”“有水印”等等。

我原来用 Ps 去水印，后来发现太低效，于是想找出水印算法，用逆变换还原打水印前的图片。

# 原理

基本思想是摸清加水印的算法，然后逆向求出原图。

经过一晚上的研究，发现以下公式：

ln(255 - s) = c ln(255 - w)

上式中 s 为原图像素，w 为加了水印的像素。c 为常数，对于水印中间的像素取 1.08856，对于没有水印的地方就是 1。可见加水印算法是类似 gamma 变换的算法。

接下来的任务就是对于图片的不同位置的像素，求出对应的常数 c，然后代以上公式。我找 了一张背景几乎纯色的截图作为蒙版。经过 Ps 处理后可以得到一张背景纯色的带水印字样的图片（下图）。

![image](https://github.com/yuchenxi2000/bilibili-watermark/blob/master/mask.png)

利用这张图就可算出 c 值。因为原图已知（去除右上角的图就是原图），带入公式求 c，再根据 c 求要去水印图片的原图即可。

# 源码（Python）

``` python
# 请先安装库：opencv，numpy
import cv2
import numpy

color0 = numpy.array([70, 51, 39])  # 蒙版背景色（BGR）
src = cv2.imread('in.png')  # 需要去水印的图片
mask = cv2.imread('mask.png')  # 制作好的蒙版图片

# 一些常数

zero = numpy.array([0, 0, 0])
white = numpy.array([255, 255, 255])
constant = numpy.log(white - color0)

# 应用公式
out = numpy.maximum(zero, white-numpy.power(white-src, constant/numpy.log(white-mask)))
cv2.imwrite('out.png', out)  # 输出图片
```

# 效果图

![image](https://github.com/yuchenxi2000/bilibili-watermark/blob/master/example-small.png)

去水印前

![image](https://github.com/yuchenxi2000/bilibili-watermark/blob/master/example-out-small.png)

去水印后

# 一些注释

源码中的 color0 是蒙版图的背景色，注意要从 RGB 转成 BGR。

蒙版的图片大小、字样位置请自行调整。

制作蒙版图的时候尽量保留字样周围的像素，不要做处理。对字样周围像素做 Ps 处理会使公式中 c 值发生变化，导致处理出来的图有白边。

# 局限性

对于浅色的图，效果非常不错，但对于深色的图效果不佳。因为深色图 RGB 值过小，最终结果会有色差。转换成 HSV 色彩空间可能可以解决，但我没试过。

# Disclaim

对于去水印造成的版权问题，本人概不负责。本人也不保证该算法完全不出问题。



yuchenxi0_0

2019.10.22