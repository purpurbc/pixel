import pygame as pg
import helpers as h
import pixel_map as pm
import render as rd
import layout as lo
import tools as tl
import saver as sv
import IO as io
import interface as interf_
from types import MethodType
import copy
from PIL import Image
from configparser import ConfigParser
import tomli

def load_palettes():
    with open("config/palettes.toml", mode="rb") as fp:
        palettes = tomli.load(fp)

    for key, value in palettes['DEFAULT_PALETTE'].items():
            palettes['DEFAULT_PALETTE'][key] = tuple(value)
    
    return palettes

def init_pygame_essentials():
    # Initialize pygame
    pg.init()

    # Initialize info text for displaying active operator
    #h.font = pg.font.Font("freesansbold.ttf", 20) 
    #h.infotext = h.font.render("c: ERASE", True, h.black)
    #h.infotext_rect = h.infotext.get_rect()  
    #h.infotext_rect.center = (h.s_W // 2 , h.s_H - 30)

    # Set the caption of the display
    pg.display.set_caption("pxls")

def set_custom_cursor(image, size):
    # Set the visibility of the default cursor to false
    pg.mouse.set_visible(False) 

    image_transformed = pg.transform.scale(image, size)

    # Return the image of the cursor for blitting
    return image_transformed

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

# TODO: make this general, and not just for palettes 
def create_button_grid(palette, tool_box, paint_size, max_width, margin):
    
    paint_buttons = []                                      # List for all the paint buttons
    paint_pos = [margin,margin]                             # Position of the current paint buttons placement
    num_columns = int(max_width/(paint_size[0]+2*margin))   # Number of columns in the grid
    
    # Loop all the colors within the palette
    for i, (_, paint_color) in enumerate(palette.colors.items()):
        
        # Create a button and set its approapriate action for each color
        paint_btn = lo.Button(lo.Structure(pg.Rect(paint_pos, paint_size), paint_color), paint_color, h.WHITE)
        paint_btn.action = MethodType(lo.change_pen_color, paint_btn)
        paint_btn.set_action_arguments({'tool_box' : tool_box, 'color': paint_color})
        
        # Append the paint button to the list
        paint_buttons.append(paint_btn)

        # Update the paint button postion for the next paint button
        # Move to the next row if the current row is full
        if (i+1)%num_columns == 0:
            paint_pos[0] = margin
            paint_pos[1] = paint_pos[1] + (paint_size[1] + margin)
            
        else:
            paint_pos[0] = paint_pos[0] + (paint_size[0] + margin) 
    
    # Return the buttons
    return paint_buttons

