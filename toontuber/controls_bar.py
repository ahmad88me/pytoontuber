import numpy as np
from PIL import Image,ImageTk
from tkinter import NW, N, W, CENTER, RAISED, TOP, LEFT
from tkinter import StringVar
from tkinter import  Label, Button, Frame
# from tkinter import ttk
from tkinter.ttk import Combobox

from tkinter import filedialog
from tkinter import Tk, Canvas, PhotoImage

from threading import Thread


from functools import partial
import cv2
import util
import sounddevice as sd
from battery_widget import BatteryWidget


class ControlsBar():

    def __init__(self, thickness=100, bar_length=400, num_buttons=10):
        self.num_buttons = num_buttons
        self.buttons = []
        self.thickness = thickness
        self.bar_length = bar_length

        self.input_devices = dict()
        self.active_input_dev = None
        self.frame = None
        self.input_dev_combo = None
        self.input_dev_battery = None
        self.input_dev_thread = None
        self.input_dev_amp_scale = 10

    # def get_active_input_dev(self):
    #     return self.input_devices[self.active_input_dev]

    def read_input_devices(self):

        devs = sd.query_devices(device=None)
        input_devs = [d for d in devs if d['max_input_channels'] > 0]
        print(f"found input devices: {input_devs}")
        d = dict()
        for idx, dev in enumerate(input_devs):
            d[dev["name"]] = dev

        self.input_devices = d
        print(f"input devices dict: {self.input_devices}")

    def draw_input_devs(self, frame):
        names = list(self.input_devices.keys())
        combo = Combobox(frame, values=names, state='readonly', width=9)
        # combo['state'] = 'readonly'

        combo.set("Pick a mic")
        combo.bind('<<ComboboxSelected>>', self._input_dev_combo_callback)
        #combo.grid(column=grid_col, row=grid_row)
        #combo.pack()
        combo.grid(row=0, column=0, sticky=NW)
        self.input_dev_combo = combo

    def draw_input_battery(self, width):
        b = BatteryWidget(self.frame, width=width, grid_row=1, grid_column=0)
        b.draw_battery(width)
        self.input_dev_battery = b

    def draw_input_controls(self, root, grid_col, grid_row):
        self.frame = Frame(root, height=self.bar_length, width=self.thickness,
                           #bg="white",
                           highlightbackground="blue",
                           highlightthickness=4)
        self.frame.grid(column=grid_col, row=grid_row)
        self.draw_input_devs(self.frame)
        self.draw_input_battery(width=self.thickness)

    def _input_dev_combo_callback(self, event):
        print(f"Event: {event}")
        input_dev_id = self.input_dev_combo.current()
        print(f"Current: {input_dev_id}")
        self.active_input_dev = list(self.input_devices.keys())[input_dev_id]
        self.capture_audio()

    def set_input_device(self, dev_name):
        self.active_input_dev = dev_name

    def audio_callback(self, indata, outdata, frames, time, status):
        print(f"num of frames {frames}")
        # callback(indata: buffer, outdata: buffer, frames: int, time: CData, status: CallbackFlags)

    def capture_audio(self):
        print(f"Capture Audio {self.active_input_dev}")
        dev = self.input_devices[self.active_input_dev]
        print(f"Active device: {dev}")
        # t = Thread(target=sound_thread, args=(dev,))
        t = Thread(target=self.sound_thread, args=(dev,))

        t.run()
        if self.input_dev_thread:
            self.input_dev_thread.kill()
        self.input_dev_thread = t
        # stream = sd.RawInputStream(device=dev['name'],
        #                         channels=dev['max_input_channels'],
        #                         samplerate=dev['default_samplerate'], callback=audio_callback)
        # stream = sd.InputStream(device=dev['id'],
        #                         # channels=dev['max_input_channels']-1,
        #                         channels=1,
        #                         samplerate=dev['default_samplerate'], callback=audio_callback2)
        # stream = sd.InputStream(device=3,
        #                         # channels=dev['max_input_channels']-1,
        #                         channels=1,
        #                         samplerate=44100.0,
        #                         callback=audio_callback2)

    def sound_thread(self, dev):
        with sd.InputStream(device=dev['index'],
                            samplerate=dev['default_samplerate'],
                            channels=dev['max_input_channels'], callback=self.audio_callback):
            print('#' * 80)
            print('press Return to quit')
            print('#' * 80)
            input()

    def audio_callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        downsample = 10
        if status:
            print(status, file=sys.stderr)
        # # Fancy indexing with mapping creates a (necessary!) copy:
        # q.put(indata[::args.downsample, mapping])

        # print(f"out num of frames {frames}")
        max_num = np.max(indata)
        min_num = np.min(indata)
        amp = max(max_num, -min_num)
        # print(f"amp {amp} max {np.max(indata)} min {np.min(indata)}")
        self.input_dev_battery.change_level(amp * self.input_dev_amp_scale)

# def audio_callback2(indata, frames, time, status):
#     """This is called (from a separate thread) for each audio block."""
#     downsample = 10
#     if status:
#         print(status, file=sys.stderr)
#     # # Fancy indexing with mapping creates a (necessary!) copy:
#     # q.put(indata[::args.downsample, mapping])
#
#     print(f"out num of frames {frames}")


# def audio_callback(indata, outdata, frames, time, status):
#     print(f"out num of frames {frames}")


# def sound_thread(dev):
#     with sd.InputStream(device=dev['index'],
#                   samplerate=dev['default_samplerate'],
#                   channels=dev['max_input_channels'], callback=audio_callback2):
#         print('#' * 80)
#         print('press Return to quit')
#         print('#' * 80)
#         input()