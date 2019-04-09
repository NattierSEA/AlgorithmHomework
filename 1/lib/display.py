import cv2
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import xlwt

# 将每一步的结果记录到视频中
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('./output/QuickSort.avi', fourcc, 10.0, (1024,768))

def FoundMax(Array):
    """
    找到数组中的最大值
    """
    Max = 0
    for i in range(len(Array)):
        if(abs(Array[i]) > Max):
            Max = abs(Array[i])
    return Max

def Show(Array, Colors, LeftNode, RightNode, i, j, Delayms):
    """
    绘制一幅图像，显示并记录到视频中
    Array: 被绘制的数组
    Colors: 记录颜色的数组
    LeftNode, RightNode: 当前排序区间的左右端点
    i, j: 排序中的指针位置
    Delayms: 每张图像展示时间
    """
    Length = len(Array)
    Width = int(1024/Length) # 根据数组长度，确定每个柱形的位置和宽度
    Maxabs = FoundMax(Array) # 找到数组中最大值，后面根据与最大值的比例确定每个柱形高度
    High = 300/Maxabs # 最高300像素，其他值乘以该系数确定高度
    ShowImage = cv2.imread("./image/white.jpg") # 读取背景，画面尺寸随之确定

    # 绘制柱形和数字
    for k in range(Length):
        Start_x = k * Width # 每个柱形横坐标的起始参考位置
        ShowImage = cv2.rectangle(ShowImage, (Start_x + int(Width * 0.2), int(310 - High * Array[k])), (Start_x + int(Width * 0.8), 310),
                                  Colors[k], -1)
        ShowImage = cv2.putText(ShowImage, str(Array[k]), (Start_x + int(Width * 0.2), 700), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                1, (0, 0, 0), 2)

    # 绘制参与排序区间的矩形框
    ShowImage = cv2.rectangle(ShowImage, (LeftNode * Width, 5), ((RightNode+1) * Width, 615),(0, 0, 255), 3)
    # 绘制basic、i和j三个下标
    ShowImage = cv2.rectangle(ShowImage, ((LeftNode + i) * Width + int(Width * 0.2), 620), ((LeftNode + i) * Width + int(Width * 0.8), 670), (255, 0, 0) , -1)
    ShowImage = cv2.putText(ShowImage, "i", ((LeftNode + i) * Width + int(Width * 0.4), 650), cv2.FONT_HERSHEY_COMPLEX_SMALL,1, (0, 0, 0), 2)
    ShowImage = cv2.rectangle(ShowImage, ((LeftNode + j) * Width + int(Width * 0.2), 620), ((LeftNode + j) * Width + int(Width * 0.8), 670),(0, 255, 0), -1)
    ShowImage = cv2.putText(ShowImage, "j", ((LeftNode + j) * Width + int(Width * 0.4), 650), cv2.FONT_HERSHEY_COMPLEX_SMALL,1, (0, 0, 0), 2)
    ShowImage = cv2.rectangle(ShowImage, (LeftNode * Width + int(Width * 0.2), 620), (LeftNode * Width + int(Width * 0.8), 670),(0, 0, 0), -1)
    ShowImage = cv2.putText(ShowImage, "B", (LeftNode * Width + int(Width * 0.4), 650), cv2.FONT_HERSHEY_COMPLEX_SMALL,1, (255, 255, 255), 2)

    # 展示生成的图像，并记录到视频中
    cv2.imshow('ShowProcess', ShowImage)
    out.write(ShowImage)
    cv2.waitKey(Delayms)

