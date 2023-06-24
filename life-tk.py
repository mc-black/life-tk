import random
import time
import copy
import tkinter as tk


class App(tk.Tk):
    '''Create new Application.

    Create new Game of Life Application object window.'''
    def __init__(self, WIDTH=16, HEIGHT=16, TILE=40, RND_COUNT=80):
        '''Constructor with some options.

        On create new window can redefine defalt options:
        WIDTH  - horizontally size of the 'cells' array
        HEIGHT - vertically size of the 'cells' array
        TILE   - size of cell in pixels include cell borders
        RND_COUNT - count of random generated cells'''
        super().__init__()          # init base class constructor

        self.title("Conway's Game of Life") # the window title
        self.config(bg="skyblue")   # background color of the window

        self.WIDTH = WIDTH          # width in cells, horizontally
        self.HEIGHT = HEIGHT        # height in cells, vertically
        self.TILE = TILE            # size of one cell, pixels
        self.RND_COUNT = RND_COUNT  # count of random filled cells

        # vertical layout Frame for menu & canvas in main window
        self.main = tk.Frame(self, bg="white")
        self.main.grid(row=0, column=0, padx=5, pady=5)

        # horizontal layout Frame for buttons in menu
        self.menu = tk.Frame(self.main, bg="white")
        self.menu.grid(row=1, column=0, padx=0, pady=0)


        # create menu buttons
        self.btnClean = tk.Button(self.menu, text="Clean", command=self.clean,
                                  font=16, bg="LightPink")
        self.btnFill = tk.Button(self.menu, text="Fill", command=self.fill,
                                 font=16,bg="Cyan")
        self.btnStep = tk.Button(self.menu, text="Step", command=self.step,
                                 font=16,bg="GreenYellow")
        self.btnPlay = tk.Button(self.menu, text="Start", command=self.play,
                                 font=16,bg="Gold")

        # place buttons in menu horizontally
        self.btnClean.grid(row=0, column=1,padx=5, pady=5)
        self.btnFill.grid(row=0, column=2, padx=5, pady=5)
        self.btnStep.grid(row=0, column=3, padx=5, pady=5)
        self.btnPlay.grid(row=0, column=4, padx=5, pady=5)

        # create canvas, place it below menu
        self.canvas = tk.Canvas(self.main, width=self.WIDTH * self.TILE,
                                height=self.HEIGHT * self.TILE, bg="Cornsilk")
        self.canvas.grid(row=2, column=0, padx=0, pady=0)
        self.canvas.bind("<Button-1>", self.canvas_click)

        self.clean()    # clean all cells, reset counter, 'has_changes' flag


    def draw(self):
        '''Draws 'cells' array as cells on the canvas.

        Draws visible cells (colored rounds) on the canvas widget using data
        of 'cells' array. A value '1' draws as life cell, a value '0' draws as
        dead cell.'''
        for i in range(self.HEIGHT):     # external loop by rows
            for j in range(self.WIDTH): # internal loop by columns
                if self.cells[i][j]:    # fill color for life cells
                    fill_color = "LawnGreen"
                else:                   # fill color for dead cell
                    fill_color = "Bisque"
                #  draw the colored roud for cell
                self.canvas.create_oval(j * self.TILE + 2,          # cell padding 2px
                                        i * self.TILE + 2,          # cell padding 2px
                                        (j + 1) * self.TILE - 2,    # cell padding 2px
                                        (i + 1) * self.TILE - 2,    # cell padding 2px
                                        fill=fill_color,            # apply fill color
                                        outline="Cornsilk")         # invisible border
        self.canvas.update()                    # update canvas on screen
        print("Generation #:", self.counter)    # output generation counter


    def clean(self):
        '''Clean all cells.

        Clean all cells, reset generation counter, unset 'has_changes' flag
        and draw the canvas.'''
        # create 'cells' array with zero values
        self.cells = [[0 for i in range(self.WIDTH)] for j in range(self.HEIGHT)]
        self.counter = 1            # reset generation counter
        self.has_changes = False    # unset 'has_changes' flag
        # the game ends if cells not changed next step
        self.draw()                 # draws 'cells' array as cells on the canvas


    def fill(self):
        '''Fill RND_COUNT random cells in array.

        Fill RND_COUNT random cells in 'cells' array. Output it indexes. Reset
        generation counter. Set 'has_changes' flag. Draw the canvas.'''
        # life - random sample RND_COUNT values in range(0, WIDTH * HEIGHT)
        # it present k values in flat presentaton of the 'cells' array
        life = random.sample(range(self.WIDTH * self.HEIGHT), k = self.RND_COUNT)
        life.sort()         # sort list for output
        # create 'cells' array with zero values
        self.cells = [[0 for i in range(self.WIDTH)] for j in range(self.HEIGHT)]
        life_list = []      # list for output only
        for one in life:    # for each life cell
            i, j = divmod(one, self.WIDTH)  # get indexes
            self.cells[i][j] = 1            # set '1' - life cell
            life_list.append([i, j])        # add life cell indexes for output
        print(life_list)                    # print life cells indexes list
        self.counter = 1        # reset generation counter
        self.has_changes = True # set 'has_changes' flag
        self.draw()             # draws 'cells' array as cells on the canvas


    def step(self):
        '''Shos next step for game of life.

        Calculate next 'cells' array copy and draw canvas.'''
        new_cells = copy.deepcopy(self.cells)
        self.counter += 1
        self.has_changes = False
        # x0, x1, y0, y1 is the nihgbors area inside 'cells' array indexes
        # including same current cell
        for i in range(self.HEIGHT):            # external loop for rows
            y0 = max(0, i - 1)                  # y0 >= 0
            y1 = min(i + 2, self.HEIGHT)        # y1 <= HEIGHT
            for j in range(self.WIDTH):         # internal loop for columns
                x0 = max(0, j - 1)              # x0 >= 0
                x1 = min(j + 2, self.WIDTH)     # x1 <= WIDTH
                # init nighbors counter exclude current cell value
                neighbors = -self.cells[i][j]
                for y in range(y0, y1):         # for neighbors rows
                    for x in range(x0, x1):     # for neighbers columns
                        neighbors += int(self.cells[y][x])  # add counter
                # birth the new cell with 3 neighbors
                if self.cells[i][j] == 0 and neighbors == 3:
                    new_cells[i][j] = 1         # set current cell '1' life
                    self.has_changes = True     # set 'has_changes' flag
                # death of cell if neighbors not 2 or 3
                elif self.cells[i][j] == 1 and (neighbors < 2 or neighbors > 3):
                    new_cells[i][j] = 0         # set current cell '0' dead
                    self.has_changes = True     # set 'has_changes' flag
        self.cells = copy.deepcopy(new_cells)   # 'cells' array replacement
        if not self.has_changes:
            return      # stop the game
        self.draw()     # draws 'cells' array as cells on the canvas


    def play(self):
        '''Show game of life loop with fixed time intervals.

        Loop step() method while 'has_changes' flag if set.'''
        while self.has_changes:
            time.sleep(1 / 6)       # FPS = 6
            self.step()             # next one step


    def canvas_click(self, event):
        '''Event handler for left mouse click on the canvas

        Convert click coordinates to 'cells' array indexes and invert value of
        the array element.'''
        # get array indexes
        i = event.y // self.TILE   # row number
        j = event.x // self.TILE   # column number
        # invert value in the array element 0 <-> 1
        self.cells[i][j] = int(not self.cells[i][j])
        # reset counter, set 'has_changes' flag
        self.counter = 1        # reset counter
        self.has_changes = True # set 'has_changes' flag
        self.draw()    # draws 'cells' array as cells on the canvas


if __name__ == "__main__":
    '''Application entry point.

    This code ignored when running in module mode (import or python -m).'''
    app = App()     # create App object instace
    app.mainloop()  # application message loop
