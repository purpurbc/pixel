import pygame as pg
from stuff import helpers as h
from stuff import pixel_map as pm
from stuff import render as rd
from stuff import layout as lo
from stuff import tools as tl
from stuff import saver as sv
from stuff import interface as interf_
from types import MethodType
import copy
from PIL import Image


def init():
    """Initialize everything that is needed"""

    # Initialize pygame
    pg.init()

    # Initialize info text for displaying active operator
    #h.font = pg.font.Font("freesansbold.ttf", 20) 
    #h.infotext = h.font.render("c: ERASE", True, h.black)
    #h.infotext_rect = h.infotext.get_rect()  
    #h.infotext_rect.center = (h.s_W // 2 , h.s_H - 30)

    # Set the visibility of the default cursor to false
    pg.mouse.set_visible(False)

    # Set the caption of the display
    pg.display.set_caption("pxls")
    
    # Create the pixelmap
    x = 10
    s = 500
    pixel_map = pm.PixelMap((int(s/x),int(s/x)), pg.Rect(250,50,s,s))
    
    pen = tl.Pen()
    tool_box = tl.ToolBox()
    tool_box.add_tool('pen',pen)
    tool_box.set_active_tool('pen')
    
    saver = sv.Saver()
    
    internal_window = lo.InternalWindow(pg.Rect(100,100,100,100))
    
    interf_.interface.add_pixelmap(pixel_map)
    interf_.interface.add_toolbox(tool_box)
    interf_.interface.add_saver(saver)
    interf_.interface.add_internal_window(internal_window)


def buttons_pressed(buttons : list, mouse_pos, left_mouse_btn_pressed):
    for btn in buttons:
        if btn.on_pressed(mouse_pos,left_mouse_btn_pressed):
            pass

def buttons_clicked(buttons : list, mouse_pos, left_mouse_btn_pressed):
    for btn in buttons:
        if btn.on_clicked(mouse_pos,left_mouse_btn_pressed):
            pass
        
def buttons_hovered(buttons : list, mouse_pos, left_mouse_btn_pressed):
    for btn in buttons:
        if btn.on_hovered(mouse_pos,left_mouse_btn_pressed):
            pass
        

