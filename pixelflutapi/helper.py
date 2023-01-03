

def hex_to_floats(h):
    """
    Takes a hex rgb string (e.g. #ffffff) and returns an RGB tuple (float, float, float).
    """
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) # skip '#'

def get_pixel_packet(x, y):
    return str.encode(f"PX {x} {y}\n")

def get_pixels(socket, X, Y):
    pass

def set_pixel_packet(x, y, c):
    return str.encode(f"PX {x} {y} {c}\n")

def set_pixels(socket, X, Y, C):
    pass

def recv_until(socket, b):
    buf = b""
    while True:
        c = socket.recv(1)
        buf += c
        if c == b:
            break
    return buf