"""Custom types used in the tatum client package."""
from .virtual_account_types import AccountQueryDict
from .virtual_account_types import BatchAccountDict
from .virtual_account_types import CreateAccountDict
from .virtual_account_types import CustomerRegistrationDict
from .virtual_account_types import UpdateAccountDict

__all__ = [
    "CustomerRegistrationDict",
    "AccountQueryDict",
    "UpdateAccountDict",
    "CreateAccountDict",
    "BatchAccountDict",
]
