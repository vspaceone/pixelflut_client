import sys
import cv2
import socket
import numpy as np
import tqdm

imagefile = sys.argv[1]
server = sys.argv[2]
port = int(sys.argv[3])

def getpx(socket, x, y):
    socket.sendall(str.encode(f"PX {x} {y}\n"))
    res = socket.recv(1024).decode('utf-8').split(" ")
    return (res[3])

def px(socket, x, y, c):
    return f"PX {x} {y} {c}\n"

def size(socket):
    socket.sendall(str.encode("SIZE"))
    size = socket.recv(1024).decode('utf-8')
    size = size.split(" ")
    return (int(size[1]), int(size[2]))

def hextofloats(h):
    '''Takes a hex rgb string (e.g. #ffffff) and returns an RGB tuple (float, float, float).'''
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) # skip '#'

s = socket.create_connection((server,port))
(W,H) = size(s)
print("W:", W)
print("H: ", H)

image = np.zeros((H,W,3), np.uint8)
for x in range(0,H,4):
    print(x)
    for y in tqdm.tqdm(range(1200,W,4)):
        image[x,y] = hextofloats(f"#{getpx(s,y,x)}")

cv2.imwrite(imagefile, image)