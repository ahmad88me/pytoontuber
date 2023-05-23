

import pyaudio

audio = pyaudio.PyAudio()

info = audio.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
        if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))


# dev = audio.get_device_info_by_host_api_device_index(0, 0)
dev = audio.get_device_info_by_index(0)
print(f"device is: {dev}")

def callback(in_data, frame_count, time_info, status):
    global dev
    # data = dev.readframes(frame_count)
    print(f"frame_count: {frame_count}")
    print(f"time_info: {time_info}")
    print(f"status: {status}")
    print("#" * 80)
    data = in_data
    # If len(data) is less than requested frame_count, PyAudio automatically
    # assumes the stream is finished, and the stream stops.
    return (data, pyaudio.paContinue)

stream = audio.open(format=audio.get_format_from_width(1),
            #format=pyaudio.paInt16,
             #format=audio.get_format_from_width(dev.getsampwidth()),
                input_device_index=0,
                # format=audio.get_format_from_width(dev.getsampwidth()),
                channels=dev['maxInputChannels'],
                rate=int(dev['defaultSampleRate']),
                input=True,
                stream_callback=callback)