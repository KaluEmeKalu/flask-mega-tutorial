import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
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
SCATTER_OPTIONS = dict(size=12, alpha=0.5)
TOOLS="pan,wheel_zoom,box_zoom,reset,save"

data = lambda: [random.choice([i for i in range(100)]) for r in range(10)]

red = figure(sizing_mode='scale_width', tools=TOOLS, **PLOT_OPTIONS)
red.scatter(seasons.Year, seasons.ppg, color="red", **SCATTER_OPTIONS)


resources = INLINE.render()

script, div = components({'red': red})