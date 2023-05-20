

import math
from tkinter import Canvas
from tkinter import BOTH

class BatteryWidget():
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, widgetName="battery", **kwargs)
    #     # self.bins = 10
    #     # self.canvas = Canvas(100, 100)
    def __init__(self, master, grid_row, grid_column, width, bins=10):
        self.master = master
        self.recs = []
        self.level = 1
        self.active_bins = bins
        self.bins = bins
        self.active_color = "#0A0"
        self.inactive_color = "#252"
        self.grid_row = grid_row
        self.grid_column = grid_column
        self.canvas = Canvas(self.master, width=width, height=width)
        print(f"Battery Widget width: {width}")
        # self.canvas = Canvas(self.master)

        self.width = width


    def draw_battery(self, width=None):
        if width:
            self.width = width
        self.canvas.delete()
        # h = 20
        # w = self.thickness
        w = self.width/2
        h = int(self.width/(self.bins+1))

        # print(f"The master width is: {self.width}")
        # print(f"The x position: {self.width/2 - w/2} with canvas width {self.width} and bin width {w}")
        for bi in range(self.bins):
            x0 = self.width/2 - w/2
            x1 = x0 + w
            y0 = (bi+1) * h
            y1 = (bi+2) * h
            if bi >= (self.bins - self.active_bins):
                color = self.active_color
            else:
                color = self.inactive_color
            r = self.canvas.create_rectangle(x0, y0, x1, y1,  outline="#0f0", fill=color, width=1)
            self.recs.append(r)
        # canvas.create_rectangle(150, 10, 240, 80,
        #                         outline="#f50", fill="#f50")
        # canvas.create_rectangle(270, 10, 370, 80,
        #                         outline="#05f", fill="#05f")
        # canvas.pack(fill=BOTH, expand=1)
        #canvas.pack(fill=BOTH, expand=1)
        self.canvas.grid(row=self.grid_row, column=self.grid_column)

    def change_level(self, level):
        if 0 <= level <= 1:
            self.active_bins = round(self.bins * level)
            self.level = level
            # print(f"active bins: {self.active_bins}")
            self.draw_battery()
        elif level > 1:
            self.active_bins = self.bins
            self.level = 1
            self.draw_battery()


