import tkinter as tk
from tkinter import ttk
import time
from  A_Star import astar
'''

App that works as a maze editor. Running this program opens the maze editor. 
In the editor you can create a maze by creating walls, starting point, and ending point. 
When you have a maze built you can see the solution for it by pressing 'Solve' button. 


Also this program can be opened to just show the solution for a solved maze (Go see maze_pathfinding.py for example).

'''

CELL_SIZE = 30

class MazeGrid:
    def __init__(self, canvas, maze, cell_size, editor):
        self.canvas = canvas
        self.maze = maze
        self.cell_size = cell_size
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.canvas.pack()
        self.draw_maze()
        self.tile = 0 
        if editor:
            canvas.bind("<Button-1>", self.modify_maze_on_click)
            self.showButtons()

    def draw_maze(self):
        self.canvas.delete('all')
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = self.get_color(self.maze[row][col])
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

    def draw_path(self, path):
        # animates the path drawing. 
        for i in range(len(path) - 1):
            x1 = path[i][1] * self.cell_size + self.cell_size // 2
            y1 = path[i][0] * self.cell_size + self.cell_size // 2
            x2 = path[i+1][1] * self.cell_size + self.cell_size // 2
            y2 = path[i+1][0] * self.cell_size + self.cell_size // 2
            try: # If the user closes the window the app crashes so I used a lazy solution for this.
                self.canvas.create_line(x1, y1, x2, y2, fill="#000", width=5)
                self.canvas.update()
                time.sleep(0.1)
                
                self.canvas.create_line(x1, y1, x2, y2, fill="#f55", width=5)
            except:
                print("Window closed")
                break

    def showButtons(self):
        # Create a frame on the right side of the window
        control_frame = ttk.Frame(self.canvas)
        control_frame.place(relx=1.0, rely=0.0, anchor='ne', x=-20, y=20)

        def solveMaze():
            start = None
            end = None

            # Search for the start and end position and set them to 0's on the board.
            for cols in range(self.cols):
                for rows in range(self.rows):
                    if self.maze[rows][cols] == 2:
                        start = (rows, cols)
                        self.maze[rows][cols] = 0 
                    elif self.maze[rows][cols] == 3:
                        end = (rows, cols)
                        self.maze[rows][cols] = 0

            path = astar(self.maze, start, end)
            if path:
                self.draw_path(path)
            else:
                x = self.rows * self.cell_size // 2
                y = self.rows * self.cell_size // 2

                self.canvas.create_text(x, y, text="Path not found.", font=("Helvetica", 24), fill="red", anchor="center")

        def resetMaze():
            self.maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
            self.draw_maze()

        # Create and add the solve and reset buttons
        ttk.Button(control_frame, text="Solve", command=solveMaze).pack(pady=5)
        ttk.Button(control_frame, text="Reset", command=resetMaze).pack(pady=5)
        
        def setTile(n):
            self.tile = n
            
        # Create and add the tile buttons
        ttk.Button(control_frame, text="Set start tile", command=lambda: setTile(2)).pack(pady=5)
        ttk.Button(control_frame, text="Set end tile", command=lambda: setTile(3)).pack(pady=5)
        ttk.Button(control_frame, text="Default tile", command=lambda: setTile(0)).pack(pady=5)

    def modifyMaze(self, row, col):
        if self.tile > 1:
            # Remove old starts or ending blocks 
            for cols in range(self.cols):
                for rows in range(self.rows):
                    if self.maze[rows][cols] == self.tile:
                        self.maze[rows][cols] = 0
            self.maze[row][col] = self.tile  # Set the new start/end position
        else:
            # This one updates the maze part from 0 to 1 and vice verca.
            self.maze[row][col] = 0 if self.maze[row][col] == 1 else 1

        # Redraw the whole maze.
        self.draw_maze()

    def modify_maze_on_click(self, event):
        # Get the cell that was clicked
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if 0 <= col < self.cols and 0 <= row < self.rows:
            self.modifyMaze(row, col)

    def get_color(self, value):
        if value == 1:
            return "black"
        elif value == 2:
            return "green"
        elif value == 3:
            return "yellow"
        else:
            return "white"


def initMaze(maze, path=[], editor=False):
    '''
    Initiates canvas and shows the solution for path if editor false.
    Otherwise it shows the canvas in editor mode.

    '''
    root = tk.Tk()
    title = "Maze Editor" if editor else "Maze visualization"
    root.title(title)

    # Create canvas
    editorWidth = 100 if editor else 0
    canvas = tk.Canvas(root, width=CELL_SIZE * len(maze[0]) + editorWidth, height=CELL_SIZE * len(maze))

    # Create the Maze
    app = MazeGrid(canvas, maze, CELL_SIZE, editor)

    if not editor:
        app.draw_path(path) # Draw the path if not in editor

    root.mainloop()


if __name__ == "__main__":
    maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    initMaze(maze, editor=True)