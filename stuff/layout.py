import pygame as pg
from stuff import helpers as h
from stuff import interface as interf_


# TODO: Move these functions to a proper class/file
def close_window(self):
    print("CLOSING WINDOW...")
    pg.event.post(pg.event.Event(pg.QUIT))
    
def change_pen_color(self):
    interf_.interface.tool_box.get_active_tool().color = self.color
      

class Button:
    """
    Create/Use a button:
    1. def action_name(): .... # Create a function
    2. button = Button(rect) # Create button instance
    3. button.action = MethodType(action_name, button) # Attach function to button
    4. button.action() # Perform action/function
    """
    def __init__(self, rect : pg.Rect, color=h.red, hovered_color=h.light_red, pressed_color=h.white):
        self.rect = rect
        self.color = color
        self.hovered_color = hovered_color
        self.pressed_color = pressed_color
        self.image = None
        self.action = None
        self.image_element = None
        self.was_pressed = False
        
    def set_pressed(self, state : bool):
        self.was_pressed = state

    # IS methods, either True or False
    def is_hovered(self, mouse_pos, left_mouse_btn_pressed):
        return True if self.rect.collidepoint(mouse_pos) and not left_mouse_btn_pressed else False
    
    def is_pressed(self,mouse_pos, left_mouse_btn_pressed):
        return True if self.rect.collidepoint(mouse_pos) and left_mouse_btn_pressed else False
    
    def is_released(self, mouse_pos, left_mouse_btn_pressed):
        return True if not self.was_pressed and self.is_hovered(mouse_pos,left_mouse_btn_pressed) and not left_mouse_btn_pressed else False
    
    def is_clicked(self,mouse_pos, left_mouse_btn_pressed):
        return True if self.was_pressed and self.is_hovered(mouse_pos, left_mouse_btn_pressed) else False
    
    # ON methods, what actually occurs
    def on_hovered(self,mouse_pos, left_mouse_btn_pressed):
        """Hover: mouse_pos is on the buttons rect and the left_mouse_button is NOT pressed"""
        if self.is_hovered(mouse_pos, left_mouse_btn_pressed):
            # Do nothing (essentially a useless method)
            return True
        return False
    
    def on_pressed(self,mouse_pos, left_mouse_btn_pressed):
        """Press: mouse_pos is on the buttons rect and the left_mouse_button IS pressed"""
        if self.is_pressed(mouse_pos, left_mouse_btn_pressed):
            # Set was_pressed to True
            self.set_pressed(True)
            return True
        return False

    def on_released(self,mouse_pos, left_mouse_btn_pressed):
        """Release: mouse_pos is on the buttons rect, the left_mouse_button is NOT pressed and
            the button was NOT pressed initially."""
        if self.is_released(mouse_pos, left_mouse_btn_pressed):
            # Do nothing (essentially a useless method)
            return True
        return False

    def on_clicked(self,mouse_pos, left_mouse_btn_pressed):
        """Click: mouse_pos is on the buttons rect, the left_mouse_button is NOT pressed and
            the button WAS pressed initially."""
        if self.is_clicked(mouse_pos, left_mouse_btn_pressed) and self.action:
            # Perform the action and set was_pressed to True
            self.action()
            self.set_pressed(False)
            return True
        return False 


class Container:
    def __init__(self, rect, objects : list = []):
        self.rect = rect
        self.objects = []
        for obj in objects:
            self.add_button(obj, [obj.rect.x, obj.rect.y])
        self.color = h.grey_2
        self.line_color = h.black
        self.line_width = 3
        
    def add_button(self, button : Button, local_coords):
        global_coords = h.get_global_coords(self.rect, local_coords)
        button.rect.x, button.rect.y = global_coords[0], global_coords[1]
        self.objects.append(button)
        
        
class TextArea:
    def __init__(self, rect):
        self.rect = rect

class InputArea:
    def __init__(self, rect):
        self.rect = rect
        
class InternalWindow:
    def __init__(self, rect : pg.Rect, name : str='new_window'):
        self.rect = rect
        self.color = h.dark_grey
        self.line_color = h.white
        self.line_width = 3
        self.name = name
        self.active = False
        
    def highlight_window(self):
        pass
    
    def set_active(self, active):
        self.active = active
        if active:
            self.line_color = h.light_red
        else:
            self.line_color = h.white


