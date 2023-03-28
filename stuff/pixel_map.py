import collections
from stuff import helpers as h
from stuff import layout as lo
import pygame as pg

# TODO: find a place for this class
class Palette:
    def __init__(self, name : str, colors : dict): 
        self.name = name
        self.colors = colors # -> {'color_name' : RGBA-tuple, 'color_name_2' : RGBA-tuple ... }

class Pixel:
    def __init__(self, rect, color=None):
        self.rect = rect
        self.color = color
        self.previous_color = None

class PixelMap:
    def __init__(self, pixel_dims, structure : lo.Structure):
        pixel_size = [structure.rect.w/pixel_dims[1], structure.rect.h/pixel_dims[0]]
        self.pixels = [[Pixel(pg.Rect(structure.rect.x + i*pixel_size[0], structure.rect.y + j*pixel_size[1], pixel_size[0], pixel_size[1])) for i in range(pixel_dims[0])] for j in range(pixel_dims[1])]
        self.pixel_dimensions = pixel_dims
        self.structure = structure
        self.grid_line_color = h.medium_grey

    def get_pixel(self, pos : tuple) -> pg.Rect:
        """ Get the rect of the pixel from the pixel_map. The rect encapsulates the pos"""

        # Extract a pixel's rect
        pixel_rect = self.pixels[0][0].rect

        # Find the right column and row
        column = ((pos[0] - self.structure.rect.x)/pixel_rect.w)
        row = ((pos[1] - self.structure.rect.y)/pixel_rect.h)

        # Check so that the pixel is in the pixelmap
        if (column >= self.pixel_dimensions[1] or column < 0) or (row >= self.pixel_dimensions[0] or row < 0):
            return None
        
        # Return the pixel    
        return self.pixels[int(row)][int(column)]

    def get_pixel_size(self) -> list[2]:
        """Get the size of the pixels in the pixelmap"""

        # Extract a pixel's rect
        pixel_rect = self.pixels[0][0].rect
        
        # Return only the width and height in a list
        return [pixel_rect.w,pixel_rect.h]
    
    def get_png_pixels(self) -> list:
        pixels = []
        for pixel_row in self.pixels:
            for pixel in pixel_row:
                color = pixel.color
                if color == None:
                    color = (0,0,0,0)
                pixels.append(color)
        return pixels