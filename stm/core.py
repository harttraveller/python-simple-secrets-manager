from __future__ import annotations

import pendulum

from pydantic import BaseModel, field_validator
from stm import setup
from stm.sep.io import open_toml, save_toml
from stm.sep.term import vprint
from stm.schema import PendulumDatetime
from stm.env import PATH_TOKENS_DEFAULT

# todo: imports for later use
# from datetime import datetime
# from pendulum.duration import Duration
# from pendulum.datetime import DateTime
# from typing import Optional, Union


# @dataclass
class Token(BaseModel):
    name: str
    secret: str
    created: PendulumDatetime = pendulum.now()
    # delete_after # todo, delete after period
    # valid: Optional[bool] = None # known == unknown, True, validated, False, auto val failed
    # todo: can add expiry, other features etc later when actually needed
    # expiry: Optional[DateTime] = None

    # def __post_init__(self) -> None:
    #     self.is_known: bool = False # todo: check if known service for auto validation later

    def __str__(self):
        return f"Token(name={self.name})"

    # todo: can add validation, params/features later when needed
    # validate: bool, expiry: Union[datetime, DateTime],
    @staticmethod
    def make(
        name: str,
        secret: str,
    ) -> Token:
        return Token(name=name, secret=secret)


class TokenAccessor:
    def __init__(self, tokens_dict: dict[dict]) -> None:
        self.__attach(tokens_dict)

    def __attach(self, tokens_dict: dict[dict]) -> None:
        for token_name in tokens_dict.keys():
            temp: dict = tokens_dict[token_name]
            temp["name"] = token_name
            setattr(self, token_name, Token.make(**temp))


class TokenHandler:
    def __init__(self) -> None:
        setup.token_storage()
        self.reload()

    @staticmethod
    def __load_tokens() -> dict[dict]:
        return open_toml(PATH_TOKENS_DEFAULT)

    # * temp test
    @staticmethod
    def __load_test_tokens() -> dict[dict]:
        return {"A": {"secret": "1234"}, "B": {"secret": "2345"}}

    # todo
    # def _count(self):
    #     pass

    # todo
    # def _search(self):
    #     pass

    def reload(self) -> None:
        self.__data = self.__load_tokens()
        # self.obj = TokenAccessor(tokens_dict=self.__data)

    def erase(self, force: bool = False) -> None:
        "erase all tokens"
        if not force:
            raise ValueError(
                "to avoid accidentally erasing your tokens, you must pass True to 'force'"
            )
        setup.token_storage(erase=True)

    def __iter__(self) -> dict:
        for token_name, token_data in self.data.items():
            yield token_name, token_data

    @property
    def data(self) -> dict:
        """
        Show token dictionary.

        Returns:
            dict[str, str]: [token name]:[token secret] dictionary
        """
        return self.__data

    @property
    def names(self) -> list[str]:
        """
        Return token names.

        Returns:
            list[str]: list of stored token names
        """
        return list(self.data.keys())

    def exists(self, name: str) -> bool:
        """
        Check if token name exists.

        Args:
            name (str): name of stored token

        Returns:
            bool: True if exists, else False
        """
        return name in self.names

    def check(self, name: str) -> None:
        """
        Check if token name exists, raises ValueError if False.

        Args:
            name (str): name of stored token

        Raises:
            ValueError: no available token
        """
        if not self.exists(name):
            raise ValueError("token does not exist")

    def secret(self, name: str) -> str:
        """
        Get a token secret.

        Args:
            name (str): name of stored token

        Returns:
            str: token secret
        """
        self.check(name)
        return self.data[name]["secret"]

    def save(self, name: str, secret: str) -> None:
        """
        Save a new token.

        Args:
            name (str): name of new token
            secret (str): token secret
        """
        token = Token.make(name=name, secret=secret).model_dump()
        del token["name"]
        self.reload()
        self.__data[name] = token
        save_toml(self.__data, PATH_TOKENS_DEFAULT)

    def delete(self, name: str) -> None:
        """
        Delete existing token.

        Args:
            name (str): name of stoed token
        """
        self.check(name)
        creds = self.data
        del creds[name]
        save_toml(creds, PATH_TOKENS_DEFAULT)


tokens = TokenHandler()

if __name__ == "__main__":
    # token = Token.make(name="test", secret="fakesecret")
    # vprint(token)
    # vprint(token.model_dump())
    tokens = TokenHandler()
    tokens.erase(force=True)
    tokens.save(name="test", secret="asdf")
    vprint(dict(tokens))
    vprint(tokens.secret("test"))
    # vprint(tokens.obj.A)
