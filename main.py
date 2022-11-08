import pygame ,sys, random, math
import sys
from tkinter import messagebox, Tk

window_width = 500                          # set the height  and width of pop_up window 
window_height = 500

window = pygame.display.set_mode((window_width, window_height))

columns = 50
rows = 50

box_width = window_width // columns
box_height = window_height // rows

grid = []                  #create grid array that contain all box
queue = []                 # this array keep the track of queued box
path = []                  # this array will keep all box that is in the path of shortest path


class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []   # this array  will store the neighbour of individual blocks
        self.prior = None

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * box_width, self.y * box_height, box_width-2, box_height-2))

    def set_neighbours(self):                  # push all neghbour of current box.
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])


# Create Grid
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)

# Set Neighbours
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()

start_box = grid[2][2]                     #mark start box and make them true s.t it won't go in queue
start_box.start = True                     
target_box=grid[35][35]                    #mark target box    ......... This can be also taken by mouse
target_box.target=True
target_box_set = True
start_box.visited = True
queue.append(start_box)                    #first push the start box in the queue


def main():
    begin_search = False                   #intially false and when we will get start_box , target_box, and wall then it will be true and algorith start working
    searching = True

    while True:
        for event in pygame.event.get():
            # Quit Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Mouse Controls
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                # Draw Wall
                if event.buttons[0]:
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = True
                # Set Target
                # if event.buttons[2] and not target_box_set:
                #     i = x // box_width
                #     j = y // box_height
                #     target_box = grid[i][j]
                #     target_box.target = True
                #     target_box_set = True
             # Start Algorithm
            if event.type == pygame.KEYDOWN and target_box_set:
                begin_search = True

        if begin_search:
            
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            queue.append(neighbour)
            else:                                            #this is used for when no solution exist . when solution exist then we will get a pop_up window that no solution exists
                if searching:                                 # for only this we import messagebox from tkinter
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There is no solution!")
                    searching = False

        window.fill((0, 0, 0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]                    
                box.draw(window, (50,50,50))                      # initially this coloured all the box by this colour code

                if box.queued:
                    box.draw(window, (200, 0, 0))                  # this will coloured all queued box by this color code
                if box.visited:
                    box.draw(window, (0, 200, 0))
                if box in path:
                    box.draw(window, (0, 0, 200))                 # this will colored the only path by particular color

                if box.start:                                     # for coloring the start block 
                    box.draw(window, (0, 200, 200))
                if box.wall:
                    box.draw(window, (10, 10, 10))                 # coloring the wall
                if box.target:
                    box.draw(window, (200, 200, 0))                 # colour the target

        pygame.display.flip()


main()
