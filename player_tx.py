import csv
import pandas as pd
import os
from kloppy import statsbomb
from mplsoccer.pitch import Pitch
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
from kloppy.domain.models.event import EventDataset, Event

def read_filenames_from_csv(csv_file_name):
    ids = []
    with open(csv_file_name, mode='r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # 跳过CSV文件的表头
        for idx, row in enumerate(reader):
            if idx >= 100:  # 只读取前100行数据
                break
            filename = row[0]
            file_id = int(filename.split('.')[0])
            ids.append(file_id)
    return ids

def generate_threat_heatmap(player_name):
    # 指定CSV文件名
    csv_file_name = 'soccer/data/output_filenames.csv'  # 替换成您保存文件名的CSV文件名

    # 从CSV文件中读取所有文件名并保存在ids数组内
    ids = read_filenames_from_csv(csv_file_name)

    # 批量加载比赛数据集的代码，利用了kloppy的数据结构
    class SbBatch:
        def __init__(self, base_url='soccer/data'):
            self.base_url = base_url
            url = f'{self.base_url}competitions.json'

        def load_match_by_ids(self, ids):
            events = []
            meta = None
            for id in ids:
                dataset = statsbomb.load(
                    event_data=os.path.join(self.base_url, 'events/%s.json' % id),
                    lineup_data=os.path.join(self.base_url, 'lineups/%s.json' % id),
                    coordinates='statsbomb'
                )

                for e in dataset.records:
                    events.append(e)
                # 只保留一个metadata，这里metadata只是为了构建EventDataset
                # 里面的信息是不正确的
                meta = dataset.metadata
            dataset = EventDataset(events, meta)
            return dataset

    sb = SbBatch()
    # 加载多场比赛的数据集。这里违反了kloppy的使用规范，dataset里的元数据metadata是错误的
    dataset = sb.load_match_by_ids(ids)

    # 从CSV文件中读取威胁度矩阵数据
    v = pd.read_csv('soccer/data/threat_heatmap.csv')

    # 射门事件
    shots_x_y = dataset.filter('shot').filter(
            lambda e: e.player.name == player_name
        ).to_df('coordinates*', lambda e: {'player_name': e.player.name},)

    # 传球事件，这里只保留了成功的传球
    pass_x_y = dataset.filter('pass.complete').filter(
            lambda e: e.player.name == player_name
        ).to_df('coordinates*', lambda e: {'player_name': e.player.name},)

    # 将球场划分为16×12的区域
    cells_x = 16
    cells_y = 12
    # 球场大小，单位是码
    pitch_x = 120
    pitch_y = 80
    # 米表示的标准球场大小
    pitch_length = 105
    pitch_width = 68

    # 计算射门和传球的价值
    def get_value(row):
        x = row['coordinates_x']
        y = row['coordinates_y']
        x_idx = x * cells_x // pitch_x
        y_idx = y * cells_y // pitch_y
        return v.loc[x_idx * cells_y + y_idx, 'threat']

    shots_x_y['shot_value'] = shots_x_y.apply(get_value, axis=1)
    pass_x_y['pass_value'] = pass_x_y.apply(get_value, axis=1)

    # 计算 shots_x_y 和 pass_x_y 各自的总和
    shots_total_value = shots_x_y['shot_value'].sum()
    pass_total_value = pass_x_y['pass_value'].sum()

    # 计算 shots_x_y 和 pass_x_y 两者加在一起的总和
    total_value = shots_total_value + pass_total_value

    # 输出结果
    print("Shots Value:", shots_total_value)
    print("Passes Value:", pass_total_value)
    print("Total Value:", total_value)

    pitch = Pitch(line_zorder=2, line_color='black')
    fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                        endnote_height=0.04, title_space=0, endnote_space=0)

    # 将球场按条带划分并进行统计
    bin_statistic = pitch.bin_statistic(
        v.x, v.y,
        bins=(16, 12),
        statistic= 'count',
        normalize=False
    )

    v = v.sort_values(['y', 'x'])

    # 将'threat'列的值转换为二维数组
    threat_array = v['threat'].values.reshape((cells_y, cells_x))

    # 将 threat_array 赋值给 bin_statistic["statistic"]
    bin_statistic["statistic"] = threat_array

    # 绘制热力图
    pcm = pitch.heatmap(bin_statistic, cmap='Reds', edgecolor='grey', ax=ax['pitch'])

    # 添加额外的散点，表示射门的位置
    ax['pitch'].scatter(shots_x_y['coordinates_x'], shots_x_y['coordinates_y'], color='blue', marker='o', s=30, alpha=0.8, label='Shots')

    # 添加额外的散点，表示传球的位置
    ax['pitch'].scatter(pass_x_y['coordinates_x'], pass_x_y['coordinates_y'], color='green', marker='o', s=30, alpha=0.8, label='Passes')
    # 调整颜色范围
    pcm.set_clim(vmin=0, vmax=30)  # 根据需要设置最小值和最大值

    # 添加颜色条
    divider = make_axes_locatable(ax['pitch'])
    cax = divider.new_horizontal(size="5%", pad=0.1, pack_start=True)
    fig.add_axes(cax)
    cbar = plt.colorbar(pcm, cax=cax)
    cax.xaxis.set_label_position('top')
    cax.set_xlabel('Threat Level', fontsize=12)

    # 修改输出文本为英文，并加入球员名字
    output_text = f"Shots Value: {shots_total_value}    Passes Value: {pass_total_value}    Total Value: {total_value}"
    ax['endnote'].text(0.1, 0.4, output_text, fontsize=12, color='black')  # 将颜色设置为黑色

    # 设置图像标题
    fig.suptitle(f"{player_name}'s Value", fontsize=30)

    # 显示图例
    ax['pitch'].legend(loc='upper right')

    # plt.show()

'''
if __name__ == "__main__":
    # 使用示例
    player_name = 'Lionel Andrés Messi Cuccittini'
    generate_threat_heatmap(player_name)
'''

