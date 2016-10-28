from tkinter import PhotoImage
import random

class Maze:
    COLOR_BLACK = (0, 0, 0)
    COLOR_RED = (255, 0, 0)
    COLOR_WHITE = (255, 255, 255)

    def __init__(self, grid_width, grid_height, cell_width):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_width = cell_width
        self.background_color = self.COLOR_BLACK
        self.foreground_color = self.COLOR_WHITE
        self.start_pos = (0, 0)
        self.on_draw = None
        self.create_image()
        pass

    def get_image(self):
        return self.screen

    def create_image(self):
        pixel_width = self.get_image_width()
        pixel_height = self.get_image_height()
        self.screen = PhotoImage(width=pixel_width, height=pixel_height)

    def get_image_width(self):
        return (2 * self.grid_width + 1) * self.cell_width

    def get_image_height(self):
        return (2 * self.grid_height + 1) * self.cell_width

    def fill_background(self):
        size = (self.get_image_width(), self.get_image_height())
        self.fill((0, 0), size, self.background_color)

    def fill(self, pos, size, color):
        width, height = size
        hexcode = self.color_to_hex(color)
        horizontal_line = "{" + " ".join([hexcode] * width) + "}"
        self.screen.put(" ".join([horizontal_line] * height), pos)

    def color_to_hex(self, color):
        return "#{:02x}{:02x}{:02x}".format(*color)

    def get_neighbors(self, cell):
        cx, cy = cell
        a, b = 1, 0

        result = []
        for i in range(4):
            x, y = cx + a, cy + b
            if x >= 0 and x < self.grid_width and y >= 0 and y < self.grid_height:
                result.append((x, y))
            a, b = b, -a

        return result

    def get_unv_neighbors(self, cell):
        unv_neighbors = []

        for neighbor in self.get_neighbors(cell):
            if neighbor not in self.visited:
                unv_neighbors.append(neighbor)

        return unv_neighbors

    def choose_unv_neighbor(self, cell):
        neighbors = self.get_unv_neighbors(cell)
        if len(neighbors) == 0:
            return None
        else:
            return random.choice(neighbors)

    def get_cell_image_pos(self, cell):
        x, y = cell
        return (2 * x + 1) * self.cell_width, (2 * y + 1) * self.cell_width

    def get_wall_image_pos(self, cell_a, cell_b):
        ax, ay = cell_a
        bx, by = cell_b

        sy = int(ax == bx)
        sx = int(ay == by)

        x = (2 * min(ax, bx) + 1 + sx) * self.cell_width
        y = (2 * min(ay, by) + 1 + sy) * self.cell_width

        return x, y

    def remove_wall(self, cell_a, cell_b, color=None):
        if color is None:
            color = self.foreground_color
        wall_pos = self.get_wall_image_pos(cell_a, cell_b)
        self.fill(wall_pos, (self.cell_width,) * 2, color)

    def fill_cell(self, cell, color=None):
        if color is None:
            color = self.foreground_color
        self.fill(self.get_cell_image_pos(cell), (self.cell_width,) * 2, color)

    def create_maze(self):
        grid_width = self.grid_width
        grid_height = self.grid_height
        cell_width = self.cell_width

        width = self.get_image_width()
        height = self.get_image_height()

        self.fill_background()

        self.visited = set()
        stack = [ self.start_pos ]

        while len(stack) > 0:
            current_cell = stack[-1]
            self.visited.add(current_cell)
            self.fill_cell(current_cell, self.COLOR_RED)
            next_cell = self.choose_unv_neighbor(current_cell)

            if next_cell:
                stack.append(next_cell)
                self.remove_wall(current_cell, next_cell, self.COLOR_RED)
            else:
                self.fill_cell(current_cell)
                stack.pop()
                if len(stack) > 0:
                    self.remove_wall(current_cell, stack[-1])

            if callable(self.on_draw):
                self.on_draw()
