import pandas as pd
import numpy as np
import random as rd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import warnings



def find_similar_players(Player_Name1, Percentage_of_player1, No_of_Similar_players):
    warnings.filterwarnings("ignore")
    data = pd.read_excel('soccer/data/masterdata.xlsx')

    # 从数据集中获取球员的位置信息
    position_column = data[data['Player'] == Player_Name1]['Position']
    if len(position_column) > 0:
        Position1 = position_column.iloc[0].split(',')[0]  # 提取第一个逗号前的位置
    else:
        raise ValueError("Invalid player name or player not found in dataset.")

    p = Percentage_of_player1 / 100

    def player_similarity(df, target1, p, position):
        target_player1 = df[df['Player'] == target1]
        target_position = target_player1['Categorical position']
        i = target_player1.index[0]

        df1 = df[df['Position'].str.contains(position, case=False, na=False)]
        df1 = df1[df1['Categorical position'] == target_position[i]]

        col_names = []
        for col in data.columns:
            col_names.append(col)
        # del col_names[-18:]
        del col_names[0:22]

        X = df1[col_names]

        kmeans = KMeans(n_clusters=4, random_state=100)
        kmeans.fit(X)
        df1['cluster'] = kmeans.predict(X)

        final_table1 = df1[['Player','Team','Categorical position','Position','Age','Market value','Contract expires','cluster']]
        target_player1 = df1[df1['Player'] == target1]
        i = target_player1.index[0]
        target_cluster1 = target_player1['cluster']

        final_table1 = final_table1[final_table1['cluster'] == target_cluster1[i]]

        final_table1['Similarity'] = 0.00
        # final_table1['Distance'] = 0.0000
        for j, row in df1.iterrows():
            x = row['cluster']
            if x == target_cluster1[i]:
                comparing_player = row[col_names]
                target1 = target_player1[col_names]
                T1 = np.array(target1).reshape(-1)
                B = np.array(comparing_player).reshape(-1)
                A = T1

                cos_sim = np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B))
                final_table1['Similarity'][j] = cos_sim * 100
                # final_table1['Distance'][j] = (1-cos_sim)

        final_table1.drop(final_table1[final_table1['Player'] == Player_Name1].index, inplace=True)
        final_table1.sort_values("Similarity", axis=0, ascending=False, inplace=True)
        final_table1.reset_index(inplace=True)
        final_table1 = final_table1.drop(['cluster','index'], axis=1)
        return final_table1

    final_table = player_similarity(data, Player_Name1, p, Position1)
    final_table = final_table.head(No_of_Similar_players)
    final_table['Similarity'] = final_table['Similarity'].apply(lambda x: round(x, 2))
    final_table['Similarity'] = final_table['Similarity'].apply(lambda x: f"{x:,} %")
    final_table['Market value'] = final_table['Market value'].apply(lambda x: f"{x:,} €")
    final_table.drop(columns=['Contract expires'], inplace=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    col_widths = [0.2, 0.2, 0.2, 0.15, 0.05, 0.15, 0.1]
    ax.axis('off')
    table = ax.table(cellText=final_table.values, colLabels=final_table.columns, loc='center', cellLoc='center', colWidths=col_widths)

    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.2)

    ax.set_title(f'Top {No_of_Similar_players} Similar Players to {Player_Name1} ({Position1})', fontsize=14)

    plt.tight_layout()
    # plt.show()
'''
if __name__ == "__main__":
    # Example usage:
    Player_Name1 = 'L. Messi'
    Percentage_of_player1 = 80
    No_of_Similar_players = 10
    find_similar_players(Player_Name1, Percentage_of_player1, No_of_Similar_players)

'''



# 球员雷达图分析：

from soccerplots.radar_chart import Radar

