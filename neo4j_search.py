from py2neo import Graph
from collections import Counter
from .models import Player

graph = Graph("http://localhost:7474", user='neo4j', password='12345678', name='neo4j')

def search1(search1,attribute1,value,attribute2):
    qerry = f'''
        match(n:{search1})
        where n.{attribute1} = '{value}'
        return distinct n.{attribute2} as final    
    '''
    result = graph.run(qerry)

    finals = [record['final'] for record in result]
    return finals

result = search1('赛事','赛季','2022','名称')
# print(search('赛事','赛季','2022','名称'))

def search2(country):
    qerry = f'''
        match(n:`比赛`)
        where n.主队 ='{country}' or n.客队 = '{country}'
        return distinct n.主队 as home, n.客队 as away 
    '''
    result = graph.run(qerry)

    homes = [record['home'] for record in result]
    aways = [record['away'] for record in result]
    final = homes + aways
    filtered_final = [team for team in final if team != country]
    return filtered_final

result2 = search2('Germany')
# print(result2)

def search_sim(name):
    qerry_pos = f'''
            MATCH (p1:队员)
            where p1.姓名 = '{name}'
            return distinct p1.位置 as pos
        '''
    result_pos = graph.run(qerry_pos)
    pos = [record['pos'] for record in result_pos]
    rp = []
    c = 0
    for position in pos:
        qerry_rp = f'''
                MATCH (p1:队员)
                where p1.姓名 = '{name}'
                MATCH (p2:队员)
                WHERE p2 <> p1 AND p2.位置 = '{position}'
                return distinct p2.姓名 as rp
            '''
        result_rp = graph.run(qerry_rp)
        rp += [record['rp'] for record in result_rp]
        c += 1

    counter = Counter(rp)
    most_common = counter.most_common(min(3,len(rp)))
    if most_common:

        return most_common
    else:
        return [('NULL',0)]

result3 = search_sim('Alex Sandro Lobo Silva')
# print(result3)

def search_p():
    qerry = '''
        match(n:英超球员)
        return n.姓名 as name, n.队伍 as team
    '''

    results = graph.run(qerry).data()

    players = [Player(name=result['name'], team=result['team']) for result in results]

    return players