def DisplayResult(ArrayLength, CompareTimes, MoveTimes, TotalTimes):
    plt.ion()
    plt.plot(ArrayLength, CompareTimes[0], 'r+-', label='Quick Sort')
    plt.plot(ArrayLength, CompareTimes[1], 'g+-', label='Shell Sort')
    plt.plot(ArrayLength, CompareTimes[2], 'b+-', label='Merge Sort')
    plt.plot(ArrayLength, CompareTimes[3], 'y+-', label='Heap Sort')
    plt.legend(loc= 'upper left')
    plt.title('Compare Times')
    plt.xlabel('Number of Compare Times')
    plt.ylabel('Average Time')
    plt.savefig("./output/CompareTimes.png")
    plt.ioff()
    plt.pause(1)
    plt.close()
    plt.ion()
    plt.plot(ArrayLength, MoveTimes[0], 'r+-', label='Quick Sort')
    plt.plot(ArrayLength, MoveTimes[1], 'g+-', label='Shell Sort')
    plt.plot(ArrayLength, MoveTimes[2], 'b+-', label='Merge Sort')
    plt.plot(ArrayLength, MoveTimes[3], 'y+-', label='Heap Sort')
    plt.legend(loc='upper left')
    plt.title('Move Times')
    plt.xlabel('Number of Move Times')
    plt.ylabel('Average Time')
    plt.savefig("./output/MoveTimes.png")
    plt.ioff()
    plt.pause(1)
    plt.close()
    plt.ion()
    plt.plot(ArrayLength, TotalTimes[0], 'r+-', label='Quick Sort')
    plt.plot(ArrayLength, TotalTimes[1], 'g+-', label='Shell Sort')
    plt.plot(ArrayLength, TotalTimes[2], 'b+-', label='Merge Sort')
    plt.plot(ArrayLength, TotalTimes[3], 'y+-', label='Heap Sort')
    plt.legend(loc='upper left')
    plt.title('Total Times')
    plt.xlabel('Number of Total Times')
    plt.ylabel('Average Time')
    plt.savefig("./output/TotalTimes.png")
    plt.ioff()
    plt.pause(1)
    plt.close()

    ax1 = plt.subplot(1, 3, 1)
    ax2 = plt.subplot(1, 3, 2)
    ax3 = plt.subplot(1, 3, 3)
    plt.sca(ax1)
    plt.plot(ArrayLength, CompareTimes[0], 'r+-', label='Quick Sort')
    plt.plot(ArrayLength, CompareTimes[1], 'g+-', label='Shell Sort')
    plt.plot(ArrayLength, CompareTimes[2], 'b+-', label='Merge Sort')
    plt.plot(ArrayLength, CompareTimes[3], 'y+-', label='Heap Sort')
    plt.legend(loc='upper left')
    plt.title('Compare Times')
    plt.xlabel('Number of Compare Times')
    plt.ylabel('Average Time')
    plt.sca(ax2)
    plt.plot(ArrayLength, MoveTimes[0], 'r+-', label='Quick Sort')
    plt.plot(ArrayLength, MoveTimes[1], 'g+-', label='Shell Sort')
    plt.plot(ArrayLength, MoveTimes[2], 'b+-', label='Merge Sort')
    plt.plot(ArrayLength, MoveTimes[3], 'y+-', label='Heap Sort')
    plt.legend(loc='upper left')
    plt.title('Move Times')
    plt.xlabel('Number of Move Times')
    plt.ylabel('Average Time')
    plt.sca(ax3)
    plt.plot(ArrayLength, TotalTimes[0], 'r+-', label='Quick Sort')
    plt.plot(ArrayLength, TotalTimes[1], 'g+-', label='Shell Sort')
    plt.plot(ArrayLength, TotalTimes[2], 'b+-', label='Merge Sort')
    plt.plot(ArrayLength, TotalTimes[3], 'y+-', label='Heap Sort')
    plt.legend(loc='upper left')
    plt.title('Total Times')
    plt.xlabel('Number of Total Times')
    plt.ylabel('Average Time')
    plt.show()

