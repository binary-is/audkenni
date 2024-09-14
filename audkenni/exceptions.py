class AudkenniException(Exception):
    pass


class AuthException(AudkenniException):
    pass


class AuthInProgressException(AudkenniException):
    pass


class UserAbortedException(AudkenniException):
    pass


class TimeoutException(AudkenniException):
    pass


class WrongNumberException(AudkenniException):
    pass
