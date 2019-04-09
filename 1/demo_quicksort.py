from lib.display import Show
import random


# 自定义目标数组
Array = [6,-3,8,24,4,2,9,11,6,5,-11,0,-13,15,-1,3,7,1]

ArrLen = len(Array)
Step = 0 # 数字移动的步数
Colors = [] # 定义每个元素对应的颜色

def Exchange(a, b):
    """
    交换两个元素的值
    """
    Temp = a
    a = b
    b = Temp
    return a, b

def QuickSort(Array, LeftNode, RightNode):
    """
    快速排序算法，循环迭代
    Array: 被排序的目标数组
    LightNode， RightNode: 数组被排序部分的左右端点的下标
    每次排序的基准basic为第一位，比basic大的数移到右侧，比basic小的数移到左侧
    """
    global Step
    Length = RightNode - LeftNode + 1 # 待排列的部分长度

    i = 1
    j = Length - 1
    State = 0 # 查找方向标志位

    while(i <= j):
        Show(Array, Colors, LeftNode, RightNode, i, j, 50) # 绘图显示
        if(State == 0): # 首先从左侧找比basic大的数
            if(Array[LeftNode + i] >= Array[LeftNode]):
                State = 1 # 找到比basic大的数，从右侧找比basic小的数
            else:
                i += 1
        else:
            if(Array[LeftNode + j] < Array[LeftNode]):
                # 从右侧找到比basic小的数，与左侧比较大的数值交换，并且重新从左侧找比basic大的数
                Array[LeftNode + i], Array[LeftNode + j] = Exchange(Array[LeftNode + i], Array[LeftNode + j]) # 数值交换位置
                Colors[LeftNode + i], Colors[LeftNode + j] = Exchange(Colors[LeftNode + i], Colors[LeftNode + j]) # 颜色随元素改变位置
                State = 0
                Show(Array, Colors, LeftNode, RightNode, i, j, 100) # 绘图显示
                Step += 1
                print("Step "+ str(Step) + " : " + str(Array))
            else:
                j -= 1

    # 将basic的值与左半边最后一个元素交换，即以basic为分界线，左侧都比basic小，右侧大于等于basic
    Array[LeftNode + j], Array[LeftNode] = Exchange(Array[LeftNode + j], Array[LeftNode])
    Colors[LeftNode], Colors[LeftNode + j] = Exchange(Colors[LeftNode], Colors[LeftNode + j])
    Show(Array, Colors, LeftNode, RightNode, i, j, 100) # 绘图显示

    Step += 1
    print("Step " + str(Step) + " : " + str(Array))

    # 使用循环中的i和j为左右两部分计数，如果比basic小或大的部分多余1个元素，则迭代调用本函数为其排序
    if(i - 1 > 1):
        Array = QuickSort(Array, LeftNode, LeftNode + i - 2)
    if(Length - 1 - j > 1):
        Array = QuickSort(Array, LeftNode + i, RightNode)

    return Array

if __name__ == '__main__':
    for num in range(ArrLen): #为每个元素随机生成一个对应的颜色
        Colors.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    Show(Array, Colors, 0, ArrLen-1, 0, 0, 1000) # 展示1秒原始数组
    print(QuickSort(Array, 0, ArrLen-1)) # 排序并打印结果
    Show(Array, Colors, 0, ArrLen-1, 0, 0, 5000) # 展示5秒排序结果