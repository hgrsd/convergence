class InvalidLogin(Exception):
    """Invalid username and/or password at login"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class AccountDetailsError(Exception):
    """E.g. Invalid or already-taken username at registration"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class PermissionDenied(Exception):
    """Permission denied"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class EventNotFound(Exception):
    """Event does not exist"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class UserNotFound(Exception):
    """User does not exist"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class InvalidLocation(Exception):
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
