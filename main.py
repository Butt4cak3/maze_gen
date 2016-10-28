from tkinter import Tk, Label
from maze import Maze

WIDTH = 100
HEIGHT = 100
CELL_WIDTH = 2

def main():
    def draw():
        master.update_idletasks()
        master.update()

    master = Tk()
    master.wm_title("Maze")
    maze = Maze(WIDTH, HEIGHT, CELL_WIDTH)
    maze.on_draw = draw
    label = Label(master, image=maze.get_image())
    label.grid()

    master.update_idletasks()
    master.update()

    maze.create_maze()

    master.mainloop()

if __name__ == "__main__":
    main()
