import lib.tsp
import lib.parameter as pa

def TwoSwap():
    PathLen = len(pa.CurrentBestPath)
    PathVal = AllPathDistance(pa.CurrentBestPath)
    pa.state = not pa.state
    for i in range(PathLen - 1):
        for j in range(i + 1, PathLen):
            CopyPath = pa.CurrentBestPath.copy()
            if(pa.state):
                left = i
                right = j
            else:
                left = PathLen - 1 - i
                right = PathLen - 1 - j
            left, right = min(left, right), max(left, right)
            CopyPath = Exchange(CopyPath, left, right)
            if left == 0:
                LeftBasic = 0
            else: LeftBasic = pa.CurrentBestPath[left - 1]
            if right == PathLen - 1:
                RightBasic = 0
            else: RightBasic = pa.CurrentBestPath[right + 1]

            LeftReduceDistance = pa.DistanceMatrix[pa.CurrentBestPath[left]][LeftBasic]
            RightReduceDistance = pa.DistanceMatrix[pa.CurrentBestPath[right]][RightBasic]
            LeftAddDistance = pa.DistanceMatrix[pa.CurrentBestPath[left]][RightBasic]
            RightAddDistance = pa.DistanceMatrix[pa.CurrentBestPath[right]][LeftBasic]
            NewPathVal = PathVal - LeftReduceDistance - RightReduceDistance + LeftAddDistance + RightAddDistance
            if(NewPathVal < PathVal ):
                pa.CurrentBestPath = CopyPath
                pa.global_Value = NewPathVal
                return 0
    return 1

def Exchange(Array, i, j):
    result = Array
    a, b = i, j
    # if (i <= j):
    #     a, b = i, j
    # else:
    #     a, b = j, i
    while(a <= b ):
        result[a], result[b] = result[b], result[a]
        a += 1
        b -= 1
    return result

def AllPathDistance(path):
    """
    计算路线总长度
    :param path:
    :return:
    """
    global DistanceMatrix
    temp = pa.DistanceMatrix[0][path[0]]
    # 从两点间距离矩阵中找到路线中每一条路径的长度，求和得到路线长度
    for i in range(len(path) - 1):
        temp += pa.DistanceMatrix[path[i]][path[i + 1]]
    temp += pa.DistanceMatrix[path[-1]][0]
    return temp