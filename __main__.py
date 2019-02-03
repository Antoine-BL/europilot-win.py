

from __future__ import print_function

import os
from datetime import datetime

import inputs

from GameRecorder import GameRecorder, DATA_BASEDIR
from threading_ext.GamePadTracker import GamePadTracker
from threading_ext.KeyboardTracker import KeyboardTracker
from threading_ext.ScreenshotThread import ScreenshotThread


def main():
    xboxctrl = inputs.devices.gamepads[0]
    jstest = GameRecorder(xboxctrl)
    kb_track = KeyboardTracker()

    sample_name = 'sample-{}'.format(datetime.now()).replace(':', '.')
    path = '{}/{}/screenshots'.format(DATA_BASEDIR, sample_name)

    os.makedirs(path)

    gamepad_tracker_thread = GamePadTracker(jstest)
    screenshot_thread = ScreenshotThread(sample_name)
    keyboard_tracker_thread = KeyboardTracker()

    gamepad_tracker_thread.start()
    screenshot_thread.start()
    keyboard_tracker_thread.start()

    gamepad_tracker_thread.join()
    screenshot_thread.join()
    keyboard_tracker_thread.join()

    kill = False
    while not kill:
        if kb_track.check_for_kill():
            gamepad_tracker_thread.kill()
            screenshot_thread.kill()
            keyboard_tracker_thread()
            kill = True

        if kb_track.check_for_pause():
            gamepad_tracker_thread.pause()
            screenshot_thread.pause()


if __name__ == "__main__":
    main()
