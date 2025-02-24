import pandas as pd
import os
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch
from kloppy import statsbomb
import matplotlib.patches as patches

def plot_passes(match_id, team_name):
    base_url = 'soccer/data'

    # 加载数据并设定'kloppy'坐标系统，长宽坐标为0~1
    # 注意有些未经转换的statsbomb附加数据的单位仍然是yard
    dataset = statsbomb.load(
        event_data=os.path.join(base_url, 'events/%s.json'%match_id),
        lineup_data=os.path.join(base_url, 'lineups/%s.json'%match_id),
        coordinates='kloppy'
    )

    #-------------------------传球案例-----------------------------


    pass_data = dataset.filter('pass')
    # 查看数据集的球场尺寸（英制的码）
    print(dataset.metadata.pitch_dimensions)
    # 进攻方坐标总是从左到右
    print(dataset.metadata.orientation)
    # 数据集的坐标系统，具体轻查看随statsbomb open data的数据集规范文档
    print(dataset.metadata.coordinate_system)
    # 从数据集元数据中展开两支参赛队伍
    (team1, team2) = dataset.metadata.teams
    print(team1.name, team2.name)

    team_pass_df = pass_data.filter(
        # 按照队伍名称过滤传球
        lambda e: e.team.name==team_name and e.raw_event['play_pattern']!='From Throw In'
    ).to_df(
        # 在转换为pandas DataFrame时保留传球起止坐标和球员名称
        '*coordinates*',
        lambda e: {'player_name': e.player.name}
    )

    print(team_pass_df.columns)

    # 按照球员将DataFrame分组
    dfs = dict(tuple(team_pass_df.groupby('player_name')))

    pitch = VerticalPitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')

    fig, axs = pitch.grid(
        ncols = 6, nrows = 3, grid_height=0.85, title_height=0.06, axis=False,
        endnote_height=0.04, title_space=0.04, endnote_space=0.01
    )

    # 自定义足球场尺寸和边界
    pitch_length = 105
    pitch_width = 68

    for name, ax in zip(dfs.keys(), axs['pitch'].flat[:len(dfs.keys())]):
        # 画出球员名字
        ax.text(
            40, -10, name,
            ha='center', va='center', fontsize=10
        )
        # 从展开球员的传球数据
        player_df = dfs[name]
        pitch.scatter(
            player_df.coordinates_x * pitch_length * 1.11 + 2,
            player_df.coordinates_y * pitch_width * 1.16 + 2,
            alpha=0.5, s=10, color="blue", ax=ax
        )
        pitch.arrows(
            player_df.coordinates_x * pitch_length  * 1.11 + 2,
            player_df.coordinates_y * pitch_width * 1.16 + 2,
            player_df.end_coordinates_x * pitch_length  * 1.11 + 2,
            player_df.end_coordinates_y * pitch_width * 1.16 + 2,
            color="blue", ax=ax, width=1
        )

    # 移除多余的空白场地
    for ax in axs['pitch'].flat[len(dfs.keys()):]:
        ax.remove()

    axs['title'].text(
        0.5, 0.5, '%s Team Player Pass Visualization'%(team_name), 
        ha='center', va='center', fontsize=30
    )
    #plt.show()

'''
if __name__ == "__main__":
    # 示例调用
    match_id = 7567
    team_name = "Germany"
    plot_passes(match_id, team_name)
'''