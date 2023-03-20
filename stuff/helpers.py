import pygame as pg
from stuff import pixel_map as pm

# dimensions
s_W =800
s_H =600
s_dimension = (s_W,s_H)

# colors
white = (255,255,255)
light_grey = (220,220,220)
grey =(100,100,100)
grey_2 = (84,84,84)
medium_grey =(75,75,75)
dark_grey =(40,40,40)
black = (15,15,15)
blue = (51,169,205)
red = (220,20,20)
light_red = (220,100,100)

"""# optional text
font = pg.font.Font("freesansbold.ttf", 32) 
infotext = font.render("TEXT", True, black)
infotext_rect = infotext.get_rect()  
infotext_rect.center = (s_W // 2 , 100)"""

clock = pg.time.Clock()
fps = 60. # not really h.fps

# load background image
bg = pg.image.load("pics/bg_markers.png")
cursor_image = pg.image.load("pics/cursor_pixel_v1.png")




