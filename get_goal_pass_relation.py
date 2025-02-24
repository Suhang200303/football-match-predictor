import pandas as pd
import os
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch
from kloppy import statsbomb
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mplsoccer.pitch import Pitch
import matplotlib.patches as patches

def visualize_heatmap(team_name, id):
    base_url = 'soccer/data'
    pass_to_shot = pd.DataFrame()

    events = statsbomb.load(
        event_data=os.path.join(base_url, 'events/%s.json'%id),
        lineup_data=os.path.join(base_url, 'lineups/%s.json'%id),
        coordinates='statsbomb'
    )
    # 过滤得到英格兰女足的所有射门，转换为DataFrame
    shots = events.filter('shot').filter(
        lambda e: e.team.name==team_name
    ).to_df()

    from kloppy.domain import SetPieceQualifier
    passes = events.filter('pass.complete').filter(
        lambda e: e.team.name==team_name
    ).filter(
        # 去掉定位球
        lambda e: 'type' not in e.raw_event['pass']
    )

    df = passes.to_df(
        # 添加球员名字列
        '*coordinates*',
        lambda e: {'player_name': e.player.name},
        'period_id',
        'timestamp'
    )

    # 去掉多余的列，重命名为简单的名称，洁癖专用
    df = df[['player_name', 'period_id',
        'timestamp', 'coordinates_x', 'coordinates_y',
        'end_coordinates_x', 'end_coordinates_y']]
    df.rename(columns={
        'coordinates_x':'x', 'coordinates_y':'y',
        'end_coordinates_x': 'end_x',
        'end_coordinates_y': 'end_y'
        }, inplace=True)

    passes_df = df[df.apply(
        lambda x: True in (
            # 与进球事件处于同一个半场
            # 并且发生在往前15秒之内的传球事件，视为危险传球
            (x.timestamp+15>shots[shots['period_id']==x.period_id]['timestamp']) & \
            (x.timestamp<shots[shots['period_id']==x.period_id]['timestamp'])
        ).unique(),
        # 按行过滤
        axis=1
    )]
    # 将传球事件拼接成一个DataFrame
    pass_to_shot = pd.concat([pass_to_shot, passes_df])

    print(pass_to_shot)
    print(pass_to_shot.shape)


    # pitch = Pitch(line_color='black')
    # fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
    #                      endnote_height=0.04, title_space=0, endnote_space=0)
    # pitch.scatter(pass_to_shot.x, pass_to_shot.y, s=100, color='blue', edgecolors='grey', linewidth=1, alpha=0.2, ax=ax["pitch"])
    # fig.suptitle('German', fontsize = 30)
    # plt.show()


    pitch = Pitch(line_zorder=2, line_color='black')
    fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                        endnote_height=0.04, title_space=0, endnote_space=0)
    # 将球场按条带划分并进行统计
    # 这个函数是mplsoccer自带
    bin_statistic = pitch.bin_statistic(
        pass_to_shot.x, pass_to_shot.y,
        statistic='count', bins=(12, 10),
        normalize=False
    )

    # 按照球赛场数平均一下
    bin_statistic["statistic"] = bin_statistic["statistic"]  # /len(ids)
    pcm = pitch.heatmap(bin_statistic, cmap='Reds', edgecolor='grey', ax=ax['pitch'])

    # 调整颜色范围
    pcm.set_clim(vmin=0, vmax=10)  # 根据需要设置最小值和最大值

    ax_cbar = fig.add_axes((1, 0.093, 0.03, 0.786))
    cbar = plt.colorbar(pcm, cax=ax_cbar)
    fig.suptitle('Danger passes by ' + team_name + " per game", fontsize=30)

    # 添加颜色条
    divider = make_axes_locatable(ax['pitch'])
    cax = divider.new_horizontal(size="5%", pad=0.1, pack_start=True)
    fig.add_axes(cax)
    cbar = plt.colorbar(pcm, cax=cax)
    cax.xaxis.set_label_position('top')
    cax.set_xlabel('DP Count', fontsize=12)

    fig.suptitle('Danger passes by ' + team_name + " per game", fontsize=30)
    # plt.show()


    #-------------------------热力图---------------------------
'''
if __name__ == "__main__":
    # 调用函数进行可视化
    team_name = 'Germany'
    ids = 7567
    visualize_heatmap(team_name, ids)
'''

