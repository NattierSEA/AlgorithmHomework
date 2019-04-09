def ShellInsetSort(Array, LenArray, dk, M, C):  # 直接插入排序

    for i in range(dk, LenArray):  # 从下标为dk的数进行插入排序
        position = i
        current_val = Array[position]  # 要插入的数

        index = i
        j = int(index / dk)  # index与dk的商
        index = index - j * dk

        # position>index,要插入的数的下标必须得大于第一个下标
        C += 2
        C += 2
        while position > index and current_val < Array[position-dk]:
            M += 1
            Array[position] = Array[position-dk]  # 往后移动
            position = position-dk
            C += 2
        else:
            M += 1
            Array[position] = current_val

    return M, C, Array



def ShellSort(Array):  # 希尔排序
    M = 0
    C = 0
    LenArray = len(Array)
    dk = int(LenArray/2)  # 增量
    C += 1
    while(dk >= 1):
        M, C, Array = ShellInsetSort(Array, LenArray, dk, M, C)
        dk = int(dk/2)
        C += 1
    return M, C, Array
