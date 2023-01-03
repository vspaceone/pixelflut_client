from .helper import get_pixel_packet, recv_until, set_pixel_packet

def get_pixel(socket, x, y):
    socket.sendall(get_pixel_packet(x, y))
    res = recv_until(socket,b'\n').decode('utf-8').split(" ")
    return (res[3])

def set_pixel(socket, x, y, c):
    socket.sendall(set_pixel_packet(x,y,c))

def get_size(socket):
    socket.sendall(b"SIZE\n")
    size = recv_until(socket,b'\n').decode('utf-8').split(" ")
    return (int(size[1]), int(size[2]))