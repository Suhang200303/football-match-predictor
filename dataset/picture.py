import pandas as pd
import os
from kloppy import statsbomb

# 直接指定比赛id
# 这是一场西甲巴塞罗那的比赛
match_id = 68366
base_url = '/location/to/your/data/statsbomb/data'

# 设定'statsbomb'坐标系统，单位是yard
dataset = statsbomb.load(
    # 拼接出事件的文件路径
    # 文件组织参看statsbomb open data的数据集规范文档
    event_data=os.path.join(base_url, 'events/%s.json'%match_id),
    # 拼接出阵容文件的路径
    lineup_data=os.path.join(base_url, 'lineups/%s.json'%match_id),
    coordinates='statsbomb'
)

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
import matplotlib as mpl
from mplsoccer.pitch import Pitch
import matplotlib.pyplot as plt

# 解决Linux下matplotlib的中文显示问题，这里采用了仿黑字体，需要从外部安装到Linux系统
# 觉得麻烦可以直接用英文
mpl.rcParams['font.sans-serif'] = ['simhei']
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

# 图雷的全名
# 在事件数据中，每个球员都使用正式全名
# 如果不知道全名，可以从数据集元数据中获取参赛的所有球员全名
player_name = 'Gnégnéri Yaya Touré'

# 开始画球场
pitch = Pitch()
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)

# 过滤掉其他球员
# 过滤掉界外球
# 这里filter是过滤操作，可以级联操作
df_pass = pass_data.filter(
    lambda e: e.player.name==player_name and e.raw_event['play_pattern']!='From Throw In'
).to_df()   # 转换为pandas DataFrame

# 根据传球的起止坐标画箭头
pitch.arrows(
    df_pass.coordinates_x, df_pass.coordinates_y,
    df_pass.end_coordinates_x, df_pass.end_coordinates_y, 
    color = "blue", ax=ax['pitch']
)
# 画圆圈表示球员位置
pitch.scatter(
    df_pass.coordinates_x,
    df_pass.coordinates_y,
    alpha = 0.2, s = 500, color = "blue", ax=ax['pitch']
)
fig.suptitle('%s与%s队比赛时的传球'%(player_name, team2.name), fontsize = 30)
plt.show()
team_pass_df = pass_data.filter(
    # 按照队伍名称过滤传球
    lambda e: e.team.name==team1.name and e.raw_event['play_pattern']!='From Throw In'
).to_df(
    # 在转换为pandas DataFrame时保留传球起止坐标和球员名称
    '*coordinates*',
    lambda e: {'player_name': e.player.name}
)

# 按照球员将DataFrame分组
dfs = dict(tuple(team_pass_df.groupby('player_name')))

pitch = Pitch(line_color='black', pad_top=20)
fig, axs = pitch.grid(
    ncols = 4, nrows = 4, grid_height=0.85, title_height=0.06, axis=False,
    endnote_height=0.04, title_space=0.04, endnote_space=0.01
)
for name, ax in zip(dfs.keys(), axs['pitch'].flat[:len(dfs.keys())]):
    # 画出球员名字
    ax.text(
        60, -10, name,
        ha='center', va='center', fontsize=10
    )
    # 从展开球员的传球数据
    player_df = dfs[name]
    pitch.scatter(
        player_df.coordinates_x, 
        player_df.coordinates_y, 
        alpha = 0.2, s = 50, color = "blue", ax=ax
    )
    pitch.arrows(
        player_df.coordinates_x,
        player_df.coordinates_y,
        player_df.end_coordinates_x,
        player_df.end_coordinates_y,
        color = "blue", ax=ax, width=1
    )
# 移除多余的空白场地
for ax in axs['pitch'][-1, 16 - len(dfs.keys()):]:
    ax.remove()

axs['title'].text(
    0.5, 0.5, '%s与%s队比赛时的传球'%(team1.name, team2.name), 
    ha='center', va='center', fontsize=30
)
plt.show()