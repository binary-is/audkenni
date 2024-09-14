class AudkenniException(Exception):
    pass


class AudkenniAuthenticationException(AudkenniException):
    pass


class AudkenniAuthenticationInProgress(AudkenniException):
    pass


class AudkenniUserAbortedException(AudkenniException):
    pass


class AudkenniTimeoutException(AudkenniException):
    pass


class AudkenniWrongNumberException(AudkenniException):
    pass
