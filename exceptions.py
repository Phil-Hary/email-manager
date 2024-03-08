class AppError(Exception):
    def __init__(self, message, hard_error=False) -> None:
        self.message = message
        self.hard_error = hard_error
        super().__init__(message)