from collections import namedtuple
import curses
import numpy as np
import curses as curses


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
    
    def render_grid(grid):
        
        display_chars = dict(zip(
            ["block_double", "empty_double"],
            ["\u2588\u2588"+"\u2588\u2588", "\u2591\u2591"+"\u2591\u2591"]
        ))
        
        grid = grid.astype(str)
        
        grid[grid=="0"]=display_chars["empty_double"]+display_chars["empty_double"]
        grid[grid=="1"]=display_chars["block_double"]+display_chars["block_double"]
        
        print(grid)
        for i in range(grid.shape[0]):
            line = ""
            for ii in grid[i]:
                line += f"{ii}{ii}"
            write_line(line, 1)
                    
    def manual_placement(grid):
        write_line("unimplemented manual_placement()")
           
    def random_placement(grid):
        
        randoms = np.random.choice(["0", "0", "1"], grid.size)
        grid = np.reshape(randoms, grid.shape)
        
        return grid
    
    def conways(grid):
        grid = grid.astype(int)
        new_grid = np.zeros(np.shape(grid))

        for y in range(np.shape(new_grid)[0]):
            for x in range(np.shape(new_grid)[1]):
                print([*range(np.shape(new_grid)[0])])
                print(f"[{x}, {y}] = [{new_grid[y, x]}, {grid[y, x]}]")
                
                tempX = x
                if tempX+1 == np.shape(new_grid)[1]:
                    tempX = 0
                
                tempY = y
                if tempY+1 == np.shape(new_grid)[0]:
                    tempY = 0
                
                
                write(f"{grid[y-1, x-1]=} | {grid[y-1, x]=} | {grid[y-1, tempX]=}")
                write_line(f"{grid[y, x-1]=} | {grid[y, tempX]=}")
                write_line(f"{grid[tempY, x-1]=} | {grid[tempY, x]=} | {grid[tempY, tempX]=}")
                write_line("|")
                
                 
                new_grid[y, x] = (
                grid[y-1, x-1]+grid[y-1, x]+grid[y-1, tempX]+
                grid[y, x-1]+grid[y, tempX]+
                grid[tempY, x-1]+grid[tempY, x]+grid[tempY, tempX]
                )
        
        write_line("new_grid:")
        for i in range(new_grid.shape[0]):
            line = ""
            for ii in new_grid[i]:
                line += f"{ii}|"
            write_line(line, 1)
                
    placement_dict = dict(zip(
        ["manual", "random"],
        [manual_placement, random_placement]
        ))
    
    curses.noecho()
    
    if not curses.has_colors():
        write_line("your console does not support colour, some text may be unreadable")
    
    placement_mode = ask(f"what placement mode would you like to use? ({', '.join(placement_dict.keys())})")

    rows = int(ask("how many rows? (min 3)"))
    cols = int(ask("how many columns? (min 3)"))

    if rows < 3:
        rows = 3
    if cols < 3:
        cols = 3
    
    grid = np.zeros((rows, cols))
    grid = placement_dict[placement_mode](grid)
    render_grid(grid)
    conways(grid)
    
    ask("press enter to exit program")
curses.wrapper(entry)