"""
Taken from https://github.com/bokeh/bokeh/blob/1.3.4/examples/embed/embed_multiple_responsive.py
"""
import random

from jinja2 import Template

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.browser import view

########## BUILD FIGURES ################

PLOT_OPTIONS = dict(plot_width=800, plot_height=300)
SCATTER_OPTIONS = dict(size=12, alpha=0.5)
TOOLS="pan,wheel_zoom,box_zoom,reset,save"

data = lambda: [random.choice([i for i in range(100)]) for r in range(10)]

red = figure(sizing_mode='scale_width', tools=TOOLS, **PLOT_OPTIONS)
red.scatter(data(), data(), color="red", **SCATTER_OPTIONS)

blue = figure(sizing_mode='scale_width', tools=TOOLS, **PLOT_OPTIONS)
blue.scatter(data(), data(), color="blue", **SCATTER_OPTIONS)

green = figure(sizing_mode='scale_width', tools=TOOLS, **PLOT_OPTIONS)
green.scatter(data(), data(), color="green", **SCATTER_OPTIONS)


resources = INLINE.render()

script, div = components({'red': red, 'blue': blue, 'green': green})
