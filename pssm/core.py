from __future__ import annotations

from copy import deepcopy
from datetime import datetime

from pydantic import BaseModel, field_validator
from typing import Optional
from pssm import setup
from pssm.sep.io import open_toml, save_toml
from pssm.sep.term import vprint
from pssm.env import PATH_SECRETS_DEFAULT

# todo: imports for later use
# from datetime import datetime
# from pendulum.duration import Duration
# from pendulum.datetime import DateTime
# from typing import Optional, Union


# @dataclass
class Secret(BaseModel):
    uid: str
    key: str
    created: Optional[datetime] = datetime.now()
    # service # todo
    # user # todo
    # scope # todo
    # delete_after # todo, delete after period
    # valid: Optional[bool] = None # known == unknown, True, validated, False, auto val failed
    # todo: can add expiry, other features etc later when actually needed
    # expiry: Optional[DateTime] = None

    @field_validator("uid")
    def __validate_uid(cls, uid: str) -> str:
        # secret uid must be only alphanumeric and underscore, and cannot start with number
        if not len(uid):
            raise ValueError("the secret uid must be at least one character long")
        if uid[0].isnumeric():
            raise ValueError("the secret uid cannot start with a number")
        if not all([i.isalnum() or i == "_" for i in uid]):
            raise ValueError(
                "the secret uid can only contain alphanumeric and underscore chars"
            )
        return uid

    # def __post_init__(self) -> None:
    #     self.is_known: bool = False # todo: check if known service for auto validation later

    def __repr__(self):
        return f"Secret(uid={self.uid})"

    def __str__(self):
        return f"Secret(uid={self.uid})"

    # todo: can add validation, params/features later when needed
    # validate: bool, expiry: Union[datetime, DateTime],
    # @staticmethod
    # def make(
    #     uid: str,
    #     key: str,
    # ) -> Secret:
    #     return Secret(uid=uid, key=key)

    # age, measure in hours, days, weeks, etc
    def age(self, measure):
        pass

    def time_to_expiry(self):
        pass


class SecretAccessor:
    def __init__(self, secrets_dict: dict[dict]) -> None:
        self.__attach(secrets_dict)

    def __attach(self, secrets_dict: dict[dict]) -> None:
        # deepcopy prevents mem error that adds uid back to original dict
        secrets_dict_copy = deepcopy(secrets_dict)
        for secret_uid in secrets_dict_copy.keys():
            temp: dict = secrets_dict_copy[secret_uid]
            temp["uid"] = secret_uid
            setattr(self, secret_uid, Secret.model_validate(temp))


class SecretHandler:
    def __init__(self) -> None:
        setup.secret_storage()
        self.reload()

    @staticmethod
    def __load_secrets() -> dict[dict]:
        return open_toml(PATH_SECRETS_DEFAULT)

    def count(self) -> int:
        return len(self.data)

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
        for secret_uid, secret_key in self.data.items():
            yield secret_uid, secret_key

    @property
    def data(self) -> dict:
        """
        Show secret dictionary.

        Returns:
            dict[str, str]: [secret uid]:[secret key] dictionary
        """
        return self.__data

    @property
    def uids(self) -> list[str]:
        """
        Return secret uids.

        Returns:
            list[str]: list of stored secret uids
        """
        return list(self.data.keys())

    def exists(self, uid: str) -> bool:
        """
        Check if secret uid exists.

        Args:
            uid (str): uid of stored secret

        Returns:
            bool: True if exists, else False
        """
        return uid in self.uids

    def check(self, uid: str) -> None:
        """
        Check if secret uid exists, raises ValueError if False.

        Args:
            uid (str): uid of stored secret

        Raises:
            ValueError: no available secret
        """
        if not self.exists(uid):
            raise ValueError("secret does not exist")

    def get(self, uid: str) -> str:
        """
        Get a secret key.

        Args:
            uid (str): uid of stored secret

        Returns:
            str: secret key
        """
        self.check(uid)
        return self.data[uid]["key"]

    def keep(self, uid: str, key: str) -> None:
        """
        Save a new secret.

        Args:
            uid (str): uid of new secret
            key (str): secret key
        """
        secret_dict = {"uid": uid, "key": key}
        secret = Secret.model_validate(secret_dict).model_dump()
        del secret["uid"]
        self.reload()
        self.__data[uid] = secret
        save_toml(self.__data, PATH_SECRETS_DEFAULT)
        self.reload()

    def forget(self, uid: str) -> None:
        """
        Delete existing secret.

        Args:
            uid (str): uid of stored secret
        """
        self.check(uid)
        creds = self.data
        del creds[uid]
        save_toml(creds, PATH_SECRETS_DEFAULT)


secrets = SecretHandler()
