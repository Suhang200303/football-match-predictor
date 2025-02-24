import pandas as pd
import os
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch
from kloppy import statsbomb

def visualize_passes(match_id, team_name):
    base_url = 'soccer/data'

    # 加载数据并设定'kloppy'坐标系统，长宽坐标为0~1
    # 注意有些未经转换的statsbomb附加数据的单位仍然是yard
    dataset = statsbomb.load(
        event_data=os.path.join(base_url, 'events/%s.json'%match_id),
        lineup_data=os.path.join(base_url, 'lineups/%s.json'%match_id),
        coordinates='kloppy'
    )

    (team1, team2) = dataset.metadata.teams

    # 找出第一次换人事件，只分析第一次换人之前的传球网络
    subst = dataset.find('substitution')

    # 'pass.complete'表示只保留成功的传球事件
    # 只需要一只队伍的数据
    df = dataset.filter('pass.complete').filter(
        lambda e: e.raw_event['index'] < subst.raw_event['index'] and e.team.name == team_name
    ).to_df(
        '*coordinates*',
        lambda e: {'player_name': e.player.name},
        lambda e: {'receiver_name': e.receiver_player.name}
    )

    # 计算每个球员的位置
    outgoing_x = df.groupby(['player_name'])[['coordinates_x']].agg(['sum', 'count'])
    outgoing_x.columns = outgoing_x.columns.droplevel(0)
    outgoing_y = df.groupby(['player_name'])[['coordinates_y']].agg(['sum', 'count'])
    outgoing_y.columns = outgoing_y.columns.droplevel(0)
    incoming_x = df.groupby(['receiver_name'])[['end_coordinates_x']].agg(['sum', 'count'])
    incoming_x.columns = incoming_x.columns.droplevel(0)
    incoming_y = df.groupby(['receiver_name'])[['end_coordinates_y']].agg(['sum', 'count'])
    incoming_y.columns = incoming_y.columns.droplevel(0)

    pos_x = outgoing_x + incoming_x
    pos_y = outgoing_y + incoming_y

    pos = pd.DataFrame(pos_x.index).set_index('player_name')
    pos['x'] = pos_x['sum'] / pos_x['count']
    pos['y'] = pos_y['sum'] / pos_y['count']

    # 按照最大传球数量设定上限
    max_count = outgoing_x['count'].max()

    # 计算每两个球员之间的传球数量
    passes_count = df.groupby(['player_name', 'receiver_name']).agg(['count'])
    passes_count.columns = passes_count.columns.droplevel(0)
    passes_count = passes_count.loc[:, ~passes_count.columns.duplicated()].copy().reset_index()

    pitch = VerticalPitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')

    fig, ax = pitch.draw(figsize=(10, 7))

    # 获取球场的坐标范围
    x_range = pitch.dim.left, pitch.dim.right
    y_range = pitch.dim.bottom, pitch.dim.top

    pos['rel_x'] = pos['x'] * (x_range[1] - x_range[0]) + x_range[0]
    pos['rel_y'] = pos['y'] * (y_range[1] - y_range[0]) + y_range[0]

    pitch.scatter(
        pos['rel_x'], pos['rel_y'],
        s=pos_x['count'] / max_count * 300,
        edgecolors='grey', linewidth=1, alpha=1,
        ax=ax, zorder=3
    )

    for _, row in pos.iterrows():
        pitch.annotate(
            row.name,
            xy=(row.rel_x, row.rel_y),
            c='black', va='center', ha='center',
            weight="bold", size=8, ax=ax, zorder=4
        )

    for _, row in passes_count.iterrows():
        pitch.lines(
            pos.loc[row['player_name']].rel_x,
            pos.loc[row['player_name']].rel_y,
            pos.loc[row['receiver_name']].rel_x,
            pos.loc[row['receiver_name']].rel_y,
            alpha=1, zorder=2, color="red", ax=ax,
            lw=row['count'] / passes_count['count'].max() * 10
        )



    passes_no = df.groupby(['player_name']).agg(['count'])
    passes_no.columns = passes_no.columns.droplevel(0)
    passes_no = passes_no.loc[:, ~passes_no.columns.duplicated()].copy().reset_index()
    print(passes_no)
    max_no = passes_no["count"].max()
    denominator = 10 * passes_no["count"].sum()
    nominator = (max_no - passes_no["count"]).sum()
    centralisation_index = nominator / denominator
    print("Centralisation Index:", centralisation_index)

    fig.suptitle('%s Team Player Pass Network' % team_name, fontsize=24)
    plt.figtext(0.5, 0.8, "Centralisation Index: %.2f" % centralisation_index, ha='center', fontsize=14)

    # plt.show()

'''
if __name__ == "__main__":
# 示例调用
    match_id = 3869685
    team_name = "Argentina"
    visualize_passes(match_id, team_name)

'''
