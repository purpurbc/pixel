from stuff import helpers as h
from stuff import pixel_map as pm
from stuff import tools as tl
from stuff import saver as sv
import pygame as pg

# TODO: come up with a better name
class Interface:
    def __init__(self, pixel_map : pm.PixelMap=None, tool_box : tl.ToolBox=None, saver : sv.Saver=None):
        self.pixel_map = pixel_map
        self.tool_box = tool_box
        self.saver = saver
        
    def add_toolbox(self, tool_box : tl.ToolBox):
        self.tool_box = tool_box
        
    def add_pixelmap(self, pixel_map : pm.PixelMap):
        self.pixel_map = pixel_map
        
    def add_saver(self, saver : sv.Saver):
        self.saver = saver
    
interface = Interface()