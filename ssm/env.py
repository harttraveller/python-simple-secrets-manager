from pathlib import Path
from importlib import metadata

PKG_VERSION = metadata.version("simple-token-manager")


PATH_STORE_DEFAULT = Path.home() / ".stm"
PATH_TOKENS_DEFAULT = PATH_STORE_DEFAULT / "tokens.toml"
