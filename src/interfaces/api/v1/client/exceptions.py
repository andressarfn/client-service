from src.shared.exceptions import CustomException


class PostClientException(CustomException):
    pass


class GetClientException(CustomException):
    pass


class UpdateClientException(CustomException):
    pass


class DeleteClientException(CustomException):
    pass
