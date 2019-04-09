import numpy as np
import random
from lib.display import Show
import time

N = 1000  # 城市数量
CurrentPathNumber = 0  # 记录当前这一代的候选路线数量
StayGen = 0  # 停止进化的代数
PathValue = []
Path = []
state = True
Best = 0 # 2交换中寻找最优解的标志位
DistanceMatrix = []

def BuildCities(N):
    Nodes = []
    for i in range(N):
        Nodes.append([random.randint(0, 500), random.randint(0, 500)])
    DistanceMatrix = np.zeros((N, N))
    for i in range(N):
        for j in range(i + 1, N):
            distance = np.sqrt((Nodes[i][0] - Nodes[j][0]) ** 2 + (Nodes[i][1] - Nodes[j][1]) ** 2)
            DistanceMatrix[i][j], DistanceMatrix[j][i] = distance, distance
    return Nodes, DistanceMatrix

def AllPathDistance(path):
    """
    计算路线总长度
    :param path:
    :return:
    """
    global DistanceMatrix
    temp = DistanceMatrix[0][path[0]]
    # 从两点间距离矩阵中找到路线中每一条路径的长度，求和得到路线长度
    for i in range(len(path) - 1):
        temp += DistanceMatrix[path[i]][path[i + 1]]
    temp += DistanceMatrix[path[-1]][0]
    return temp


def TwoSwap(Path, state):
    PathLen = len(Path)
    PathVal = AllPathDistance(Path)
    for i in range(PathLen - 1):
        for j in range(i + 1, PathLen):
            CopyPath = Path.copy()
            if(state):
                left = i
                right = j
            else:
                left = PathLen - 1 - i
                right = PathLen - 1 - j
            left, right = min(left, right), max(left, right)
            CopyPath = Exchange(CopyPath, left, right)

            if left == 0:
                LeftBasic = 0
            else: LeftBasic = Path[left - 1]
            if right == PathLen - 1:
                RightBasic = 0
            else: RightBasic = Path[right + 1]

            LeftReduceDistance = DistanceMatrix[Path[left]][LeftBasic]
            RightReduceDistance = DistanceMatrix[Path[right]][RightBasic]
            LeftAddDistance = DistanceMatrix[Path[left]][RightBasic]
            RightAddDistance = DistanceMatrix[Path[right]][LeftBasic]

            NewPathVal = PathVal - LeftReduceDistance - RightReduceDistance + LeftAddDistance + RightAddDistance
            if(NewPathVal < PathVal ):
                return 0, CopyPath, NewPathVal, not state
    return 1, Path, PathVal, not state


def Exchange(Array, i, j):
    result = Array
    if(i <= j):
        a,b = i,j
    else:
        a, b = j, i
    while(a <= b ):
        temp = result[a]
        result[a] = result[b]
        result[b] = temp
        a += 1
        b -= 1
    return result

def FindNextNode(i):
    global  DistanceMatrix, N, Path
    Candidate = DistanceMatrix[i]
    NodeIndexes = list(range(0, N, 1))
    indexes = np.argsort(Candidate)
    NodeIndexes = np.array(NodeIndexes)[indexes]
    for i in range(1, N):
        if NodeIndexes[i] not in Path:
            return NodeIndexes[i]
    return -1

def Main():
    global Nodes, DistanceMatrix, PathValue, Path, CurrentPathNumber, state

    Nodes, DistanceMatrix = BuildCities(N)  # 得到初始点的坐标和距离矩阵
    Start = time.time()
    CurrentNode = 0
    Path.append(0)
    for i in range(1, N):
        NextTarget = FindNextNode(CurrentNode)
        if NextTarget !=  -1:
            CurrentNode = NextTarget
            Path.append(NextTarget)
    Path = Path[1: N]

    PathValue = AllPathDistance(Path)
    Show(Nodes, Path, PathValue, 'Processed by Greed Algorithm')
    Best = 0
    while (Best == 0):
        Show(Nodes, Path, PathValue, 'Processed by 2-Swap Algorithm')
        Best, Path, PathValue, state = TwoSwap(Path, state)
    print("Finished in " + str(time.time() - Start) + " seconds")

if __name__ == '__main__':

    Main()

