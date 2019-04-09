import random
import time
import numpy as np
from lib.quicksort import *
from lib.mergesort import *
from lib.shellsort import *
from lib.heapsort import *
from lib.display import *



"""
0: QuickSort,快速排序
1: ShellSort,希尔排序
2: MergeSort,归并排序
3: HeapSort,堆排序
"""
ArrayLength = []
TargetArray = []
MoveTimes = [[], [], [], []] # 四个数组分别记录四种算法的移动次数
CompareTimes = [[], [], [], []] # 四个数组分别记录四种算法的比较次数
TestRound = 10

for i in range(16):
    ArrayLength.append(2 ** (i+2))

def TestOnce(Num, Round):

    global CompareTimes, MoveTimes
    M0, M1, M2, M3, C0, C1, C2, C3 = 0, 0, 0, 0, 0, 0, 0, 0

    for i in range(Round):
        print('Round ' + str(i + 1))
        # 每一轮生成一个新的数组
        TargetArray = []
        for j in range(Num):
            TargetArray.append(random.randint(0, 500000))
        # 分别使用四种算法对数组排序，得到移动次数和比较次数，多次的累加起来
        M, C, Result = QuickSort(TargetArray.copy())
        M0 += M
        C0 += C
        M, C, Result = ShellSort(TargetArray.copy())
        M1 += M
        C1 += C
        M, C, Result = MergeSort(TargetArray.copy())
        M2 += M
        C2 += C
        M, C, Result = HeapSort(TargetArray.copy())
        M3 += M
        C3 += C

    # 将多次运行的平均次数计入数组
    MoveTimes[0].append(M0 / Round)
    MoveTimes[1].append(M1 / Round)
    MoveTimes[2].append(M2 / Round)
    MoveTimes[3].append(M3 / Round)
    CompareTimes[0].append(C0 / Round)
    CompareTimes[1].append(C1 / Round)
    CompareTimes[2].append(C2 / Round)
    CompareTimes[3].append(C3 / Round)

for i in range(len(ArrayLength)):
    print('Testing ' + str(ArrayLength[i]) + ' length...')
    StartTime = time.time()
    TestOnce(ArrayLength[i], TestRound)
    print('Finished in ' + str(time.time() - StartTime) + ' seconds.')
    print('----------------------------------------')

TotalTimes = np.array(CompareTimes) + np.array(MoveTimes)# 得到总的操作次数



PrintResult(ArrayLength, CompareTimes, MoveTimes, TotalTimes)
DisplayResult(ArrayLength, CompareTimes, MoveTimes, TotalTimes)