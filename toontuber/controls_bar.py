
from PIL import Image,ImageTk
from tkinter import NW, N, CENTER, RAISED, TOP
from tkinter import  Label, Button, Frame
# from tkinter import ttk
from tkinter.ttk import Combobox

from tkinter import filedialog
from tkinter import Tk, Canvas, PhotoImage

from functools import partial
import cv2
import util
import sounddevice as sd

class ControlsBar():

    def __init__(self, thickness=200, bar_length=400, num_buttons=10):
        self.num_buttons = num_buttons
        self.buttons = []
        self.thickness = thickness
        self.bar_length = bar_length

        self.input_devices = dict()
        self.active_input_dev = None
        self.frame = None

    def read_input_devices(self):

        devs = sd.query_devices(device=None)
        input_devs = [d for d in devs if d['max_input_channels'] > 0]
        print(f"found input devices: {input_devs}")
        d = dict()
        for dev in input_devs:
            d[dev["name"]] = dev
        self.input_devices = d
        print(f"input devices dict: {self.input_devices}")

    def draw_input_devs(self, frame):
        names = list(self.input_devices.keys())
        combo = Combobox(frame, values=names)
        combo.set("Pick a mic")
        combo.bind('<<ComboboxSelected>>', self.combo_callback)
        #combo.grid(column=grid_col, row=grid_row)
        combo.pack()



    def draw_input_controls(self, root, grid_col, grid_row):
        self.frame = Frame(root, height=self.bar_length, width=self.thickness)
        self.frame.grid(column=grid_col, row=grid_row)
        self.draw_input_devs(self.frame)


    def combo_callback(self, event):
        print(f"Event: {event}")

    def set_input_device(self, dev_name):
        self.active_input_dev = dev_name