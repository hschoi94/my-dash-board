import plotly.graph_objects as go
import json
import os
from pathlib import Path
import pandas as pd
import numpy as np
import re
from config import *
# docker run -it --rm -v $PWD:/app docker-manager
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'NanumGothic'
def csvFigSave(file_path, data):
    fig = data.plot()
    fig = fig.get_figure()
    fig.savefig(file_path)

def filteringKey(file_path, index):
    df = pd.read_csv(file_path)
    key = list(df.keys())
    key = key[1:]
    dfn = np.array(df)[index][1:]
    empty_index = np.array(dfn == 0)
    filled_index = np.array(empty_index == False)
    filtered_key = []
    for i in range(len(key)):
        if filled_index[i]:
            filtered_key += [key[i]]

    v_temp = []
    for i in range(len(key)):
        if filled_index[i]:
            v_temp += [dfn[i]]
    return filtered_key, v_temp


def dict2fig(dict_, fig_path):
    # Daily visitors
    name = os.path.basename(fig_path).split(".")[0]
    k = (list(dict_.keys()))
    if len(k) > 0:
        v = np.abs(np.array(list(dict_.values()), dtype=float))
        df = pd.DataFrame(
            {'sample1': k, name: v})
        sum_df = df.groupby("sample1").sum()
        p = v/np.sum(v)*100
        labels = ['{}, {:0.1f}% {:d}'.format(
            l, s, int(va)) for l, s, va in zip(k, p, v)]
        pie = sum_df.plot(kind="pie",
                          figsize=(10, 6),
                          legend=True,
                          use_index=False,
                          subplots=True,
                          colormap="Pastel1",
                          title=[''],)
        #   autopct='%1.1f%%')
        plt.legend(bbox_to_anchor=(0.9, 1), loc='upper left', labels=labels)
        plot = pie[0].get_figure()
        plot.savefig(fig_path)


# Setup our colours
color_link = ['#000000', '#FFFF00', '#1CE6FF', '#FF34FF', '#FF4A46',
              '#008941', '#006FA6', '#A30059', '#FFDBE5', '#7A4900',
              '#0000A6', '#63FFAC', '#B79762', '#004D43', '#8FB0FF',
              '#997D87', '#5A0007', '#809693', '#FEFFE6', '#1B4400',
              '#4FC601', '#3B5DFF', '#4A3B53', '#FF2F80', '#61615A',
              '#BA0900', '#6B7900', '#00C2A0', '#FFAA92', '#FF90C9',
              '#B903AA', '#D16100', '#DDEFFF', '#000035', '#7B4F4B',
              '#A1C299', '#300018', '#0AA6D8', '#013349', '#00846F',
              '#372101', '#FFB500', '#C2FFED', '#A079BF', '#CC0744',
              '#C0B9B2', '#C2FF99', '#001E09', '#00489C', '#6F0062',
              '#0CBD66', '#EEC3FF', '#456D75', '#B77B68', '#7A87A1',
              '#788D66', '#885578', '#FAD09F', '#FF8A9A', '#D157A0',
              '#BEC459', '#456648', '#0086ED', '#886F4C', '#34362D',
              '#B4A8BD', '#00A6AA', '#452C2C', '#636375', '#A3C8C9',
              '#FF913F', '#938A81', '#575329', '#00FECF', '#B05B6F',
              '#8CD0FF', '#3B9700', '#04F757', '#C8A1A1', '#1E6E00',
              '#7900D7', '#A77500', '#6367A9', '#A05837', '#6B002C',
              '#772600', '#D790FF', '#9B9700', '#549E79', '#FFF69F',
              '#201625', '#72418F', '#BC23FF', '#99ADC0', '#3A2465',
              '#922329', '#5B4534', '#FDE8DC', '#404E55', '#0089A3',
              '#CB7E98', '#A4E804', '#324E72', '#6A3A4C'
              ]

label = ['Google Search', 'YouTube', 'AdMob', 'Google Play', 'Google Cloud',
         'Other', 'Ad Revenue', 'Revenue', 'Gross Profit', 'Cost of Revenues',
         'Operating Profit', 'Operating Expenses', 'TAC', 'Others',
         'Net Profit', 'Tax', 'Other', 'R&D', 'S&M', 'G&A'
         ]

# Data
source = [0, 1, 2, 3, 4, 5]  # 6 Source Nodes
target = [6, 6, 6, 7, 7, 7]  # 2 Target Nodes
value = [39.5, 7.1, 7.9, 6.9, 6.9, 0.88]  # 6 Values

link = dict(source=source, target=target, value=value, color=color_link)
node = dict(label=label, pad=35, thickness=20)
data = go.Sankey(link=link, node=node)

# Setup our Plotly chart
fig = go.Figure(data)

# Upddate our chart with a title, font size and colour
# and the background colour of the chart
fig.update_layout(
    hovermode='x',
    title='1st Building Block - Revenue Sources',
    font=dict(size=10, color='white'),
    paper_bgcolor='#51504f'
)

# display our  Chart
fig.show()
