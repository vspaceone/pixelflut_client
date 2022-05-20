import sys
import cv2
import socket

imagefile = sys.argv[1]
server = sys.argv[2]
port = int(sys.argv[3])
positionX = int(sys.argv[4])
positionY = int(sys.argv[5])

print("Server: ", server)
print("Port:   ", port)

print(f"Loading image {imagefile}...")
image = cv2.imread(imagefile, cv2.IMREAD_UNCHANGED)
print("Loaded")

def px(socket, x, y, c):
    return f"PX {x} {y} {c}\n"

def size(socket):
    socket.sendall(str.encode("SIZE"))
    size = socket.recv(1024).decode('utf-8')
    print(size)
print(image.shape)
W,H,C = image.shape

s = socket.create_connection((server,port))
packet = ""
for x in range(0,W):
    for y in range(0,H):
        r = image[x,y,0]
        g = image[x,y,1]
        b = image[x,y,2]
        a = image[x,y,3]
        if a != 0:
            packet += px(s,y,x, '%02x%02x%02x' % (r, g, b))
print("Packet:")
print(packet)

while True:
    s.sendall(str.encode(packet))