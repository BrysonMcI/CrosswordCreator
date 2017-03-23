"""
Author: Bryson McIver
Created: 3/23/17
Description: With the help of pattern matching and a dictionary fill in the remaining words in a crossword grid
"""

#Globals
wordDictionary = "words.txt"
initState = "crossword.txt"
rows = 0
cols = 0

"""
Prints the provided grid
"""
def printGrid(grid):
    for row in grid:
        for col in row:
            print(col, end='')
        print('\n', end='')

#Initialize
with open(initState) as f:
    # Grab Rows and Columns
    line = f.readline().strip()
    line = line.split(' ')
    rows = int(line[0])
    cols = int(line[0])
    #Create 2d array as all black (&)
    grid = [['&' for x in range(rows)] for y in range(cols)]
    
    #Cycle and store values
    for y in range(cols):
        line = f.readline().strip()
        line = list(line)
        for x in range(rows):
            grid[x][y] = line[x]


printGrid(grid)