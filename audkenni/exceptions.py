class AudkenniException(Exception):
    pass


class AudkenniUserAbortedException(AudkenniException):
    pass


class AudkenniTimeoutException(AudkenniException):
    pass


class AudkenniWrongNumberException(AudkenniException):
    pass
