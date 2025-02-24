import pandas as pd
import numpy as np
import random as rd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings("ignore")

data = pd.read_excel('masterdata.xlsx')

Player_Name1 = input("请输入球员的名字：")  #@param {allow-input: true}
Percentage_of_player1 = 90 #@param {type:"slider", min:1, max:99, step:1}

# 从数据集中获取球员的位置信息
position_column = data[data['Player'] == Player_Name1]['Position']
if len(position_column) > 0:
    Position1 = position_column.iloc[0].split(',')[0]  # 提取第一个逗号前的位置
else:
    raise ValueError("Invalid player name or player not found in dataset.")

p = Percentage_of_player1 / 100

warnings.filterwarnings("ignore")
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
print(final_table.head(10))
