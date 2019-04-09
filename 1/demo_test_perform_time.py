from lib.onlysort import *
from lib.display import *
import time
import random
from prettytable import PrettyTable

"""
0: QuickSort,快速排序
1: ShellSort,希尔排序
2: MergeSort,归并排序
3: HeapSort,堆排序
"""
ArrayLength = []
TargetArray = []
CostTime = [[], [], [], []]
TestRound = 10

for i in range(16):
    ArrayLength.append(2 ** (i+2))

def TestOnce(Num, Round):

    global CostTime
    T0, T1, T2, T3 = 0, 0, 0, 0

    for i in range(Round):
        print('Round ' + str(i + 1))
        TargetArray = []
        for j in range(Num):
            TargetArray.append(random.randint(0, 500000))
        Start_time = time.time()
        QuickSort(TargetArray.copy())
        End_time = time.time()
        T0 += End_time - Start_time

        Start_time = time.time()
        ShellSort(TargetArray.copy())
        End_time = time.time()
        T1 += End_time - Start_time

        Start_time = time.time()
        MergeSort(TargetArray.copy())
        End_time = time.time()
        T2 += End_time - Start_time

        Start_time = time.time()
        HeapSort(TargetArray.copy())
        End_time = time.time()
        T3 += End_time - Start_time

    CostTime[0].append(T0 / Round)
    CostTime[1].append(T1 / Round)
    CostTime[2].append(T2 / Round)
    CostTime[3].append(T3 / Round)

for i in range(len(ArrayLength)):
    print('Testing ' + str(ArrayLength[i]) + ' length...')
    StartTime = time.time()
    TestOnce(ArrayLength[i], TestRound)
    print('Finished in ' + str(time.time() - StartTime) + ' seconds.')
    print('----------------------------------------')

PrintCostTime(ArrayLength, CostTime)
DisplayCostTime(ArrayLength, CostTime)
