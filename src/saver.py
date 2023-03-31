import helpers as h
import pixel_map as pm
import tools as tl
from PIL import Image
import pygame as pg

# TODO: come up with a better name
class Saver:
    def __init__(self, file_name : str='image_out', extension : str='.png',location : str='../pixel/saved_images/'):
        self.file_name = file_name
        self.extension = extension
        self.location = location
        
    def set_filename(self, name : str):
        self.file_name = name
        
    def set_extension(self, extension : str):
        self.extension = extension
        
    def set_location(self, location : str):
        self.location = location
        
    def save_as_png(self, pixel_map):
        print("SAVING IMAGE...")
        
        # Create image
        image_out = Image.new(mode='RGBA',size=pixel_map.pixel_dimensions)
        
        # Get the pixels from the pixelmap in the right format
        pixels = pixel_map.get_png_pixels()
        
        # Put the pixels onto the image
        image_out.putdata(pixels)
        
        print("- SAVE AS:",self.file_name + self.extension)
        print("- AT LOCATION:", self.location)
        
        # Save the image as
        image_out.save(self.location + self.file_name + self.extension)
        
        print("IMAGE SAVED!")
        
    