
import cv2


class Window:

    _wName = "OptionsWindow"

    def show_opts_window(self):
        cv2.namedWindow(self._wName)
        cv2.resizeWindow(self._wName, 600, 600)
