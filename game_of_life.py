from collections import namedtuple
import curses
import numpy as np
import math
import curses

def ask(msg, stdscr):
    stdscr.addstr(msg)
    stdscr.refresh()
    #return input()

def render_grid(grid):    
    display_chars = dict(zip(
        ["block_double", "empty_double"],
        ["\u2588\u2588", "\u2591\u2591"]
    ))
    
    grid = grid.astype(str)
    
    grid[grid=="0"]=display_chars["empty_double"]
    grid[grid=="1"]=display_chars["block_double"]
    
    print(grid)
    for i in range(grid.shape[0]):
        #print("".join(grid[i]))
        line = ""
        for ii in grid[i]:
            line += f"{ii}{ii}"
        print(line)

def manual_placement(grid):
    print("unimplemented")
       
def random_placement(grid):
    randoms = np.random.choice(["0", "0", "1"], grid.size)
    grid = np.reshape(randoms, grid.shape)
    
    render_grid(grid)

placement_dict = dict(zip(
    ["manual", "random"],
    [manual_placement, random_placement]
    ))

def main(stdscr):
    
    curses.noecho()
    curses.nocbreak()
    stdscr.addstr("test_test")
    stdscr.refresh()
    return
    placement_mode = ask(f"what placement mode would you like to use? ({', '.join(placement_dict.keys())})")

    rows = int(ask("how many rows?"))
    cols = int(ask("how many columns?"))

    grid = np.zeros((rows, cols))
    placement_dict[placement_mode](grid)
    
curses.wrapper(main)