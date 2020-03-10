'''
author: Patrick Ziajski
'''
import random, sys
from copy import deepcopy

marker = '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
shortestPath = []
totalPath = []

def mazeGen(r, c):
    maze = [None for r in range(r)]
    rowIndex = 0
    (rows, cols) = (r, c)

    rows -= 1
    cols -= 1
    (blank, roof, wall, corner) = ' -|+'
    M = str(roof * int(cols / 2))
    n = random.randint(1, (int(cols / 2)) * (int(rows / 2) - 1))

    for i in range(int(rows / 2)) :
        e = s = t = ''
        N = wall
        if i == 0 :
            t = '@'  # add entry marker '@' on first row first col only
        for j in range(int(cols / 2)) :
            if i and(random.randint(0, 1) or j == 0) :
                s += N + blank
                t += wall
                N = wall
                M = M[1 : ] + corner
            else :
                s += M[0] + roof
                if i or j :
                    t += blank  # add blank to compensate for '@' on first row only
                N = corner
                M = M[1 : ] + roof
            n -= 1
            t += ' #' [n == 0]
        if cols & 1 :
            s += s[-1]
            t += blank
            e = roof
        maze[rowIndex] = list(s + N)
        rowIndex += 1
        maze[rowIndex] = list(t + wall)
        rowIndex += 1
    if rows & 1 :
        maze[rowIndex] = list(t + wall)
        rowIndex += 1
    maze[rowIndex] = list(roof.join(M) + e + roof + corner)
    return maze

def traverseMaze(x, y, maze):
    ignore = ['|', '-', '+']
    if maze[x][y] == '#': # checks if current spot is the '#' which is needed for recursion
        return x, y
    if maze[x + 1][y] not in ignore:
        if [x + 1, y] not in totalPath:
            totalPath.append([x + 1, y]) # store to full path list
        i, j = traverseMaze(x + 1, y, maze) # check the surrounding spots recursively
        if i != None or j != None:
            shortestPath.insert(0, [x, y]) # stores only the path directly related to finding the '#'
            return i, j
    if maze[x][y + 1] not in ignore:
        if [x, y + 1] not in totalPath:
            totalPath.append([x, y + 1]) # store to full path list
        i, j = traverseMaze(x, y + 1, maze) # check the surrounding spots recursively
        if i != None or j != None: # checks if '#' is found or not
            shortestPath.insert(0, [x, y]) # stores only the path directly related to finding the '#'
            return i, j
    return None, None # returns only if there are no open spaces to move to, needed in case this method is the n'th method in recursion

def TotalPathsPossible(maze): # used to see all space in the maze
    temp = 0
    for i in maze:
        for j in i:
            if j == ' ':
                temp += 1
    return temp

def ConvertShortestPath(): # used to find the directions, N or E, using the shortest route
    temp = ''
    for i in range(1, len(shortestPath)):
        if shortestPath[i][0] == shortestPath[i - 1][0]: # if the y values of the current and previous positions are the same
            temp += 'N'
        else:
            temp += 'E'
    return temp

def ConvertTotalPath(): # create a string of all paths taken
    temp = ''
    index = 0
    newNode = False
    for i in range(0, len(totalPath) - 1):
        if i == 0: # required to function because later checks look at 2 previous position
            temp += marker[index]
        elif i == 1: # required to function because later checks look at 2 previous position
            index += 1
            temp += marker[index]
        # checks if the change is position is only down
        elif not newNode and (totalPath[i][0] - totalPath[i - 1][0] == 1) and totalPath[i][1] == totalPath[i - 1][1]:
            # checks if the previous position is also only down, if not that means the movement is a turn and must be modified
            if not ((totalPath[i - 1][0] - totalPath[i - 2][0] == 1) and totalPath[i - 1][1] == totalPath[i - 2][1]):
                index += 1
                temp += marker[index]
            else:
                temp += marker[index]
        # checks if the change is position is only right
        elif not newNode and(totalPath[i][1] - totalPath[i - 1][1] == 1) and totalPath[i][0] == totalPath[i - 1][0]:
            # checks if the previous position is also only right, if not that means the movement is a turn and must be modified
            if not ((totalPath[i- 1][1] - totalPath[i - 2][1] == 1) and totalPath[i - 1][0] == totalPath[i - 2][0]):
                index += 1
                temp += marker[index]
            else:
                temp += marker[index]
        # needed to continue along a path correctly if is jumps to a previous node found from a different recursion
        elif newNode and (totalPath[i][1] != totalPath[i - 1][1]):
            newNode = False
            temp += marker[index]
        # if all previous are false, it means that the recurion node has ended and a new node is being checked
        else:
            newNode = True
            index += 1
            temp += marker[index]
    return temp

def CreateSolvedMaze(maze, path): # used to display the path in the correct indexes of the maze
    for i in range(len(totalPath) - 1):
        maze[totalPath[i][0]][totalPath[i][1]] = path[i]
    return maze

def PrintMaze(maze): # prints the maze
    for i in maze:
        for j in i:
            print(j, end="")
        print()

if __name__ == "__main__":
    try:
        rows, cols = int(sys.argv[1]), int(sys.argv[2])
    except (ValueError, IndexError):
        print("2 command line arguments expected...")
        print("Usage: python maze.py rows cols")
        print("       minimum rows >= 15 minimum cols >= 15 / maximum rows <= 25 maximum cols <= 25")
        sys.exit(0)
    try:
        assert rows >= 15 and rows <= 25 and cols >= 15 and cols <= 25
    except AssertionError:
        print("Error: maze dimensions must be at least 15 x 15 and no greater than 25 x 25 ...")
        print("Usage: python maze.py rows cols")
        print("       minimum rows >= 15 minimum cols >= 15 / maximum rows <= 25 maximum cols <= 25")
        sys.exit(0)
    print('\nPYTHON MAZE GENERATOR and SOLVER!')
    print('\nRANDOM MAZE ({}, {})'.format(rows, cols))
    maze = mazeGen(rows, cols)
    allPossibleMovements = TotalPathsPossible(maze)
    x, y = traverseMaze(1, 0, maze)
    PrintMaze(maze)
    direction = ConvertShortestPath()
    path = ConvertTotalPath()
    solvMaze = CreateSolvedMaze(deepcopy(maze), path)
    movementsUsedToSolve = len(totalPath)
    percent = format((movementsUsedToSolve / allPossibleMovements) * 100, '.4f')
    print('\nSOLVED MAZE ({}, {})'.format(rows, cols))
    PrintMaze(solvMaze)
    print('\nmaze dimensions: ({}x{})\nfound # at coords: ({}, {})\ndirections: ({})\npath: {}\ntotal searches: ({}/{}) [{}%] of maze'.format(rows, cols, x, y, direction, path, movementsUsedToSolve, allPossibleMovements, percent))