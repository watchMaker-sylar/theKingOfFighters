from PIL import Image
import os
import random

file_name = input("请输入文件名:")
dir_name = file_name[:-4]
gif_path = os.path.join(os.path.dirname(__file__), file_name)
os.mkdir(dir_name)
img = Image.open(gif_path)
while True:
    curr = img.tell()
    name = os.path.join(dir_name, '第%s帧.png' % str(curr + 1))
    img.save(name)
    img.seek(curr + 1)
