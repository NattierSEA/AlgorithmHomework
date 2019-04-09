import cv2
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import xlwt

# 将每一步的结果记录到视频中
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('./output/TSP.avi', fourcc, 2.0, (700,700))

def Show(Nodes, Pack, global_Value, stage):
    ShowImage = cv2.imread("./image/white.jpg")  # 读取背景，画面尺寸随之确定
    # 画出所有点
    for i in range(len(Nodes)):
        Start_x = Nodes[i][0] + 100
        Start_y = 600 - Nodes[i][1]
        ShowImage = cv2.rectangle(ShowImage, (Start_x - 2, Start_y + 2),(Start_x + 2, Start_y - 2),[255, 0, 0], -1)

    # 画出所有边
    for i in range(len(Pack)-1):
        Start_x = Nodes[Pack[i]][0] + 100
        Start_y = 600 - Nodes[Pack[i]][1]
        End_x = Nodes[Pack[i+1]][0] + 100
        End_y = 600 - Nodes[Pack[i+1]][1]
        cv2.line(ShowImage, (Start_x, Start_y), (End_x, End_y), (0, 0, 255), 2)
    cv2.line(ShowImage, (Nodes[Pack[len(Pack)-1]][0] + 100, 600 - Nodes[Pack[len(Pack)-1]][1]), (Nodes[0][0] + 100, 600 - Nodes[0][1]), (0, 0, 255), 2)
    cv2.line(ShowImage, (Nodes[Pack[0]][0] + 100, 600 - Nodes[Pack[0]][1]), (Nodes[0][0] + 100, 600 - Nodes[0][1]), (0, 0, 255), 2)

    ShowImage = cv2.putText(ShowImage, 'Stage : ' + stage, (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 2)
    ShowImage = cv2.putText(ShowImage, 'Total Length = '+ str(global_Value), (10, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 2)
    cv2.imshow('ShowProcess', ShowImage)
    cv2.waitKey(1)
    cv2.imwrite("./image/"+stage+".jpg", ShowImage)
    out.write(ShowImage)

def DisplayResult(TestNumber, CostTime, CostTime2, TotalTime, GeneticVal, SwapVal, Name):

    # 打印并保存成表格，需要使用prettytable、xlwt模块，可以pip安装，也可以注释掉
    x = PrettyTable(["Citie", "Average Time(s)", "Genetic Algorithm", "GA Cost Time", "2-Swap Algorithm", "2-Swap Cost Time"])
    for i in range(len(TestNumber)):
        x.add_row([TestNumber[i], CostTime[i] + CostTime2[i], GeneticVal[i], CostTime[i], SwapVal[i], CostTime2[i]])
    print(x)

    f = xlwt.Workbook()  # 创建工作簿
    sheet1 = f.add_sheet('sheet1', cell_overwrite_ok=True)
    sheet1.write(0, 0, "Citie")
    sheet1.write(0, 1, "Average Time(s)")
    sheet1.write(0, 2, "Genetic Algorithm")
    sheet1.write(0, 3, "GA Cost Time")
    sheet1.write(0, 4, "2-Swap Algorithm")
    sheet1.write(0, 5, "2-Swap Cost Time")
    for i in range(len(TestNumber)):
        sheet1.write(i + 1, 0, TestNumber[i])
        sheet1.write(i + 1, 1, CostTime[i] + CostTime2[i])
        sheet1.write(i + 1, 2, GeneticVal[i])
        sheet1.write(i + 1, 3, CostTime[i])
        sheet1.write(i + 1, 4, SwapVal[i])
        sheet1.write(i + 1, 5, CostTime2[i])
    f.save("./output/temp/"+ Name +"-Result.xls")
    f.save("./output/Result.xls")

    plt.ion()
    plt.plot(TestNumber, CostTime, 'g+-', label='Genetic Algorithm')
    plt.plot(TestNumber, CostTime2, 'b+-', label='2-Swap Algorithm')
    plt.plot(TestNumber, TotalTime, 'r+-', label='Total')
    plt.legend(loc= 'upper left')
    plt.title('CostTime')
    plt.xlabel('Number of Cities')
    plt.ylabel('Average Time')
    plt.savefig("./output/temp/"+ Name +"-CostTime.png")
    plt.savefig("./output/CostTime.png")
    plt.ioff()
    plt.pause(1)
    plt.close()
    plt.ion()
    plt.plot(TestNumber, GeneticVal, 'g+-', label='Genetic Algorithm')
    plt.plot(TestNumber, SwapVal, 'b+-', label='2-Swap Algorithm')
    plt.legend(loc= 'upper left')
    plt.title('ToTal Distance')
    plt.xlabel('Number of Cities')
    plt.ylabel('Average Distance')
    plt.savefig("./output/temp/"+ Name +"-ToTalDistance.png")
    plt.savefig("./output/ToTalDistance.png")
    plt.ioff()
    plt.pause(1)
    plt.close()