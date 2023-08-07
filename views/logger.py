import flet

from logger import Logger


class LoggerView(flet.UserControl):
    def __init__(self):
        super().__init__()
        self.logger_field = flet.Ref[flet.TextField]()
        Logger().log_function = self.write_log

    def build(self):
        return flet.TextField(ref=self.logger_field, read_only=True, multiline=True)

    def write_log(self, message: str):
        self.logger_field.current.value += f"{message}\n"
        self.logger_field.current.update()