def radar(data, num, bg, pc, lc, rc, player1, player2, comparing_player, Player_Name, Metrics):
    warnings.filterwarnings("ignore")
    data = pd.read_excel('soccer/data/masterdata.xlsx')



    label1 = ['Non-penalty goals per 90', 'xG per 90', 'xG/Shot', 'Head goals per 90', 'Shots per 90',
              'Dribbles per 90', 'Shots on target %', 'Goal conv., %', 'Touches in box per 90']
    label2 = ['xA per 90', 'Key passes per 90', 'Smt passes per 90', 'Passes to penalty area per 90', 'Passes per 90',
              'Passes acc. %', 'Avg pass length, m']
    label3 = ['Aerial duels per 90', 'Aerial duels won %', 'Def duels per 90', 'Def duels won %', 'Fouls per 90',
              'PAdj Interceptions']

    ranges1 = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100),
               (0, 100), (0, 100), (0, 100)]
    ranges2 = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100),
               (0, 100)]
    ranges3 = [(0, 100), (0, 100), (0, 100), (0, 100), (0, 100), (0, 100)]

    attacking = [[round(data['Non-penalty goals per 90'].values[0], 2), round(data['xG per 90'].values[0], 2),
                  round(data['xG/Shot'].values[0], 2),
                  round(data['Head goals per 90'].values[0], 2), round(data['Shots per 90'].values[0], 2),
                  round(data['Dribbles per 90'].values[0], 2), round(data['Shots on target, %'].values[0], 2),
                  round(data['Goal conversion, %'].values[0], 2), round(data['Touches in box per 90'].values[0], 2)],
                 [round(data['Non-penalty goals per 90'].values[1], 2), round(data['xG per 90'].values[1], 2),
                  round(data['xG/Shot'].values[1], 2),
                  round(data['Head goals per 90'].values[1], 2), round(data['Shots per 90'].values[1], 2),
                  round(data['Dribbles per 90'].values[1], 2), round(data['Shots on target, %'].values[1], 2),
                  round(data['Goal conversion, %'].values[1], 2), round(data['Touches in box per 90'].values[1], 2)]]

    passing = [[round(data['xA per 90'].values[0], 2), round(data['Key passes per 90'].values[0], 2),
                round(data['Smart passes per 90'].values[0], 2),
                round(data['Passes to penalty area per 90'].values[0], 2), round(data['Passes per 90'].values[0], 2),
                round(data['Accurate passes, %'].values[0], 2), round(data['Average pass length, m'].values[0], 2)],
               [round(data['xA per 90'].values[1], 2), round(data['Key passes per 90'].values[1], 2),
                round(data['Smart passes per 90'].values[1], 2),
                round(data['Passes to penalty area per 90'].values[1], 2), round(data['Passes per 90'].values[1], 2),
                round(data['Accurate passes, %'].values[1], 2), round(data['Average pass length, m'].values[1], 2)]]

    defending = [[round(data['Aerial duels per 90'].values[0], 2), round(data['Aerial duels won, %'].values[0], 2),
                  round(data['Defensive duels per 90'].values[0], 2),
                  round(data['Defensive duels won, %'].values[0], 2), round(data['Fouls per 90'].values[0], 2),
                  round(data['PAdj Interceptions'].values[0], 2)],
                 [round(data['Aerial duels per 90'].values[1], 2), round(data['Aerial duels won, %'].values[1], 2),
                  round(data['Defensive duels per 90'].values[1], 2),
                  round(data['Defensive duels won, %'].values[1], 2), round(data['Fouls per 90'].values[1], 2),
                  round(data['PAdj Interceptions'].values[1], 2)]]

    print(attacking, passing, defending)

    title = dict(
        title_name=' ',
        title_color='#DB4437',  # 修改标题颜色为红色
        title_name_2=' ',
        title_color_2='#4285F4',  # 修改第二个标题颜色为蓝色
        title_fontsize=20)

    print('title in radier:',title['title_name'])
    radar = Radar(fontfamily="Arial", background_color=bg, patch_color=pc, label_color=lc,
                  range_color=rc)
    if Metrics == 'Attacking and creativity':
        attacking = radar.plot_radar(ranges=ranges1, params=label1, values=attacking, radar_color=[player1, player2],
                                     filename="web/static/attacking.png", end_color=bg, dpi=600, compare=True, title=title)
    elif Metrics == 'Passing and progression':
        passing = radar.plot_radar(ranges=ranges2, params=label2, values=passing, radar_color=[player1, player2],
                                   filename="web/static/passing.png", end_color=bg, dpi=600, compare=True, title=title)
    elif Metrics == 'Defensive actions':
        defending = radar.plot_radar(ranges=ranges3, params=label3, values=defending, radar_color=[player1, player2],
                                     filename="web/static/defending.png", end_color=bg, dpi=600, compare=True, title=title)
    else:
        attacking = radar.plot_radar(ranges=ranges1, params=label1, values=attacking, radar_color=[player1, player2],
                                     filename="web/static/attacking.png", end_color=bg, dpi=600, compare=True, title=title)

        passing = radar.plot_radar(ranges=ranges2, params=label2, values=passing, radar_color=[player1, player2],
                                   filename="web/static/passing.png", end_color=bg, dpi=600, compare=True, title=title)

        defending = radar.plot_radar(ranges=ranges3, params=label3, values=defending, radar_color=[player1, player2],
                                     filename="web/static/defending.png", end_color=bg, dpi=600, compare=True, title=title)


def compare_players_radar(comparing_player, target_player):
    warnings.filterwarnings("ignore")
    data = pd.read_excel('soccer/data/masterdata.xlsx')

    Metrics = 'All'
    target_player = data[data['Player'] == target_player]

    p1t = target_player['Team']
    comparing_player1 = data[data['Player'] == comparing_player]
    p2t = comparing_player1['Team']
    frames = [target_player, comparing_player1]


    print(frames)
    df = pd.concat(frames)
    print(df)
    radar(df, 2, "#1B1B1B", "#111111", "#FFFFFF", "#FFFFFF", "#D4011D", "#0020C4", comparing_player, target_player,
          Metrics)

'''
if __name__ == "__main__":
    Player_Name = 'S. Akhtar'  # @param {allow-input: true}

    comparing_player = "Jorge Meré"  # @param {type:"string"}

    compare_players_radar(comparing_player, Player_Name)
    print("finish")
'''
