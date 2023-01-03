




def get_pixel(socket, x, y):
    socket.sendall(str.encode(f"PX {x} {y}\n"))
    res = socket.recv(1024).decode('utf-8').split(" ")
    return (res[3])

def get_pixels(socket, X, Y):
    pass

def set_pixel(socket, x, y, c):
    return f"PX {x} {y} {c}\n"


def set_pixels(socket, X, Y, C):
    pass

def get_size(socket):
    socket.sendall(str.encode("SIZE"))
    size = socket.recv(1024).decode('utf-8')
    size = size.split(" ")
    return (int(size[1]), int(size[2]))