import pygame as pg
import helpers as h


# TODO: Move these functions to a proper class/file
def close_window(self):
    print("CLOSING WINDOW...")
    pg.event.post(pg.event.Event(pg.QUIT))
    
def change_pen_color(self, tool_box, color):
    tool_box.get_active_tool().color = color
    
def save_as(self, saver, pixel_map, internal_window):
    pass





class Structure:
    def __init__(self, rect, color = h.grey_2, line_color = h.black, line_width = 3):
        self.rect = rect
        self.color = color
        self.line_color = line_color
        self.line_width = line_width

class Button:
    """
    Create/Use a button:
    1. def action_name(): .... # Create a function
    2. button = Button(rect) # Create button instance
    3. button.action = MethodType(action_name, button) # Attach function to button
    4. button.action() # Perform action/function
    """
    def __init__(self,structure : Structure, hovered_color=h.light_red, pressed_color=h.WHITE):
        self.structure = structure
        self.action = None
        self.action_arguments = dict()
        self.action_mode = 'clicked'
        self.was_pressed = {'state':False,'pos':(-1,-1)}
        self.hovered_color = hovered_color
        self.pressed_color = pressed_color
        
        self.image = None           # TODO: implement
        self.image_element = None   # TODO: implement
        
    def set_action_arguments(self,action_arguments : dict):
        for key, value in action_arguments.items():
            self.action_arguments[key] = value
        
    def set_pressed(self, state : bool, mouse_pos):
        self.was_pressed['state'] = state
        self.was_pressed['pos'] = mouse_pos

    # IS methods, either True or False
    def is_hovered(self, mouse_pos, left_mouse_btn_pressed):
        return True if self.structure.rect.collidepoint(mouse_pos) and not left_mouse_btn_pressed else False
    
    def is_pressed(self,mouse_pos, left_mouse_btn_pressed):
        return True if self.structure.rect.collidepoint(mouse_pos) and left_mouse_btn_pressed else False
    
    def is_released(self, mouse_pos, left_mouse_btn_pressed):
        return True if not self.was_pressed['state'] and self.is_hovered(mouse_pos,left_mouse_btn_pressed) and not left_mouse_btn_pressed else False
    
    def is_clicked(self,mouse_pos, left_mouse_btn_pressed):
        return True if self.was_pressed['state'] and self.is_hovered(mouse_pos, left_mouse_btn_pressed) else False
    
    # ON methods, what actually occurs
    def on_hovered(self,mouse_pos, left_mouse_btn_pressed):
        """Hover: mouse_pos is on the buttons rect and the left_mouse_button is NOT pressed"""
        if self.is_hovered(mouse_pos, left_mouse_btn_pressed):
            # Do nothing (essentially a useless method)
            return True
        return False
    
    def on_pressed(self,mouse_pos, left_mouse_btn_pressed):
        """Press: mouse_pos is on the buttons rect and the left_mouse_button IS pressed"""
        if self.is_pressed(mouse_pos, left_mouse_btn_pressed) or (self.was_pressed['state'] and self.action_mode == 'was_pressed'):
            # Set was_pressed to True
            if not self.was_pressed['state']:
                self.set_pressed(True,mouse_pos)
            if self.action and (self.action_mode == 'was_pressed' or self.action_mode == 'pressed'):
                self.action(**self.action_arguments)
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
        if self.is_clicked(mouse_pos, left_mouse_btn_pressed):
            # Perform the action and set was_pressed to True
            if self.action and self.action_mode == 'clicked':
                self.action(**self.action_arguments)
            self.set_pressed(False,mouse_pos)
            return True
        return False 


