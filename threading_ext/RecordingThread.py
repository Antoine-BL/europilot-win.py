import os
import time

import numpy as np

import cv2
from mss import mss

from GameRecorder import GameRecorder
from threading_ext.PausableThread import PausableThread


class RecordingThread(PausableThread):
    def __init__(self, training_data_path: str, session_number: int, recorder: GameRecorder):
        super(RecordingThread, self).__init__()
        self.recorder = recorder
        self.training_data = []
        self.training_data_path = training_data_path
        self.session_number = session_number
        print(session_number)

    def run(self):
        monitor = {"top": 0, "left": 0, "width": 1024, "height": 768}
        frames = 0
        last_time = time.time()

        with mss() as sct:
            while not self.killed:
                frames += 1

                screen = np.asarray(sct.grab(monitor))
                screen = cv2.resize(screen, (480, 270))
                screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

                self.training_data.append([screen, self.recorder.flattened_state()])

                self.sleep_if_paused()

                if time.time() - last_time >= 1:
                    print('fps: {}'.format(frames / (time.time() - last_time)))
                    print('data points: {}'.format(len(self.training_data)))
                    last_time = time.time()
                    frames = 0

                self.save_if_necessary()

    def save_if_necessary(self):
        if len(self.training_data) % 100 == 0:
            print(len(self.training_data))

            if len(self.training_data) == 500:
                np.save(self.training_data_path.format(self.session_number), self.training_data)
                print('saved_data in file nb {}'.format(self.session_number))
                self.session_number += 1
                self.training_data = []
