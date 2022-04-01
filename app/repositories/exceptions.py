class SportRepositoryException(Exception):
    pass


class SportValidationErrorException(SportRepositoryException):
    pass


class SportNotFoundException(SportRepositoryException):
    def __init__(self):
        Exception.__init__(self)
        self.message = "Sport not found"


class SportIntegrityError(SportRepositoryException):
    def __init__(self, message):
        self.message = message
