import cv2
import matplotlib.pyplot as plt
import math
from prettytable import PrettyTable
import xlwt

# 将每一步的结果记录到视频中
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('./output/QuickHull.avi', fourcc, 2.0, (700,700))

def Show(Node, Edge):
    ShowImage = cv2.imread("./image/white.jpg")  # 读取背景，画面尺寸随之确定
    # 画出所有点
    for i in range(len(Node)):
        Start_x = Node[i][0] + 100
        Start_y = 600 - Node[i][1]
        ShowImage = cv2.rectangle(ShowImage, (Start_x, Start_y),
                                  (Start_x + 2, Start_y - 2),
                                  [255, 0, 0], -1)
        # ShowImage = cv2.putText(ShowImage, str(i), (Start_x, Start_y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 2)
        # ShowImage = cv2.putText(ShowImage, str(Node[i][0])+","+str(Node[i][1]), (Start_x, Start_y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 2)

    # 画出所有边
    for i in range(len(Edge)):
        Start_x = Node[Edge[i][0]][0] + 100
        Start_y = 600 - Node[Edge[i][0]][1]
        End_x = Node[Edge[i][1]][0] + 100
        End_y = 600 - Node[Edge[i][1]][1]
        cv2.line(ShowImage, (Start_x, Start_y), (End_x, End_y), (0, 0, 255), 2)

    cv2.imshow('ShowProcess', ShowImage)
    cv2.waitKey(1)
    cv2.imwrite("./output/result.jpg", ShowImage)
    out.write(ShowImage)

def ShowResult(nodenum, CostTime):
    nlogn = []
    for i in range(len(nodenum)):
        x = nodenum[i] * math.log(float(nodenum[i]), 2.0)
        nlogn.append(x / 5000)
    plt.plot(nodenum, CostTime, 'r+-', label='Cost Time')
    plt.plot(nodenum, nlogn, 'g', label='nlogn')
    plt.legend(loc='upper left')
    plt.title('Cost Time')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Cost Time(ms)')
    plt.savefig("./output/CostTime.png")
    plt.show()

def PrintResult(nodenum, CostTime):
    x = PrettyTable(["Length", "Time(ms)"])
    for i in range(len(nodenum)):
        x.add_row([nodenum[i], CostTime[i]])
    print(x)
    f = xlwt.Workbook()  # 创建工作簿
    sheet1 = f.add_sheet('Time', cell_overwrite_ok=True)
    sheet1.write(0, 0, "Length")
    sheet1.write(0, 1, "Average Time(ms)")
    for i in range(len(nodenum)):
        sheet1.write(i + 1, 0, nodenum[i])
        sheet1.write(i + 1, 1, CostTime[i])
    f.save('./output/Result.xls')
