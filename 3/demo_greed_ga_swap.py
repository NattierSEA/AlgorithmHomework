import numpy as np
import random
from lib.display import Show
import time

N = 100  # 城市数量
PathNumber = 40  # 每一代存活的路线数量
CrossoverProbability = 0.9  # 交配的概率
MutationProbability = 0.9  # 变异的概率
MaxStop = 5  # 最长停止进化代数
CandidateNumber = PathNumber * PathNumber  # 按照算法，每一代产生的候选路线，最大数量是第一代的平方
CandidatePath = [[0] * N] * CandidateNumber
CandidatePathValue = [0] * CandidateNumber
CurrentPathNumber = 0  # 记录当前这一代的候选路线数量
StayGen = 0  # 停止进化的代数
PathValue = []
Path = []
state = True
Best = 0 # 2交换中寻找最优解的标志位
CurrentBestPath = []

def CrossOver(i, j):
    """
    交配过程
    将上一代的两条路线交配，将产生两条新的路线
    :param i:
    :param j:
    :return:
    """
    global N, Path, CandidatePath, CandidatePathValue, CurrentPathNumber
    times = random.randint(1, N - 2)
    indexes = [0] * times
    for t in range(times):
        if t == 0:
            indexes[t] = random.randint(0, N - times - 1)
        else:
            indexes[t] = random.randint(indexes[t - 1] + 1, N - times + t - 1)
    CandidatePath[CurrentPathNumber] = Path[i].copy()
    Path_j_reindex = Path[j].copy()[indexes]
    count = 0
    for v in range(N - 1):
        if count >= times: break
        if CandidatePath[CurrentPathNumber][v] in Path_j_reindex:
            CandidatePath[CurrentPathNumber][v] = Path_j_reindex[count]
            count += 1
    CandidatePathValue[CurrentPathNumber] = AllPathDistance(CandidatePath[CurrentPathNumber])

    CurrentPathNumber += 1
    CandidatePath[CurrentPathNumber] = Path[j].copy()
    Path_i_reindex = Path[i].copy()[indexes]
    count = 0
    for v in range(N - 1):
        if count >= times: break
        if CandidatePath[CurrentPathNumber][v] in Path_i_reindex:
            CandidatePath[CurrentPathNumber][v] = Path_i_reindex[count]
            count += 1
    CandidatePathValue[CurrentPathNumber] = AllPathDistance(CandidatePath[CurrentPathNumber])

    CurrentPathNumber += 1

def Mutation(i):
    """
    变异过程
    每条路线相当于一条染色体，染色体上基因的位置互换
    :param i:
    :return:
    """
    global N, Path, CandidatePath, CandidatePathValue, CurrentPathNumber
    times = random.randint(1, N - 2) # 换位置的基因数量
    # 生成换位置的基因的编号，每个编号在上一个编号的右侧，并且右侧空出的区间比剩下的待选位置数量多。
    indexes = [0] * times
    for t in range(times):
        if t == 0:
            indexes[t] = random.randint(0, N - times - 1)
        else:
            indexes[t] = random.randint(indexes[t - 1] + 1, N - times + t - 1)
    origin_indexes = indexes.copy() # 生成的位置序列是有序的，复制一下
    random.shuffle(indexes) # 打乱位置序列，再复制一下
    CandidatePath[CurrentPathNumber] = Path[i].copy()

    # 使用原路径、打乱前和打乱后的位置序列，为新的路线更换具体路径
    for t in range(times):
        CandidatePath[CurrentPathNumber][indexes[t]] = Path[i][origin_indexes[t]]
    CandidatePathValue[CurrentPathNumber] = AllPathDistance(CandidatePath[CurrentPathNumber])
    CurrentPathNumber += 1

def Select():
    """
    自然选择过程
    选出与第一代数量相同，最短的路径
    :return:
    """
    global N, Path, CandidatePath, CandidatePathValue, CurrentPathNumber , LEN, PathValue
    # 上一代路线、变异产生的路线、交配产生的路线的总数
    tpk = CandidatePath[:CurrentPathNumber ]
    tpkv = CandidatePathValue[:CurrentPathNumber ]

    # 实用路线长度数组得出排序索引，对路线数组排序
    indexes = np.argsort(tpkv)
    tpk = np.array(tpk)[indexes]
    tpkv = np.sort(tpkv)

    Path = tpk[:PathNumber]
    PathValue = tpkv[:PathNumber]

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

