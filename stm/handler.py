from stm.environment import PATH_STORE_DEFAULT


class TokenHandler:
    @property
    def data(self) -> dict:
        return open_toml(FILE_CREDENTIALS)

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
        save_toml(creds, FILE_CREDENTIALS)

    def delete(self, name: str) -> None:
        self.check(name)
        creds = self.data
        del creds[name]
        save_toml(creds, FILE_CREDENTIALS)


tokens = TokenHandler()
