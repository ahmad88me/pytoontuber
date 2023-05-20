
import os
import random


class AnimationManager:

    def __init__(self):
        self.actions = ["talk", "idle", "set", "peak"]
        self.vids = dict()
        for act in self.actions:
            self.vids[act] = []


    def organise(self, vids):
        for vpath in vids:
            fname = vpath.split(os.sep)[-1]
            for act in self.actions:
                stored = False
                if fname.startswith(act):
                    self.vids[act].append(vpath)
                    stored = True
                    break
            if not stored:
                print(f"Invalid file name: {vpath}. The file name should start with one of the following: {self.actions}")

    def get_action_vid(self, action):
        if action not in self.actions:
            print(f"Invalid action {action}")
            return None
        if self.vids[action]:
            vpath = random.choice(self.vids[action])
            return vpath
        else:
            print(f"No available videos for {action}")
        return None
