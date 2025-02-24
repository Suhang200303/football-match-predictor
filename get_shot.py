import pandas as pd
import os
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch
from kloppy import statsbomb
from mpl_toolkits.axes_grid1 import make_axes_locatable

def visualize_shots(match_id, team_name):
    base_url = 'soccer/data/'

    # 加载数据并设定'kloppy'坐标系统，长宽坐标为0~1
    # 注意有些未经转换的statsbomb附加数据的单位仍然是yard
    dataset = statsbomb.load(
        event_data=os.path.join(base_url, 'events/%s.json' % match_id),
        lineup_data=os.path.join(base_url, 'lineups/%s.json' % match_id),
        coordinates='kloppy'
    )

    # 从数据集中过滤出射门事件
    shots = dataset.filter('shot')

    # 米表示的标准球场大小
    pitch_length = 105
    pitch_width = 68

    # 我们只分析一只球队，所以画半场图形更方便
    pitch = VerticalPitch(line_color='black', half=True, pitch_length=pitch_length, pitch_width=pitch_width)
    fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                        endnote_height=0.04, title_space=0, endnote_space=0)

    # 将射门事件转换为DataFrame
    # 保留了参赛队名称、射门的球场坐标和期望进球xG
    df = shots.to_df(
        lambda e: {'team': e.team.name},
        'coordinate*',
        lambda e: {'statsbomb_xg': e.raw_event['shot']['statsbomb_xg']}
    )

    # 筛选出其中一只队伍
    df = df.loc[df['team'] == team_name]

    # 将射门事件用点散点图画出来，xG用条带颜色表示，颜色越深进球可能性越高
    # 坐标位于[0,1]，还有按照球场长宽进行转换
    sc = pitch.scatter(
        df.coordinates_x * pitch_length,
        df.coordinates_y * pitch_width,
        alpha=1, s=200, c=df.statsbomb_xg, cmap='Reds', vmin=0, vmax=1,
        ax=ax['pitch'], edgecolors='black'
    )

    # 添加颜色条
    divider = make_axes_locatable(ax['pitch'])
    cax = divider.new_horizontal(size="5%", pad=0.1, pack_start=True)
    fig.add_axes(cax)
    cbar = plt.colorbar(sc, cax=cax)
    cax.xaxis.set_label_position('top')
    cax.set_xlabel('Expected Goals', fontsize=12)

    # 设置标题
    plt.suptitle(f"{team_name} Shot Analysis Based On XG", fontsize=20)

    return plt
    # 显示图形
    # plt.show()

    # 关闭图形
    # plt.close()
'''
    if __name__ == "__main__":
        match_id = 7567
        team_name = "Germany"

        visualize_shots(match_id, team_name)
'''
