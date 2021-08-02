from collections import namedtuple
import curses
import numpy as np
import curses as curses

from numpy.core.fromnumeric import std


def entry(stdscr):
    
    colours = dict(zip(
        ["default", "grid"],
        [0, 1]
        ))
    
    curses.init_pair(colours["grid"], curses.COLOR_WHITE, curses.COLOR_BLUE)
     
    def write(msg, colour_index = 0):
        stdscr.addstr(msg, curses.color_pair(colour_index))
        stdscr.refresh()
    
    def write_line(msg, colour_index = 0):
        write(msg+"\n", colour_index)
    
    def ask(msg, colour_index = 0):
        
        curses.echo()
        write_line(msg, colour_index)
        answ = stdscr.getstr()
        curses.noecho()
        return answ.decode()
    
    def print_details(mode, rows, cols, itter):
        write_line(f"mode: {mode} rows: {rows} cols: {cols} itteration number: {iterr}")
    
    def render_grid(grid):
        
        display_chars = dict(zip(
            ["block_double", "empty_double"],
            ["\u2588\u2588", "\u2591\u2591"]
        ))
        
        grid = grid.astype(str)
        
        grid[grid=="0"]=display_chars["empty_double"]
        grid[grid=="1"]=display_chars["block_double"]
        
        for i in grid:
            write_line("".join(i), 1)
                    
    def manual_placement(grid):
        write_line("unimplemented manual_placement()")
           
    def random_placement(grid):
        
        randoms = np.random.choice([0, 0, 1], grid.size)
        grid = np.reshape(randoms, grid.shape)
        
        return grid
    
    def conways(grid):
        #grid = grid.astype(int)
        new_grid = np.zeros(np.shape(grid)).astype(int)

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
                
        return new_grid
        """
        for i in range(new_grid.shape[0]):
            line = ""
            for ii in new_grid[i]:
                line += f"{ii}|"
            write_line(line, 1)
        """
                
    placement_dict = dict(zip(
        ["manual", "random"],
        [manual_placement, random_placement]
        ))
    
    
    if not curses.has_colors():
        write_line("your console does not support colour, some text may be unreadable")
    
    placement_mode = ask(f"what placement mode would you like to use? ({', '.join(placement_dict.keys())})")
    stdscr.clear()
    
    rows = int(ask("how many rows? (min 3)"))
    stdscr.clear()
    cols = int(ask("how many columns? (min 3)"))
    stdscr.clear()
    
    if rows < 3:
        rows = 3
    if cols < 3:
        cols = 3
    
    grid = np.zeros((rows, cols))
    grid = placement_dict[placement_mode](grid)
    
    iterr_no = 0
    
    write_line(f"itteration number: {iterr_no}", 1)
    iterr_no+=1
    
    grid = conways(grid)
    render_grid(grid)
    
    while True:
        
        write_line(f"itteration number: {iterr_no}", 1)
        iterr_no+=1
    
        grid = conways(grid)
        render_grid(grid)
    
        if ask("would you like to render another step?")[0] != "y":
            break
    
    ask("press enter to exit program")
curses.wrapper(entry)