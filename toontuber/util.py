import cv2
from PIL import Image,ImageTk
from tkinter import NW, N, CENTER, RAISED, TOP
from tkinter import  Label, Button, Frame
from tkinter import filedialog
from tkinter import Tk, Canvas, PhotoImage

from functools import partial

def img_from_vid(vpath, resize=None):
    cap = cv2.VideoCapture(vpath)
    ret, img = cap.read()
    if ret:
        if resize and len(resize)==2:
            img = cv2.resize(img, (resize[0], resize[1]))

        photo = photo_image(img)
        return photo
    return None


def photo_image(img):
    h, w = img.shape[:2]
    data = f'P6 {w} {h} 255 '.encode() + img[..., ::-1].tobytes()
    return PhotoImage(width=w, height=h, data=data, format='PPM')