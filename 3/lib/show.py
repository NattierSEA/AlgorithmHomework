import cv2
# 将每一步的结果记录到视频中
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('./image/TSP.avi', fourcc, 2.0, (700,700))

def Show(Nodes, Pack, global_Value, stage):
    ShowImage = cv2.imread("./image/white.jpg")  # 读取背景，画面尺寸随之确定
    # 画出所有点
    for i in range(len(Nodes)):
        Start_x = Nodes[i][0] + 100
        Start_y = 600 - Nodes[i][1]
        ShowImage = cv2.rectangle(ShowImage, (Start_x - 2, Start_y + 2),
                                  (Start_x + 2, Start_y - 2),
                                  [255, 0, 0], -1)
        ShowImage = cv2.putText(ShowImage, str(i), (Start_x, Start_y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0),
                                2)

    # 画出所有边
    for i in range(len(Pack)-1):
        Start_x = Nodes[Pack[i][0]][0] + 100
        Start_y = 600 - Nodes[Pack[i][0]][1]
        End_x = Nodes[Pack[i][1]][0] + 100
        End_y = 600 - Nodes[Pack[i][1]][1]
        cv2.line(ShowImage, (Start_x, Start_y), (End_x, End_y), (0, 0, 255), 2)
    # cv2.line(ShowImage, (Nodes[Pack[len(Pack)-1][0]][0] + 100, 600 - Nodes[Pack[len(Pack)-1][0]][1]), (Nodes[0][0] + 100, 600 - Nodes[0][1]), (0, 0, 255), 2)
    # cv2.line(ShowImage, (Nodes[Pack[0][0]][0] + 100, 600 - Nodes[Pack[0][0]][1]), (Nodes[0][0] + 100, 600 - Nodes[0][1]), (0, 0, 255), 2)

    ShowImage = cv2.putText(ShowImage, 'Stage : ' + stage, (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 2)
    ShowImage = cv2.putText(ShowImage, 'Total Length = '+ str(global_Value), (10, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 2)
    cv2.imshow('ShowProcess', ShowImage)
    cv2.waitKey(100)
    cv2.imwrite("./image/"+stage+"result.jpg", ShowImage)
    out.write(ShowImage)