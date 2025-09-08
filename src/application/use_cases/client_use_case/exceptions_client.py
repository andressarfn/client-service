from src.shared.exceptions import CustomHttpException


class EmailAlreadyExistsException(CustomHttpException):
    pass


class ClientNotFoundException(CustomHttpException):
    pass
