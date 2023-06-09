import pygame as pg

# TODO: Move the globals to interface?

# dimensions
s_W =800
s_H =600
s_dimension = (s_W,s_H)

# colors
WHITE = (255,255,255,255)
light_grey = (220,220,220,255)
grey =(100,100,100,255)
grey_2 = (84,84,84,255)
medium_grey =(75,75,75,255)
dark_grey =(40,40,40,255)
black = (25,25,25,255)
blue = (51,169,205,255)
light_blue = (81,199,235,255)
red = (220,20,20,255)
LIGHT_RED = (220,100,100,255)
yellow = (255,223,6,255)

clock = pg.time.Clock()
fps = 60. # not really fps

# load background image
cursor_image = pg.image.load("images/cursor_pixel_v1.png")

def get_global_coords(rect, local_coords):
    """Get the global coords from local coords inside of rect"""
    x = rect.x + local_coords[0]
    y = rect.y + local_coords[1]
    return [x,y]

def get_local_coords(rect, global_coords):
    """Get the local coords from global coords inside of rect"""
    x = global_coords[0] - rect.x
    y = global_coords[1] - rect.y
    return [x,y]

