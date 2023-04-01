import pygame as pg
import helpers as h
import pixel_map as pm
import render as rd
import layout as lo
import tools as tl
import saver as sv
import interface as interf_
from types import MethodType
import copy
from PIL import Image
from configparser import ConfigParser
import tomli

with open("config/palettes.toml", mode="rb") as fp:
    palettes = tomli.load(fp)
for key, value in palettes['DEFAULT_PALETTE'].items():
        palettes['DEFAULT_PALETTE'][key] = tuple(value)


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
    pixel_map = pm.PixelMap((int(s/x),int(s/x)), lo.Structure(pg.Rect(250,50,s,s),h.grey,h.dark_grey,3))

    pen = tl.Pen()
    pen_plus = tl.Pen([[0,1,0],[1,1,1],[0,1,0]],[1,1])
    tool_box = tl.ToolBox()
    tool_box.add_tool('pen',pen)
    tool_box.add_tool('pen_plus',pen_plus)
    tool_box.set_active_tool('pen')
    
    saver = sv.Saver()
    
    internal_window = lo.InternalWindow(lo.Structure(pg.Rect(h.s_W - 235, 5,150,20),line_width=2),name='save_as_filename')

    Interface = interf_.Interface()
    Interface.add_pixelmap(pixel_map)
    Interface.add_toolbox(tool_box)
    Interface.add_saver(saver)
    Interface.add_internal_window(internal_window)

    return Interface


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


# TODO: find a place for this 
# FIXME: OPTIMIZE!!!
def create_palette_container( palette : pm.Palette, structure : lo.Structure, tool_box : tl.ToolBox):
    paints = []
    rect = structure.rect
    paint_size = [20,20] #TODO add a proper define
    margin = 2
    num_columns = int(rect.w/(paint_size[0]+2*margin))
    print(num_columns)
    column = 0
    paint_pos = [margin,margin]
    for paint_name, paint_color in palette.colors.items():
        paint_btn = lo.Button(lo.Structure(pg.Rect(paint_pos[0], paint_pos[1], paint_size[0], paint_size[1]), paint_color), paint_color, h.WHITE)
        paint_btn.action = MethodType(lo.change_pen_color, paint_btn)
        paint_btn.set_action_arguments({'tool_box' : tool_box, 'color': paint_color})
        paints.append(paint_btn)
        column += 1
        if column >= num_columns:
            paint_pos[1] = paint_pos[1] + (paint_size[1] + margin)
            paint_pos[0] = margin
            column = 0
        else:
            paint_pos[0] = paint_pos[0] + (paint_size[0] + margin)
    palette_container = lo.Container(structure,buttons=paints)
    return palette_container

# TODO: find a place for this 
# FIXME: OPTIMIZE!!!
def create_rgb_picker_container( structure : lo.Structure):
    sliders = []
    colors = [(255,0,0),(0,255,0),(0,0,255)]
    
    for c in range(0,3):
        slider_structure = lo.Structure(pg.Rect(10,10+c*12,100,10))
        slider = lo.Slider(slider_structure,value_range=[0,255])
        slider.button.action = slider.move_slider
        slider.button.action_mode = 'was_pressed'
        slider.button.structure.color = colors[c]
        slider.button.hovered_color = colors[c]
        slider.button.set_action_arguments({'cur_mouse_pos' : [-1,-1], 'prev_mouse_pos' : [-1,-1]})
        sliders.append(slider)
    slider_container = lo.Container(structure)
    for slr in sliders:
        slider_container.sliders.append(slr)
        
    slider_container.structure.color = h.black
    return slider_container
        
    

