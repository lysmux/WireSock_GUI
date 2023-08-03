from logging import Handler


class LogHandler(Handler):
    def __init__(self):
        super(LogHandler, self).__init__()
        self.log_function = None

    def emit(self, record):
        message = self.format(record)

        if self.log_function:
            self.log_function(message)
