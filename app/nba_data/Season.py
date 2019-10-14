
import numpy as np
import pandas as pd
from bokeh.plotting import figure
from bokeh.plotting import ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.models import HoverTool
from bokeh.layouts import row, column
from bokeh.io import curdoc
from bokeh.layouts import widgetbox
from bokeh.models import Slider, Select


class Season:
    def __init__(self, seasons_csv='app/nba_data/Seasons_Stats.csv', players_csv='app/nba_data/Players.csv'):
        self.seasons_csv = seasons_csv
        self.players_csv = players_csv
        self._df = None

    @property
    def df(self):
        return self._df or self._get_seasons_df()
    

    def _get_seasons_df(self, players_csv=None, seasons_csv=None):
        players_csv = players_csv or self.players_csv
        seasons_csv = seasons_csv or self.seasons_csv

        players = pd.read_csv(players_csv)
        seasons = pd.read_csv(seasons_csv)

        players.drop(players.columns[0], axis=1, inplace=True)
        seasons.drop(seasons.columns[0], axis=1, inplace=True)

        players.dropna(how="all", inplace=True)
        seasons.dropna(how="all", inplace=True)
        players = players[players.birth_city.notnull()]
        self._df = seasons

        return seasons

    @property
    def seasons_1990_on(self):
        return self.get_seasons_1990_on()
    
    def get_seasons_1990_on(self):
        seasons = self.df
        seasons_1990_on = seasons[seasons.Year >= 1990]
        seasons_1990_on = seasons_1990_on[
            (seasons_1990_on["3P%"].notnull())
            & (seasons_1990_on["3P%"] > 0)
            & (seasons_1990_on["3P"].notnull())
            & (seasons_1990_on["3P"] > 0)
            & (seasons_1990_on["3PA"].notnull())
            & (seasons_1990_on["3PA"] > 0)
            & (seasons_1990_on["GS"] > 0)
            & (seasons_1990_on["G"].notnull())
            & (seasons_1990_on["G"] > 0)
            & (seasons_1990_on["2PA"].notnull())
            & (seasons_1990_on["2PA"] > 0)
            & (seasons_1990_on["2P"].notnull())
            & (seasons_1990_on["2P"] > 0)
        ]

        new_index = np.arange(0, len(seasons_1990_on)).tolist()
        seasons_1990_on.index = new_index
        return seasons_1990_on

    @staticmethod
    def get_color_dict():
        color_dict = {
            "VAN": "Blue",
            "MIL": "Red",
            "LAC": "Yellow",
            "BOS": "Purple",
            "SAC": "Silver",
            "HOU": "Magenta",
            "POR": "Green",
            "CHI": "CornFlowerBlue",
            "ORL": "Chocolate",
            "SEA": "Coral",
            "GSW": "Crimson",
            "TOR": "DarkCyan",
            "TOT": "Gold",
            "MIA": "GreenYellow",
            "MIN": "HotPink",
            "LAL": "Khaki",
            "NJN": "Lavender",
            "DAL": "LightSkyBlue",
            "PHO": "Orange",
            "NYK": "MediumAquamarine",
            "CHH": "OrangeRed",
            "IND": "PaleVioletRed",
            "SAS": "SpringGreen",
            "UTA": "YellowGreen",
            "CLE": "RoyalBlue",
            "WAS": "SteelBlue",
            "DEN": "RoseBrown",
            "DET": "IndianRed",
            "PHI": "Salmon",
            "ATL": "DarkOrchid",
            "MEM": "Tomato",
            "NOH": "DarkKhaki",
            "CHA": "MediumSeaGreen",
            "NOK": "OliveDrab",
            "OKC": "Orange",
            "BRK": "Blue",
            "NOP": "PowderBlue",
            "CHO": "Navy",
        }
        return color_dict

    @staticmethod
    def get_palette():
        palette = [
            "aliceblue",
            "antiquewhite",
            "aqua",
            "aquamarine",
            "azure",
            "beige",
            "bisque",
            "black",
            "blanchedalmond",
            "blue",
            "blueviolet",
            "brown",
            "burlywood",
            "cadetblue",
            "chartreuse",
            "chocolate",
            "coral",
            "cornflowerblue",
            "cornsilk",
            "crimson",
            "cyan",
            "darkblue",
            "darkcyan",
            "darkgoldenrod",
            "darkgray",
            "darkgreen",
            "darkkhaki",
            "darkmagenta",
            "darkolivegreen",
            "darkorange",
            "darkorchid",
            "darkred",
            "darksalmon",
            "darkseagreen",
            "darkslateblue",
            "darkslategray",
            "darkturquoise",
            "darkviolet",
            "red",
        ]
        return palette