class Slider:
    def __init__(self, structure : Structure, value_range = [0,10], increment = 1.0):
        self.structure = structure
        self.button = None
        self.add_slider_button()
        self.value_range = value_range
        self.increment = increment
        self.value = value_range[0]
        
    def add_slider_button(self):
        btn_coords = h.get_global_coords(self.structure.rect,[0,0])
        btn_structure = Structure(pg.Rect(btn_coords[0],btn_coords[1],10,10))
        btn_structure.color = h.red
        btn = Button(btn_structure)
        #button1.action = MethodType(lo.change_pen_color,button1)
        #button1.add_action_arguments({'tool_box' : Interface.tool_box, 'color': h.WHITE})
        self.button = btn
    
    # TODO: refactor   
    def move_slider(self,cur_mouse_pos,prev_mouse_pos):
        cur_slider_btn_pos = self.button.structure.rect[0]
        move_by = cur_mouse_pos[0] - cur_slider_btn_pos# - prev_mouse_pos[0]
        new_x_pos = cur_slider_btn_pos + move_by
        width = self.structure.rect.w - self.button.structure.rect.w
        global_range = [self.structure.rect.x, self.structure.rect.x + width]
        self.button.structure.rect[0] = min(max(new_x_pos,global_range[0]),global_range[1])
      
    # TODO: refactor  
    def get_value(self):
        global_btn_pos = [self.button.structure.rect.x, self.button.structure.rect.y]
        local_btn_pos = h.get_local_coords(self.structure.rect,global_btn_pos)
        width = self.structure.rect.w - self.button.structure.rect.w
        rel = (self.value_range[1] - self.value_range[0]) / width
        val = ((rel*local_btn_pos[0])/self.increment + self.value_range[0])
        if val != self.value:
            self.value = val
            return self.value
        return val
        


class Container:
    def __init__(self, structure : Structure, containers : list = [], buttons : list = [], sliders : list = []):
        self.structure = structure
 
        self.containers = []
        for ctn in containers:
            self.add_container(ctn, [ctn.structure.rect.x, ctn.structure.rect.y])
            
        self.buttons = []
        for btn in buttons:
            self.add_button(btn, [btn.structure.rect.x, btn.structure.rect.y])
            
        self.sliders = []
        for slr in sliders:
            self.add_slider(slr, [slr.structure.rect.x, slr.structure.rect.y])
        
        
    def add_container(self, container, local_coords):
        global_coords = h.get_global_coords(self.structure.rect, local_coords)
        container.structure.rect.x, container.structure.rect.y = global_coords[0], global_coords[1]
        self.containers.append(container)
        
    def add_button(self, button : Button, local_coords):
        global_coords = h.get_global_coords(self.structure.rect, local_coords)
        button.structure.rect.x, button.structure.rect.y = global_coords[0], global_coords[1]
        self.buttons.append(button)
        
    def add_slider(self, slider : Slider, local_coords):
        global_coords = h.get_global_coords(self.structure.rect, local_coords)
        slider.structure.rect.x, slider.structure.rect.y = global_coords[0], global_coords[1]
        self.sliders.append(slider)

    def buttons_pressed(self, mouse_pos, left_mouse_btn_pressed):
        for btn in self.buttons:
            if btn.on_pressed(mouse_pos, left_mouse_btn_pressed):
                pass

    def buttons_clicked(self, mouse_pos, left_mouse_btn_pressed):
        for btn in self.buttons:
            if btn.on_clicked(mouse_pos, left_mouse_btn_pressed):
                pass
            
    def buttons_hovered(self, mouse_pos, left_mouse_btn_pressed):
        for btn in self.buttons:
            if btn.on_hovered(mouse_pos, left_mouse_btn_pressed):
                pass
        
class TextArea:
    def __init__(self, rect):
        self.rect = rect

class InputArea:
    def __init__(self, rect):
        self.rect = rect
        
class InternalWindow:
    def __init__(self, window_structure : Structure, name : str='DEFAULT_NAME'):
        self.window_structure = window_structure
        self.name = name
        self.active = False
        self.containers = []
        
    def highlight_window(self):
        pass

    def add_container(self,container):
        self.containers.append(container)
    
    def set_active(self, active):
        self.active = active
        if active:
            self.window_structure.line_color = h.dark_grey
        else:
            self.window_structure.line_color = h.WHITE
        
