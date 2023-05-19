
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

    def __init__(self, thickness=200, num_buttons=10, vertical=True):
        self.num_buttons = num_buttons
        self.buttons = []
        self.thickness = thickness
        self.upload_img = Image.open('upload.png')
        self.button_height = None
        self.vids = [None for i in range(self.num_buttons)]
        self.vertical = vertical
        self.frame = None

    def get_vid(self, vid_id):
        return self.vids[vid_id]

    def resize_buttons(self, bar_length):
        # img_height = min(self.thickness, int(bar_length/self.num_buttons))
        img_height = min(self.thickness, int(bar_length/(self.num_buttons+1)))

        print(f"img height: {img_height} thickness: {self.thickness} bar_length: {bar_length}")
        for b in self.buttons:
            b.config(height=img_height, width=img_height)

    def draw_animation_grid(self, root,  bar_length=400, grid_row=0, grid_col=0):
        # b=Button(root, text="Hello")
        # b.pack()
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
        if self.vertical:
            anim_grid_frame = Frame(root, width=self.thickness, height=bar_length)
        else:
            anim_grid_frame = Frame(root, height=self.thickness, width=bar_length )
        anim_grid_frame.grid(row=grid_row,column=grid_col)
        self.frame = anim_grid_frame
        # anim_grid_frame.pack(side=TOP)
        window = anim_grid_frame
        for i in range(self.num_buttons):
            j = 0
            frame = Frame(
                master=window,
                relief=RAISED,
                borderwidth=1
            )
            if self.vertical:
                frame.grid(row=i, column=j)
            else:
                frame.grid(row=j, column=i)

            upload_vid_partial = partial(self.upload_vid, i)

            b = Button(master=frame, image=upload_img_file, height=img_height, width=img_height, command=upload_vid_partial)
            b.image = upload_img_file
            if self.vertical:
                b.grid(row=0, column=1)
            else:
                b.grid(row=0, column=0)
            # b.pack()
            # l = Label(master=b, text=str(i))
            # l.pack()
            self.buttons.append(b)
            l = Label(master=frame, text=str(i), anchor=E)
            if self.vertical:
                l.grid(row=0, column=0)
            else:
                l.grid(row=1, column=0)
            # l.pack(side="left")
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
