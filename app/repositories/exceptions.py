class RepositoryException(Exception):
    pass


class SportValidationErrorException(RepositoryException):
    pass


class SportNotFoundException(RepositoryException):
    def __init__(self):
        self.message = "Sport not found"


class SportIntegrityError(RepositoryException):
    def __init__(self, message):
        self.message = message


class RepositoryOperationalError(RepositoryException):
    def __init__(self, message):
        self.message = message


class EventNotFoundException(RepositoryException):
    def __init__(self):
        self.message = "Event not found"


class EventForeignKeyException(RepositoryException):
    def __init__(self):
        self.message = "Sport not found"


class EventValidationErrorException(RepositoryException):
    def __init__(self, message):
        self.message = message
