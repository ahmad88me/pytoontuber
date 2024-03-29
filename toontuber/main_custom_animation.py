"""
This interface supports custom animations. The second iteration will support the
change of animation based on the volumn and will have more improvements.
"""

from PIL import Image,ImageTk
from tkinter import NW, N, CENTER, RAISED, TOP, E
from tkinter import  Label, Button, Frame
from tkinter import filedialog
from tkinter import Tk, Canvas, PhotoImage
import math
from animation_bar import AnimationBar
from controls_bar import ControlsBar
import datetime
import keybind


from functools import partial
import cv2

# toon_view_width = 1200
# toon_view_height = 700

toon_view_width = 400
toon_view_height = 400

anim_grid_height = 200

# anim_vids = [None for _ in range(10)]


w_width = 400
w_height = w_width

MIN_WIN_DELTA = 2
MIN_TIME_DELTA_MSECS = 500

last_resize = datetime.datetime.now()

upload_img = None  # PhotoImage(file='upload.png')
window_resize_active=False
active_video_path = "/Users/aalobaid/Downloads/Tuber/Tuber/idlenormal.mp4"
active_video_fps = None

def on_window_resize(event):
    global last_resize, w_height, w_width, anim_bar
#    print("widget", event.widget)
#     print("height", event.height, "width", event.width)

    # w_height = event.height
    # w_width = root.winfo_width()
    # w_height = root.winfo_height()
    # print(f"Window Height: {event.height}")
    time_diff = datetime.datetime.now() - last_resize
    if abs(w_height - event.height) > MIN_WIN_DELTA and time_diff.microseconds > MIN_TIME_DELTA_MSECS:
        w_height = root.winfo_height()
        w_width = root.winfo_width()
        print(f"Resize event height: {event.height} height: {w_height} width: {w_width}")
        anim_bar.resize_buttons(w_height)
        last_resize = datetime.datetime.now()
    # else:
    #     print(f"Skip")
    # if True:
    # #if window_resize_active:
    #     print("widget", event.widget)
    #     print("height", event.height, "width", event.width)
    # else:
    #     print("resize is inactive")

def loop_video():
    global cap, active_video_path, active_video_fps
    # vpath = "/Users/aalobaid/Downloads/Tuber/Tuber/idlenormal.mp4"
    # vpath = "/Users/aalobaid/Downloads/Tuber/Tuber/talknormal.mp4"
    vpath = active_video_path
    cap = cv2.VideoCapture(vpath)
    active_video_fps = cap.get(cv2.CAP_PROP_FPS)
#cv2.GetCaptureProperty(cap, CV_CAP_PROP_FPS)
    print(f"FPS: {active_video_fps}")
# filename = filedialog.askopenfilename




def photo_image(img):
    h, w = img.shape[:2]
    data = f'P6 {w} {h} 255 '.encode() + img[..., ::-1].tobytes()
    return PhotoImage(width=w, height=h, data=data, format='PPM')



def update():
    global w_width, w_height, cap
    ret, img = cap.read()

    if ret:
        # image resize
        # w_width = root.winfo_width()
        # w_height = root.winfo_height()
        w_width = canvas.winfo_width()
        w_height = canvas.winfo_height()
        toon_view_width = min(w_width, w_height)
        toon_view_height = toon_view_width
        img = cv2.resize(img, (toon_view_width, toon_view_height))

        photo = photo_image(img)
        # canvas.create_image(0, 0, image=photo, anchor=NW)
        canvas.create_image(w_width/2 - toon_view_width/2, w_height/2 - toon_view_height/2, image=photo, anchor=NW)
        # canvas.create_image(0, 0, image=photo, anchor=NW)
        canvas.image = photo
    else:
        loop_video()
        # anim_bar.resize_buttons(400)
    wait_time = int(1000/active_video_fps)
    root.after(wait_time, update)

    # root.after(15, update)







# vpath = "/Users/aalobaid/Downloads/Tuber/Tuber/idlenormal.mp4"
# vpath = "/Users/aalobaid/Downloads/Tuber/Tuber/talknormal.mp4"

root = Tk()
root.title("Video")

# cap = cv2.VideoCapture(vpath)
loop_video()


canvas = Canvas(root, width=toon_view_width, height=toon_view_height)



# upload_img = Image.open('y.png')
# upload_img = Image.open('upload.png')

# image2 = deathwing.resize((100, 50), Image.ANTIALIAS)
# Deathwing2 = ImageTk.PhotoImage(image2)
#
# upload_img = PhotoImage(file='upload.png')
# draw_animation_grid()
canvas.grid(row=0, column=1, sticky="news")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
# canvas.pack(fill="both", expand=True)
#canvas.pack()
# draw_animation_grid()
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


root.bind('<Key>', key_press)
root.bind("<Configure>", on_window_resize)




update()
root.mainloop()
cap.release()