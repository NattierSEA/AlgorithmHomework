from lib.swap import *
from lib.tsp import *
from lib.display import*
import lib.parameter as pa
import time
from prettytable import PrettyTable
import xlwt
import numpy as np

TestTime = 5 # 每个点数的测试次数
TestNumber = []
GeneticVal = []
SwapVal = []
CostTime = []
CostTime2 = []


def TestOnce(Num):
    global N
    pa.N = Num
    pa.Nodes, pa.DistanceMatrix = BuildCities(pa.N)  # 得到初始点的坐标和距离矩阵
    time_start = time.time()
    pa.PathValue, pa.Path = Initial() # 得到排序好的第一代路径及其长度
    pa.CurrentBestPath, pa.global_Value = TSP()
    GenVal = pa.global_Value
    time_one_end = time.time()
    Best = 0
    while (Best == 0):
        Best = TwoSwap()
    time_end = time.time()
    # Show(pa.Nodes, pa.CurrentBestPath, pa.global_Value, str(pa.N)+' Nodes Result')
    SwVal = pa.global_Value
    return GenVal, SwVal, time_one_end - time_start, time_end - time_one_end

def TestPerformance(Num):
    GenVal = 0
    SwVal = 0
    OneStageTime = 0
    TwoStageTime = 0

    print("Testing " + str(Num) + " cities...")
    for i in range(TestTime):
        print('round '+ str(i+1))
        LenGen, LenSw, OneStageCostTime, TwoStageCostTime = TestOnce(Num)
        GenVal += LenGen
        SwVal += LenSw
        OneStageTime += OneStageCostTime
        TwoStageTime += TwoStageCostTime

    CostTime.append(OneStageTime / TestTime)
    CostTime2.append(TwoStageTime / TestTime)
    GeneticVal.append(GenVal / TestTime)
    SwapVal.append(SwVal / TestTime)
    print("Finished in " + str(round((OneStageTime + TwoStageTime), 2)) + " seconds.\n-----------------------------")


if __name__ == '__main__':

    for i in range(10, 31, 10):
        TestNumber.append(i)
        TestPerformance(i)
        TotalTime = np.array(CostTime) + np.array(CostTime2)
        DisplayResult(TestNumber, CostTime, CostTime2, TotalTime, GeneticVal, SwapVal, str(i))

