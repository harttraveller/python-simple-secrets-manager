from pathlib import Path
from importlib import metadata

PKG_VERSION = metadata.version("simple-secrets-manager")


PATH_STORE_DEFAULT = Path.home() / ".ssm"
PATH_SECRETS_DEFAULT = PATH_STORE_DEFAULT / "tokens.toml"
