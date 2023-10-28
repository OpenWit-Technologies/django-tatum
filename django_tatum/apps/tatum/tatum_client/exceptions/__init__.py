"""Exception pagacke for Tatum client"""
from .base import BaseException
from .virtual_account_exceptions import MissingparameterException

__all__ = [
    "BaseException",
    "MissingparameterException",
]
