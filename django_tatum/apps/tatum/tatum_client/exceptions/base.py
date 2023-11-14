"""Base exception class for Tatum Client"""


class BaseException(Exception):
    """Base exception class for Tatum Client"""

    def __init__(self, message: str = None, *args, **kwargs):
        """Base exception class for Tatum Client"""
        super().__init__(message, *args, **kwargs)
        self.message = message

    def __str__(self):
        """Base exception class for Tatum Client"""
        return self.message
