from __future__ import print_function

import os
import time

import inputs

from GameRecorder import GameRecorder
from threading_ext.GamePadTracker import GamePadTracker
from threading_ext.KeyboardTracker import KeyboardTracker
from threading_ext.RecordingThread import RecordingThread

DATA_FILENAME = 'session-{}.npy'
DATA_BASEDIR = 'data'


def main():
    xboxctrl = inputs.devices.gamepads[0]
    jstest = GameRecorder(xboxctrl)

    data_path = create_training_data_directory()
    session_number = find_session_num(data_path)

    threads = []

    gamepad_tracker_thread = GamePadTracker(jstest)
    screenshot_thread = RecordingThread(data_path, session_number, jstest)
    keyboard_tracker_thread = KeyboardTracker()

    threads.append(gamepad_tracker_thread)
    threads.append(screenshot_thread)
    threads.append(keyboard_tracker_thread)

    for thread in threads:
        thread.pause()

    for thread in threads:
        thread.start()

    while True:
        if keyboard_tracker_thread.check_for_kill():
            print('killing all threads')
            for thread in threads:
                thread.kill()
            break

        if keyboard_tracker_thread.check_for_pause():
            print('pausing/unpausing threads')
            gamepad_tracker_thread.pause()
            screenshot_thread.pause()

        time.sleep(0.5)


def find_session_num(data_path):
    session_number = 1
    while not True:
        file_name = os.path.join(data_path, DATA_FILENAME.format(session_number))

        if os.path.isfile(file_name):
            session_number += 1
        else:
            print('Saving data in file: {}'.format(file_name))
            break
    return session_number


def create_training_data_directory():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(dir_path, DATA_BASEDIR)

    if not os.path.isdir(data_path):
        os.makedirs(data_path)

    return os.path.join(data_path, DATA_FILENAME)


if __name__ == "__main__":
    main()
