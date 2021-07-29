from collections import namedtuple
import curses
import numpy as np
import curses as curses


def entry(stdscr):
    
    def write(msg):
        stdscr.addstr(msg)
        stdscr.refresh()
    
    def ask(msg):
        
        curses.echo()
        write(msg)
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
            #write("".join(grid[i]) + "\n")
            
            line = ""
            for ii in grid[i]:
                line += f"{ii}{ii}"
            write(line + "\n")
                    
    def manual_placement(grid):
        write("\nunimplemented manual_placement()\n")
           
    def random_placement(grid):
        
        randoms = np.random.choice(["0", "0", "1"], grid.size)
        grid = np.reshape(randoms, grid.shape)
        
        render_grid(grid)
    
    def conways(grid):
        write("\nunimplemeneted conways()\n")
    
    placement_dict = dict(zip(
        ["manual", "random"],
        [manual_placement, random_placement]
        ))
    
    curses.noecho()
    
    stdscr.addstr("\n".join(np.full(30, "test_test")) + "\n")
    stdscr.refresh()
    
    """
    q=ask("test question:")
    key = stdscr.getstr()
    curses.echo()
    curses.endwin()
    print(key.decode())
    
    stdscr.addstr(f"\n{q=}\n")                                                 
    print(f"\n{q=}\n")
    """
    
    placement_mode = ask(f"what placement mode would you like to use? ({', '.join(placement_dict.keys())})")

    rows = int(ask("how many rows?"))
    cols = int(ask("how many columns?"))

    grid = np.zeros((rows, cols))
    grid = placement_dict[placement_mode](grid)
    conways(grid)
    
    ask("press enter to exit program")
curses.wrapper(entry) 