def run_application():
    """The game loop"""

    #////////////////////-- Intial Setup --/////////////////////

    # initialize the pygame essentials
    init_pygame_essentials()
    
    # Create the game display
    game_display = pg.display.set_mode(h.s_dimension) 

    IO_handler = io.IO_handler()
    
    palettes = load_palettes()

    #////////////////////-- Interface Setup --/////////////////////
    
    # Create a toolbox
    toolbox = tl.ToolBox()

    # Create a pixelmap
    w_h = 500           #width and height
    r_c = 20            #rows and columns
    pix_dim = (int(w_h/r_c),int(w_h/r_c))
    pixel_map = pm.PixelMap(pix_dim, lo.Structure(pg.Rect(250,50,w_h,w_h),h.grey,h.dark_grey,3))

    # Create a saving unit
    saver = sv.Saver()

    # Create an internal window
    internal_window = lo.InternalWindow(lo.Structure(pg.Rect(h.s_W - 235, 5,150,20),line_width=2),name='save_as_filename')

    # Create the interface
    Interface = interf_.Interface(pixel_map=pixel_map, 
                                  toolbox=toolbox, 
                                  saver=saver,
                                  internal_window=internal_window) 
    
    #////////////////////-- Buttons/Sliders/Cursor --/////////////////////

    cursor_image = set_custom_cursor(h.cursor_image, (20,20))

    # SAVE_AS AND QUIT BUTTONS
    side = 20
    button_c = lo.Button(lo.Structure(pg.Rect(h.s_W-side-20,5,side + 15,side),h.red),h.light_red,h.WHITE)
    button_c.action = MethodType(lo.close_window,button_c)
    
    button_s = lo.Button(lo.Structure(pg.Rect(h.s_W-side- 40 - side,5,side + 15,side),h.blue),h.light_blue,h.WHITE)
    button_s.action = Interface.set_active_internal_window
    button_s.set_action_arguments({'window_name' : 'save_as_filename', 'active' : True})

    # DEFAULT PALETTE
    default_palette = pm.Palette('default', palettes['DEFAULT_PALETTE'])
    palette_structure = lo.Structure(pg.Rect(15,200,220,250))
    paint_buttons = create_button_grid(default_palette, Interface.toolbox, (20,20), palette_structure.rect.w, 2)
    palette_container = default_palette.create_palette_container(palette_structure, paint_buttons)

    # TEST INPUT
    user_input = ''
    base_font = pg.font.Font(None, 20)
    input_rect = Interface.internal_windows['save_as_filename'].window_structure.rect
    
    # TEST SLIDER
    slider_structure = lo.Structure(pg.Rect(10,10,100,34))
    slider_container = create_rgb_picker_container(slider_structure)

    #////////////////////-- Application Loop --/////////////////////

    while Interface.running:
        
        # Continously update the mouse position
        mouse_pos = pg.mouse.get_pos()
        Interface.set_mouse_pos(mouse_pos)

        #////////////////////-- Event Handling --/////////////////////

        user_input = IO_handler.handle_event(Interface, 
                                            button_s, 
                                            button_c, 
                                            palette_container, 
                                            slider_container, 
                                            user_input)


        #////////////////////-- Render/Blit to Screen --/////////////////////
                 
        # Blit the pixelmap                
        rd.blit_pixelmap(game_display, Interface.pixel_map)
        
        # ESSENTIAL
        # Blit a cell around the hovered pixel to highlight it
        hovered_pixel = Interface.pixel_map.get_pixel(mouse_pos)
        if hovered_pixel:
            rd.draw_cell(game_display, hovered_pixel.rect, Interface.pixel_map.structure.line_color, 2)
        
        # ESSENTIAL 
        # TODO: make it prettier
        # Draw the container
        rd.draw_container(game_display, palette_container)
        
        # Draw all the buttons
        rd.draw_buttons(game_display, palette_container.buttons, mouse_pos, IO_handler.left_mouse_btn_pressed)
        # Handle button hovers if there are any
        #buttons_hovered(buttons,mouse_pos,left_mouse_btn_pressed)
        
        # ESSENTIAL
        # FIXME
        for btn in palette_container.buttons:
            try: 
                if Interface.toolbox.get_active_tool().color == btn.action_arguments['color']:
                    rd.draw_cell(game_display, btn.structure.rect, h.yellow, 2)
            except KeyError:
                pass

        # ESSENTIAL
        # TODO: fix this
        rd.draw_button(game_display, button_c, mouse_pos, IO_handler.left_mouse_btn_pressed)
        rd.draw_button(game_display, button_s, mouse_pos, IO_handler.left_mouse_btn_pressed)
        
        # ESSENTIAL
        # Draw the internal windows
        rd.draw_internal_windows(game_display,Interface.internal_windows)

        # ESSENTIAL
        # TESTING SLIDER
        rd.draw_container(game_display, slider_container)
        for i, slr in enumerate(slider_container.sliders):
            rd.draw_slider(game_display, slr, mouse_pos, IO_handler.left_mouse_btn_pressed)
            val = int(slr.get_value())
            if val:
                tool_color = Interface.toolbox.get_active_tool().color
                if i == 0:
                    Interface.toolbox.get_active_tool().color = (val,tool_color[1],tool_color[2])
                elif i == 1:
                    Interface.toolbox.get_active_tool().color = (tool_color[0],val,tool_color[2])
                elif i == 2:
                    Interface.toolbox.get_active_tool().color = (tool_color[0],tool_color[1],val)
        
        # ESSENTIAL
        # FIXME:
        active_window = Interface.get_active_internal_window()
        if active_window:
            if active_window.name == 'save_as_filename':
                text_surface = base_font.render(user_input, True, (255, 255, 255))
                game_display.blit(text_surface, (input_rect.x+5, input_rect.y+5))
        
        # ESSENTIAL
        # Blit the custom cursor
        cursor_image_rect = cursor_image.get_rect()
        cursor_image_rect.center = mouse_pos  # update position 
        game_display.blit(cursor_image,(cursor_image_rect.x,cursor_image_rect.y) ) # draw the cursor

        # ESSENTIAL
        # Update the window
        #pg.display.update()
        pg.display.flip()
        h.clock.tick(h.fps)
        
    print("WINDOW CLOSED!")

        
        
    