def run_application():
    """The game loop"""

    # Create the game display
    game_display = pg.display.set_mode(h.s_dimension) 

    left_mouse_btn_pressed = False
    running = True

    h.cursor_image = pg.transform.scale(h.cursor_image, (20, 20))
    cursor_img_rect = h.cursor_image.get_rect()
    
    side = 20
    button1 = lo.Button(pg.Rect(4,4,side,side),h.white,h.white,h.white)
    button1.action = MethodType(lo.change_pen_color,button1)
    
    button2 = lo.Button(pg.Rect(8+side,4,side,side),h.black,h.black,h.white)
    button2.action = MethodType(lo.change_pen_color,button2)
    
    button3 = lo.Button(pg.Rect(12+2*side,4,side,side),h.blue,h.blue,h.white)
    button3.action = MethodType(lo.change_pen_color,button3)
    
    button4 = lo.Button(pg.Rect(16+3*side,4,side,side),h.red,h.red,h.white)
    button4.action = MethodType(lo.change_pen_color,button4)
    
    button_c = lo.Button(pg.Rect(h.s_W-side-20,5,side + 15,side),h.red,h.light_red,h.white)
    button_c.action = MethodType(lo.close_window,button_c)
    
    button_s = lo.Button(pg.Rect(h.s_W-side- 40 - side,5,side + 15,side),h.blue,h.light_blue,h.white)
    button_s.action = interf_.interface.saver.save_as_png
    
    buttons = [button1, button2, button3, button4]
    
    btn_container = lo.Container(pg.Rect(50,50,100,500),buttons)
    
    # FIXME:
    user_input = ''
    base_font = pg.font.Font(None, 20)
    input_rect = interf_.interface.internal_windows['new_window'].rect
    
    while running:
        
        # Continously update the mouse position
        mouse_pos = pg.mouse.get_pos()
    
        # Handle events/input from the user
        for event in pg.event.get(): 
            
            # If the event is a quit event. Close program
            if event.type == pg.QUIT: 
                running = False
                
            """if event.type == lo.CHANGE_PEN_COLOR:
                pass"""

            # If the left mouse button is pressed
            if (event.type == pg.MOUSEBUTTONDOWN and event.button == 1) or left_mouse_btn_pressed:
                
                left_mouse_btn_pressed = True
                
                # Fill the pixel, if one is pressed
                interf_.interface.tool_box.get_active_tool().fill_pixels(interf_.interface.pixel_map, mouse_pos)

                # Handle button presses if there are any
                buttons_pressed(buttons,mouse_pos,left_mouse_btn_pressed) 
                
                # TODO: fix this
                if button_c.on_pressed(mouse_pos,left_mouse_btn_pressed):
                    pass
                
                if button_s.on_pressed(mouse_pos,left_mouse_btn_pressed):
                    pass

                # FIXME:
                if interf_.interface.internal_windows['new_window'].rect.collidepoint(event.pos):
                    interf_.interface.internal_windows['new_window'].set_active(True)
                else: 
                    interf_.interface.internal_windows['new_window'].set_active(False)
            
            # If the left mouse button is released
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                
                left_mouse_btn_pressed = False
                
                # Handle button clicks if there are any
                buttons_clicked(buttons,mouse_pos,left_mouse_btn_pressed)
                
                # TODO: fix this
                if button_c.on_clicked(mouse_pos,left_mouse_btn_pressed):
                    pass
                
                if button_s.on_clicked(mouse_pos,left_mouse_btn_pressed):
                    pass

            # If a key is pressed
            if event.type == pg.KEYDOWN:
                
                # FIXME:
                for internal_window_name, internal_window in interf_.interface.internal_windows.items():
                    if internal_window.active and event.key != pg.K_BACKSPACE:
                        user_input += event.unicode
                    elif internal_window.active and event.key == pg.K_BACKSPACE:
                        user_input = user_input[:-1]

                # If the pressed key is C
                if event.key == pg.K_c:
                    # Clear the pixel_map
                    rd.clear_pixelmap(interf_.interface.pixel_map)
                    
                # If the pressed key is S
                if event.key == pg.K_s: 
                    # Save image as png
                    interf_.interface.saver.save_as_png()

                
        # Blit the pixelmap                
        rd.blit_pixelmap(game_display, interf_.interface.pixel_map)

        # Blit a cell around the hovered pixel to highlight it
        hovered_pixel = interf_.interface.pixel_map.get_pixel(mouse_pos)
        if hovered_pixel:
            rd.draw_cell(game_display, hovered_pixel.rect, interf_.interface.pixel_map.line_color, 2)
        
        # Draw the container
        rd.draw_container(game_display, btn_container)
        # Draw all the buttons
        rd.draw_buttons(game_display, buttons, mouse_pos, left_mouse_btn_pressed)
        

        # TODO: fix this
        rd.draw_button(game_display, button_c, mouse_pos, left_mouse_btn_pressed)
        rd.draw_button(game_display, button_s, mouse_pos, left_mouse_btn_pressed)
        

        # FIXME: 
        rd.draw_internal_window(game_display,interf_.interface.internal_windows['new_window'])
        text_surface = base_font.render(user_input, True, (255, 255, 255))
        game_display.blit(text_surface, (input_rect.x+5, input_rect.y+5))
        

        # Handle button hovers if there are any
        buttons_hovered(buttons,mouse_pos,left_mouse_btn_pressed)
        
        # Blit the custom cursor
        cursor_img_rect.center = pg.mouse.get_pos()  # update position 
        game_display.blit(h.cursor_image,(cursor_img_rect.x,cursor_img_rect.y) ) # draw the cursor

        # Update the window
        #pg.display.update()
        pg.display.flip()
        h.clock.tick(h.fps)
        
    print("WINDOW CLOSED!")

        
        
    