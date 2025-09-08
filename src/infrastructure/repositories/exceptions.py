from dataclasses import dataclass

from src.shared.exceptions import CustomException


@dataclass
class NotFoundException(CustomException):
    title: str = "Not found"
