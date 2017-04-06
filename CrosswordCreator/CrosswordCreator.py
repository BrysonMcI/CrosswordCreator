"""
Author: Bryson McIver
Created: 3/23/17
Description: With the help of pattern matching and a dictionary fill in the remaining words in a crossword grid
"""

#Python regular expressions
import re
import random
import string
from copy import deepcopy

#Globals
wordDictionary = "cleanWords.txt"
initState = "crossword.txt"
rows = 0
cols = 0
blackSquares = []
uncompletedWords = []
#Set to true if your word list has punctuation, really really slow.
puncClean = False
#Set to print every grid
printDebug = False
#Helpful for getting repeat results
#random.seed(1)

punctuation = set(string.punctuation)
punctuation.add("'")

"""
Prints the provided grid
"""
def printGrid(grid):
    for row in grid:
        for col in row:
            print(col, end='')
        print('\n', end='')

"""
Checks if the whole puzzle is filled
"""
def isDone(grid):
    for row in grid:
        for el in row:
            if (el == '.'):
                return False
    return True

"""
Uses python re to check dictionary for occurences of word
"""
def regex(exp):
    with open(wordDictionary) as words:
        filetext = words.read().replace('\n', ' ')
        starter = "\\b[^ ]{" + str(len(exp)) + "}\\b"
        matches = re.findall(starter, filetext, re.IGNORECASE)
        matches = ' '.join(matches)
        matches = re.findall( "\\b" + exp + "\\b", matches, re.IGNORECASE)
        #Clean out any with punctuation
        if puncClean:
            if (len(matches) > 0):
                x = 0
                while x < len(matches)-1:
                    if any(char in punctuation for char in matches[x]):
                        del matches[x]
                        x-=1
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

"""
Set up all the words.
"""
def prepGrid(grid):

    """
    Now Scan The Grid, looking for the row or col with least amount of words avail
    First do the top boarder
    """
    lowestCount = None
    for y in range(cols):
        #All black squares will be handled in next loop
        if (grid[0][y] != '&'):
            #Scan down
            exp = ""
            x = 0
            while (x < rows and grid[x][y] != '&'):
                exp+=grid[x][y]
                x+=1
            matches = regex(exp)
            if (len(matches) == 0 and exp != ''):
                return False
            if "." in exp:
                uncompletedWords.append((0, y, matches, 0))
            
    """
    Scan the left side
    """
    for x in range(rows):
        #All black squares will be handled in next loop
        if (grid[x][0] != '&'):
            #Scan Right
            exp = ""
            y = 0
            while (y < cols and grid[x][y] != '&'):
                exp+=grid[x][y]
                y+=1
            matches = regex(exp)
            if (len(matches) == 0 and exp != ''):
                return False
            if '.' in exp:
                uncompletedWords.append((x, 0, matches, 1))

    """
    Scan the black squares
    """
    for element in blackSquares:
        #check to the right
        exp = ""
        x = element[0]
        y = element[1]+1
        while (y < cols and grid[x][y] != '&'):
            exp+=grid[x][y]
            y+=1
        matches = regex(exp)
        if (len(matches) == 0 and exp != ''):
            return False
        if '.' in exp:
            uncompletedWords.append((x, element[1]+1, matches, 1))

        #check down
        exp = ""
        x = element[0]+1
        y = element[1]
        while (x < rows and grid[x][y] != '&'):
            exp+=grid[x][y]
            x+=1
        matches = regex(exp)
        if (len(matches) == 0 and exp != ''):
            return False
        if '.' in exp:
            uncompletedWords.append((element[0]+1, y, matches, 0))

"""
Solve the grid.
"""
def solveGrid(grid, uncompletedWords):
    
    grid = deepcopy(grid)
    uncompletedWords = deepcopy(uncompletedWords)
    #Check if done
    if isDone(grid):
        return grid

    if printDebug:
        print("")
        printGrid(grid)
        print("")
    
    #Resort uncompleted words
    uncompletedWords.sort(key=lambda tup: len(tup[2]))
       
    #Check if lowest match size is 0 and there is no hope
    if(len(uncompletedWords[0][2]) == 0):
        return False
    
    #Including the orginial
    saveCur = uncompletedWords[0]
    del uncompletedWords[0]
    
    while saveCur[2]:
        #Put word, update wordsToUpdate
        wordsToUpdate = []
        wordIdx = random.randint(0, len(saveCur[2])-1)
        word = saveCur[2][wordIdx]
        #Put word in grid (0 is down, 1 is right)
        x = saveCur[0]
        y = saveCur[1]
        #Down
        if (saveCur[3] == 0):
            for i in range(0, len(word)):
                grid[x+i][y] = word[i]
                #Each square will have a word to its left
                tempY = y
                while tempY >= 0 and grid[x+i][tempY] != '&':
                    if tempY == 0 or grid[x+i][tempY-1] == '&':
                        completed = False
                        try:
                            item = next(j for j in uncompletedWords if j[0] is x+i and j[1] is tempY and j[3] is 1)
                        except:
                            completed = True
                        if not completed:
                            wordsToUpdate.append(item)
                            uncompletedWords.remove(item)
                        break;
                    tempY-=1
        #Right
        else:
            for i in range(0, len(word)):
                grid[x][y+i] = word[i]
                tempX = x
                while tempX >= 0 and grid[tempX][y+i] != '&':
                    if tempX == 0 or grid[tempX-1][y+i] == '&':
                        completed = False
                        try:
                            item = next(j for j in uncompletedWords if j[0] is tempX and j[1] is y+i and j[3] is 0)
                        except:
                            completed = True
                        if not completed:
                            wordsToUpdate.append(item)
                            uncompletedWords.remove(item)
                        break;
                    tempX-=1
        
        #Update words that got affected
        #Put back words that got completed by this word
        readdWords = []
        
        updateFine = True
        for element in wordsToUpdate:
            if element[3] == 1:
                #check to the right
                exp = ""
                x = element[0]
                y = element[1]
                while (y < cols and grid[x][y] != '&'):
                    exp+=grid[x][y]
                    y+=1
                matches = regex(exp)
                if (len(matches) == 0 and exp != ''):
                    uncompletedWords.append(element)
                    updateFine = False
                elif '.' in exp:
                    uncompletedWords.append((x, element[1], matches, 1))
                else:
                    readdWords.append(element)
            else:
                #check down
                exp = ""
                x = element[0]
                y = element[1]
                while (x < rows and grid[x][y] != '&'):
                    exp+=grid[x][y]
                    x+=1
                matches = regex(exp)
                if (len(matches) == 0 and exp != ''):
                    uncompletedWords.append(element)
                    updateFine = False
                elif '.' in exp:
                    uncompletedWords.append((element[0], y, matches, 0))
                else:
                    readdWords.append(element)

        if updateFine:
            result = solveGrid(grid, uncompletedWords)
            if result is not False:
                return result

        (uncompletedWords.append(element) for element in readdWords)
        del saveCur[2][wordIdx]
        
    return False

prepFail = prepGrid(grid)

if prepFail is False:
    print("Bad starting configuration")
    print("")
else:
    print("Begin Solve")
    grid = solveGrid(grid, uncompletedWords)
    if grid is False:
        print("No possible configurations")
        print("")
    else:
        print("\nCompleted Configuration")
        printGrid(grid)
        print()
        #And Write the grid to a new file because why not
        with open('finishedCrossword.txt', 'w') as output:
            output.write(str(rows) + " " + str(cols) + "\n")
            for x in range(rows):
                for y in range(cols):
                    output.write(grid[x][y])
                output.write('\n')