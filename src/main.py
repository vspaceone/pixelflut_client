import sys
import cv2
import socket
import tqdm

imagefile = sys.argv[1]
server = sys.argv[2]
port = int(sys.argv[3])


print("Server: ", server)
print("Port:   ", port)

image = cv2.imread(imagefile, cv2.IMREAD_UNCHANGED)
print("Loaded")

print(image.shape)
W,H,C = image.shape

s = socket.create_connection((server,port))

print(f"Loading image {imagefile}...")
packet = ""
for x in tqdm.tqdm(range(0,W)):
    for y in range(0,H):
        r,g,b,a = image[x,y,0],image[x,y,1],image[x,y,2],image[x,y,3]
        if a != 0:
            packet += px(s,y,x, '%02x%02x%02x' % (r, g, b))
print("Packet:")
print(packet)

print("Sending to server... (endless)")
print("Strg-C to cancel")
while True:
    s.sendall(str.encode(packet))