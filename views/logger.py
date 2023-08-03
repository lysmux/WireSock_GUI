import flet
import logging

from misc import LogHandler

log_handler = LogHandler()
logging.getLogger("wire_sock").addHandler(log_handler)


class LoggerView(flet.UserControl):
    def __init__(self):
        super().__init__()
        self.logger_field = flet.TextField(read_only=True, multiline=True)
        log_handler.log_function = self.write_log

    def build(self):
        return self.logger_field

    def write_log(self, message: str):
        self.logger_field.value += f"{message}\n"
        self.logger_field.update()
