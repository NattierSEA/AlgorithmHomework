from lib.quickhull import *
from lib.show import *


nodenum = []
TestRound = 10
Nodes = []
AverageCostTime = []

for i in range(16):
    nodenum.append(10 * 2 ** i)
print(nodenum)

def TestOnce(Num, Round):

    TotalTime = 0
    for i in range(Round):
        print('Round ' + str(i + 1))
        Nodes = []
        for i in range(Num):
            # 如果要显示，只能从0到500取值
            Nodes.append([random.randint(0, 10000), random.randint(0, 10000)])
        Edge, CostTime = QuickHull(Nodes)
        TotalTime += CostTime
        # Show(Nodes, Edge)
    AverageCostTime.append(TotalTime / Round * 1000)

for i in range(len(nodenum)):
    print('Testing ' + str(nodenum[i]) + ' Nodes')
    Start = time.time()
    TestOnce(nodenum[i], TestRound)
    print('Finished in ' + str(round((time.time() - Start) * 1000, 2)) + ' ms\n-----------------------------')

PrintResult(nodenum, AverageCostTime)
ShowResult(nodenum, AverageCostTime)
