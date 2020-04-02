# 去掉BiliBili番剧右上角的水印
import cv2
import numpy
import argparse
import re

# input, output image
parser = argparse.ArgumentParser(description='BiliBili番剧截图去水印')
parser.add_argument('-i', '--input', help='input image')
parser.add_argument('-o', '--output', help='output image')
parser.add_argument('-m', '--mask', help='mask image')
parser.add_argument('-s', '--scissor', help='自动修剪上下的黑边，输入尺寸必须为2880x1800。只适用于MacBook Pro 13寸全屏幕截屏！', action='store_true')
args = parser.parse_args()

if args.input is None or args.output is None or args.mask is None:
    parser.print_help()
    exit(0)

# 蒙版背景色（BGR）
# 获取文件名
mask_name = args.mask.rsplit('/', maxsplit=1).pop()
mask_name = mask_name.rsplit('\\', maxsplit=1).pop()
# search for 'r', 'g', 'b'
r = int(re.search(r'r([0-9]+)([^0-9]|$)', mask_name).group(1))
g = int(re.search(r'g([0-9]+)([^0-9]|$)', mask_name).group(1))
b = int(re.search(r'b([0-9]+)([^0-9]|$)', mask_name).group(1))
color0 = numpy.array([b, g, r])

src = cv2.imread(args.input)
if src is None:
    print("can't open input image")
    exit(-1)

mask = cv2.imread(args.mask)
if mask is None:
    print("can't open mask image")
    exit(-1)

if src.shape != mask.shape:
    print("the shape of input and mask must equal")
    exit(-1)

# 一些常数
zero = numpy.array([0, 0, 0])
white = numpy.array([255, 255, 255])
constant = numpy.log(white - color0)

out = numpy.maximum(zero, white-numpy.power(white-src, constant/numpy.log(white-mask)))

# 修剪上下黑边
if args.scissor and src.shape == (1800, 2880, 3):
    out = out[90:1710]

cv2.imwrite(args.output, out)
