from pathlib import Path
from importlib import metadata

PACKAGE_NAME = "simple-secrets-manager"
PACKAGE_VERSION = metadata.version(PACKAGE_NAME)
PATH_STORE_DEFAULT = Path.home() / ".secrets"
PATH_SECRETS_DEFAULT = PATH_STORE_DEFAULT / "tokens.toml"
# PATH_CONFIG_DEFAULT
