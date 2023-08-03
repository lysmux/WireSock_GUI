import flet


class LoggerView(flet.UserControl):
    def __init__(self):
        super().__init__()
        self.logger_field = flet.TextField(read_only=True, multiline=True)

    def build(self):
        return self.logger_field

    def write_message(self, message: str):
        self.logger_field.value += f"{message}\n"
        self.logger_field.update()
