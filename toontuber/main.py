from PIL import Image,ImageTk

import math

import sounddevice as sd
from animan import AnimationManager
import datetime
import keybind
import argparse
import queue
from functools import partial
import cv2
from threading import Lock
from micman import MicMan

cap_lock = Lock()

action_history = []
playing_action = "idle"

micman = MicMan()

same_vid = True

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

cap = None

anime_q = queue.Queue()
# anime_q = []
anime_manager = AnimationManager()

selected_property = ""

cv2.namedWindow("window", cv2.WINDOW_NORMAL)
cv2.startWindowThread()


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

    cap_lock.acquire()
    if cap:
        cap.release()
        # del cap
        cap = None
    cap = cv2.VideoCapture(vpath)
    cap_lock.release()

    active_video_fps = cap.get(cv2.CAP_PROP_FPS)
    # print(f"FPS: {active_video_fps}")




def photo_image(img):
    h, w = img.shape[:2]
    data = f'P6 {w} {h} 255 '.encode() + img[..., ::-1].tobytes()
    return PhotoImage(width=w, height=h, data=data, format='PPM')


def cmd_controls(pressed_key):
    global selected_property
    if pressed_key == ord("s"):
        selected_property = "sensitivity"
        print(f"Selected property: {selected_property} and value is {micman.sensitivity}")
    elif pressed_key == ord("+") or pressed_key == ord("-"):
        sign = 1
        if pressed_key == ord("-"):
            sign = -1

        if selected_property == "sensitivity":
            new_sens = micman.sensitivity + 1*sign
            if 0 < new_sens < 30:
                micman.sensitivity = new_sens
                print(f"new sensitivity: {new_sens}")
            else:
                print(f"invalid sensitivity: {new_sens}")


def update():
    global cap, same_vid
    # global w_width, w_height, cap
    while same_vid:
        cap_lock.acquire()
        ret, img = cap.read()
        cap_lock.release()
        if ret:
            cv2.imshow('Frame', img)
            pressed_key = cv2.waitKey(25)
            if pressed_key == ord('q'):
                print(f"stoping the app")
                break
            else:
                cmd_controls(pressed_key)
            # if cv2.waitKey(25) & 0xFF == ord('q'):
            #     print(f"stoping the app")
            #     break

            # Press Q on keyboard to  exit
            # if cv2.waitKey(25) & 0xFF == ord('q'):
            #     return

            # w_width = canvas.winfo_width()
            # w_height = canvas.winfo_height()
            # toon_view_width = min(w_width, w_height)
            # toon_view_height = toon_view_width
            # img = cv2.resize(img, (toon_view_width, toon_view_height))
            #
            # photo = photo_image(img)
            # canvas.delete()
            # canvas.create_image(w_width/2 - toon_view_width/2, w_height/2 - toon_view_height/2, image=photo, anchor=NW)
            # canvas.image = photo
        else:
            loop_video()
        # if anime_q.empty():
        # # q_lock.acquire()
        # # if not anime_q:
        #     print(f"queue is empty")
        #     loop_video()
        #     # q_lock.release()
        # else:
        #     # vpath = anime_q.get(block=True)
        #     # vpath = anime_q.pop(0)
        #     vpath = anime_q.get(0)
        #
        #     # q_lock.release()
        #     print(f"getting a new vpath: {vpath}")
    #         loop_video(vpath)
    # wait_time = int(1000/active_video_fps)
    # root.after(wait_time, update)






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
    global anime_manager, playing_action

    if amp < 0.05:
        action = "idle"
    # else:
    #     action = "talk"
    elif amp < 0.7:
        action = "talk"
    else:
        action = "peak"

    if "talk" in action_history or "peak" in action_history:
        action_history.pop(0)
        action_history.append(action)
        if playing_action == "talk" and action=="peak":
            pass
            # action_history.append(action)
            # do peak
        elif playing_action == "peak" and action=="talk":
            pass
            # action_history.append(action)
            # do talk
        else:
            # action_history.append(action)
            if playing_action in ["talk", "peak"]:
                # continue to play the same animation
                print(f"Continue the animation {playing_action}")
                return
            # else:
            #     # in case playing action was idle but should've been talking or peak.
            #     action = "talk"
    else:
        action_history.pop(0)
        action_history.append(action)

        # if adle continue to be adle
        # if was adle and now talk or peak. do the new action


    print(f"audio to action: {action} and amp {('{:.2f}'.format(amp))}")
    vpath = anime_manager.get_action_vid(action)
    loop_video(vpath)
    playing_action = action





def parse():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--videos', required=True, nargs='+', help='the list of videos to be utilised')
    parser.add_argument('-d', '--device', type=int, help="The index of the number. This should be an integer")
    parser.add_argument('-s', '--sensitivity', default=1, type=int, help="How sensitive are the mics",
                        choices=range(1, 50),
                        metavar="[0-50]",
                        )
    args = parser.parse_args()
    print(f"The arguments are parsed:")
    print(f"args: {args}")
    if isinstance(args.device, int):
        dev_id = args.device
    else:
        dev_id = micman.get_device_from_user()

    return args.videos, dev_id, args.sensitivity


def exit_app():
    global cap, cap_lock
    print(f"Exiting the app and releasing the resources.")
    micman.stop_audio_capture()
    cap_lock.acquire()
    if cap:
        cap.release()
        cap = None
    cap_lock.release()
    cv2.destroyAllWindows()


def setup_action_history(history=3,action="idle"):
    global action_history
    for i in range(history):
        action_history.append(action)


def main():
    global root, cap, anime_manager
    videos, dev_id, sens = parse()
    setup_action_history(history=3)
    anime_manager.organise(videos)
    micman.callback = audio_to_action
    micman.sensitivity = sens
    micman.capture_audio(dev_id)
    loop_video(anime_manager.get_action_vid("idle"))
    try:
        update()
    except KeyboardInterrupt:
        print(f"Keyboard is interrupted. Now releasing the resources.")
    exit_app()


    # cap.release()

if __name__ == "__main__":
    main()






