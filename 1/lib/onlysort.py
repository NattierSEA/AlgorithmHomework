

def Sift(Array, Low, High):
    i = Low      # 父节点
    j = 2 * i + 1   # 左子节点
    tmp = Array[i]   # 父节点值
    while j <= High:    # 子节点在节点中
        if j < High and Array[j] < Array[j + 1]:  # 有右子节点且右节点比父节点值大
            j += 1
        if tmp < Array[j]:
            Array[i] = Array[j]   # 将父节点替换成新的子节点的值
            i = j   # 变成新的父节点
            j = 2 * i + 1   # 新的子节点
        else:
            break
    Array[i] = tmp   # 将替换的父节点值赋给最终的父节点
    return Array


def HeapSort(Array):
    n = len(Array)
    # 创建堆
    for i in range(n//2-1, -1, -1):
        Array = Sift(Array, i, n-1)

    # 挨个出数
    for i in range(n-1, -1, -1):    # 从大到小
        Array[0], Array[i] = Array[i], Array[0]     # 将最后一个值与父节点交互位置
        Array = Sift(Array, 0, i-1)

    return Array

def MergeSort(Array):
    Len = len(Array)
    #不断递归调用自己一直到拆分成成单个元素的时候就返回这个元素，不再拆分了
    if Len == 1:
        return Array

    #取拆分的中间位置
    mid = Len // 2
    #拆分过后左右两侧子串
    left = Array[:mid]
    right = Array[mid:]

    #对拆分过后的左右再拆分 一直到只有一个元素为止
    #最后一次递归时候ll和lr都会接到一个元素的列表
    # 最后一次递归之前的ll和rl会接收到排好序的子序列
    ll = MergeSort(left)
    rl = MergeSort(right)

    # 我们对返回的两个拆分结果进行排序后合并再返回正确顺序的子列表
    # 这里我们调用拎一个函数帮助我们按顺序合并ll和lr
    result = Merge(ll, rl)
    return result

#这里接收两个列表
def Merge(left, right):
    # 从两个有顺序的列表里边依次取数据比较后放入result
    # 每次我们分别拿出两个列表中最小的数比较，把较小的放入result
    result = []
    while len(left)>0 and len(right)>0 :
        #为了保持稳定性，当遇到相等的时候优先把左侧的数放进结果列表，因为left本来也是大数列中比较靠左的
        if left[0] <= right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    #while循环出来之后 说明其中一个数组没有数据了，我们把另一个数组添加到结果数组后面
    result += left
    result += right
    return result


def Exchange(a, b):
    """
    交换两个元素的值
    """
    global M
    Temp = a
    a = b
    b = Temp
    return a, b

def Quick(Array, LeftNode, RightNode):
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

    while(i <= j):
        if(State == 0): # 首先从左侧找比basic大的数
            if(Array[LeftNode + i] >= Array[LeftNode]):
                State = 1 # 找到比basic大的数，从右侧找比basic小的数
            else:
                i += 1
        else:
            if(Array[LeftNode + j] < Array[LeftNode]):
                # 从右侧找到比basic小的数，与左侧比较大的数值交换，并且重新从左侧找比basic大的数
                Array[LeftNode + i], Array[LeftNode + j] = Exchange(Array[LeftNode + i], Array[LeftNode + j]) # 数值交换位置
                State = 0
            else:
                j -= 1

    # 将basic的值与左半边最后一个元素交换，即以basic为分界线，左侧都比basic小，右侧大于等于basic
    Array[LeftNode + j], Array[LeftNode] = Exchange(Array[LeftNode + j], Array[LeftNode])

    # 使用循环中的i和j为左右两部分计数，如果比basic小或大的部分多余1个元素，则迭代调用本函数为其排序
    if(i - 1 > 1):
        Array = Quick(Array, LeftNode, LeftNode + i - 2)
    if(Length - 1 - j > 1):
        Array = Quick(Array, LeftNode + i, RightNode)

    return Array

def QuickSort(Array):
    Result = Quick(Array, 0, len(Array) - 1)
    return  Result

def ShellInsetSort(Array, LenArray, dk):  # 直接插入排序

    for i in range(dk, LenArray):  # 从下标为dk的数进行插入排序
        position = i
        current_val = Array[position]  # 要插入的数

        index = i
        j = int(index / dk)  # index与dk的商
        index = index - j * dk

        # position>index,要插入的数的下标必须得大于第一个下标
        while position > index and current_val < Array[position-dk]:
            Array[position] = Array[position-dk]  # 往后移动
            position = position-dk
        else:
            Array[position] = current_val

    return Array



def ShellSort(Array):  # 希尔排序
    LenArray = len(Array)
    dk = int(LenArray/2)  # 增量
    while(dk >= 1):
        Array = ShellInsetSort(Array, LenArray, dk)
        dk = int(dk/2)
    return Array