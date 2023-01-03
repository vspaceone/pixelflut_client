

def hex_to_floats(h):
    """
    Takes a hex rgb string (e.g. #ffffff) and returns an RGB tuple (float, float, float).
    """
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) # skip '#'