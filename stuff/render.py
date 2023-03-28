import pygame as pg
import copy as copy
from stuff import pixel_map as pm
from stuff import helpers as h
from stuff import layout as lo


def draw_cell_side(game_display, start_pos, direction, pixel_size, line_color, line_width):

    # Create an endposition by copying the startposition
    end_pos = copy.deepcopy(start_pos)

    # Manipulate the endposition depending on the direction
    if direction == "left":
        end_pos[0] -= pixel_size[0]
    elif direction == "up":
        end_pos[1] -= pixel_size[1]
    elif direction == "right":
        end_pos[0] += pixel_size[0]
    elif direction == "down":
        end_pos[1] += pixel_size[1]

    # Draw the line with the given and calculated parameters
    pg.draw.line(game_display, line_color, start_pos, end_pos, line_width)

    return end_pos



def draw_cell(game_display, cell_rect, line_color, line_width):
   
    # Directions corresponding on the order to be drawn
    directions = ["right","down","left","up"]

    # Create an endposition by copying the startposition
    end_pos = copy.deepcopy([cell_rect.x,cell_rect.y])
    pixel_size = [cell_rect.w, cell_rect.h]

    # Draw all of the lines in the order specified in the directions
    for i in range(4):
        end_pos = draw_cell_side(game_display, end_pos, directions[i], pixel_size, line_color, line_width)
    


def draw_pixelmap(game_display, pixel_map : pm.PixelMap):
    """Blit the whole pixelmap(grid layout and the individual pixels)"""

    #TODO: fix this function. No for loops

    pixel_size = pixel_map.get_pixel_size()
    
    pg.draw.rect(game_display, pixel_map.structure.color, pixel_map.structure.rect)

    draw_cell(game_display, pixel_map.structure.rect, pixel_map.structure.line_color, pixel_map.structure.line_width)       
    
    # Draw the grid 
    for row in range(pixel_map.pixel_dimensions[1]+1):

        """pg.draw.line(game_display, 
                     pixel_map.grid_line_color, 
                     [pixel_map.rect.x, pixel_map.rect.y + row*pixel_size[1]], 
                     [pixel_map.rect.x + pixel_map.rect.w, pixel_map.rect.y + row*pixel_size[1]], 
                     pixel_map.line_width)"""

        for column in range(pixel_map.pixel_dimensions[0]+1):
            
            """pg.draw.line(game_display, 
                         pixel_map.grid_line_color, 
                         [pixel_map.rect.x + column*pixel_size[0], pixel_map.rect.y], 
                         [pixel_map.rect.x + column*pixel_size[0], pixel_map.rect.y + pixel_map.rect.h], 
                         pixel_map.line_width)"""
            pass
            #draw_cell(game_display, pixel_map.pixels[row][column].rect, pixel_map.line_color, pixel_map.line_width)

    # Draw the pixels
    for row in range(pixel_map.pixel_dimensions[1]):

        for column in range(pixel_map.pixel_dimensions[0]):

            if pixel_map.pixels[row][column].color:

                pg.draw.rect(game_display, pixel_map.pixels[row][column].color, pixel_map.pixels[row][column].rect) 
    
    

    

def clear_pixelmap(pixel_map : pm.PixelMap):
    """Sets the color of all pixels in the pixelmap to None"""

    for row in range(pixel_map.pixel_dimensions[1]):
        for column in range(pixel_map.pixel_dimensions[0]):
            pixel_map.pixels[row][column].color = None #pixel_map.pixels[row][column].previous_color


def draw_buttons(game_display, buttons : list, mouse_pos, left_mouse_btn_pressed : bool):
    for btn in buttons:
        draw_button(game_display, btn, mouse_pos, left_mouse_btn_pressed)


def draw_button(game_display, button : lo.Button, mouse_pos, left_mouse_btn_pressed : bool):
    if button.is_hovered(mouse_pos,left_mouse_btn_pressed):
        pg.draw.rect(game_display, button.hovered_color, button.structure.rect)
    elif button.is_pressed(mouse_pos,left_mouse_btn_pressed):
        pg.draw.rect(game_display, button.pressed_color, button.structure.rect)
    else:
        pg.draw.rect(game_display, button.structure.color, button.structure.rect)
    
        
def draw_container(game_display, container : lo.Container):
    #TODO: create Surface and blit that instead. Can use alpha values
    pg.draw.rect(game_display, container.structure.color, container.structure.rect)


def draw_slider(game_display, slider : lo.Slider, mouse_pos, left_mouse_btn_pressed):
    #TODO: create Surface and blit that instead. Can use alpha values
    pg.draw.rect(game_display, slider.structure.color, slider.structure.rect)
    draw_button(game_display, slider.button, mouse_pos, left_mouse_btn_pressed)




def draw_internal_window(game_display, internal_window : lo.InternalWindow):
    #TODO: create Surface and blit that instead. Can use alpha values
    win_struct = internal_window.window_structure
    pg.draw.rect(game_display, win_struct.color, win_struct.rect)
    draw_cell(game_display, win_struct.rect, win_struct.line_color, win_struct.line_width)

def draw_internal_windows(game_display, internal_windows : dict):
    for name, window in internal_windows.items():
        if window.active:
            draw_internal_window(game_display, window)


def blit_pixelmap(game_display, pixel_map):
    """Blit/Render everything"""

    #TODO: S in SOLID. Move the fill elwewhere
    # Clean slate
    game_display.fill(h.medium_grey)

    # Blit background
    # game_display.blit(pg.transform.scale(h.bg, (h.s_W, h.s_H)), (0, 0))

    # Draw the m
    draw_pixelmap(game_display, pixel_map)

    # blit optional infotext
    #game_display.blit(h.infotext, h.infotext_rect)

    