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




class Grid:
    def __init__(self, font):
        self.cell_size = 100
        self.lines_coordinates = create_line_coordinates(self.cell_size)
        self.grid = create_grid(SUB_GRID_SIZE)
        self.game_font = font
        
    def get_cell(self, x: int, y: int) -> int:
        "get the value of the cell in position (y,x)"
        return self.grid[y][x]
        
    def set_cell(self, x: int, y: int, value: int) -> None:
        "set the value of the cell in position (y, x)"
        self.grid[y][x] = value
        
        
    def draw_lines(self, pg, surface) -> None:
        for index, point in enumerate(self.lines_coordinates):
            if index == 2 or index == 5 or index == 10 or index == 13 or index == 16:
                pg.draw.line(surface, (0, 0, 0), point[0], point[1], 2)
            else:
                pg.draw.line(surface, (220, 220, 220), point[0], point[1])
    
    def show(self):
        for cell in self.grid:
            print(cell)
            
    def draw_numbers(self, surface):
        "Draw Game Numbers"
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                text_surface = self.game_font.render(str(self.get_cell(x, y)), False, (0,200, 255))
                surface.blit(text_surface, (x * self.cell_size, y * self.cell_size))
                


if __name__ == "__main__":
    grid = Grid()
    grid.show()