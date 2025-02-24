import pandas as pd

# 读取CSV文件
premier_league_df = pd.read_csv('Premier League.csv')
points_df = pd.read_csv('points03.csv')

# 筛选出Season为0303的数据
filtered_df = premier_league_df[premier_league_df['Season'] == 2003]

# 初始化第二行及之后的第二列及之后的单元格为0
points_df.iloc[1:len(points_df), 1:len(points_df.columns)] = 0

# 遍历筛选后的DataFrame的每一行
for index, row in filtered_df.iterrows():
    date = row['Date']
    ftr = row['FTR']
    home_team = row['HomeTeam']
    away_team = row['AwayTeam']

    # 根据条件更新points.csv中的值
    if date in points_df['Date'].values:
        # 获取对应日期的行索引
        date_index = points_df[points_df['Date'] == date].index[0]

        if ftr == 'H':
            # 找到相同日期和HomeTeam的单元格，加3
            points_df.loc[date_index, home_team] += 3
        elif ftr == 'A':
            # 找到相同日期和AwayTeam的单元格，加3
            points_df.loc[date_index, away_team] += 3
        elif ftr == 'D':
            # 找到相同日期和HomeTeam的单元格，加1
            points_df.loc[date_index, home_team] += 1
            # 找到相同日期和AwayTeam的单元格，加1
            points_df.loc[date_index, away_team] += 1

# 遍历从第二行开始的每一行
for i in range(1, len(points_df)):
    # 遍历从第二列开始的每一列
    for j in range(1, len(points_df.columns)):
        # 获取当前单元格的值
        cell_value = points_df.iloc[i, j]
        # 获取同一列上一行单元格的值
        prev_cell_value = points_df.iloc[i-1, j]
        # 更新当前单元格的值为当前值加上同一列上一行的值
        points_df.iloc[i, j] += prev_cell_value

# 将修改后的DataFrame写回points03.csv文件
points_df.to_csv('points03.csv', index=False)
print('finished')
