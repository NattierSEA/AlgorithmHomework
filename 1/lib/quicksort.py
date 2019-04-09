
def Exchange(a, b):
    """
    交换两个元素的值
    """
    global M
    Temp = a
    a = b
    b = Temp
    return a, b

def Quick(Array, LeftNode, RightNode, M, C):
    """
    快速排序算法，循环迭代
    Array: 被排序的目标数组
    LightNode， RightNode: 数组被排序部分的左右端点的下标
    每次排序的基准basic为第一位，比basic大的数移到右侧，比basic小的数移到左侧
    """
    Length = RightNode - LeftNode + 1 # 待排列的部分长度

    i = 1
    j = Length - 1
    State = 0 # 查找方向标志位

    C += 1  # 第一次循环前，比较i和j
    while(i <= j):
        C +=1 # 比较i和j
        if(State == 0): # 首先从左侧找比basic大的数
            C +=1 # 比较Array[LeftNode + i]和Array[LeftNode]
            if(Array[LeftNode + i] >= Array[LeftNode]):
                State = 1 # 找到比basic大的数，从右侧找比basic小的数
            else:
                i += 1
        else:
            C += 1  # 比较Array[LeftNode + j]和Array[LeftNode]
            if(Array[LeftNode + j] < Array[LeftNode]):
                # 从右侧找到比basic小的数，与左侧比较大的数值交换，并且重新从左侧找比basic大的数
                M += 2
                Array[LeftNode + i], Array[LeftNode + j] = Exchange(Array[LeftNode + i], Array[LeftNode + j]) # 数值交换位置
                State = 0
            else:
                j -= 1
        C += 1  # 下一次循环无论是否执行，都要比较i和j

    # 将basic的值与左半边最后一个元素交换，即以basic为分界线，左侧都比basic小，右侧大于等于basic
    M +=2
    Array[LeftNode + j], Array[LeftNode] = Exchange(Array[LeftNode + j], Array[LeftNode])

    # 使用循环中的i和j为左右两部分计数，如果比basic小或大的部分多余1个元素，则迭代调用本函数为其排序
    C += 2 # 分析左右区间的长度
    if(i - 1 > 1):
        M, C, Array = Quick(Array, LeftNode, LeftNode + i - 2, M, C)
    if(Length - 1 - j > 1):
        M, C, Array = Quick(Array, LeftNode + i, RightNode, M, C)

    return M, C, Array

def QuickSort(Array):
    M = 0
    C = 0
    M, C, Result = Quick(Array, 0, len(Array) - 1, M, C)
    return M, C, Result