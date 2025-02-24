from py2neo import Graph, Node, Relationship
from neo4j import GraphDatabase

import csv
import pandas as pd

graph = Graph("http://localhost:7474", user='neo4j', password='12345678', name='neo4j')
'''
with open('data/Premier League.csv') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        compet_id = row[0]
        compet_date = row[2]
        home_team = row[3]
        away_team = row[4]

        home_goal = row[5]
        away_goal = row[6]
        final_result = row[7]

        referee = row[11]
        home_shot = row[12]
        away_shot = row[13]
        home_shot_tar = row[14]
        away_shot_tar = row[15]

        home_legal = row[17]
        away_legal = row[18]

        home_yellow = row[20]
        away_yellow = row[21]
        home_red = row[22]
        away_red = row[23]

        qerry_compet = '''
'''
merge(n:比赛{编号: $id, 时间: $date, 主队: $home_team, 客队: $away_team, 主裁判: $referee, 结果: $final_result, 
            主队得分: $home_goal, 客队得分: $away_goal, 主队射门数: $home_shot, 主队射正数: $home_shot_tar, 客队射门数: $away_shot, 
            客队射正数: $away_shot_tar, 主队犯规: $home_legal, 客队犯规: $away_legal, 主队黄牌数: $home_yellow, 主队红牌数: $home_red,
            客队黄牌数: $away_yellow, 客队红牌数: $away_red})
            return n     
'''

'''

        result = graph.run(qerry_compet, id=compet_id, date=compet_date, home_team=home_team, away_team=away_team, referee=referee,
                           final_result=final_result, home_goal=home_goal, away_goal=away_goal, home_shot=home_shot, home_shot_tar=home_shot_tar,
                           away_shot=away_shot, away_shot_tar=away_shot_tar, home_legal=home_legal, away_legal=away_legal, home_yellow=home_yellow,
                           home_red=home_red, away_yellow=away_yellow, away_red=away_red)

'''


data_p = pd.read_excel('data/masterdata.xlsx')

for index, row in data_p.iterrows():
    node = Node("英超球员", 姓名=row['Player'], 队伍=row['Team'])
    graph.create(node)