def run_application():
    """The game loop"""
    
    left_mouse_btn_pressed = False
    running = True

    # Create the interface
    # TODO: separate the init function into two
    Interface = init() 

    # Create the game display
    game_display = pg.display.set_mode(h.s_dimension) 

    # CUSTOM CURSOR
    h.cursor_image = pg.transform.scale(h.cursor_image, (20, 20))
    cursor_img_rect = h.cursor_image.get_rect()

    # SAVE_AS AND QUIT BUTTONS
    side = 20
    button_c = lo.Button(lo.Structure(pg.Rect(h.s_W-side-20,5,side + 15,side),h.red),h.light_red,h.WHITE)
    button_c.action = MethodType(lo.close_window,button_c)
    
    button_s = lo.Button(lo.Structure(pg.Rect(h.s_W-side- 40 - side,5,side + 15,side),h.blue),h.light_blue,h.WHITE)
    button_s.action = Interface.set_active_internal_window
    button_s.set_action_arguments({'window_name' : 'save_as_filename', 'active' : True})

    # TEST PALETTE
    palette = pm.Palette('default',palettes['DEFAULT_PALETTE'])
    btn_container = create_palette_container(palette, lo.Structure(pg.Rect(15,200,220,250)), Interface.tool_box)

    # TEST INPUT
    user_input = ''
    base_font = pg.font.Font(None, 20)
    input_rect = Interface.internal_windows['save_as_filename'].window_structure.rect
    
    # TEST SLIDER
    slider_structure = lo.Structure(pg.Rect(10,10,100,34))
    slider_container = create_rgb_picker_container(slider_structure)
    
    while running:
        
        # Continously update the mouse position
        mouse_pos = pg.mouse.get_pos()
        Interface.set_mouse_pos(mouse_pos)
    
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
                Interface.tool_box.get_active_tool().fill_pixels(Interface.pixel_map, mouse_pos)

                # Handle button presses if there are any
                buttons_pressed(btn_container.buttons,mouse_pos,left_mouse_btn_pressed) 
                
                # TODO: fix this
                if button_c.on_pressed(mouse_pos,left_mouse_btn_pressed):
                    pass
                
                if button_s.on_pressed(mouse_pos,left_mouse_btn_pressed):
                    pass
                
                for slider in slider_container.sliders:
                    prev_btn_state = slider.button.was_pressed['state']
                    if slider.button.on_pressed(mouse_pos,left_mouse_btn_pressed) or slider.button.was_pressed['state']:
                        if not prev_btn_state and slider.button.was_pressed['state']:
                            slider.button.set_action_arguments({'prev_mouse_pos' : Interface.mouse_pos})
                        slider.button.set_action_arguments({'cur_mouse_pos' : Interface.mouse_pos})
                        pass

                # FIXME: 
                active_window = Interface.get_active_internal_window()
                if active_window:
                    active_window_pressed = Interface.on_active_window_pressed(mouse_pos, left_mouse_btn_pressed)
                    if active_window_pressed and active_window.name == 'save_as_filename':
                        user_input = ''
            
            # If the left mouse button is released
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                
                left_mouse_btn_pressed = False
                
                # Handle button clicks if there are any
                buttons_clicked(btn_container.buttons,mouse_pos,left_mouse_btn_pressed)
                
                # TODO: fix this
                if button_c.on_clicked(mouse_pos,left_mouse_btn_pressed):
                    pass
                
                if button_s.on_clicked(mouse_pos,left_mouse_btn_pressed):
                    user_input = Interface.saver.file_name
                    pass
                
                for slider in slider_container.sliders:
                    if slider.button.on_clicked(mouse_pos,left_mouse_btn_pressed):
                        pass
                    elif slider.button.was_pressed['state']:
                        slider.button.set_pressed(False,mouse_pos)

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
                    if Interface.tool_box.active_tool == 'pen':
                        Interface.tool_box.set_active_tool('pen_plus')
                    else:
                        Interface.tool_box.set_active_tool('pen')
                    
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
                            
        # Blit the pixelmap                
        rd.blit_pixelmap(game_display, Interface.pixel_map)
        
        # Blit a cell around the hovered pixel to highlight it
        hovered_pixel = Interface.pixel_map.get_pixel(mouse_pos)
        if hovered_pixel:
            rd.draw_cell(game_display, hovered_pixel.rect, Interface.pixel_map.structure.line_color, 2)
        
        # Draw the container
        rd.draw_container(game_display, btn_container)
        
        # Draw all the buttons
        rd.draw_buttons(game_display, btn_container.buttons, mouse_pos, left_mouse_btn_pressed)
        # Handle button hovers if there are any
        #buttons_hovered(buttons,mouse_pos,left_mouse_btn_pressed)
        
        # FIXME
        for btn in btn_container.buttons:
            try: 
                if Interface.tool_box.get_active_tool().color == btn.action_arguments['color']:
                    rd.draw_cell(game_display, btn.structure.rect, h.yellow, 2)
            except KeyError:
                pass

        # TODO: fix this
        rd.draw_button(game_display, button_c, mouse_pos, left_mouse_btn_pressed)
        rd.draw_button(game_display, button_s, mouse_pos, left_mouse_btn_pressed)
        
        # Draw the internal windows
        rd.draw_internal_windows(game_display,Interface.internal_windows)

        # TESTING SLIDER
        rd.draw_container(game_display,slider_container)
        for i, slr in enumerate(slider_container.sliders):
            rd.draw_slider(game_display, slr, mouse_pos, left_mouse_btn_pressed)
            val = int(slr.get_value())
            if val:
                tool_color = Interface.tool_box.get_active_tool().color
                if i == 0:
                    Interface.tool_box.get_active_tool().color = (val,tool_color[1],tool_color[2])
                elif i == 1:
                    Interface.tool_box.get_active_tool().color = (tool_color[0],val,tool_color[2])
                elif i == 2:
                    Interface.tool_box.get_active_tool().color = (tool_color[0],tool_color[1],val)
        
        # FIXME:
        active_window = Interface.get_active_internal_window()
        if active_window:
            if active_window.name == 'save_as_filename':
                text_surface = base_font.render(user_input, True, (255, 255, 255))
                game_display.blit(text_surface, (input_rect.x+5, input_rect.y+5))
        
        
        # Blit the custom cursor
        cursor_img_rect.center = pg.mouse.get_pos()  # update position 
        game_display.blit(h.cursor_image,(cursor_img_rect.x,cursor_img_rect.y) ) # draw the cursor

        # Update the window
        #pg.display.update()
        pg.display.flip()
        h.clock.tick(h.fps)
        
    print("WINDOW CLOSED!")

        
        
    