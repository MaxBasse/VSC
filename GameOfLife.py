import matplotlib.pyplot as plt
import numpy as np
import json

fig, ax = plt.subplots()
size = 100
it: int = 0
delay = 0.01  
patterns = json.load(open('patterns.json'))


##Structuring class for the grid
class Grid:
    def __init__(self, size: int):
        self.size = size
        self.tiles = [[Tile(0.0, j, i, self) for i in range(size)] for j in range(size)]

    def dataDisplay(self):
        return [[self.tiles[i][j].getAlive() for i in range(self.size)] for j in range(self.size)]     

    def updateTile(self, x: int, y: int, status: float):
        self.tiles[x][y].updateStatus(status)

    def step(self):
        newGrid = Grid(size)
        for row in self.tiles[:]:
            for tile in row:
                nbAlive = tile.nbNeigborsAlive()
                status = tile.getAlive()
                if((nbAlive == 2 or nbAlive == 3) and status == 1):
                    newGrid.tiles[tile.x][tile.y].updateStatus(1)
                elif(nbAlive < 2 and status == 1):
                    newGrid.tiles[tile.x][tile.y].updateStatus(0)
                elif(nbAlive == 3 and status == 0):
                    newGrid.tiles[tile.x][tile.y].updateStatus(1)
        return newGrid

    def addPattern(self, pattern: str, x: int, y: int):
        pattern = patterns[pattern]
        for line in pattern:
            self.updateTile(x+line['x'], y+line['y'], 1)

##Structuring class for the tiles
class Tile:
    def __init__(self, status:float, x:int, y:int, grid: Grid):
        self.status = status
        self.x = x
        self.y = y
        self.grid = grid

    def __str__(self):
        return f"x: {self.x} y: {self.y} status: {self.status}"
    
    def nbNeigborsAlive(self):
        if(self.y == 0):
            if(self.x==0):
                return self.grid.tiles[1][0].getAlive() + self.grid.tiles[1][1].getAlive() + self.grid.tiles[0][1].getAlive()
            elif(self.x==size-1):
                return self.grid.tiles[size-2][0].getAlive() + self.grid.tiles[size-2][1].getAlive() + self.grid.tiles[size-1][1].getAlive()
            else:
                return (self.grid.tiles[self.x-1][0].getAlive() + self.grid.tiles[self.x+1][0].getAlive() 
                      + self.grid.tiles[self.x-1][1].getAlive() + self.grid.tiles[self.x][1].getAlive() + self.grid.tiles[self.x+1][1].getAlive())
            
        elif(self.x == 0):
            if(self.y==size-1):
                return self.grid.tiles[0][size-2].getAlive() + self.grid.tiles[1][size-2].getAlive() + self.grid.tiles[1][size-1].getAlive()
            else:
                return (self.grid.tiles[0][self.y-1].getAlive() + self.grid.tiles[0][self.y+1].getAlive() 
                      + self.grid.tiles[1][self.x-1].getAlive() + self.grid.tiles[1][self.y].getAlive() + self.grid.tiles[1][self.x+1].getAlive())

            
        elif(self.x == size-1):
            if(self.y==size-1):
                return self.grid.tiles[size-2][size-1].getAlive() + self.grid.tiles[size-2][size-2].getAlive() + self.grid.tiles[size-1][size-2].getAlive()
            else:
                return (self.grid.tiles[size-1][self.y-1].getAlive() + self.grid.tiles[size-1][self.y+1].getAlive() 
                      + self.grid.tiles[size-2][self.x-1].getAlive() + self.grid.tiles[size-2][self.y].getAlive() + self.grid.tiles[size-2][self.y+1].getAlive())
            
        elif(self.y == size-1):
            return (self.grid.tiles[self.x-1][size-1].getAlive() + self.grid.tiles[self.x+1][size-1].getAlive() 
                  + self.grid.tiles[self.x-1][size-2].getAlive() + self.grid.tiles[self.x][size-2].getAlive() + self.grid.tiles[self.x+1][size-2].getAlive())

        
        else: 
            return (self.grid.tiles[self.x-1][self.y-1].getAlive() + self.grid.tiles[self.x][self.y-1].getAlive() + self.grid.tiles[self.x+1][self.y-1].getAlive()
                  + self.grid.tiles[self.x-1][self.y].getAlive() + self.grid.tiles[self.x+1][self.y].getAlive()
                  + self.grid.tiles[self.x-1][self.y+1].getAlive() + self.grid.tiles[self.x][self.y+1].getAlive() + self.grid.tiles[self.x+1][self.y+1].getAlive())

    def getAlive(self):
        return self.status
    
    def updateStatus(self, status: float):
        if(status >= 1):
            self.status = 1
        else:
            self.status = 0

    def test(self):
        for row in [row[self.y-1:self.y+2] for row in self.grid.tiles[self.x-1:self.x+2]]:
            for tile in row:
                print(tile)

grid = Grid(size)
grid.addPattern('GGG', 10, 10)


#update method for the plot
while True:
    it += 1
    ax.clear() 
    ax.imshow(grid.dataDisplay())
    grid = grid.step()
    plt.title(f'Iteration n°{it}')
    plt.pause(delay)









