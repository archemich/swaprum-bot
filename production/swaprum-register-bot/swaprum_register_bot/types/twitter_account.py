from typing import TypedDict

from .email import Email


class TwitterAccount(TypedDict):
    login: str
    password: str
    email: Email