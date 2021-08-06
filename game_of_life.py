from collections import namedtuple
import curses
import numpy as np
import curses as curses

from numpy.core.fromnumeric import std
from numpy.random.mtrand import random


def entry(stdscr):
    
    colours = dict(zip(
        ["default", "grid", "selected", "error", "warning"],
        [0, 1, 2, 3, 4]
        ))
    
    curses.init_pair(colours["grid"], curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(colours["selected"], curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(colours["error"], curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(colours["warning"], curses.COLOR_WHITE, curses.COLOR_YELLOW)
     
    def write(msg, colour_index = 0):
        stdscr.addstr(msg, curses.color_pair(colour_index))
        stdscr.refresh()
    
    def write_line(msg, colour_index = 0):
        write(msg+"\n", colour_index)
    
    def read():
        return stdscr.getkey()
    
    def read_line():
        answ = stdscr.getstr()
        curses.noecho()
        return answ.decode()
    
    def ask(msg, colour_index = 0):
        
        curses.echo()
        write_line(msg, colour_index)
        return read_line()
    
    class conway_grid:
        
        def __init__(self, mode, rows, cols):
            self.mode = mode; self.rows = rows; self.cols = cols
            
            #self.grids.append(np.zeros((rows, cols)))
            #self.placement_dict[mode]()
            
            self.grids.append(np.zeros((rows, cols)).astype(int))
            populated_grid = self.placement_dict[mode](self, -1)
            self.grids.append(populated_grid)

        mode = ""
        
        grids = []
        rows = 3; cols = 3
        
        display_chars = dict(zip(
            ["block_double", "empty_double"],
            ["\u2588\u2588", "\u2591\u2591"]
        ))

        def manual_placement(self, index):
            grid = self.grids[index]
            write_line("controls: WASD/arrow keys for cursor movement, space to toggle alive/dead, enter to complete")
            curses.noecho(); curses.cbreak()
            stdscr.keypad(True)
            
            self.print_grid(-1)
            
            origin = curses.getsyx()
            y_pos = 0
            x_pos = 0
            
            def update_cursor_attr(screen_y, screen_x, colour_name):
                
                char = chr(stdscr.inch(screen_y, screen_x) & 0xFF)
                
                stdscr.addstr(
                    screen_y, screen_x,
                    char+char,
                    curses.color_pair(colours[colour_name])
                    )
                
                    #inchh = chr(stdscr.inch(screen_y, screen_x) & 0xFF)
                    #write_line(f"{inchh}{inchh}")
                
            grid_shape = np.shape(grid)
            new_grid = grid
            while True:
                screen_y = origin[0]+y_pos
                screen_x = origin[1]+2*x_pos
                
                update_cursor_attr(screen_y, screen_x, "selected")
                
                input = read()
                
                if input == "w" or input == curses.KEY_UP:
                    update_cursor_attr(screen_y, screen_x, "error")
                    if y_pos == 0: y_pos = grid_shape[0]-1
                    else: y_pos -= 1
                elif input == "a" or input == curses.KEY_LEFT:
                    update_cursor_attr(screen_y, screen_x, "error")
                    if x_pos == 0: x_pos = grid_shape[0]-1
                    else: x_pos -= 1
                elif input == "s" or input == curses.KEY_DOWN:
                    update_cursor_attr(screen_y, screen_x, "error")
                    if y_pos == grid_shape[0]-1: y_pos = 0
                    else: y_pos += 1
                elif input == "d" or input == curses.KEY_RIGHT:
                    update_cursor_attr(screen_y, screen_x, "error")
                    if x_pos == grid_shape[0]-1: x_pos = 0
                    else: x_pos += 1
                elif input == " ":
                    new_text = "empty_double"
                    new_state = (grid[y_pos, x_pos]-1)**2
                    
                    new_grid[y_pos, x_pos] = new_state
                    
                    if new_state == 1: new_text = "block_double"
                    stdscr.addstr(screen_y, screen_x, self.display_chars[new_text], curses.color_pair(colours["selected"]))
                elif input == "\n":
                    stdscr.clear()
                    curses.echo()
                    return grid
            
                update_cursor_attr(screen_y, screen_x, "selected")
                

        def random_placement(self, index):
        
            randoms = np.random.choice([0, 0, 1], self.grids[index].size)
            grid = np.reshape(randoms, self.grids[index].shape)
         
            return grid
        
        def both_placement(self, index):
            self.grids.append(self.random_placement(index))
            return self.manual_placement(index)
        
        placement_dict = dict(zip(
        ["manual", "random", "both"], 
        [manual_placement, random_placement, both_placement]
        ))
                
        def print_details(self):
            write_line(f"mode: {self.mode} rows: {self.rows} cols: {self.cols} iteration number: {len(self.grids)}")
        
        def print_grid(self, index):
            grid = self.grids[index]

            grid = grid.astype(str)

            grid[grid=="0"]=self.display_chars["empty_double"]
            grid[grid=="1"]=self.display_chars["block_double"]

            for i in grid:
                write_line("".join(i), 1)

        def iterate(self):
            grid = self.grids[-1]
            new_grid = np.zeros((rows, cols)).astype(int)

            for y in range(np.shape(new_grid)[0]):
                for x in range(np.shape(new_grid)[1]):

                    #obsolete debugging code
                    #print([*range(np.shape(new_grid)[0])])
                    #print(f"[{x}, {y}] = [{new_grid[y, x]}, {grid[y, x]}]")

                    tempX = x+1
                    if tempX == np.shape(new_grid)[1]:
                        tempX = 0

                    tempY = y+1
                    if tempY == np.shape(new_grid)[0]:
                        tempY = 0

                    neighbours = (
                    grid[y-1, x-1]+grid[y-1, x]+grid[y-1, tempX]+
                    grid[y, x-1]+grid[y, tempX]+
                    grid[tempY, x-1]+grid[tempY, x]+grid[tempY, tempX]
                    )

                    if neighbours == 2:
                        new_grid[y, x] = grid[y, x]
                    elif neighbours == 3:
                        new_grid[y, x] = 1

            self.grids.append(new_grid)


    if not curses.has_colors():
        write_line("your console does not support colour, some text may be unreadable")
    
    #placement_mode = ask(f"what placement mode would you like to use? ({', '.join(placement_dict.keys())})")
    placement_mode = ask(f"what placement mode would you like to use? (manual, random, both)"); stdscr.clear()
    
    rows = int(ask("how many rows? (min 3)")); stdscr.clear()
    cols = int(ask("how many columns? (min 3)")); stdscr.clear()
    
    if rows < 3: rows = 3
    if cols < 3: cols = 3
    
    grid = conway_grid(placement_mode, rows, cols)
    
    while True:

        grid.print_details(); grid.print_grid(-1)
    
        if ask("would you like to render the next step? (yes/no)")[0] != "y": break
        
        grid.iterate()
    
    ask("program terminated, press enter to exit")
curses.wrapper(entry)