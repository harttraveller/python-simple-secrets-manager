from stm.io import open_toml, save_toml
from stm.environment import PATH_TOKENS_DEFAULT


class TokenHandler:
    @property
    def data(self) -> dict:
        return open_toml(PATH_TOKENS_DEFAULT)

    @property
    def tokens(self) -> list[str]:
        return list(self.data.keys())

    def exists(self, name: str) -> bool:
        return name in self.tokens

    def check(self, name) -> None:
        if not self.exists(name):
            raise ValueError("key does not exist")

    def get(self, name: str) -> str:
        self.check(name)
        return self.data[name]

    def save(self, name: str, key: str) -> None:
        creds = self.data
        creds[name] = key
        save_toml(creds, PATH_TOKENS_DEFAULT)

    def delete(self, name: str) -> None:
        self.check(name)
        creds = self.data
        del creds[name]
        save_toml(creds, PATH_TOKENS_DEFAULT)


tokens = TokenHandler()
