from tkinter import *
from PIL import ImageTk,Image
import tkinter.ttk as ttk
import random as ran

global app

class Window(Frame):
    size_width = 10
    size_height = 10

    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master

        self.life_image = ImageTk.PhotoImage(Image.open('./resource/circle_1x1.png').resize((20, 20), Image.ANTIALIAS))
        self.death_image = ImageTk.PhotoImage(Image.open('./resource/cross_1x1.png').resize((20, 20), Image.ANTIALIAS))

        self.playing = False

        self.alive = 0

        self.init_window()
    
    def init_window(self):
        self.set_title()

        tabControl = ttk.Notebook(self.master)

        self.tab1 = ttk.Frame(tabControl)
        tabControl.add(self.tab1, text = "Setting")
        tabControl.pack(expand=1, fill='both')

        self.init_setting(self.tab1)

        self.tab2 = ttk.Frame(tabControl)
        tabControl.add(self.tab2, text = "Game Board")
        tabControl.pack(expand=1, fill='both')

        self.board_control = ttk.Frame(self.tab2)
        self.board_control.pack(side=LEFT, expand=1, fill='both')
        right_board = ttk.Frame(self.tab2)
        right_board.pack(side=RIGHT, expand=1, fill='both')
        upper_board = ttk.Frame(right_board)
        upper_board.pack(expand=1, fill='both')
        self.upper_board_label = Label(upper_board)
        self.upper_board_label.pack(expand = 1, fill='both')
        self.board_canvas = ttk.Frame(right_board)
        self.board_canvas.pack(expand=1, fill='both')
        lower_board = ttk.Frame(right_board)
        lower_board.pack(expand=1, fill='both')
        self.lower_board_label = Label(lower_board)
        self.lower_board_label.pack(expand = 1, fill='both')
        self.init_board()

    def init_setting(self, master):
        label_promp = Label(master, text = 'Please set game board size', font=("Helvetica", 24))
        label_promp.grid(row = 0, column = 0, columnspan = 2, pady = 2)

        label_width = Label(master, text = 'Width(5 - 20):');
        label_width.grid(row = 1, column = 0, sticky = W, pady = 2)

        self.width_variable = IntVar()
        self.width_variable.set(self.size_width)
        entry_width = Entry(master, textvariable = self.width_variable)
        entry_width.selection_range(5, 20)
        entry_width.grid(row = 1, column = 1, sticky = W, pady = 2)

        label_height = Label(master, text = 'Height(5 - 20):');
        label_height.grid(row = 2, column = 0, sticky = W, pady = 2)

        self.height_variable = IntVar()
        self.height_variable.set(self.size_height)
        entry_height = Entry(master, textvariable = self.height_variable)
        entry_height.selection_range(5, 20)
        entry_height.grid(row = 2, column = 1, sticky = W, pady = 2)

        button = Button(master, text = 'Confirm', command = self.set_board)
        button.grid(row=3, column = 0, columnspan = 2, sticky = W, pady = 2)

    def set_board(self):
        self.size_height = self.height_variable.get()
        self.size_width = self.width_variable.get()
        self.set_title()
        self.update_board(True)

    def set_title(self):
        title = "Game of Life ({w} x {h})"
        self.master.title(title.format(w = self.size_width, h = self.size_height))
        
    def init_board(self):
        self.manual_button = Button(self.board_control, text='Manual Set', command=self.manual_button_click)
        self.manual_button.pack(expand=1, fill=BOTH)

        random_button = Button(self.board_control, text="Random Set", command = self.random_button_click)
        random_button.pack(expand=1, fill=BOTH)

        play_button = Button(self.board_control, text="Play", command = self.play_button_click)
        play_button.pack(expand=1, fill=BOTH)
        
        reset_button = Button(self.board_control, text="Reset", command = self.reset_button_click)
        reset_button.pack(expand=1, fill=BOTH)

        self.board = board(self.board_canvas, self.life_image, self.death_image, self.size_width, self.size_height, self.playing)
        self.board.display()
        self.upper_board_display()

    def update_board(self, reset):
        self.board.set_board(self.board_canvas, self.life_image, self.death_image, self.size_width, self.size_height, self.playing, reset)
        self.board.display()
        self.upper_board_display()

    def manual_button_click(self):
        self.playing = not self.playing
        if (self.playing):
            self.manual_button.configure(text='Manual Set')
        else:
            self.manual_button.configure(text='Done with Manual Set')
        self.update_board(False)
        self.upper_board_display()

    def random_button_click(self):
        self.board.shuffle()
        self.upper_board_display()

    def play_button_click(self):
        self.board.next_round()
        self.upper_board_display()

    def reset_button_click(self):
        self.board.reset()
        self.upper_board_display()

    def upper_board_display(self):
        self.upper_board_label.configure(text='GENERATION {0}'.format(self.board.generation))
        self.lower_board_display()
        

    def lower_board_display(self):
        self.lower_board_label.configure(text='live:{l}  dead:{d}'.format(l=self.board.alive, d=self.board.dead()))

