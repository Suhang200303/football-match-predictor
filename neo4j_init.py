from py2neo import Graph
import csv

graph = Graph("http://localhost:7474", user='neo4j', password='12345678', name='neo4j')

graph.delete_all()

with open('data/2022data.csv', encoding='UTF-8') as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:

        match_id = row[0]
        compet_date = row[1]

        compet_area = row[3]
        compet_name = row[4]

        season = row[6]
        home_team = row[8]
        away_team = row[10]
        home_score = row[11]
        away_score = row[12]

        compet_pattern = row[14]


        query1 = 'merge(n:赛事{名称: $name, 赛季: $season, 区域: $area}) return n'
        result1 = graph.run(query1, name=compet_name, season=season, area=compet_area)

        query2 = 'merge(n:比赛{类别: $pattern, 比赛编号: $match_id, 主队: $home_team, 主队得分: $home_score, 客队: $away_team, 客队得分: $away_score}) return n'
        result2 = graph.run(query2, pattern=compet_pattern, match_id=match_id, home_team=home_team, home_score=home_score, away_team=away_team, away_score=away_score)


        query_relation = '''
            match(n:赛事),(m:比赛)
            where n.名称 = $name and
            m.比赛编号 = $match_id
            merge (m)-[:划分]->(n)
            
        '''
        result_relation = graph.run(query_relation, name=compet_name, match_id=match_id)

with open('data/2021data.csv') as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        match_id = row[0]
        compet_date = row[1]

        compet_area = row[3]
        compet_name = row[4]

        season = row[6]
        home_team = row[8]
        away_team = row[10]
        home_score = row[11]
        away_score = row[12]

        compet_pattern = row[14]

        query1 = 'merge(n:赛事{名称: $name, 赛季: $season, 区域: $area}) return n'
        result1 = graph.run(query1, name=compet_name, season=season, area=compet_area)

        query2 = 'merge(n:比赛{类别: $pattern, 比赛编号: $match_id, 主队: $home_team, 主队得分: $home_score, 客队: $away_team, 客队得分: $away_score}) return n'
        result2 = graph.run(query2, pattern=compet_pattern, match_id=match_id, home_team=home_team,
                            home_score=home_score, away_team=away_team, away_score=away_score)

        query_relation = '''
            match(n:赛事),(m:比赛)
            where n.名称 = $name and
            m.比赛编号 = $match_id
            merge (m)-[:划分]->(n)

        '''
        result_relation = graph.run(query_relation, name=compet_name, match_id=match_id)

with open('data/2018data.csv') as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        match_id = row[0]
        compet_date = row[1]

        compet_area = row[3]
        compet_name = row[4]

        season = row[6]
        home_team = row[8]
        away_team = row[10]
        home_score = row[11]
        away_score = row[12]

        compet_pattern = row[14]

        query1 = 'merge(n:赛事{名称: $name, 赛季: $season, 区域: $area}) return n'
        result1 = graph.run(query1, name=compet_name, season=season, area=compet_area)

        query2 = 'merge(n:比赛{类别: $pattern, 比赛编号: $match_id, 主队: $home_team, 主队得分: $home_score, 客队: $away_team, 客队得分: $away_score}) return n'
        result2 = graph.run(query2, pattern=compet_pattern, match_id=match_id, home_team=home_team,
                            home_score=home_score, away_team=away_team, away_score=away_score)

        query_relation = '''
            match(n:赛事),(m:比赛)
            where n.名称 = $name and
            n.赛季 = $season and
            m.比赛编号 = $match_id
            merge (m)-[:划分]->(n)

        '''
        result_relation = graph.run(query_relation, name=compet_name, season=season, match_id=match_id)

with open('data/lineups.csv', encoding='UTF-8') as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        match_id = row[0]
        player_id = row[1]

        player_name = row[2]
        player_clo_id = row[3]

        country = row[4]
        if row[6] !='none':
            position = row[6]
        else:
            position = "NULL"
        card_name = row[7]
        card_date = row[8]
        card_reason = row[9]

        query3 = 'merge(n:队伍{参赛场次: $id, 名称: $country}) return n'
        result3 = graph.run(query3, id=match_id, country=country)


        query4 = 'merge(n:队员{编号: $id, 姓名: $name, 球衣号码: $number, 位置: $position, 国家: $country, 罚牌名称: $card_name, 罚牌时间: $card_date, 罚牌原因: $card_reason}) return n'
        result4 = graph.run(query4, id=player_id, name=player_name, number=player_clo_id, position=position, country=country, card_name=card_name, card_date=card_date, card_reason=card_reason)

        query_relation2 = '''
                    match(n:队员),(m:队伍)
                    where n.姓名 = $name and
                    n.国家 = m.名称 and
                    m.参赛场次 = $match_id
                    merge (n)-[:属于]->(m)

                '''
        result_relation2 = graph.run(query_relation2, name=player_name, match_id=match_id)

        query_relation3 = '''
                            match(n:比赛),(m:队伍)
                            where n.比赛编号 = m.参赛场次 and (n.主队 = m.名称 or n.客队 = m.名称)
                            merge (m)-[:参加]->(n)

                        '''
        result_relation3 = graph.run(query_relation3)


with open('data/Premier League.csv') as file:
    reader = csv.reader(file)