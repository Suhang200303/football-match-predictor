import pandas as pd
import json

# 读取CSV文件
df = pd.read_csv('points23.csv')

# 转换为JSON格式
result = {}
for index, row in df.iterrows():
    date = row['Date']
    teams = {}
    for column in df.columns[1:]:
        team = column
        score = row[column]
        teams[team] = score
    result[date] = teams

# 格式化为带缩进的JSON字符串
json_data = json.dumps(result, indent=4, ensure_ascii=False)

# 保存为JSON文件
with open('points23.json', 'w', encoding='utf-8') as file:
    file.write(json_data)

print("JSON文件保存成功！")