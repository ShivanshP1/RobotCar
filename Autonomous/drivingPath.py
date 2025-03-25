import AstarPathFinding
import ShivPathfind
import numpy as np


direcList = np.vstack(([-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]))
moveList = []
def driving(src,dest,direcIndex):

    # AstarPathFinding.main(src, dest)
    # path = AstarPathFinding.path
    ShivPathfind.main(src,dest)
    path = ShivPathfind.pathOut

    # print("path: \n", path)
    x =0
    while x < np.size(path,0) -1:
        diffPath = path[x + 1] - path[x]
        pathIndex = np.intersect1d(np.where(direcList[:, 0] == diffPath[0]), np.where(direcList[:, 1] == diffPath[1]))
        diffIndex = direcIndex-pathIndex[0]
        print("\npath index",pathIndex[0])
        print("direction index", direcIndex)
        print("diff index", diffIndex)


        if direcIndex == pathIndex[0]:
            moveList.append("f")
            print("move",x," fw")
            numTurns = 0
        elif  diffIndex ==2 or diffIndex == 1 or diffIndex == -6 or direcIndex ==-7:
            numTurns = diffIndex % 4
            if numTurns == 1:
                moveList.append("l")
            else:
                moveList.append("l2")
            print("move",x," fw + left x", numTurns)
            direcIndex = pathIndex[0]

        elif diffIndex == -2 or diffIndex == -1 or diffIndex == 6 or direcIndex == 7:
            numTurns = (diffIndex *-1)%4
            if numTurns == 1:
                moveList.append("r")
            else:
                moveList.append("r2")
            print("move",x," fw + right x", numTurns )
            direcIndex = pathIndex[0]
        else:
            direcIndex = (direcIndex+4)%8
            moveList.append("s")
            print("move",x,"wamp wamp, do a 180")
            x = x - 1

        if len(moveList) > len(path[:]):
            print("error: movement list exceeds path node list")
        x = x + 1
    print("\nStop\n")

if __name__ == "__main__":
    src = [29, 129]  # Starting position (row, column)
    dest = [284, 393]  # Destination position
    initialDirecIndex = 2
    driving(src,dest,initialDirecIndex)
    print(moveList)
