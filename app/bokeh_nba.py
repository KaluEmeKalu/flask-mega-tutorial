""" Take from https://www.kaggle.com/drgilermo/goats-the-greatest-players-of-all-time
"""

import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import random


from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE


players_path = 'app/nba_data/Players.csv'
season_path = 'app/nba_data/Seasons_Stats.csv'
players = pd.read_csv(players_path)
seasons = pd.read_csv(season_path)
seasons['ppg'] = seasons.PTS/seasons.G




########## BUILD FIGURES ################

PLOT_OPTIONS = dict(plot_width=800, plot_height=300)
SCATTER_OPTIONS = dict(size=6, alpha=0.5)
TOOLS="pan,wheel_zoom,box_zoom,reset,save"

data = lambda: [random.choice([i for i in range(100)]) for r in range(10)]

red = figure(sizing_mode='scale_width', tools=TOOLS, **PLOT_OPTIONS)
red.scatter(seasons.Year, seasons.ppg, color="red", **SCATTER_OPTIONS)

# 
jordan_years = seasons.Year[seasons.Player == 'Michael Jordan*']
jordan_ppg = seasons.ppg[seasons.Player == 'Michael Jordan*']
lebron_years = seasons.Year[seasons.Player == 'Lebron James']
lebron_ppg = seasons.ppg[seasons.Player == 'Lebron James']
wilt_years = seasons.Year[seasons.Player == 'Wilt Chamberlain*']
wilt_ppg = seasons.ppg[seasons.Player == 'Wilt Chamberlain*']




red.line(jordan_years, jordan_ppg, legend="Jordan", line_color="orange", line_dash="4 4")
red.circle(jordan_years, jordan_ppg, legend="Jordan", fill_color="orange", line_color="orange", size=6)


red.circle(wilt_years, wilt_ppg, legend="Wilt", fill_color="blue", line_color="blue", size=6)
red.line(wilt_years, wilt_ppg, legend="Wilt", line_color="blue")

resources = INLINE.render()

script, div = components({'red': red})