def PrintResult(ArrayLength, CompareTimes, MoveTimes, TotalTimes):
    print("Compare Times")
    x = PrettyTable(["Length", "Quick Sort", "Shell Sort", "Merge Sort", "Heap Sort"])
    for i in range(len(ArrayLength)):
        x.add_row([ArrayLength[i], CompareTimes[0][i], CompareTimes[1][i], CompareTimes[2][i], CompareTimes[3][i]])
    print(x)
    print('----------------------------------------')
    print("Move Times")
    x = PrettyTable(["Length", "Quick Sort", "Shell Sort", "Merge Sort", "Heap Sort"])
    for i in range(len(ArrayLength)):
        x.add_row([ArrayLength[i], MoveTimes[0][i], MoveTimes[1][i], MoveTimes[2][i], MoveTimes[3][i]])
    print(x)
    print('----------------------------------------')
    print("Total Times")
    x = PrettyTable(["Length", "Quick Sort", "Shell Sort", "Merge Sort", "Heap Sort"])
    for i in range(len(ArrayLength)):
        x.add_row([ArrayLength[i], round(TotalTimes[0][i], 1), round(TotalTimes[1][i], 1), round(TotalTimes[2][i], 1),
                   round(TotalTimes[3][i], 1)])
    print(x)
    print('----------------------------------------')

    f = xlwt.Workbook()  # 创建工作簿
    sheet1 = f.add_sheet('CompareTimes', cell_overwrite_ok=True)
    sheet1.write(0, 0, "Length")
    sheet1.write(0, 1, "Quick Sort")
    sheet1.write(0, 2, "Shell Sort")
    sheet1.write(0, 3, "Merge Sort")
    sheet1.write(0, 4, "Heap Sort")
    for i in range(len(ArrayLength)):
        sheet1.write(i + 1, 0, ArrayLength[i])
        sheet1.write(i + 1, 1, CompareTimes[0][i])
        sheet1.write(i + 1, 2, CompareTimes[1][i])
        sheet1.write(i + 1, 3, CompareTimes[2][i])
        sheet1.write(i + 1, 4, CompareTimes[3][i])
    sheet2 = f.add_sheet('MoveTimes', cell_overwrite_ok=True)
    sheet2.write(0, 0, "Length")
    sheet2.write(0, 1, "Quick Sort")
    sheet2.write(0, 2, "Shell Sort")
    sheet2.write(0, 3, "Merge Sort")
    sheet2.write(0, 4, "Heap Sort")
    for i in range(len(ArrayLength)):
        sheet2.write(i + 1, 0, ArrayLength[i])
        sheet2.write(i + 1, 1, MoveTimes[0][i])
        sheet2.write(i + 1, 2, MoveTimes[1][i])
        sheet2.write(i + 1, 3, MoveTimes[2][i])
        sheet2.write(i + 1, 4, MoveTimes[3][i])
    sheet3 = f.add_sheet('TotalTimes', cell_overwrite_ok=True)
    sheet3.write(0, 0, "Length")
    sheet3.write(0, 1, "Quick Sort")
    sheet3.write(0, 2, "Shell Sort")
    sheet3.write(0, 3, "Merge Sort")
    sheet3.write(0, 4, "Heap Sort")
    for i in range(len(ArrayLength)):
        sheet3.write(i + 1, 0, ArrayLength[i])
        sheet3.write(i + 1, 1, TotalTimes[0][i])
        sheet3.write(i + 1, 2, TotalTimes[1][i])
        sheet3.write(i + 1, 3, TotalTimes[2][i])
        sheet3.write(i + 1, 4, TotalTimes[3][i])
    f.save('./output/TestResult.xls')

def DisplayCostTime(ArrayLength, CostTime):
    plt.plot(ArrayLength, CostTime[0], 'r+-', label='Quick Sort')
    plt.plot(ArrayLength, CostTime[1], 'g+-', label='Shell Sort')
    plt.plot(ArrayLength, CostTime[2], 'b+-', label='Merge Sort')
    plt.plot(ArrayLength, CostTime[3], 'y+-', label='Heap Sort')
    plt.legend(loc= 'upper left')
    plt.title('CostTime')
    plt.xlabel('Number of Cities')
    plt.ylabel('Average Time')
    plt.savefig("./output/CostTime.png")
    plt.show()

def PrintCostTime(ArrayLength, CostTime):
    x = PrettyTable(["Length", "Quick Sort", "Shell Sort", "Merge Sort", "Heap Sort"])
    for i in range(len(ArrayLength)):
        x.add_row([ArrayLength[i], CostTime[0][i] * 1000, CostTime[1][i] * 1000, CostTime[2][i] * 1000,
                   CostTime[3][i] * 1000])
    print(x)
    f = xlwt.Workbook()  # 创建工作簿
    sheet1 = f.add_sheet('CostTime', cell_overwrite_ok=True)
    sheet1.write(0, 0, "Length")
    sheet1.write(0, 1, "Quick Sort")
    sheet1.write(0, 2, "Shell Sort")
    sheet1.write(0, 3, "Merge Sort")
    sheet1.write(0, 4, "Heap Sort")
    for i in range(len(ArrayLength)):
        sheet1.write(i + 1, 0, ArrayLength[i])
        sheet1.write(i + 1, 1, CostTime[0][i])
        sheet1.write(i + 1, 2, CostTime[1][i])
        sheet1.write(i + 1, 3, CostTime[2][i])
        sheet1.write(i + 1, 4, CostTime[3][i])
    f.save('./output/CostTime.xls')