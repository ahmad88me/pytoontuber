
from PIL import Image,ImageTk
from tkinter import NW, N, CENTER, RAISED, TOP
from tkinter import  Label, Button, Frame
from tkinter import filedialog
from tkinter import Tk, Canvas, PhotoImage

from functools import partial
import cv2
import util



class ControlsBar():

    def __init__(self, frame_height=200, num_buttons=10):
        self.num_buttons = num_buttons
        self.buttons = []
        self.frame_height = frame_height
        self.upload_img = Image.open('upload.png')
        self.button_height = None
        self.vids = [None for i in range(self.num_buttons)]

    def get_vid(self, vid_id):
        return self.vids[vid_id]

    def draw_animation_grid(self, root,  w_width=400):
        # b=Button(root, text="Hello")
        # b.pack()
        upload_img = self.upload_img
        frame_height = self.frame_height
        img_height = min(frame_height, int(w_width/self.num_buttons))
        self.button_height = img_height
        # img_height = frame_height
        print(f"Image button height: {img_height}")
        print(f"original height: {upload_img.height}")
        upload_img2 = upload_img.resize((img_height, img_height), Image.LANCZOS)
        print(f"scaled height: {upload_img2.height}")
        upload_img_file = ImageTk.PhotoImage(upload_img2)

        # upload_img_file = PhotoImage(file='y.png')

        anim_grid_frame = Frame(root, height=self.frame_height, width=w_width)
        anim_grid_frame.grid(row=0,column=0)
        # anim_grid_frame.pack(side=TOP)
        window = anim_grid_frame
        for i in range(self.num_buttons):
            j = 0
            frame = Frame(
                master=window,
                relief=RAISED,
                borderwidth=1
            )
            frame.grid(row=j, column=i)

            upload_vid_partial = partial(self.upload_vid, i)

            b = Button(master=frame, image=upload_img_file, height=img_height, width=img_height, command=upload_vid_partial)
            b.image = upload_img_file
            b.pack()
            # l = Label(master=b, text=str(i))
            # l.pack()
            self.buttons.append(b)
            l = Label(master=frame, text=str(i))
            l.pack()
            # l.grid(row=j+1, column=i)

    def upload_vid(self, idx):
        filename = filedialog.askopenfilename()
        self.vids[idx] = filename
        print(f"Filename {filename} for idx: {idx}")
        photo = util.img_from_vid(filename, resize=(self.button_height, self.button_height))
        self.buttons[idx].configure(image=photo)
        self.buttons[idx].photo=photo
        #
        # def change_pic(labelname):
        #     photo1 = ImageTk.PhotoImage(Image.open("demo.jpg"))
        #     labelname.configure(image=photo1)
        #     labelname.photo = photo1
        #     print
        #     "updated"

        # vpath = "/Users/aalobaid/Downloads/Tuber/Tuber/idlenormal.mp4"
        # # vpath = "/Users/aalobaid/Downloads/Tuber/Tuber/talknormal.mp4"
        #
        # cap = cv2.VideoCapture(vpath)
