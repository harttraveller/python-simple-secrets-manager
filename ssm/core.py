from __future__ import annotations

import pendulum

from pydantic import BaseModel, field_validator
from ssm import setup
from ssm.sep.io import open_toml, save_toml
from ssm.sep.term import vprint
from ssm.schema import PendulumDatetime
from ssm.env import PATH_SECRETS_DEFAULT

# todo: imports for later use
# from datetime import datetime
# from pendulum.duration import Duration
# from pendulum.datetime import DateTime
# from typing import Optional, Union


# @dataclass
class Secret(BaseModel):
    name: str
    key: str
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
    def keep(
        name: str,
        key: str,
    ) -> Secret:
        return Secret(name=name, key=key)


class SecretAccessor:
    def __init__(self, secrets_dict: dict[dict]) -> None:
        self.__attach(secrets_dict)

    def __attach(self, secrets_dict: dict[dict]) -> None:
        for secret_name in secrets_dict.keys():
            temp: dict = secrets_dict[secret_name]
            temp["name"] = secret_name
            setattr(self, secret_name, Secret.keep(**temp))


class SecretHandler:
    def __init__(self) -> None:
        setup.secret_storage()
        self.reload()

    @staticmethod
    def __load_secrets() -> dict[dict]:
        return open_toml(PATH_SECRETS_DEFAULT)

    # todo
    # def _count(self):
    #     pass

    # todo
    # def _search(self):
    #     pass

    def reload(self) -> None:
        self.__data = self.__load_secrets()
        self.obj = SecretAccessor(secrets_dict=self.__data)

    def erase(self, force: bool = False) -> None:
        "erase all secrets"
        if not force:
            raise ValueError(
                "to avoid accidentally erasing your secrets, you must pass True to 'force'"
            )
        setup.secret_storage(erase=True)

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
        token = Secret.keep(name=name, key=secret).model_dump()
        del token["name"]
        self.reload()
        self.__data[name] = token
        save_toml(self.__data, PATH_SECRETS_DEFAULT)

    def delete(self, name: str) -> None:
        """
        Delete existing token.

        Args:
            name (str): name of stoed token
        """
        self.check(name)
        creds = self.data
        del creds[name]
        save_toml(creds, PATH_SECRETS_DEFAULT)


secrets = SecretHandler()

if __name__ == "__main__":
    # token = Token.make(name="test", secret="fakesecret")
    # vprint(token)
    # vprint(token.model_dump())
    secrets = SecretHandler()
    secrets.erase(force=True)
    secrets.save(name="test", secret="asdf")
    vprint(dict(secrets))
    vprint(secrets.secret("test"))
    # vprint(secrets.obj.A)
