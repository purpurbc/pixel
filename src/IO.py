import helpers as h
import pixel_map as pm
import tools as tl
from PIL import Image
import pygame as pg
import render as rd

class IO_handler:
    def __init__(self):
        self.event = None
        self.left_mouse_btn_pressed = False
        self.saver = None
    
    def set_event(self,event):
        self.event = event

    # TODO: remove all parameters except Interface
    def handle_event(self, 
                     Interface, 
                     button_s,
                     button_c, 
                     btn_container, 
                     slider_container, 
                     user_input):
        

        # Handle events/input from the user
        for event in pg.event.get():
            self.set_event(event)

             # If the event is a quit event. Close program
            if event.type == pg.QUIT: 
                Interface.running = False
                
            """if event.type == lo.CHANGE_PEN_COLOR:
                pass"""

            # If the left mouse button is pressed
            if (event.type == pg.MOUSEBUTTONDOWN and event.button == 1) or self.left_mouse_btn_pressed:
                
                self.left_mouse_btn_pressed = True
                
                # Fill the pixel, if one is pressed
                Interface.toolbox.get_active_tool().fill_pixels(Interface.pixel_map, Interface.mouse_pos)

                # Handle button presses if there are any
                btn_container.buttons_pressed(Interface.mouse_pos, self.left_mouse_btn_pressed) 
                
                button_c.on_pressed(Interface.mouse_pos, self.left_mouse_btn_pressed)
                
                button_s.on_pressed(Interface.mouse_pos, self.left_mouse_btn_pressed)

                for slider in slider_container.sliders:
                    #prev_btn_state = slider.button.was_pressed['state']
                    if slider.button.on_pressed(Interface.mouse_pos, self.left_mouse_btn_pressed) or slider.button.was_pressed['state']:
                        """if not prev_btn_state and slider.button.was_pressed['state']:
                            slider.button.set_action_arguments({'prev_mouse_pos' : Interface.mouse_pos})"""
                        slider.button.set_action_arguments({'cur_mouse_pos' : Interface.mouse_pos})
                        pass

                # FIXME: 
                active_window = Interface.get_active_internal_window()
                if active_window:
                    active_window_pressed = Interface.on_active_window_pressed(Interface.mouse_pos, self.left_mouse_btn_pressed)
                    if active_window_pressed and active_window.name == 'save_as_filename':
                        user_input = ''
            
            # If the left mouse button is released
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                
                self.left_mouse_btn_pressed = False
                
                # Handle button clicks if there are any
                btn_container.buttons_clicked(Interface.mouse_pos, self.left_mouse_btn_pressed)
                
                # TODO: fix this
                if button_c.on_clicked(Interface.mouse_pos, self.left_mouse_btn_pressed):
                    pass
                
                if button_s.on_clicked(Interface.mouse_pos, self.left_mouse_btn_pressed):
                    user_input = Interface.saver.file_name
                    pass
                
                for slider in slider_container.sliders:
                    if slider.button.on_clicked(Interface.mouse_pos, self.left_mouse_btn_pressed):
                        pass
                    elif slider.button.was_pressed['state']:
                        slider.button.set_pressed(False,Interface.mouse_pos)

            # If a key is pressed
            if event.type == pg.KEYDOWN:
                
                # FIXME:
                for internal_window_name, internal_window in Interface.internal_windows.items():
                    if internal_window.active and event.key != pg.K_BACKSPACE and event.key != pg.K_RETURN:
                        user_input += event.unicode
                    elif internal_window.active and event.key == pg.K_BACKSPACE:
                        user_input = user_input[:-1]

                # If the pressed key is DELETE
                if event.key == pg.K_DELETE:
                    # Clear the pixel_map
                    rd.clear_pixelmap(Interface.pixel_map)
                
                # If the pressed key is B
                if event.key == pg.K_b:
                    # Clear the pixel_map
                    if Interface.toolbox.active_tool == 'pen':
                        Interface.toolbox.set_active_tool('pen_plus')
                    else:
                        Interface.toolbox.set_active_tool('pen')
                    
                # If the pressed key is S
                if event.key == pg.K_s: 
                    # Save image as png
                    #Interface.saver.save_as_png(Interface.pixel_map)
                    pass

                # If the pressed key is ENTER
                if event.key == pg.K_RETURN and Interface.internal_windows['save_as_filename'].active: 
                    Interface.saver.set_filename(user_input)
                    Interface.saver.save_as_png(Interface.pixel_map)
                    Interface.set_active_internal_window('save_as_filename',False)
                    user_input = ''

        return user_input
        