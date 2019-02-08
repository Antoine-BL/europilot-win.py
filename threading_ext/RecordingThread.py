import asyncio
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
        monitor = {"top": 40, "left": 0, "width": 1024, "height": 728}
        ns_to_ms = 1000000

        with mss() as sct:
            while not self.killed:
                start_time_ms = time.time_ns() * ns_to_ms

                screen = np.asarray(sct.grab(monitor))
                screen = cv2.resize(screen, (480, 270))
                screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

                self.training_data.append([screen, self.recorder.flattened_state()])
                self.sleep_if_paused()
                self.save_if_necessary()
                self.wait(start_time_ms)

    def save_if_necessary(self):
        if len(self.training_data) % 100 == 0:
            print(len(self.training_data))

            if len(self.training_data) == 500:
                np.save(self.training_data_path.format(self.session_number), self.training_data)
                print('saved_data in file nb {}'.format(self.session_number))
                self.session_number += 1
                self.training_data = []

    def wait(self, start_time_ms: int):
        delay_ms = 100

        end_time_ms = time.time_ns()
        duration_ms = end_time_ms - start_time_ms
        print('loop duration: {}ms'.format(duration_ms))
        time.sleep(max(delay_ms - duration_ms, 0))

    def rewind(self):
        self.session_number -= 1
        self.training_data = []
