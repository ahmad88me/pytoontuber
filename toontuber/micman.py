import sounddevice as sd
from threading import Thread
import numpy as np

class MicMan:

    def __init__(self):
        self.input_devices = self.read_devices()
        self.callback = None
        self.sensitivity = 1

    def read_devices(self):
        devs = sd.query_devices(device=None)
        input_devs = [d for d in devs if d['max_input_channels'] > 0]
        print(f"found input devices: {input_devs}")
        d = dict()
        for idx, dev in enumerate(input_devs):
            d[dev["index"]] = dev

        return d

    def get_device_from_user(self):
        print(f"You have to choose an input device: ")
        print(sd.query_devices())
        dev_id = input("Enter the index of the device you would like to choose: ")
        if not dev_id.isdigit():
            print(f"Error: Expecting a number.")
        elif int(dev_id) in self.input_devices:
            return int(dev_id)
        else:
            print(f"Error: Invalid device id.")
        return self.get_device_from_user()


    def capture_audio(self, dev_id):
        """
        Capture the audio
        """
        print(f"Creating a listening thread ...")
        t = Thread(target=self._sound_cap_thread, args=(dev_id,))
        t.start()



    def _sound_cap_thread(self, dev_id):
        """
        Sound monitoring thread
        """
        dev = self.input_devices[dev_id]
        with sd.InputStream(device=dev['index'],
                            samplerate=dev['default_samplerate'],
                            # channels=dev['max_input_channels'],
                            channels=1,
                            #dither_off=True, # to stop dither. It lowers the quality
                            callback=self._audio_callback):
            # print('#' * 80)
            # print('press Return to quit mic monitor')
            # print('#' * 80)
            # input()
            while True:
                sd.sleep(10000)

    def _audio_callback(self, indata, frames, time, status):
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
        if self.callback:
            self.callback(amp * self.sensitivity)
        # self.input_dev_battery.change_level(amp * self.input_dev_amp_scale)
        # self.post_audio_callback(amp)
