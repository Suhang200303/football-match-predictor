import csv
import pandas as pd

# 读取CSV文件
df = pd.read_csv('Premier League.csv')
all_data = []
# 初始化主队和客队的统计指标字典
home_team_statistics = {
    'points': 0,
    'current_points': 0,
    'goal': 0,
    'loss': 0,
    'shot': 0,
    'shot_on_target': 0,
    'redcard': 0
}

away_team_statistics = {
    'points': 0,
    'current_points': 0,
    'goal': 0,
    'loss': 0,
    'shot': 0,
    'shot_on_target': 0,
    'redcard': 0
}

history_home_team_statistics = {
    'points': 0,
    'goal': 0,
    'shot': 0,
    'shot_on_target': 0,
    'redcard': 0
}

history_away_team_statistics = {
    'points': 0,
    'goal': 0,
    'shot': 0,
    'shot_on_target': 0,
    'redcard': 0
}

# 遍历每一行
for index, row in df.iterrows():
    df['Date'] = pd.to_datetime(df['Date'])
    season = row['Season']
    home_team = row['HomeTeam']
    away_team = row['AwayTeam']
    date = row['Date']
    

    if season:
        # 找到该主队参与的比赛
        home_matches_as_home = df[(df['HomeTeam'] == home_team) & (df['Date'] <= date)].tail(10)
        total_home_matches_as_home = df[(df['HomeTeam'] == home_team) & (df['Season'] == season) & (df['Date'] <= date)]
        total_home_matches_as_away = df[(df['AwayTeam'] == home_team) & (df['Season'] == season) & (df['Date'] <= date)]

        # 找到该主队作为客队参与的比赛
        home_matches_as_away = df[(df['AwayTeam'] == home_team) & (df['Date'] < date)].tail(10)

        # 重置主队的统计指标
        for key in home_team_statistics:
            home_team_statistics[key] = 0
        
        for _, match in total_home_matches_as_home.iterrows():
            ftr = match['FTR']
            if ftr == 'H':
                home_team_statistics['current_points'] += 3
            elif ftr == 'A':
                home_team_statistics['current_points'] += 0  
            elif ftr == 'D':
                home_team_statistics['current_points'] += 1
                
        for _, match in total_home_matches_as_away.iterrows():
            ftr = match['FTR']
            if ftr == 'H':
                home_team_statistics['current_points'] += 0
            elif ftr == 'A':
                home_team_statistics['current_points'] += 3  
            elif ftr == 'D':
                home_team_statistics['current_points'] += 1
        
        # 针对每个找到的比赛更新主队的统计指标
        for _, match in home_matches_as_home.iterrows():
            ftr = match['FTR']
            fthg = match['FTHG']
            ftag = match['FTAG']
            hs = match['HS']
            as_ = match['AS']
            hst = match['HST']
            ast = match['AST']
            hr = match['HR']
            ar = match['AR']

            if ftr == 'H':
                home_team_statistics['points'] += 3
            elif ftr == 'A':
                home_team_statistics['points'] += 0  # 这里代表主场的主队输球，仍然加0分
            elif ftr == 'D':
                home_team_statistics['points'] += 1

            home_team_statistics['goal'] += fthg
            home_team_statistics['loss'] += ftag
            home_team_statistics['shot'] += hs
            home_team_statistics['shot_on_target'] += hst
            home_team_statistics['redcard'] += hr


        # 针对每个找到的比赛更新主队的统计指标（作为客队时）
        for _, match in home_matches_as_away.iterrows():
            ftr = match['FTR']
            fthg = match['FTHG']
            ftag = match['FTAG']
            hs = match['HS']
            as_ = match['AS']
            hst = match['HST']
            ast = match['AST']
            hr = match['HR']
            ar = match['AR']

            if ftr == 'H':
                home_team_statistics['points'] += 0  # 这里代表客场的主队输球，仍然加0分
            elif ftr == 'A':
                home_team_statistics['points'] += 3
            elif ftr == 'D':
                home_team_statistics['points'] += 1

            home_team_statistics['goal'] += ftag
            home_team_statistics['loss'] += fthg
            home_team_statistics['shot'] += as_
            home_team_statistics['shot_on_target'] += ast
            home_team_statistics['redcard'] += ar

        # 找到该客队参与的比赛
        away_matches_as_away = df[(df['AwayTeam'] == away_team) & (df['Date'] <= date)].tail(10)

        # 找到该客队作为主队参与的比赛
        away_matches_as_home = df[(df['HomeTeam'] == away_team) & (df['Date'] <= date)].tail(10)
        
        total_away_matches_as_home = df[(df['HomeTeam'] == away_team) & (df['Season'] == season) & (df['Date'] <= date)]
        total_away_matches_as_away = df[(df['AwayTeam'] == away_team) & (df['Season'] == season) & (df['Date'] <= date)]

        # 重置客队的统计指标
        for key in away_team_statistics:
            away_team_statistics[key] = 0
        
        for _, match in total_away_matches_as_home.iterrows():
            ftr = match['FTR']
            if ftr == 'H':
                away_team_statistics['current_points'] += 3
            elif ftr == 'A':
                away_team_statistics['current_points'] += 0  
            elif ftr == 'D':
                away_team_statistics['current_points'] += 1
                
        for _, match in total_away_matches_as_away.iterrows():
            ftr = match['FTR']
            if ftr == 'H':
                away_team_statistics['current_points'] += 0
            elif ftr == 'A':
                away_team_statistics['current_points'] += 3  
            elif ftr == 'D':
                away_team_statistics['current_points'] += 1

        # 针对每个找到的比赛更新客队的统计指标
        for _, match in away_matches_as_away.iterrows():
            ftr = match['FTR']
            fthg = match['FTHG']
            ftag = match['FTAG']
            hs = match['HS']
            as_ = match['AS']
            hst = match['HST']
            ast = match['AST']
            hr = match['HR']
            ar = match['AR']

            if ftr == 'H':
                away_team_statistics['points'] += 0  # 这里代表客场的客队输球，仍然加0分
            elif ftr == 'A':
                away_team_statistics['points'] += 3
            elif ftr == 'D':
                away_team_statistics['points'] += 1

            away_team_statistics['goal'] += ftag
            away_team_statistics['loss'] += fthg
            away_team_statistics['shot'] += as_
            away_team_statistics['shot_on_target'] += ast
            away_team_statistics['redcard'] += ar
            

        # 针对每个找到的比赛更新客队的统计指标（作为主队时）
        for _, match in away_matches_as_home.iterrows():
            ftr = match['FTR']
            fthg = match['FTHG']
            ftag = match['FTAG']
            hs = match['HS']
            as_ = match['AS']
            hst = match['HST']
            ast = match['AST']
            hr = match['HR']
            ar = match['AR']

            if ftr == 'H':
                away_team_statistics['points'] += 3
            elif ftr == 'A':
                away_team_statistics['points'] += 0  # 这里代表主场的客队输球，仍然加0分
            elif ftr == 'D':
                away_team_statistics['points'] += 1

            away_team_statistics['goal'] += fthg
            away_team_statistics['loss'] += ftag
            away_team_statistics['shot'] += hs
            away_team_statistics['shot_on_target'] += hst
            away_team_statistics['redcard'] += hr
            
        # 输出主队的统计指标值
        print(f"Season: {season}")
        print(f"Date: {date}")
        print(f"Home Team: {home_team}")
        for key, value in home_team_statistics.items():
            print(f"{key}: {value}")
        print()

        # 输出客队的统计指标值
        print(f"Season: {season}")
        print(f"Date: {date}")
        print(f"Away Team: {away_team}")
        for key, value in away_team_statistics.items():
            print(f"{key}: {value}")
        print()
        
        history_matches_normal = df[((df['HomeTeam'] == home_team) & (df['AwayTeam'] == away_team)) & (df['Date'] <= date)].tail(5)
        history_matches_abnormal = df[((df['HomeTeam'] == away_team) & (df['AwayTeam'] == home_team)) & (df['Date'] <= date)].tail(5)
        for key in history_away_team_statistics:
            history_away_team_statistics[key] = 0
        for key in history_home_team_statistics:
            history_home_team_statistics[key] = 0
        
        for _, match in history_matches_normal.iterrows():
            ftr = match['FTR']
            fthg = match['FTHG']
            ftag = match['FTAG']
            hs = match['HS']
            as_ = match['AS']
            hst = match['HST']
            ast = match['AST']
            hr = match['HR']
            ar = match['AR']

            if ftr == 'H':
                history_home_team_statistics['points'] += 3
                history_away_team_statistics['points'] += 0  
            elif ftr == 'A':
                history_home_team_statistics['points'] += 0
                history_away_team_statistics['points'] += 3
            elif ftr == 'D':
                history_home_team_statistics['points'] += 1
                history_away_team_statistics['points'] += 1

            history_home_team_statistics['goal'] += fthg
            history_away_team_statistics['goal'] += ftag
            history_home_team_statistics['shot'] += hs
            history_away_team_statistics['shot'] += as_
            history_home_team_statistics['shot_on_target'] += hst
            history_away_team_statistics['shot_on_target'] += ast
            history_home_team_statistics['redcard'] += hr
            history_away_team_statistics['redcard'] += ar

        for _, match in history_matches_abnormal.iterrows():
            ftr = match['FTR']
            fthg = match['FTHG']
            ftag = match['FTAG']
            hs = match['HS']
            as_ = match['AS']
            hst = match['HST']
            ast = match['AST']
            hr = match['HR']
            ar = match['AR']

            if ftr == 'H':
                history_away_team_statistics['points'] += 3
                history_home_team_statistics['points'] += 0  
            elif ftr == 'A':
                history_away_team_statistics['points'] += 0
                history_home_team_statistics['points'] += 3
            elif ftr == 'D':
                history_away_team_statistics['points'] += 1
                history_home_team_statistics['points'] += 1

            history_away_team_statistics['goal'] += fthg
            history_home_team_statistics['goal'] += ftag
            history_away_team_statistics['shot'] += hs
            history_home_team_statistics['shot'] += as_
            history_away_team_statistics['shot_on_target'] += hst
            history_home_team_statistics['shot_on_target'] += ast
            history_away_team_statistics['redcard'] += hr
            history_home_team_statistics['redcard'] += ar
       
            
        '''# 输出主队的统计指标值
        prin(f"Home Team: {home_team}")
        for key, value in history_home_team_statistics.items():
            print(f"Season: {season}")
        print(f"Date: {date}")
        printt(f"{key}: {value}")
        print()

        # 输出客队的统计指标值
        print(f"Season: {season}")
        print(f"Date: {date}")
        print(f"Away Team: {away_team}")
        for key, value in history_away_team_statistics.items():
            print(f"{key}: {value}")
        print()'''

        # 创建一个空列表data
        new_row = {
            'home_team_points': home_team_statistics['points'],
            'home_team_current_points': home_team_statistics['current_points'],
            'home_team_goal': home_team_statistics['goal'],
            'home_team_loss': home_team_statistics['loss'],
            'home_team_shot': home_team_statistics['shot'],
            'home_team_shot_on_target': home_team_statistics['shot_on_target'],
            'home_team_redcard': home_team_statistics['redcard'],
            'away_team_points': away_team_statistics['points'],
            'away_team_current_points': away_team_statistics['current_points'],
            'away_team_goal': away_team_statistics['goal'],
            'away_team_loss': away_team_statistics['loss'],
            'away_team_shot': away_team_statistics['shot'],
            'away_team_shot_on_target': away_team_statistics['shot_on_target'],
            'away_team_redcard': away_team_statistics['redcard'],
            'history_home_team_points': history_home_team_statistics['points'],
            'history_home_team_goal': history_home_team_statistics['goal'],
            'history_home_team_shot': history_home_team_statistics['shot'],
            'history_home_team_shot_on_target': history_home_team_statistics['shot_on_target'],
            'history_home_team_redcard': history_home_team_statistics['redcard'],
            'history_away_team_points': history_away_team_statistics['points'],
            'history_away_team_goal': history_away_team_statistics['goal'],
            'history_away_team_shot': history_away_team_statistics['shot'],
            'history_away_team_shot_on_target': history_away_team_statistics['shot_on_target'],
            'history_away_team_redcard': history_away_team_statistics['redcard']
        }

        all_data.append(new_row)

# 将所有数据转换为 DataFrame 对象
processed_df = pd.DataFrame(all_data)

# 将处理后的数据保存到新的 CSV 文件中
processed_df.to_csv('processed_data.csv', index=False)