class board:

    def __init__(self, master, life_image, death_image, width, height, playing):
        self.generation = 0
        self.width = width
        self.height = height
        self.cells = []
        self.alive = 0
        self.playing = playing
        self.set_board(master, life_image, death_image, width, height, playing, True)

    def set_board(self, master, life_image, death_image, width, height, playing, reset):
        self.destroy(reset)
        self.width = width
        self.height = height
        
        if (reset):
            for y in range(self.height):
                row = []
                for x in range(self.width):
                    row.append(cell(master, life_image, death_image, playing))
                self.cells.append(row)
        else:
            for row in self.cells:
                for c in row:
                    c.playing = playing

    def destroy(self, reset):
        for row in self.cells:
            for c in row:
                c.destroy()
        if (reset):
            self.cells = []

    def getCell(self, x, y):
        x_fix = x % self.width
        y_fix = y % self.height
        return self.cells[y_fix][x_fix];
    
    def display(self):
        for y in range(self.height):
            for x in range(self.width):
                the_cell = self.getCell(x, y)
                the_cell.display()
                the_cell.label.grid(row = y, column = x, sticky = W, pady =1)

    def shuffle(self):
        self.generation = 0
        self.alive = 0
        for y in range(self.height):
            for x in range(self.width):
                the_cell = self.getCell(x, y)
                r = ran.random()
                the_cell.status = r > 0.8
                if the_cell.status:
                    self.alive = self.alive + 1
                the_cell.display()

    def reset(self):
        self.alive = 0
        self.generation = 0
        for y in range(self.height):
            for x in range(self.width):
                the_cell = self.getCell(x, y)
                the_cell.status = False
                the_cell.display()       

    def cellNeighbors(self, x, y):
        arr = []
        arr.append(self.getCell(x - 1, y - 1))
        arr.append(self.getCell(x, y - 1))
        arr.append(self.getCell(x + 1, y - 1))
        arr.append(self.getCell(x - 1, y ))
        arr.append(self.getCell(x + 1, y ))
        arr.append(self.getCell(x - 1, y + 1))
        arr.append(self.getCell(x, y + 1))
        arr.append(self.getCell(x + 1, y + 1))
        return arr
    
    def liveOrDeath(self, x, y):
        neighbors = self.cellNeighbors(x, y)
        num = 0
        for neighbor in neighbors:
            if neighbor.status:
                num  = num + 1
        currCell = self.getCell(x, y)
        if currCell.status:
            return num == 2 or num == 3
        else:
            return num == 3

    def next_round(self):
        self.generation = self.generation + 1
        self.alive = 0
        cells = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(self.liveOrDeath(x, y))
            cells.append(row)
        for y in range(self.height):
            for x in range(self.width):
                c = self.getCell(x, y)
                c.status = cells[y][x]
                if (c.status):
                    self.alive = self.alive + 1
                c.display()
    
    def dead(self):
        return self.width * self.height - self.alive

class cell:

    def __init__(self, master, life_image, death_image, playing):
        self.life_image = life_image
        self.death_image = death_image
        self.status = False
        self.playing = playing
        self.master = master
        self.widget = False
        self.display()
    
    def display(self):
        if (not self.widget):
            self.set_widget()
        if (self.status):
            self.label.configure(image = self.life_image)
            self.label.image = self.life_image
        else:
            self.label.configure(image = self.death_image)
            self.label.image = self.death_image
    
    def switch(self):
        self.status = not self.status
        if self.status:
            app.board.alive = app.board.alive + 1
        else:
            app.board.alive = app.board.alive - 1
        print(app.board.alive)
        app.lower_board_display()
        self.display()
    
    def set_widget(self):
        if (self.playing):
            self.label = Label(self.master)
        else:
            self.label = Button(self.master, command = self.switch)
        self.widget = True

    def destroy(self):
        self.label.destroy()
        self.widget = False

root = Tk()

root.geometry("800x800")

app = Window(root)

root.mainloop()