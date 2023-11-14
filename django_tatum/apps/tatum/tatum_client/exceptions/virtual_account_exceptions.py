"""Virtual account exceptions for Tatum client"""

from .base import BaseException


class MissingparameterException(BaseException):
    """Missing parameter exception"""

    def __init__(
        self,
        missing_parameters: list[str],
        message: str = None,
        *args,
        **kwargs,
    ):
        """Missing parameter exception"""
        super().__init__(message, *args, **kwargs)
        additional_message: str = f"{missing_parameters} must be specified."
        self.message = f"{message} : {additional_message}"

    def __str__(self):
        """Missing parameter exception"""
        return self.message
