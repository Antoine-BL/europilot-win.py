import os

import numpy

import cv2
from mss import mss

from GameRecorder import DATA_BASEDIR
from threading_ext.PausableThread import PausableThread


class ScreenshotThread(PausableThread):
    def __init__(self, sample_name):
        super(ScreenshotThread, self).__init__()
        self.sample_name = sample_name

    def run(self):
        monitor = {"top": 40, "left": 0, "width": 800, "height": 640}
        frames = 0
        dir_path = os.path.dirname(os.path.realpath(__file__))

        filename_format = '{}.png'
        with mss() as sct:
            while not self.killed:
                img = numpy.asarray(sct.grab(monitor))
                frames += 1
                img_path = os.path.join(dir_path, DATA_BASEDIR, self.sample_name, 'screenshots',
                                        filename_format.format(frames))
                cv2.imwrite(img_path, img)

                self.sleep_if_paused()
