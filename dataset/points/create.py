import pandas as pd
import numpy as np

# 读取Premier League.csv文件
premier_league_df = pd.read_csv("Premier League.csv")

# 获取Season为2021的数据
filtered_df = premier_league_df[premier_league_df['Season'] == 2021]

# 获取不重复的HomeTeam值
home_teams = filtered_df['HomeTeam'].unique()

# 创建一个空的DataFrame来存储要写入的数据
points_df = pd.DataFrame(columns=['Date'] + list(home_teams))
points_df.loc[0, 'Date'] = 'Date'

# 获取不重复的Date值
dates = filtered_df['Date'].unique()

# 将不重复的Date值转换为numpy数组
dates = np.array(dates)

# 调整日期数组的形状以匹配points_df的维度
dates = dates.reshape((-1, 1))

# 将不重复的Date值写入points_df的第一列
for i in range(len(dates)):
    points_df.at[i+1, 'Date'] = dates[i][0]

# 将不重复的HomeTeam值写入points_df的第一行从第二列起
for i, home_team in enumerate(home_teams):
    points_df.iloc[0, i+1] = home_team



# 将points_df写入points21.csv文件
points_df.to_csv('points21.csv', index=False, header=False)
