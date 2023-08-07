import datetime


class Logger:
    instance = None
    log_function = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def log(self, message: str):
        timestamp = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
        msg = f"{timestamp} - {message}"

        if self.log_function:
            self.log_function(msg)
