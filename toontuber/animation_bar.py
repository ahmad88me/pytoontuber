
from PIL import Image,ImageTk
from tkinter import NW, N, CENTER, RAISED, TOP, W, E
from tkinter import  Label, Button, Frame
from tkinter import filedialog
from tkinter import Tk, Canvas, PhotoImage

from functools import partial
import cv2
import util




# def upload_vid(idx):
#     filename = filedialog.askopenfilename()
#     print(f"Filename {filename} for idx: {idx}")



class AnimationBar():

    def __init__(self, thickness=200, num_buttons=10):
        self.num_buttons = num_buttons
        self.buttons = []
        self.labels = []
        self.thickness = thickness
        self.upload_img = Image.open('upload.png')
        self.button_height = None
        self.vids = [None for i in range(self.num_buttons)]
        self.frame = None

        self.active_color = "#0A0"
        self.inactive_color = "#252"
        self.empty_color = ""


    def get_vid(self, vid_id):
        print(f" vid_id {vid_id}")
        l = self.num_buttons
        idx = (vid_id + l - 1) % l
        vpath = self.vids[vid_id]
        if vpath: # highlight the selected animation
            for i in range(l):
                self.labels[i].configure(bg=self.empty_color)
                if idx == i:
                    self.labels[i].configure(bg=self.active_color)

        # self.labels[idx].configure(highlightbackground="#252", highlightthickness=3)
        return vpath #self.vids[vid_id]

    def resize_buttons(self, bar_length):
        # img_height = min(self.thickness, int(bar_length/self.num_buttons))
        img_height = min(self.thickness, int(bar_length/(self.num_buttons+5)))

        print(f"img height: {img_height} thickness: {self.thickness} bar_length: {bar_length}")
        for b in self.buttons:
            b.config(height=img_height, width=img_height)
        # self.frame.configure(height=bar_length)

    def draw_animation_grid(self, root,  bar_length=400, grid_row=0, grid_col=0):
        # b=Button(root, text="Hello")
        # b.pack()
        self.empty_color = root.cget("background")

        upload_img = self.upload_img
        thickness = self.thickness
        img_height = min(thickness, int(bar_length/(self.num_buttons+1)))
        self.button_height = img_height
        # img_height = frame_height
        print(f"Image button height: {img_height}")
        print(f"original height: {upload_img.height}")
        upload_img2 = upload_img.resize((img_height, img_height), Image.LANCZOS)
        print(f"scaled height: {upload_img2.height}")
        upload_img_file = ImageTk.PhotoImage(upload_img2)

        # upload_img_file = PhotoImage(file='y.png')

        anim_grid_frame = Frame(root, width=self.thickness, height=bar_length)

        anim_grid_frame.grid(row=grid_row,column=grid_col)
        self.frame = anim_grid_frame
        # anim_grid_frame.pack(side=TOP)
        window = anim_grid_frame
        nums_range = [i for i in range(1, self.num_buttons)] + [0]
        print(nums_range)
        for idx, i in enumerate(nums_range):
            print(f"i: {i}")
            j = 0
            frame = Frame(
                master=window,
                relief=RAISED,
                borderwidth=1
            )

            frame.grid(row=idx, column=j)
            upload_vid_partial = partial(self.upload_vid, idx, i)

            b = Button(master=frame, image=upload_img_file, height=img_height, width=img_height, command=upload_vid_partial)
            b.image = upload_img_file

            b.grid(row=0, column=1)

            self.buttons.append(b)
            l = Label(master=frame, text=str(i), anchor=E)
            l.grid(row=0, column=0)
            self.labels.append(l)



    def upload_vid(self, idx, i):
        filename = filedialog.askopenfilename()
        self.vids[i] = filename
        print(f"Filename {filename} for idx: {idx}")
        photo = util.img_from_vid(filename, resize=(self.button_height, self.button_height))
        self.buttons[idx].configure(image=photo)
        self.buttons[idx].photo=photo

