from PIL import Image,ImageTk
from tkinter import NW, N, CENTER, RAISED, TOP
from tkinter import  Label, Button, Frame
from tkinter import filedialog
from tkinter import Tk, Canvas, PhotoImage
from animation_bar import AnimationBar
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

upload_img = None  # PhotoImage(file='upload.png')

active_video_path = "/Users/aalobaid/Downloads/Tuber/Tuber/idlenormal.mp4"



def loop_video():
    global cap, active_video_path
    # vpath = "/Users/aalobaid/Downloads/Tuber/Tuber/idlenormal.mp4"
    # vpath = "/Users/aalobaid/Downloads/Tuber/Tuber/talknormal.mp4"
    vpath = active_video_path
    cap = cv2.VideoCapture(vpath)

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
        w_width = root.winfo_width()
        w_height = root.winfo_height()
        toon_view_width = min(w_width, w_height)
        toon_view_height = toon_view_width
        img = cv2.resize(img, (toon_view_width, toon_view_height))

        photo = photo_image(img)
        # canvas.create_image(0, 0, image=photo, anchor=NW)
        canvas.create_image(w_width/2 - toon_view_width/2, w_height/2 - toon_view_height/2, image=photo, anchor=NW)

        canvas.image = photo
    else:
        loop_video()

    # draw_animation_grid()

    root.after(15, update)







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


def key_press(event):
    key = event.char
    print(f"'{key}' is pressed")
    action_name = keybind.get_action(key)
    if action_name:
        take_action(action_name)

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



update()
root.mainloop()
cap.release()