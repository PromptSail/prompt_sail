class NotFoundException(Exception):
    """
    Exception raised when an entity is not found.
    """

    def __init__(self, message: str = None):
        """
        Initialize the NotFoundException with an optional error message.

        :param message: The error message for the exception.
        """
        self.message = message or "Not found"
        super().__init__(self.message)


class AlreadyExistsException(Exception):
    """
    Exception raised when an entity already exists.
    """

    def __init__(self, message: str = None):
        """
        Initialize the AlreadyExistsException with an optional error message.

        :param message: The error message for the exception.
        """
        self.message = message or "Already exists"
        super().__init__(self.message)
