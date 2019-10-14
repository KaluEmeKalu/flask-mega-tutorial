"""  https://www.kaggle.com/kevinchiha/interactive-bokeh-plot-nba-dataset/data
"""

from bokeh.plotting import figure
from bokeh.plotting import ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.models import HoverTool
from bokeh.layouts import row, column
from bokeh.layouts import widgetbox
from bokeh.models import Slider, Select
from app.nba_data.Season import Season


def modify_doc(doc):
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    season = Season()
    seasons_1990_on = season.seasons_1990_on

    source = ColumnDataSource(
        data={
            "x_3p": seasons_1990_on["3PA"],
            "y_3p": seasons_1990_on["3P"],
            "Tm": seasons_1990_on["Tm"],
            "x_2p": seasons_1990_on["2PA"],
            "y_2p": seasons_1990_on["2P"],
            "Year": seasons_1990_on["Year"],
            "Player": seasons_1990_on["Player"],
        }
    )


    slider = Slider(title="Year", start=1990, end=2017, step=1, value=2006)
    menu_options_list = ["ALL"] + seasons_1990_on["Tm"].unique().tolist()
    menu = Select(options=menu_options_list, value="ALL", title="Team")

    palette = season.get_palette()
    color_mapper = CategoricalColorMapper(
        factors=seasons_1990_on["Tm"].unique().tolist(),
        palette=palette
    )

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    p1 = figure(
        x_axis_label="3 Points Attempted",
        y_axis_label="3 Points Made",
        tools=TOOLS
    )
    p2 = figure(
        x_axis_label="2 Points Attempted",
        y_axis_label="2 Points Made",
        tools=TOOLS
    )



    ###################
    p1.circle(
        "x_3p",
        "y_3p",
        source=source,
        alpha=0.8,
        nonselection_alpha=0.1,
        color=dict(field="Tm", transform=color_mapper),
        legend="Tm",
    )

    p1.legend.location = "bottom_right"
    ####################

    ####################
    p2.circle(
        "x_2p",
        "y_2p",
        source=source,
        alpha=0.8,
        nonselection_alpha=0.1,
        color=dict(field="Tm", transform=color_mapper),
        legend="Tm",
    )

    p2.legend.location = "bottom_right"
    #######################

    hover1 = HoverTool(tooltips=[("Player", "@Player")])
    p1.add_tools(hover1)
    hover2 = HoverTool(tooltips=[("Player", "@Player")])
    p2.add_tools(hover2)

    column1 = column(widgetbox(menu), widgetbox(slider))
    layout = row(column1, p1, p2)

    doc.add_root(layout)

    def callback(attr, old, new):
        if menu.value == "ALL":

            new_x_3p = seasons_1990_on[(seasons_1990_on["Year"] == slider.value)]["3PA"]
            new_y_3p = seasons_1990_on[(seasons_1990_on["Year"] == slider.value)]["3P"]
            new_tm = seasons_1990_on[(seasons_1990_on["Year"] == slider.value)]["Tm"]
            new_x_2p = seasons_1990_on[(seasons_1990_on["Year"] == slider.value)]["2PA"]
            new_y_2p = seasons_1990_on[(seasons_1990_on["Year"] == slider.value)]["2P"]
            new_year = seasons_1990_on[(seasons_1990_on["Year"] == slider.value)][
                "Year"
            ]
            new_player = seasons_1990_on[(seasons_1990_on["Year"] == slider.value)][
                "Player"
            ]
        else:
            new_x_3p = seasons_1990_on[(seasons_1990_on["Year"] == slider.value)]["3PA"]
            new_y_3p = seasons_1990_on[
                (seasons_1990_on["Year"] == slider.value)
                & (seasons_1990_on["Tm"] == menu.value)
            ]["3P"]
            new_tm = seasons_1990_on[
                (seasons_1990_on["Year"] == slider.value)
                & (seasons_1990_on["Tm"] == menu.value)
            ]["Tm"]
            new_x_2p = seasons_1990_on[
                (seasons_1990_on["Year"] == slider.value)
                & (seasons_1990_on["Tm"] == menu.value)
            ]["2PA"]
            new_y_2p = seasons_1990_on[
                (seasons_1990_on["Year"] == slider.value)
                & (seasons_1990_on["Tm"] == menu.value)
            ]["2P"]
            new_year = seasons_1990_on[
                (seasons_1990_on["Year"] == slider.value)
                & (seasons_1990_on["Tm"] == menu.value)
            ]["Year"]
            new_player = seasons_1990_on[
                (seasons_1990_on["Year"] == slider.value)
                & (seasons_1990_on["Tm"] == menu.value)
            ]["Player"]

        source.data = {
            "x_3p": new_x_3p,
            "y_3p": new_y_3p,
            "Tm": new_tm,
            "x_2p": new_x_2p,
            "y_2p": new_y_2p,
            "Year": new_year,
            "Player": new_player,
        }

    slider.on_change("value", callback)
    menu.on_change("value", callback)
