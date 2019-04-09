import numpy as np
import random

N = 0  # 城市数量
PathNumber = 40  # 每一代存活的路线数量
CrossoverProbability = 0.7  # 交配的概率
MutationProbability = 0.9  # 变异的概率
MaxStop = 5  # 最长停止进化代数
CandidateNumber = PathNumber * PathNumber  # 按照算法，每一代产生的候选路线，最大数量是第一代的平方
CandidatePath = [[0] * N] * CandidateNumber
CandidatePathValue = [0] * CandidateNumber
CurrentPathNumber = 0  # 记录当前这一代的候选路线数量
StayGen = 0  # 停止进化的代数
PathValue = []
Path = []
Best = 0 # 2交换中寻找最优解的标志位
CurrentBestPath = []
DistanceMatrix = np.zeros((N, N))
Nodes = []
global_Value = 0 # 记录全局最短路径
state = True # 记录2交换时，从前还是从后交换

def NewTestInitial(Num):
    global N, CurrentPathNumber, StayGen, PathValue, Path, CurrentBestPath, DistanceMatrix, Nodes, global_Value
    N = Num  # 城市数量
    CurrentPathNumber = 0  # 记录当前这一代的候选路线数量
    StayGen = 0  # 停止进化的代数
    PathValue = []
    Path = []
    CurrentBestPath = []
    DistanceMatrix = np.zeros((N, N))
    Nodes = []
    global_Value = 0  # 记录全局最短路径

def BuildCities(Num):
    global DistanceMatrix, Nodes, CandidatePath
    NewTestInitial(Num)
    for i in range(Num):
        Nodes.append([random.randint(0, 500), random.randint(0, 500)])

    for i in range(Num):
        for j in range(i + 1, Num):
            distance = np.sqrt((Nodes[i][0] - Nodes[j][0]) ** 2 + (Nodes[i][1] - Nodes[j][1]) ** 2)
            DistanceMatrix[i][j], DistanceMatrix[j][i] = distance, distance
    return Nodes, DistanceMatrix

def Initial():
    """
    初始化种群
    :return:
    """
    global N, DistanceMatrix, PathValue, Path
    init = list(range(1, N, 1)) # 顺序列出所有节点
    Path = [0] * PathNumber
    PathValue = [0] * PathNumber
    for i in range(PathNumber):
        random.shuffle(init) # 随机生成一条路径
        data = init
        Path[i] = data.copy()
        PathValue[i] = AllPathDistance(Path[i]) # 计算每一条随机路径的长度
    # 找出以上路径中最短的一条
    indexes = np.argsort(PathValue) # 将路径按长度排序,，得到索引
    Path = np.array(Path)[indexes]# 按照索引排序路径
    # 对所有路径长度排序
    PathValue = np.sort(PathValue)
    return PathValue, Path # 返回排序后的路径长度和路径，PathValue[0]即是最短路径长度


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