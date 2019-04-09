import numpy as np
import random
from lib.show import Show

N = 10  # 城市数量
PathNumber = 100  # 每一代存活的路线数量
CrossoverProbability = 0.7  # 交配的概率
MutationProbability = 0.9  # 变异的概率
MaxStop = 20  # 最长停止进化代数
CandidateNumber = PathNumber * PathNumber  # 按照算法，每一代产生的候选路线，最大数量是第一代的平方
CandidatePath = [[0] * N] * CandidateNumber
CandidatePathValue = [0] * CandidateNumber
CurrentPathNumber = 0  # 记录当前这一代的候选路线数量
StayGen = 0  # 停止进化的代数
PathValue = []
Path = []
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
    times = 1
    indexes = [0] * times
    for t in range(times):
        if t == 0:
            indexes[t] = random.randint(0, N - times - 1)
        else:
            indexes[t] = random.randint(indexes[t - 1] + 1, N - times + t - 1)
    CandidatePath[CurrentPathNumber] = Path[i].copy()
    Path_j_reindex = Path[j].copy()[indexes]

    CandidatePath[CurrentPathNumber+1] = Path[j].copy()
    Path_i_reindex = Path[i].copy()[indexes]

    NoRepeat = 1
    count = 0
    for v in range(N - 1):
        if count >= times: break
        if CandidatePath[CurrentPathNumber][v][0] == Path_j_reindex[count][1]:
            NoRepeat = 0
            break
        if CandidatePath[CurrentPathNumber + 1][v][0] == Path_i_reindex[count][1]:
            NoRepeat = 0
            break
        count += 1

    if NoRepeat == 1:
        count = 0
        for v in range(N - 1):
            if count >= times: break
            if CandidatePath[CurrentPathNumber][v] in Path_j_reindex:
                CandidatePath[CurrentPathNumber][v][1] = Path_j_reindex[count][1]
                count += 1
        CandidatePathValue[CurrentPathNumber] = AllPathDistance(CandidatePath[CurrentPathNumber])
        count = 0
        for v in range(N - 1):
            if count >= times: break
            if CandidatePath[CurrentPathNumber + 1][v] in Path_i_reindex:
                CandidatePath[CurrentPathNumber + 1][v][1] = Path_i_reindex[count][1]
                count += 1
                CandidatePathValue[CurrentPathNumber + 1] = AllPathDistance(CandidatePath[CurrentPathNumber])
        CurrentPathNumber += 2
    return NoRepeat

def Mutation(i):
    """
    变异过程
    每条路线相当于一条染色体，染色体上基因的位置互换
    :param i:
    :return:
    """
    global N, Path, CandidatePath, CandidatePathValue, CurrentPathNumber
    times = 1 # 换位置的基因数量
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

    NoRepeat = 1
    # 使用原路径、打乱前和打乱后的位置序列，为新的路线更换具体路径
    for t in range(times):
        if (CandidatePath[CurrentPathNumber][indexes[t]][0] != Path[i][origin_indexes[t]][1]):
            NoRepeat = 0
    # 使用原路径、打乱前和打乱后的位置序列，为新的路线更换具体路径
    if NoRepeat == 1 :
        for t in range(times):
            CandidatePath[CurrentPathNumber][indexes[t]][1] = Path[i][origin_indexes[t]][1]
        CandidatePathValue[CurrentPathNumber] = AllPathDistance(CandidatePath[CurrentPathNumber])
        CurrentPathNumber += 1

    return NoRepeat

def Select():
    """
    自然选择过程
    选出与第一代数量相同，最短的路径
    :return:
    """
    global N, Path, CandidatePath, CandidatePathValue, CurrentPathNumber, LEN, PathValue
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
    temp = DistanceMatrix[0][path[0][0]]
    # 从两点间距离矩阵中找到路线中每一条路径的长度，求和得到路线长度
    for i in range(len(path)):
        temp += DistanceMatrix[path[i][0]][path[i][1]]
    temp += DistanceMatrix[path[-1][1]][0]
    return temp

def Initial():
    """
    初始化种群
    :return:
    """
    global N
    init = list(range(1, N, 1)) # 顺序列出所有节点
    Path = []
    PathValue = []
    for i in range(PathNumber):
        random.shuffle(init) # 随机生成一条路径
        data = init
        Edge = []
        for i in range(N - 2):
            Edge.append([data[i], data[i + 1]])
        Edge.append([data[N - 2], data[0]])
        Path.append(Edge)
        PathValue.append(AllPathDistance(Edge))  # 计算每一条随机路径的长度
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

def TwoSwap(Path):
    PathLen = len(Path)
    PathVal = AllPathDistance(Path)
    for i in range(PathLen):
        for j in range(i+1, PathLen - 1):
            CopyPath = Path.copy()
            temp = CopyPath[i][1]
            CopyPath[i][1] = CopyPath[j][1]
            CopyPath[j][1] = temp
            NewPathVal = AllPathDistance(CopyPath)
            if(NewPathVal < PathVal ):
                return 0, CopyPath, NewPathVal
    return 1, Path, PathVal


def TSP():
    global Nodes, DistanceMatrix, PathValue, Path, CurrentPathNumber, StayGen

    Nodes, DistanceMatrix = BuildCities(N)  # 得到初始点的坐标和距离矩阵
    PathValue, Path = Initial() # 得到排序好的第一代路径及其长度

    global_Value = PathValue[0]
    Show(Nodes, Path[0], global_Value, 'Genetic Algorithm')

    while True:
        CurrentPathNumber = 0
        for i in range(PathNumber):
            Preserve(i) # 上一代的路线，被放到当前这代的候选路线中
            # if random.random() < MutationProbability:
            #     state = 0
            #     while(not state):
            #         state = Mutation(i) # 每一条路径随机变异
            if i == PathNumber - 1:
                break
            for j in range(i + 1, PathNumber): # 用上三角矩阵的下标,代表两条路线的编号，随机交配
                if CurrentPathNumber >= CandidateNumber:
                    break
                if random.random() < CrossoverProbability:
                    state = 0
                    while(not state):
                        state = CrossOver(i, j) # 两条路线随机交配
        Select() # 自然选择，产生新一代的路线
        if PathValue[0] < global_Value: # 如果新的路线距离短，替换当前最优路线
            global_Value = PathValue[0]
            Show(Nodes, Path[0], global_Value, 'Genetic Algorithm')
            StayGen = 0
        elif PathValue[0] == global_Value:# 如果新的路线距离远，停止进化
            StayGen += 1
        else:
            print("Something wrong")
            break
        if StayGen == MaxStop:# 连续停止进化几代，停止算法
            break

    Best = 0
    CurrentBestPath = Path[0]
    while(Best == 0):
        Show(Nodes, CurrentBestPath, global_Value, '2-Swap Algorithm')
        Best, CurrentBestPath, global_Value = TwoSwap(CurrentBestPath)


    print(global_Value)
    for i in Path[0]:
        print(i, end=',')
    print(0)

if __name__ == '__main__':

    TSP()

