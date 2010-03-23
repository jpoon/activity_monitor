from sensor import *
import logging
import cairo
import CairoPlot 

class LineGraph:
    def __init__(self):
        pass

    def create(self, name, data):
        CairoPlot.dot_line_plot(name=name,
                                data=data,
                                width=1000,
                                height=1000,
                                axis=True)

