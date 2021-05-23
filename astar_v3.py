# Inspiration from https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
# for his easy to understand A star explanation
class Node():

    def __init__(self, position= None, parent= None):
        self.pos = position
        self.parent = parent

        # f = g + h
        # where g is the distance or rows and cols away from start Node
        # and h is the distance from the current node and target node
        # target node in this case is always the player
        # this is used to calculate f which is the cost of the node
        # this is used to determine the node with the least cost, i.e shortest
        # path
        # initialized to 0

        self.f = 0
        self.g = 0
        self.h = 0

    def __eq__(self, other):
        return self.pos == other.pos

def aStarList(dungeon, startCoord, endCoord):
    potentialPathsList, exploredPathsList = [], []
    
    startingNode = Node(startCoord)
    potentialPathsList.append(startingNode)
    targetNode = Node(endCoord)

    while len(potentialPathsList) != 0:
        currentNode = potentialPathsList[0]

        for node in potentialPathsList:
            if node.f < currentNode.f:
                currentNode = node
    
        potentialPathsList.remove(currentNode)
        exploredPathsList.append(currentNode)

        # Awesome we found the best path!
        if currentNode == targetNode:
            bestPath = []
            presentNode = currentNode
            while presentNode.parent is not None:
                bestPath = [presentNode.pos] +  bestPath
                presentNode = presentNode.parent
            return bestPath

        children = []
        dirList = [(-1,0), (-1,-1), (0,-1), (1,0), (0,1),(1,1), (1,-1), (-1,1)]

        # checks each direction to see possible paths and makes them children nodes
        # of the starting node
        for dir in dirList:
            row, col = currentNode.pos
            drow , dcol = dir
            newRow, newCol = row+drow, col+dcol

            if dungeon[newRow][newCol] != 1:
                child = Node((newRow, newCol),currentNode)
                children.append(child)
                
        for child in children:

            if child not in exploredPathsList:
                # node distance of child from the starting Node
                child.g = currentNode.g + 1

                childRow, childCol = child.pos
                targetRow, targetCol = targetNode.pos

                # this is just pythagorus but you aren't required to take the exact
                # square root as usual as its just a distance heuristic
                # after some trial and error I determined that raising the equation
                # to the power of 0.6 instead of 0.5 speeds the algorithm by 31.4 
                # times on average but further increases have diminishing returns
                # Tldr; I improved the distance heuristic 
                child.h = ((childRow - targetRow)**2 + (childCol - targetCol)**2)**0.6
                child.f = child.g + child.h

                for node in potentialPathsList:
                    if child == node and child.g > node.g:
                        continue

                potentialPathsList.append(child)
             


            



    










        
















