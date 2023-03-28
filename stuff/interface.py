from stuff import helpers as h
from stuff import pixel_map as pm
from stuff import tools as tl
from stuff import saver as sv
from stuff import layout as lo
import pygame as pg

# TODO: come up with a better name
class Interface:
    def __init__(self, pixel_map : pm.PixelMap=None, tool_box : tl.ToolBox=None, saver : sv.Saver=None):
        self.pixel_map = pixel_map
        self.tool_box = tool_box
        self.saver = saver
        self.internal_windows = dict()
        self.mouse_pos = [-1,-1]
      
    def add_toolbox(self, tool_box : tl.ToolBox):
        self.tool_box = tool_box
        
    def add_pixelmap(self, pixel_map : pm.PixelMap):
        self.pixel_map = pixel_map
        
    def add_saver(self, saver : sv.Saver):
        self.saver = saver
    
    def set_mouse_pos(self,mouse_pos):
        self.mouse_pos = mouse_pos
        
    def add_internal_window(self, internal_window):
        self.internal_windows[internal_window.name] =  internal_window

    def set_active_internal_window(self, window_name : str, active : bool):
        self.internal_windows[window_name].set_active(active)
        if active == True:
            for name, win in self.internal_windows.items():
                if window_name != name:
                    win.set_active(False)

    def get_active_internal_window(self):
        for name, win in self.internal_windows.items():
            if win.active:
                return win
        
    def delete_internal_window(self, internal_window):
        del self.internal_windows[internal_window.name]

    def on_active_window_pressed(self, mouse_pos, left_mouse_btn_pressed):
        active_window = self.get_active_internal_window()
        if active_window:
            active_window_pressed = active_window.window_structure.rect.collidepoint(mouse_pos) and left_mouse_btn_pressed

            if active_window_pressed:
                self.set_active_internal_window(active_window.name,True)
                return True
            elif not active_window_pressed: 
                self.set_active_internal_window(active_window.name,False)
                return False
            

        