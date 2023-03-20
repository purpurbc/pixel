import pygame as pg
from stuff import helpers as h
from stuff import pixel_map as pm
from stuff import render as rd
from stuff import layout as lo
from stuff import tools as tl
from types import MethodType
import copy


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

    # Create the pixelmap
    x = 20
    s = 500
    #pixel_map = pm.PixelMap((int(h.s_H/x),int(h.s_W/x)), pg.Rect(0,0,h.s_W,h.s_H))
    pixel_map = pm.PixelMap((int(s/x),int(s/x)), pg.Rect(250,50,s,s))
    #print(pixel_map.pixel_dimensions)

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
    
    button_c = lo.Button(pg.Rect(h.s_W-side-20,5,side + 15,side))
    button_c.action = MethodType(lo.close_window,button_c)
    
    buttons = [button1, button2, button3, button4]
    
    btn_container = lo.Container(pg.Rect(50,50,100,500),buttons)
    
    pen = tl.Pen()
    tl.tool_box.add_tool('pen',pen)
    tl.tool_box.set_active_tool('pen')
    
    
    
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
                tl.tool_box.get_active_tool().fill_pixels(pixel_map, mouse_pos)

                # Handle button presses if there are any
                buttons_pressed(buttons,mouse_pos,left_mouse_btn_pressed) 
                
                if button_c.on_pressed(mouse_pos,left_mouse_btn_pressed):
                    pass
            
            # If the left mouse button is released
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                
                left_mouse_btn_pressed = False
                
                # Handle button clicks if there are any
                buttons_clicked(buttons,mouse_pos,left_mouse_btn_pressed)
                
                if button_c.on_clicked(mouse_pos,left_mouse_btn_pressed):
                    pass

            # If a key is pressed
            if event.type == pg.KEYDOWN:
                
                # If the pressed key is C
                if event.key == pg.K_c:
                    
                    # Clear the pixel_map
                    rd.clear_pixelmap(pixel_map)

        # Blit the pixelmap                
        rd.blit_pixelmap(game_display, pixel_map)

        # Blit a cell around the hovered pixel to highlight it
        hovered_pixel = pixel_map.get_pixel(mouse_pos)
        if hovered_pixel:
            rd.draw_cell(game_display, hovered_pixel.rect, pixel_map.line_color, 4)
        
        rd.draw_container(game_display, btn_container)
        
        # Draw all the buttons
        rd.draw_buttons(game_display, buttons, mouse_pos, left_mouse_btn_pressed)
        
        rd.draw_button(game_display, button_c, mouse_pos, left_mouse_btn_pressed)
        
        # Handle button hovers if there are any
        buttons_hovered(buttons,mouse_pos,left_mouse_btn_pressed)
        
        # Blit the custom cursor
        cursor_img_rect.center = pg.mouse.get_pos()  # update position 
        game_display.blit(h.cursor_image,(cursor_img_rect.x,cursor_img_rect.y) ) # draw the cursor

        # Update the window
        pg.display.update()
        h.clock.tick(h.fps)
        
    print("WINDOW CLOSED!")

        
        
    