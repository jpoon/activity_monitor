from sensor import *
import logging
import cairo
import CairoPlot 

class LineGraph:
    def __init__(self):
        pass

    def create(self, name, data, v_bounds = None):
        CairoPlot.dot_line_plot(name=name,
                                data=data,
                                width=800,
                                height=800,
                                axis=True,
                                grid=True,
                                v_bounds=v_bounds)
