import csv
import json

def json_to_csv(json_file, csv_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        
        # 写入表头
        writer.writerow(data[0].keys())

        # 写入数据
        for item in data:
            writer.writerow(item.values())

    print("转换完成！")

# 示例使用：将example.json文件转换为example.csv文件
json_to_csv('example.json', 'example.csv')