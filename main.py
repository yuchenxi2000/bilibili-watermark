# 去掉BiliBili番剧右上角的水印
import cv2
import numpy

# 蒙版背景色（BGR）
color0 = numpy.array([70, 51, 39])

src = cv2.imread('example.png')
mask = cv2.imread('mask.png')

# 一些常数
zero = numpy.array([0, 0, 0])
white = numpy.array([255, 255, 255])
constant = numpy.log(white - color0)

out = numpy.maximum(zero, white-numpy.power(white-src, constant/numpy.log(white-mask)))
cv2.imwrite('example-out.png', out)
