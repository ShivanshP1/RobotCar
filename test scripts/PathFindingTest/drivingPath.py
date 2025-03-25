import AstarPathFindingOld
import numpy as np


direcList = np.vstack(([-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]))
def main(src,dest,direcIndex):

    AstarPathFindingOld.main(src, dest)
    path = AstarPathFindingOld.path
    #print("path: \n", path)
    numTurns = 0

    for x in range(len(path[:])-1):
        #direc = direcList[direcIndex]
        diffPath = path[x + 1] - path[x]
        pathIndex = np.intersect1d(np.where(direcList[:, 0] == diffPath[0]), np.where(direcList[:, 1] == diffPath[1]))
        diffIndex = direcIndex-pathIndex[0]
        #print("\ndiff path", diffPath )
        print("\npath index",pathIndex[0])
        print("direction index", direcIndex)
        print("diff index", diffIndex)
        #print("direc:", direc)
        

        if direcIndex == pathIndex[0]:
            print("move",x," fw")
            numTurns = 0
        elif  3>= diffIndex >= 1 or -5>= diffIndex >=-7:
            numTurns = diffIndex % 4
            print("move",x," fw + left x", numTurns)
            direcIndex = pathIndex[0]

        elif -3>= diffIndex <= -1 or 5>=diffIndex <= 7:
            numTurns = (diffIndex *-1)%4
            print("move",x," fw + right x", numTurns )
            direcIndex = pathIndex[0]
        else:
            x = x-1
            direcIndex = (direcIndex+4)%8
            print("wamp wamp, do a 180")


if __name__ == "__main__":
    src = [2, 62]
    dest = [30, 2]
    initialDirecIndex = 6
    main(src,dest,initialDirecIndex)
