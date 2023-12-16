class NotFoundException(Exception):
    def __init__(self, message: str = None):
        self.message = message or "Not found"
        super().__init__(self.message)


class AlreadyExistsException(Exception):
    def __init__(self, message: str = None):
        self.message = message or "Already exists"
        super().__init__(self.message)
