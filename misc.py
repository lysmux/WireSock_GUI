from logging import Handler

from windows_toasts import WindowsToaster, ToastText2

import resources


class LogHandler(Handler):
    def __init__(self):
        super(LogHandler, self).__init__()
        self.log_function = None

    def emit(self, record):
        message = self.format(record)

        if self.log_function:
            self.log_function(message)


def notify(tunnel_name: str, message: str):
    wintoaster = WindowsToaster(resources.APP_TITLE)
    toast = ToastText2()
    toast.SetHeadline(f"{resources.TUNNEL}: {tunnel_name}")
    toast.SetBody(message)
    wintoaster.show_toast(toast)
