from stm.io import open_toml, save_toml
from stm.environment import PATH_TOKENS_DEFAULT


class TokenHandler:
    @property
    def data(self) -> dict[str, str]:
        """
        Show token dictionary.

        Returns:
            dict[str, str]: [token name]:[token secret] dictionary
        """
        return open_toml(PATH_TOKENS_DEFAULT)

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

    def get(self, name: str) -> str:
        """
        Get a token secret.

        Args:
            name (str): name of stored token

        Returns:
            str: token secret
        """
        self.check(name)
        return self.data[name]

    def save(self, name: str, secret: str) -> None:
        """
        Save a new token.

        Args:
            name (str): name of new token
            secret (str): token secret
        """
        creds = self.data
        creds[name] = secret
        save_toml(creds, PATH_TOKENS_DEFAULT)

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
