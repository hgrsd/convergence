class InvalidRequestError(Exception):
    """Invalid request"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class LoginError(Exception):
    """Invalid username and/or password at login"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class InputError(Exception):
    """Invalid input given by user"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class PermissionError(Exception):
    """Permission denied"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class NotFoundError(Exception):
    """Requested entity is not found"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class LocationError(Exception):
    """Invalid location coordinates"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class ServerError(Exception):
    """Generic server-side error class"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class DatabaseError(Exception):
    """Error writing to/reading from database"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)
