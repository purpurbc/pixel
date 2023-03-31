import pygame as pg
import helpers as h
import pixel_map as pm

class Pen:
    def __init__(self, design = [[1]], design_center = [0,0], color = h.black):
        self.design = design
        self.design_center = design_center
        self.color = color
        
    def set_color(self, color):
        self.color = color
    
    def fill_pixels(self, pixel_map : pm.PixelMap, center_pos):
        pixel_size = pixel_map.get_pixel_size()
        for row in range(len(self.design)):
            for column in range(len(self.design[0])):
                if self.design[row][column] == 1:
                    x_pos = center_pos[0] + (column - self.design_center[1]) * pixel_size[0]
                    y_pos = center_pos[1] + (row - self.design_center[0]) * pixel_size[1]
                    self.fill_pixel(pixel_map, [x_pos, y_pos])
        
    def fill_pixel(self, pixel_map : pm.PixelMap, pos):
        pressed_pixel = pixel_map.get_pixel(pos)
        if pressed_pixel:
            pressed_pixel.previous_color = pressed_pixel.color
            pressed_pixel.color = self.color
            
class ToolBox:
    def __init__(self, tools : dict={}, active_tool=None):
        self.tools = tools
        self.active_tool = active_tool
       
    def add_tool(self, tool_name : str, tool):
        self.tools[tool_name] = tool
         
    def set_active_tool(self, tool_name):
        self.active_tool = tool_name
        
    def get_active_tool(self):
        return self.tools[self.active_tool]
    
