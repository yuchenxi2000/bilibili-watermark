# 只能去黑白的水印
import cv2
import numpy as np
import sys
import os

cwd = os.path.dirname(__file__)
white_path = os.path.join(cwd, 'white.png')
black_path = os.path.join(cwd, 'black.png')

if len(sys.argv) < 3:
    print('not enough args')
    exit(1)

# 输入
in_file = sys.argv[1]
# 输出
out_file = sys.argv[2]

# 原理
#
# out = in * alpha + watermark * (1 - alpha)
#
# white = 255 * alpha + C
# black = 0 * alpha + C
#
# alpha = (white - black) / 255
# in = (out - black) / alpha
white = cv2.imread(white_path)
white = white.astype(np.float)
black = cv2.imread(black_path)
black = black.astype(np.float)

alpha = (white - black) / 255.0

img_out = cv2.imread(in_file)
img_out = img_out.astype(np.float)
img_in = (img_out - black) / (alpha + 1e-5)

img_in = np.maximum(img_in, 0.0)
img_in = np.minimum(img_in, 255.0)

cv2.imwrite(out_file, img_in)
