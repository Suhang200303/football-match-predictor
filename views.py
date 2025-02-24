from django.shortcuts import render, redirect
from neo4j import GraphDatabase

from django.http import HttpResponse
from soccer.neo4j_search import search1, search2, search_sim, search_p

import io
import matplotlib.pyplot as plt
from soccer.get_pass import plot_passes
from soccer.get_shot import visualize_shots
from soccer.get_goal import visualize_passes
from soccer.get_goal_pass_relation import visualize_heatmap
from soccer.player_tx import generate_threat_heatmap

from soccer.drawchart import draw_bar_chart, draw_y_bar_chart
from soccer.radier import find_similar_players, compare_players_radar, compare_players_radar

from .models import Player


import json

# from .neo4j_init import reader
# Create your views here.

def index(request):
    return render(request, 'bar.html')

def draw_x(request, x):
    return render(request, f'points/bar{x}.html')

def search_view(request):
    if request.GET.get('period') is not None:
        period = request.GET.get('period')
        attribute_s = request.GET.get('attribute_s')
        attribute_r = request.GET.get('attribute_r')
        value = request.GET.get('value')
        results = search1(period,attribute_s,value,attribute_r)  # 调用后台的 Neo4j 查询函数
        if results is not None:

            return render(request, 'result.html', {'results':results})


    return render(request, 'search_form.html')

def test1(request):
    return render(request, 'text.html')



# 关系图渲染：

def homepage(request):
    # Neo4j 连接信息
    uri = 'bolt://localhost:7687'
    user = 'neo4j'
    password = '12345678'

    # 创建 Neo4j 驱动程序实例
    driver = GraphDatabase.driver(uri, auth=(user, password))

    # 执行 Neo4j 查询并获取结果
    with driver.session() as session:
        cypher_query = """
            MATCH (n)-[r]->(m)
            RETURN n, r, m
            LIMIT 100
        """
        result = session.run(cypher_query)

        # 转换 Neo4j 查询结果为 ECharts 关系图所需的 JSON 格式
        nodes = []
        links = []

        for record in result:
            source_node = record['n']
            edge = record['r']
            target_node = record['m']

            source_node_properties = dict(source_node)
            source_index = next((i for i, node in enumerate(nodes) if node['id'] == str(source_node.id)), -1)
            if source_index == -1:
                nodes.append({
                    'id': str(source_node.id),
                    'name': source_node_properties.get(''),
                    # 其他节点属性
                })

            target_node_properties = dict(target_node)
            target_index = next((i for i, node in enumerate(nodes) if node['id'] == str(target_node.id)), -1)
            if target_index == -1:
                nodes.append({
                    'id': str(target_node.id),
                    'name': target_node_properties.get(''),
                    # 其他节点属性
                })

            links.append({
                'source': source_index,
                'target': target_index,
                'label': edge.type,
                # 其他边属性
            })

        # 转换 JSON 数据为字符串
        nodes_json = json.dumps(nodes)
        links_json = json.dumps(links)

        # 将数据传递给模板进行渲染
        context = {
            'nodes': nodes_json,
            'links': links_json,
        }
        return render(request, 'chart.html', context)

def search_similar(request):
    if request.method == 'GET':
        if request.GET.get('name') is not None:
            name = request.GET.get('name')

            results = search_sim(name)
            if results is not None:

                return render(request, 'result.html', {'results':results})


    return render(request, 'search_sim.html')

def total_stat(request):
    return render(request, 'total_stat.html')

def shot_view(request):
    if request.GET.get('match_id') is not None:
        match_id = request.GET.get('match_id')
        team_name = request.GET.get('team_name')

        fig1 = visualize_shots(match_id, team_name)

        buf1 = io.BytesIO()

        plt.savefig(buf1, format='png')
        buf1.seek(0)

        image_data = buf1.getvalue()

        buf1.close()
        return HttpResponse(image_data, content_type='image/png')

    return render(request, 'total_stat.html')

def pass_view(request):
    if request.GET.get('match_id') is not None:
        match_id = request.GET.get('match_id')
        team_name = request.GET.get('team_name')

        fig = plot_passes(match_id, team_name)

        buf1 = io.BytesIO()

        plt.savefig(buf1, format='png')
        buf1.seek(0)

        image_data = buf1.getvalue()
        buf1.close()

        return HttpResponse(image_data, content_type='image/png')

    return render(request, 'total_stat.html')


def pass_view(request):
    if request.GET.get('match_id') is not None:
        match_id = request.GET.get('match_id')
        team_name = request.GET.get('team_name')

        fig = plot_passes(match_id, team_name)

        buf1 = io.BytesIO()

        plt.savefig(buf1, format='png')
        buf1.seek(0)

        image_data = buf1.getvalue()
        buf1.close()

        return HttpResponse(image_data, content_type='image/png')

    return render(request, 'total_stat.html')


def goal_view(request):
    if request.GET.get('match_id') is not None:
        match_id = request.GET.get('match_id')
        team_name = request.GET.get('team_name')

        fig = visualize_passes(match_id, team_name)

        buf1 = io.BytesIO()

        plt.savefig(buf1, format='png')
        buf1.seek(0)

        image_data = buf1.getvalue()
        buf1.close()

        return HttpResponse(image_data, content_type='image/png')

    return render(request, 'total_stat.html')


def goal_pass_relation(request):
    if request.GET.get('match_id') is not None:
        match_id = request.GET.get('match_id')
        team_name = request.GET.get('team_name')

        fig = visualize_heatmap(team_name, match_id)

        buf1 = io.BytesIO()

        plt.savefig(buf1, format='png')
        buf1.seek(0)

        image_data = buf1.getvalue()
        buf1.close()

        return HttpResponse(image_data, content_type='image/png')

    return render(request, 'total_stat.html')

def total_map(request):
    if request.GET.get('team_name'):
        name = request.GET.get('team_name')
        fig = generate_threat_heatmap(name)

        buf1 = io.BytesIO()

        plt.savefig(buf1, format='png')
        buf1.seek(0)

        image_data = buf1.getvalue()
        buf1.close()

        return HttpResponse(image_data, content_type='image/png')

    return render(request, 'total_stat.html')


def draw_chart(request):

    fig = draw_bar_chart()

    buf1 = io.BytesIO()

    plt.savefig(buf1, format='png')
    buf1.seek(0)

    image_data = buf1.getvalue()
    buf1.close()

    return HttpResponse(image_data, content_type='image/png')

def draw_y_chart(request):

    fig = draw_y_bar_chart()

    buf1 = io.BytesIO()

    plt.savefig(buf1, format='png')
    buf1.seek(0)

    image_data = buf1.getvalue()
    buf1.close()

    return HttpResponse(image_data, content_type='image/png')

def sim_view(request):
    if request.GET.get('name') is not None:
        name = request.GET.get('name')
        fig = find_similar_players(name,80,10)

        buf1 = io.BytesIO()

        plt.savefig(buf1, format='png')
        buf1.seek(0)

        image_data = buf1.getvalue()
        buf1.close()

        return HttpResponse(image_data, content_type='image/png')

    return render(request, 'search_sim.html')



def player_search(request):
    players = search_p()  # 调用前面定义的查询函数
    context = {'players': players}
    return render(request, 'player_search.html', context)

def radier_p(request):
    if request.GET.get('name') is not None:
        name = request.GET.get('name')
        name_r = request.GET.get('rival')

        print(name,name_r)
        compare_players_radar(name, name_r)

        context = {
            'name': name,
            'rival': name_r
        }
        return render(request, 'radier_p.html', context)

    return render(request, 'search_sim.html')
