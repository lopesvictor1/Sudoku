from random import sample


def create_line_coordinates(cell_size:int) -> list[list[tuple]]:
    points = []
    
    #horizontal lines
    for y in range(1,9):
        temp = []
        temp.append((0, y * cell_size)) #creates a tuple that represent x,y points (0, 100), (0,200), (0,300)...
        temp.append((900, y * cell_size)) #creates a tuple that represent x,y points (900, 100), (900,200), (900,300)...
        points.append(temp)
    
    #vertical lines
    for x in range(1,10):
        temp = []
        temp.append((x * cell_size, 0)) #creates a tuple that represent x,y points (100, 0), (200,0), (300,0)...
        temp.append((x * cell_size, 900)) #creates a tuple that represent x,y points (100, 900), (200,900), (300,900)...
        points.append(temp)
    print(len(points))
    return points



SUB_GRID_SIZE = 3
GRID_SIZE = SUB_GRID_SIZE * SUB_GRID_SIZE

def pattern(row_num: int, col_num: int) -> int:
    return (SUB_GRID_SIZE * (row_num % SUB_GRID_SIZE) + row_num // SUB_GRID_SIZE + col_num) % GRID_SIZE

def shuffle(samp: range) -> list:
    return sample(samp, len(samp))

def create_grid(sub_grid: int) -> list[list]:
    #creates 9x9 field with random numbers
    
    row_base = range(sub_grid)
    rows = [g * sub_grid + r for g in shuffle(row_base) for r in shuffle(row_base)]
    cols = [g * sub_grid + r for g in shuffle(row_base) for r in shuffle(row_base)]
    nums = shuffle(range(1, sub_grid*sub_grid + 1))
    return [[nums[pattern(r, c)] for c in cols] for r in rows]


def remove_numbers(grid: list[list]) -> None:
    "Ramdomly removes a set of numbers"
    num_cells = GRID_SIZE * GRID_SIZE
    empties = num_cells * 3 // 7  #7 is good, higher number means easier game, lower number means harder game
    for i in sample(range(num_cells), empties):
        grid[i // GRID_SIZE][i % GRID_SIZE] = 0

class Grid:
    def __init__(self, font):
        self.cell_size = 100
        self.num_x_offset = 35
        self.num_y_offset = 12
        self.lines_coordinates = create_line_coordinates(self.cell_size)
        self.grid = create_grid(SUB_GRID_SIZE)
        self.game_font = font
        remove_numbers(self.grid)
        self.occupied_cells_coordinates = self.pre_occupied_cells()
        
    def get_cell(self, x: int, y: int) -> int:
        "get the value of the cell in position (y,x)"
        return self.grid[y][x]
        
    def set_cell(self, x: int, y: int, value: int) -> None:
        "set the value of the cell in position (y, x)"
        self.grid[y][x] = value
        
    def get_mouse_click(self, x: int, y: int) -> None:
        if x <= 900:
            grid_x, grid_y = x // 100, y // 100
            #print(grid_x, grid_y)
            if not self.is_cell_preoccupied(grid_x, grid_y):
                value = -1
                self.set_cell(grid_x, grid_y, value)
    
    def pre_occupied_cells(self) -> list[tuple]:
        "gets a list of the initialized cells"
        occupied_cells = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell(x, y) != 0:
                   occupied_cells.append((y, x))
        return occupied_cells
                   
    def is_cell_preoccupied(self, x: int, y: int) -> bool:
        "check if position (x, y) was initialized"
        for cell in self.occupied_cells_coordinates:
            if cell[1] == x and cell[0] == y:
                return True
        return False
        
    def __draw_lines(self, pg, surface) -> None:
        for index, point in enumerate(self.lines_coordinates):
            if index == 2 or index == 5 or index == 10 or index == 13 or index == 16:
                pg.draw.line(surface, (0, 0, 0), point[0], point[1], 2)
            else:
                pg.draw.line(surface, (220, 220, 220), point[0], point[1])
            
    def __draw_numbers(self, surface) -> None:
        "Draw Game Numbers"
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell(x, y) != 0:
                    text_surface = self.game_font.render(str(self.get_cell(x, y)), False, (0,100, 255))
                    surface.blit(text_surface, (x * self.cell_size + self.num_x_offset, y * self.cell_size + self.num_y_offset))
                
    def show(self) -> None:
        for cell in self.grid:
            print(cell)
            
    def draw_all(self, pg, surface) -> None:
        self.__draw_lines(pg, surface)
        self.__draw_numbers(surface)


if __name__ == "__main__":
    grid = Grid()
    grid.show()