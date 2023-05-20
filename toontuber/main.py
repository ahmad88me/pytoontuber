from PIL import Image,ImageTk
from tkinter import NW, N, CENTER, RAISED, TOP, E
from tkinter import  Label, Button, Frame
from tkinter import filedialog
from tkinter import Tk, Canvas, PhotoImage
import math
from animation_bar import AnimationBar
from controls_bar import ControlsBar
from animan import AnimationManager
import datetime
import keybind
import argparse
import queue
from functools import partial
import cv2

toon_view_width = 400
toon_view_height = 400

anim_grid_height = 200



w_width = 400
w_height = w_width

MIN_WIN_DELTA = 2
MIN_TIME_DELTA_MSECS = 500

last_resize = datetime.datetime.now()

upload_img = None
window_resize_active=False
active_video_path = "/Users/aalobaid/Downloads/Tuber/Tuber/idlenormal.mp4"
active_video_fps = 1000

#anime_q = queue.Queue()
anime_q = []
curr_action = "idle"
anime_manager = AnimationManager()

def on_window_resize(event):
    global last_resize, w_height, w_width, anim_bar

    time_diff = datetime.datetime.now() - last_resize
    if abs(w_height - event.height) > MIN_WIN_DELTA and time_diff.microseconds > MIN_TIME_DELTA_MSECS:
        w_height = root.winfo_height()
        w_width = root.winfo_width()
        print(f"Resize event height: {event.height} height: {w_height} width: {w_width}")
        anim_bar.resize_buttons(w_height)
        last_resize = datetime.datetime.now()

def loop_video(vpath=None):
    global cap, active_video_path, active_video_fps
    if vpath is None:
        vpath = active_video_path
    else:
        active_video_path = vpath
    cap = cv2.VideoCapture(vpath)
    active_video_fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"FPS: {active_video_fps}")




def photo_image(img):
    h, w = img.shape[:2]
    data = f'P6 {w} {h} 255 '.encode() + img[..., ::-1].tobytes()
    return PhotoImage(width=w, height=h, data=data, format='PPM')



def update():
    global w_width, w_height, cap
    ret, img = cap.read()

    if ret:
        w_width = canvas.winfo_width()
        w_height = canvas.winfo_height()
        toon_view_width = min(w_width, w_height)
        toon_view_height = toon_view_width
        img = cv2.resize(img, (toon_view_width, toon_view_height))

        photo = photo_image(img)
        canvas.create_image(w_width/2 - toon_view_width/2, w_height/2 - toon_view_height/2, image=photo, anchor=NW)
        canvas.image = photo
    else:
        # if anime_q.empty():
        if not anime_q:
            print(f"queue is empty")
            loop_video()
        else:
            # vpath = anime_q.get(block=True)
            vpath = anime_q.pop(0)
            print(f"getting a new vpath: {vpath}")
            loop_video(vpath)
    wait_time = int(1000/active_video_fps)
    root.after(wait_time, update)


root = Tk()
root.title("Video")
loop_video()


canvas = Canvas(root, width=toon_view_width, height=toon_view_height)



canvas.grid(row=0, column=1, sticky="news")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)


anim_bar = AnimationBar()
anim_bar.draw_animation_grid(root, grid_col=2, grid_row=0)

cont_bar = ControlsBar(other_frames=[anim_bar.frame])
cont_bar.read_input_devices()
cont_bar.draw_input_controls(root, grid_col=0, grid_row=0)

def key_press(event):
    key = event.char
    print(f"'{key}' is pressed")
    action_name = keybind.get_action(key)
    if action_name:
        take_action(action_name)
    if key=='u':
        cont_bar.input_dev_battery.change_level(cont_bar.input_dev_battery.level + 0.1)
    elif key=='l':
        cont_bar.input_dev_battery.change_level(cont_bar.input_dev_battery.level - 0.1)


def take_action(action_name):
    global active_video_path
    print(f"Doing action {action_name}")
    print(type(action_name))
    if action_name.isdigit():
        open_anim_id = int(action_name)
    if 0 <= open_anim_id <= 9:
        print(f"Run animation {open_anim_id}")
        vpath = anim_bar.get_vid(open_anim_id)
        if vpath:
            active_video_path = vpath
            print(f"Change active video to {vpath}")
            loop_video()

def audio_to_action(amp):
    global anime_manager, anime_q, curr_action

    if amp < 0.05:
        action = "idle"
    # else:
    #     action = "talk"
    elif amp < 0.7:
        action = "talk"
    else:
        action = "peak"

    print(f"audio to action: {action}")
    print(f"curr action{curr_action} and new action {action}")
    if anime_q and curr_action not in ["idle"]:
    # if not anime_q.empty() and curr_action not in ["idle", "set"]:
        print(f"queue is not empty {anime_q} and curr_action {curr_action}")
        return

    if curr_action == action:
        return
    # if curr_action == "idle" and action != "idle"

    # set_vpath = anime_manager.get_action_vid("set")
    # loop_video(vpath)
    # anime_q.queue.clear()
    anime_q = []
    vpath = anime_manager.get_action_vid(action)
    loop_video(vpath)
    # anime_q = [set_vpath, vpath]
    # anime_q = [vpath]

    curr_action = action
    # anime_q.put(set_vpath, block=True)
    # anime_q.put(vpath, block=True)


def parse():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--videos', nargs='+', help='the list of videos to be utilised')
    args = parser.parse_args()
    return args.videos

def main():
    global root, cap, anime_manager
    videos = parse()
    anime_manager.organise(videos)
    cont_bar.amp_ext_callback = audio_to_action
    root.bind('<Key>', key_press)
    root.bind("<Configure>", on_window_resize)
    update()
    root.mainloop()
    cap.release()

if __name__ == "__main__":
    main()


