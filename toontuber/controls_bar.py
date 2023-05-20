import numpy as np
from PIL import Image,ImageTk
from tkinter import NW, N, W, CENTER, RAISED, TOP, LEFT
from tkinter import StringVar
from tkinter import  Label, Button, Frame, Scale
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

    def __init__(self, thickness=100, bar_length=400, num_buttons=10, other_frames=[]):
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
        self.hide_button = None
        self.other_frames = other_frames
        self.amp_scale = None

    def append_frame(self, frame):
        self.other_frames.append(frame)

    def _amp_scale_callback(self, event):
        print(f" new amp scale value: {self.amp_scale.get()}")
        self.input_dev_amp_scale = self.amp_scale.get()

    def _draw_amp_scale(self):
        scale = Scale(self.frame, label="Sensitivity", from_=1, to=30, command=self._amp_scale_callback)
        self.amp_scale = scale
        scale.grid(row=4, column=0)

    def _draw_hide_button(self):
        self.hide_button = Button(self.frame, text="Hide", command=self.hide_frame)
        self.hide_button.grid(row=2, column=0)

    def hide_frame(self):
        self.frame.grid_forget()
        for f in self.other_frames:
            f.grid_forget()

    def read_input_devices(self):
        """
        Fetch input mics and store them locally
        """
        devs = sd.query_devices(device=None)
        input_devs = [d for d in devs if d['max_input_channels'] > 0]
        print(f"found input devices: {input_devs}")
        d = dict()
        for idx, dev in enumerate(input_devs):
            d[dev["name"]] = dev

        self.input_devices = d
        print(f"input devices dict: {self.input_devices}")

    def _draw_input_devs(self, frame):
        """
        To draw the Combobox that lists the available mics
        """
        names = list(self.input_devices.keys())
        combo = Combobox(frame, values=names, state='readonly', width=9)
        combo.set("Pick a mic")
        combo.bind('<<ComboboxSelected>>', self._input_dev_combo_callback)
        combo.grid(row=0, column=0, sticky=NW)
        self.input_dev_combo = combo

    def _draw_input_battery(self, width):
        """
        Draw the Battery Widget for the mic monitor
        """
        b = BatteryWidget(self.frame, width=width, grid_row=1, grid_column=0)
        b.draw_battery(width)
        self.input_dev_battery = b

    def draw_input_controls(self, root, grid_col, grid_row):
        """
        To draw all controll
        """
        self.frame = Frame(root, height=self.bar_length, width=self.thickness,
                           #bg="white",
                           highlightbackground="blue",
                           highlightthickness=4)
        self.frame.grid(column=grid_col, row=grid_row)
        self._draw_input_devs(self.frame)
        self._draw_input_battery(width=self.thickness)
        self._draw_hide_button()
        self._draw_amp_scale()

    def _input_dev_combo_callback(self, event):
        print(f"Event: {event}")
        input_dev_id = self.input_dev_combo.current()
        print(f"Current: {input_dev_id}")
        self.active_input_dev = list(self.input_devices.keys())[input_dev_id]
        self.capture_audio()

    def set_input_device(self, dev_name):
        self.active_input_dev = dev_name

    def capture_audio(self):
        """
        Create a thread to listen and monitor mic data
        """
        print(f"Capture Audio {self.active_input_dev}")
        dev = self.input_devices[self.active_input_dev]
        print(f"Active device: {dev}")
        t = Thread(target=self._sound_thread, args=(dev,))

        t.run()
        if self.input_dev_thread:
            self.input_dev_thread.kill()
        self.input_dev_thread = t

    def _sound_thread(self, dev):
        """
        Sound monitoring thread
        """
        with sd.InputStream(device=dev['index'],
                            samplerate=dev['default_samplerate'],
                            channels=dev['max_input_channels'], callback=self.audio_callback):
            print('#' * 80)
            print('press Return to quit mic monitor')
            print('#' * 80)
            input()

    def audio_callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        downsample = 10
        if status:
            print(status, file=sys.stderr)

        max_num = np.max(indata)
        min_num = np.min(indata)
        amp = max(max_num, -min_num)
        self.input_dev_battery.change_level(amp * self.input_dev_amp_scale)
        self.post_audio_callback(amp)

    def post_audio_callback(self, amp):
        amp = amp * self.input_dev_amp_scale
        print(f"amp {amp}")
        # if amp < 0.1:
        #     print("idle")
        # elif amp < 0.3:
        #     print("talk")
        # elif amp < 0.6:
        #     print("peak")
        # else:
        #     print(f"scream {amp}")

