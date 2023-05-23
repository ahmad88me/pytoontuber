import numpy as np
from threading import Thread
import sounddevice as sd


class AudioMonitor:

    def __init__(self ):
        devs = sd.query_devices(device=None)
        input_devs = [d for d in devs if d['max_input_channels'] > 0]
        print(f"found input devices: {input_devs}")
        d = dict()
        for idx, dev in enumerate(input_devs):
            d[dev["name"]] = dev

        self.input_devices = d
        print(f"input devices dict: {self.input_devices}")
        self.input_dev_thread = None

    def monitor_dev(self, dev_id):
        self.active_input_dev = list(self.input_devices.keys())[dev_id]
        self.capture_audio()

    def _sound_thread(self, dev):
        """
        Sound monitoring thread
        """
        with sd.InputStream(device=dev['index'],
                            samplerate=dev['default_samplerate'],
                            channels=1,
                            dither_off=True, # to stop dither. It lowers the quality
                            callback=self.audio_callback):
            print('#' * 80)
            print('press Return to quit mic monitor')
            print('#' * 80)
            # input()
            while True:
                sd.sleep(10000)

    def audio_callback(self, indata, frames, time, status):
        """
        This is called (from a separate thread) for each audio block.
        """
        downsample = 10
        if status:
            print(status, file=sys.stderr)

        if indata.shape[0] == 0:
            print(f"empty")
            return
        max_num = np.max(indata)
        min_num = np.min(indata)
        amp = max(max_num, -min_num)
        print(f" amp: {amp}")

    def capture_audio(self):
        """
        Create a thread to listen and monitor mic data
        """
        print(f"Capture Audio {self.active_input_dev}")
        dev = self.input_devices[self.active_input_dev]
        print(f"Active device: {dev}")
        if self.input_dev_thread:
            self.input_dev_thread.kill()

        t = Thread(target=self._sound_thread, args=(dev,))
        t.start()
        self.input_dev_thread = t


amon = AudioMonitor()
amon.monitor_dev(0)

