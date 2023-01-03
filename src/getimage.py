import sys
import cv2
import socket
import numpy as np
import tqdm

from pixelflutapi.helper import hex_to_floats
from pixelflutapi.pixelflutapi import get_pixel, get_size

imagefile = sys.argv[1]
server = sys.argv[2]
port = int(sys.argv[3])


s = socket.create_connection((server,port))
(W,H) = get_size(s)
print("W:", W)
print("H: ", H)

image = np.zeros((H,W,3), np.uint8)

for x in tqdm.tqdm(range(0,H,4)):
    for y in range(0,W,4):
        image[x,y] = hex_to_floats(f"#{get_pixel(s,y,x)}")

cv2.imwrite(imagefile, image)