import pyaudio      #for capturing the audio-signal
import struct       #for converting the binary-data from the signal to integer
import matplotlib.pyplot as plt     #for displaying the audio-signal

import numpy as np
import time

#functions
def plot_setup():
    # create matplotlib figure and axes
    fig=plt.figure()
    ax=fig.add_subplot(111)

    # variable for plotting
    x = np.arange(0, 2 * CHUNK, 2)

    # create a line object with random data
    line, = ax.plot(x, [128 for i in range(2048)], '-')

    # basic formatting for the axes
    ax.set_title('AUDIO WAVEFORM')
    ax.set_xlabel('samples')
    ax.set_ylabel('volume')
    ax.set_ylim(0, 255)
    ax.set_xlim(0, 2 * CHUNK)
    plt.xticks([0, CHUNK, 2 * CHUNK])
    plt.yticks([0, 128, 255])
    # show the plot
    plt.show(block=False)
    return fig, line

def measure():
    # binary data
    data = stream.read(CHUNK)

    # convert data to integers, make np array, then offset it by 127
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)

    # create np array and offset by 128
    data_np = np.array(data_int, dtype='b')[::2]
    data_np = [i+127 for i in data_np]

    line.set_ydata(data_np)
    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
    except:
        return 0

# constants
CHUNK = 1024 * 2             # samples per frame
FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 44100                 # samples per second

# pyaudio class instance
mic = pyaudio.PyAudio()

# stream object to get data from microphone
stream = mic.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    input_device_index=0,
    frames_per_buffer=CHUNK
)

if __name__=="__main__":
    fig, line=plot_setup()
    while True:
        m=measure()
        if m==0:
            break