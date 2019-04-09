

def Sift(Array, Low, High, M, C):
    i = Low      # 父节点
    j = 2 * i + 1   # 左子节点
    tmp = Array[i]   # 父节点值
    C += 2  # 第一次循环和最后一次循环，比较j和High
    while j <= High:    # 子节点在节点中
        C += 1 # 比较j和High
        C += 1 # 比较Array[j]和Array[j + 1]
        if j < High and Array[j] < Array[j + 1]:  # 有右子节点且右节点比父节点值大
            j += 1
        C += 1  # 比较tmp和Array[j]
        if tmp < Array[j]:
            M += 1
            Array[i] = Array[j]   # 将父节点替换成新的子节点的值
            i = j   # 变成新的父节点
            j = 2 * i + 1   # 新的子节点
        else:
            break
        C += 1 # 下次循环，比较j和High
    M += 1
    Array[i] = tmp   # 将替换的父节点值赋给最终的父节点
    return Array, M, C


def HeapSort(Array):
    M = 0
    C = 0
    n = len(Array)
    # 创建堆
    for i in range(n//2-1, -1, -1):
        Array, M, C = Sift(Array, i, n-1, M, C)

    # 挨个出数
    for i in range(n-1, -1, -1):    # 从大到小
        M += 2
        Array[0], Array[i] = Array[i], Array[0]     # 将最后一个值与父节点交互位置
        Array, M, C = Sift(Array, 0, i-1, M, C)

    return M, C, Array
