def Sort(Array, M, C):
    Len = len(Array)
    #不断递归调用自己一直到拆分成成单个元素的时候就返回这个元素，不再拆分了
    if Len == 1:
        return Array, M, C

    #取拆分的中间位置
    mid = Len // 2
    M += Len
    #拆分过后左右两侧子串
    left = Array[:mid]
    right = Array[mid:]

    #对拆分过后的左右再拆分 一直到只有一个元素为止
    #最后一次递归时候ll和lr都会接到一个元素的列表
    # 最后一次递归之前的ll和rl会接收到排好序的子序列
    ll, M, C = Sort(left, M, C)
    rl, M, C = Sort(right, M, C)

    # 我们对返回的两个拆分结果进行排序后合并再返回正确顺序的子列表
    # 这里我们调用拎一个函数帮助我们按顺序合并ll和lr
    result, M, C = Merge(ll, rl, M, C)
    return result, M, C

#这里接收两个列表
def Merge(left, right, M, C):
    # 从两个有顺序的列表里边依次取数据比较后放入result
    # 每次我们分别拿出两个列表中最小的数比较，把较小的放入result
    result = []
    C += 2
    while len(left)>0 and len(right)>0 :
        #为了保持稳定性，当遇到相等的时候优先把左侧的数放进结果列表，因为left本来也是大数列中比较靠左的
        C += 1
        M += 1
        if left[0] <= right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
        C += 2
    #while循环出来之后 说明其中一个数组没有数据了，我们把另一个数组添加到结果数组后面
    result += left
    result += right
    return result, M, C

def MergeSort(li):
    M = 0
    C = 0
    result, M, C = Sort(li, M, C)
    return M, C, result