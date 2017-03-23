"""
Author: Bryson McIver
Created: 3/23/17
Description: With the help of pattern matching and a dictionary fill in the remaining words in a crossword grid
"""

#Python regular expressions
import re

#Globals
wordDictionary = "words.txt"
initState = "crossword.txt"
rows = 0
cols = 0
blackSquares = []

"""
Prints the provided grid
"""
def printGrid(grid):
    for row in grid:
        for col in row:
            print(col, end='')
        print('\n', end='')

"""
Uses python re to check dictionary for occurences of word
"""
def regex(exp):
    with open(wordDictionary) as words:
        filetext = words.read()
        matches = re.findall(exp ,filetext)
        return matches


"""
Perform IO and load in the current state of the crossword
"""
with open(initState) as f:
    # Grab Rows and Columns
    line = f.readline().strip()
    line = line.split(' ')
    rows = int(line[0])
    cols = int(line[1])
    #Create 2d array as all black (&)
    grid = [['&' for x in range(rows)] for y in range(cols)]
    
    #Cycle and store values
    for x in range(rows):
        line = f.readline().strip()
        line = list(line)
        for y in range(cols):
            if (line[y] == '&'):
                blackSquares.append((x,y))
            grid[x][y] = line[y]

print("Provided State")
printGrid(grid)
print(blackSquares)

"""
Primary recursive search function using least values remaining.
"""
def fillWord(grid):
    """
    Now Scan The Grid, looking for the row or col with least amount of words avail
    First do the top boarder
    """
    for y in range(cols):
        #All black squares will be handled in next loop
        if (grid[0][y] != '&'):
            #Scan down
            print('down')

    """
    Scan the left side
    """

    """
    Scan the black squares
    """


    
    
