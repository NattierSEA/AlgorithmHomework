from lib.parameter import *
import lib.parameter as pa

def CrossOver(i, j):
    """
    交配过程
    将上一代的两条路线交配，将产生两条新的路线
    :param i:
    :param j:
    :return:
    """
    times = random.randint(1, pa.N - 2)
    indexes = [0] * times
    for t in range(times):
        if t == 0:
            indexes[t] = random.randint(0, pa.N - times - 1)
        else:
            indexes[t] = random.randint(indexes[t - 1] + 1, pa.N - times + t - 1)
    CandidatePath[pa.CurrentPathNumber] = pa.Path[i].copy()
    #print(pa.Path)
    Path_j_reindex = pa.Path[j].copy()[indexes]
    count = 0
    for v in range(pa.N - 1):
        if count >= times: break
        if pa.CandidatePath[pa.CurrentPathNumber][v] in Path_j_reindex:
            pa.CandidatePath[pa.CurrentPathNumber][v] = Path_j_reindex[count]
            count += 1
    pa.CandidatePathValue[pa.CurrentPathNumber] = AllPathDistance(pa.CandidatePath[pa.CurrentPathNumber])
    pa.CurrentPathNumber += 1

    pa.CandidatePath[pa.CurrentPathNumber] = pa.Path[j].copy()
    Path_i_reindex = pa.Path[i].copy()[indexes]
    count = 0
    for v in range(pa.N - 1):
        if count >= times: break
        if pa.CandidatePath[pa.CurrentPathNumber][v] in Path_i_reindex:
            pa.CandidatePath[pa.CurrentPathNumber][v] = Path_i_reindex[count]
            count += 1
    pa.CandidatePathValue[pa.CurrentPathNumber] = AllPathDistance(pa.CandidatePath[pa.CurrentPathNumber])
    pa.CurrentPathNumber += 1

def Mutation(i):
    """
    变异过程
    每条路线相当于一条染色体，染色体上基因的位置互换
    :param i:
    :return:
    """
    times = random.randint(1, pa.N - 2) # 换位置的基因数量
    # 生成换位置的基因的编号，每个编号在上一个编号的右侧，并且右侧空出的区间比剩下的待选位置数量多。
    indexes = [0] * times
    for t in range(times):
        if t == 0:
            indexes[t] = random.randint(0, pa.N - times - 1)
        else:
            indexes[t] = random.randint(indexes[t - 1] + 1, pa.N - times + t - 1)
    origin_indexes = indexes.copy() # 生成的位置序列是有序的，复制一下
    random.shuffle(indexes) # 打乱位置序列，再复制一下
    pa.CandidatePath[pa.CurrentPathNumber] = pa.Path[i].copy()

    # 使用原路径、打乱前和打乱后的位置序列，为新的路线更换具体路径
    for t in range(times):
        pa.CandidatePath[pa.CurrentPathNumber][indexes[t]] = pa.Path[i][origin_indexes[t]]
    pa.CandidatePathValue[pa.CurrentPathNumber] = AllPathDistance(pa.CandidatePath[pa.CurrentPathNumber])
    pa.CurrentPathNumber += 1

def Select():
    """
    自然选择过程
    选出与第一代数量相同，最短的路径
    :return:
    """
    # 上一代路线、变异产生的路线、交配产生的路线的总数
    tpk = pa.CandidatePath[:pa.CurrentPathNumber ]
    tpkv = pa.CandidatePathValue[:pa.CurrentPathNumber ]

    # 实用路线长度数组得出排序索引，对路线数组排序
    indexes = np.argsort(tpkv)
    tpk = np.array(tpk)[indexes]
    tpkv = np.sort(tpkv)

    pa.Path = tpk[:pa.PathNumber]
    pa.PathValue = tpkv[:pa.PathNumber]


def AllPathDistance(path):
    """
    计算路线总长度
    :param path:
    :return:
    """
    temp = pa.DistanceMatrix[0][path[0]]
    # 从两点间距离矩阵中找到路线中每一条路径的长度，求和得到路线长度
    for i in range(len(path) - 1):
        temp += pa.DistanceMatrix[path[i]][path[i + 1]]
    temp += pa.DistanceMatrix[path[-1]][0]
    return temp


def Preserve(i):
    """
    遗传过程
    直接遗传上一代的路线
    :param i:
    :return:
    """
    pa.CandidatePathValue[pa.CurrentPathNumber] = pa.PathValue[i]
    pa.CandidatePath[pa.CurrentPathNumber] = pa.Path[i].copy()
    pa.CurrentPathNumber += 1

def TSP():
    global Nodes, DistanceMatrix, PathValue, Path, CurrentPathNumber

    global_Value = pa.PathValue[0]

    while True:
        pa.CurrentPathNumber = 0
        for i in range(pa.PathNumber):
            Preserve(i) # 上一代的路线，被放到当前这代的候选路线中
            if random.random() < pa.MutationProbability:
                Mutation(i) # 每一条路径随机变异
            if i == pa.PathNumber - 1:
                break
            for j in range(i + 1, pa.PathNumber): # 用上三角矩阵的下标,代表两条路线的编号，随机交配
                if pa.CurrentPathNumber >= pa.CandidateNumber:
                    break
                if random.random() < pa.CrossoverProbability:
                    CrossOver(i, j) # 两条路线随机交配
        Select() # 自然选择，产生新一代的路线
        if pa.PathValue[0] < global_Value: # 如果新的路线距离短，替换当前最优路线
            global_Value = pa.PathValue[0]
            pa.StayGen = 0
        elif pa.PathValue[0] == global_Value:# 如果新的路线距离远，停止进化
            pa.StayGen += 1
        else:
            print("Something wrong")
            break
        if pa.StayGen == pa.MaxStop:# 连续停止进化几代，停止算法
            break

    return pa.Path[0], global_Value