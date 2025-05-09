def get_pix(x, y):
    # LEFT, TOP
    return x * 85, y * 85 + 80

def get_xy(x, y):
    return int(x / 85), int(y / 85) - 1