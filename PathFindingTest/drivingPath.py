import AstarPathFindingOld
import numpy as np


direcList = np.vstack(([-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]))
def main(src,dest,direcIndex):

    AstarPathFindingOld.main(src, dest)
    path = AstarPathFindingOld.path
    print("path: \n", path)
    print(path[1][0],path[0][0],path[1][0]-path[0][0])

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
        elif  3>= diffIndex >= 1 or -5>= diffIndex >=-7:
            print("move",x," fw + left x",diffIndex)
            direcIndex = pathIndex[0]

        elif -3>= diffIndex <= -1 or 5>=diffIndex <= 7:
            print("move",x," fw + right x", diffIndex)
            direcIndex = pathIndex[0]
        else:
            print("wamp wamp")


if __name__ == "__main__":
    src= [2,47]
    dest = [49 , 4]
    direcIndex = 6# y,x / n= -1, e=1,s=1,w=-1, orthoganal = 0
    main(src,dest,direcIndex)
