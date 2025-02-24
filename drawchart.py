import numpy as np
import matplotlib.pyplot as plt
import tempfile
import csv

def draw_bar_chart():
    data = []

    with open('soccer/data/refer.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            data.append(row)

    labels = [row[0] for row in data]
    values = [float(row[1]) for row in data]

    x = np.arange(len(labels))

    plt.figure(figsize=(12,6))

    plt.bar(x, values)
    plt.xlabel('referee name')
    plt.ylabel('referee involved periods')
    plt.title('data imply')
    plt.xticks(x, labels, rotation='vertical')
    plt.tight_layout()

    # 生成临时图像文件

    # plt.show()

def draw_y_bar_chart():
    data = []

    with open('soccer/data/refer.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            if float(row[1]) > 10:  # 添加条件判断筛选第二列大于10的数据
                data.append(row)

    # 将数据按照第二列数值进行降序排序
    sorted_data = sorted(data, key=lambda x: float(x[6]), reverse=True)

    labels = [row[0] for row in sorted_data]
    values = [float(row[6]) for row in sorted_data]

    y = np.arange(len(labels))

    plt.figure(figsize=(12, 15))

    # 修改柱的颜色
    color = ['red']  # 自定义颜色列表
    plt.barh(y, values, color=color)  # 使用plt.barh绘制水平条形图，并指定颜色参数
    plt.ylabel('referee name')
    plt.xlabel('referee given_card and score')
    plt.title('data imply')
    plt.yticks(y, labels)
    plt.tight_layout()

    # 生成临时图像文件
    # temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    # plt.savefig(temp_file.name)
    # plt.close()