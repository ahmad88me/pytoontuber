# pytoontuber

A simple app to choose different animation files. It uses animation files when you are talking and uses the idle video animation when you are not. This is inspired by [this video](https://www.youtube.com/watch?v=i-yW-3dI1oE&t=151s) which was published by [ScottFalco](https://www.youtube.com/@ScottFalco). 

## Installation
You only need to download the libraries in the `requirements.txt`. You can use `pip` as follows:
```
pip install -r requirements.txt
```
*Note: this is developed using python3.* 

## OS and other requirements
This has only been tested on MacOS. However, the libraries used also works with other
operating systems.

## How to use it
You just need to run the `main.py` using the terminal or CMD (command line interface). 
You need to pass the videos to be used and the device index. If the device index is not passed, it will list the devices and you should pick the mic that you want to use (make sure that no other processes are actually using it may produce an error).

```
usage: main.py [-h] -v VIDEOS [VIDEOS ...] [-d DEVICE] [-s [0-50]]

options:
  -h, --help            show this help message and exit
  -v VIDEOS [VIDEOS ...], --videos VIDEOS [VIDEOS ...]
                        the list of videos to be utilised
  -d DEVICE, --device DEVICE
                        The index of the number. This should be an integer
  -s [0-50], --sensitivity [0-50]
                        How sensitive are the mics
```

### Arguments
Below we explain the different arguments

#### Videos
The videos should follow the same naming presented in the video. They are expected to start with either `idle`, `peak`, and `talk`. Something like this:
```
idlenormal.mp4
peaknormal.mp4
talknormal.mp4
```
Note that you can also use regex to pass the files (e.g., `python main.py -v myvids/*mp4`)
The `idle` is activated when there is barely voice coming in through the mic. The `talk` is when there is some. The `peak` is when the voice is so loud, like screaming.

Also note that you can add multiple versions of the same action. For example, `talknormal.mp4` and `talknormal2.mp4`. This way, the app will randomly select one of them each time. This might be helpful for people who wants to add more variety.

#### Sensitivity
This is how sensitive the mics are. By default, it is 1. But you are either pass the sensitivity as a parameter or you can also adjust it while using the application. While the 
app window is active, you can click the "s" key and then click on the "+" or "-" to raise or lower the sensitivity. 