def FindNextNode(i, ThisPath):
    global  DistanceMatrix, N
    Candidate = DistanceMatrix[i]
    NodeIndexes = list(range(0, N, 1))
    indexes = np.argsort(Candidate)
    NodeIndexes = np.array(NodeIndexes)[indexes]
    for i in range(1, N):
        if NodeIndexes[i] not in ThisPath:
            return NodeIndexes[i]
    return -1

def Initial():
    """
    初始化种群
    :return:
    """
    global N
    Path = [0] * PathNumber
    PathValue = [0] * PathNumber
    for i in range(PathNumber):
        NewPath = []
        CurrentNode = 0
        NewPath.append(0)
        for j in range(1, N):
            NextTarget = FindNextNode(CurrentNode, NewPath)
            if (NextTarget != -1):
                CurrentNode = NextTarget
                NewPath.append(NextTarget)
        Path[i] = NewPath[1: N]
        PathValue[i] = AllPathDistance(Path[i]) # 计算每一条随机路径的长度
    # 找出以上路径中最短的一条
    indexes = np.argsort(PathValue) # 将路径按长度排序,，得到索引
    Path = np.array(Path)[indexes]# 按照索引排序路径
    # 对所有路径长度排序
    PathValue = np.sort(PathValue)
    return PathValue, Path # 返回排序后的路径长度和路径，PathValue[0]即是最短路径长度

def Preserve(i):
    """
    遗传过程
    直接遗传上一代的路线
    :param i:
    :return:
    """
    global CandidatePath, CandidatePathValue, Path, PathValue, CurrentPathNumber
    CandidatePathValue[CurrentPathNumber] = PathValue[i]
    CandidatePath[CurrentPathNumber] = Path[i].copy()
    CurrentPathNumber += 1

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

def TSP():
    global Nodes, DistanceMatrix, PathValue, Path, CurrentPathNumber, state, StayGen

    Nodes, DistanceMatrix = BuildCities(N)  # 得到初始点的坐标和距离矩阵
    Start = time.time()
    PathValue, Path = Initial() # 得到排序好的第一代路径及其长度

    global_Value = PathValue[0]
    Show(Nodes, Path[0], global_Value, 'Processed by Greed Algorithm')

    while True:
        CurrentPathNumber = 0
        for i in range(PathNumber):
            Preserve(i) # 上一代的路线，被放到当前这代的候选路线中
            if random.random() < MutationProbability:
                Mutation(i) # 每一条路径随机变异
            if i == PathNumber - 1:
                break
            for j in range(i + 1, PathNumber): # 用上三角矩阵的下标,代表两条路线的编号，随机交配
                if CurrentPathNumber >= CandidateNumber:
                    break
                if random.random() < CrossoverProbability:
                    CrossOver(i, j) # 两条路线随机交配
        Select() # 自然选择，产生新一代的路线
        if PathValue[0] < global_Value: # 如果新的路线距离短，替换当前最优路线
            global_Value = PathValue[0]
            Show(Nodes, Path[0], global_Value, 'Processed by Genetic Algorithm')
            StayGen = 0
        elif PathValue[0] == global_Value:# 如果新的路线距离远，停止进化
            StayGen += 1
        else:
            print("Something wrong")
            break
        if StayGen == MaxStop:# 连续停止进化几代，停止算法
            break
    Show(Nodes, Path[0], global_Value, 'Processed by Genetic Algorithm')

    Best = 0
    CurrentBestPath = Path[0]
    while(Best == 0):
        Best, CurrentBestPath, global_Value, state = TwoSwap(CurrentBestPath, state)
        Show(Nodes, CurrentBestPath, global_Value, 'Processed by 2-Swap Algorithm')

    print("Finished in " + str(time.time() - Start) + " seconds")
    print("Total Distance is " + str(global_Value))
    print(0, end='-->')
    for i in Path[0]:
        print(i, end='-->')
    print(0)

if __name__ == '__main__':

    TSP()

