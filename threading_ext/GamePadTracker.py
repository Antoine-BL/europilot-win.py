import cv2

from threading_ext.PausableThread import PausableThread


class GamePadTracker(PausableThread):
    def __init__(self, jstest):
        super(GamePadTracker, self).__init__()
        self.jstest = jstest

    def run(self):
        while not self.killed:
            self.jstest.process_events()
            if self.jstest.btn_state['E'] == 1:
                cv2.destroyAllWindows()
                break

            self.sleep_if_paused()
