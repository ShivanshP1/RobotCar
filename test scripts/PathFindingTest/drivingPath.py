import AstarPathFinding
import numpy as np


direcList = np.vstack(([-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]))
moveList = []
def main(src,dest,direcIndex):

    AstarPathFinding.main(src, dest)
    path = AstarPathFinding.path
    #print("path: \n", path)
    x =0
    while x < len(path[:])-1:
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
        elif  2>= diffIndex >= 1 or -6>= diffIndex >=-7:
            numTurns = diffIndex % 4
            if numTurns == 1:
                moveList.append("l")
            else:
                moveList.append("l2")
            print("move",x," fw + left x", numTurns)
            direcIndex = pathIndex[0]

        elif -2>= diffIndex <= -1 or 6>=diffIndex <= 7:
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
        x = x + 1
    print("\nStop\n")

if __name__ == "__main__":
    src = [2, 62]
    dest = [30, 2]
    initialDirecIndex = 6
    main(src,dest,initialDirecIndex)
    print(moveList)
