# Quickstart

## Installation

=== "pip"

    ```sh
    pip install python-simple-secrets-manager
    ```

=== "poetry"

    ```sh
    poetry add python-simple-secrets-manager
    poetry install
    ```

=== "conda"

    ```sh
    conda create -n pssm python=3.11 -y
    conda activate pssm
    pip install python-simple-secrets-manager
    ```


## Usage

You can test to make sure it has successfully installed with:

```sh
secrets --version
```

Which should return this output:

```sh
python-simple-secrets-manager, version [number]
```

You can now add a secret. You will be prompted to specify the uid and key.

```sh
secrets keep
```

Then, if you want to access the secret from within python, just make sure the package is installed and get the secret by the uid set earlier.

```python
from pssm import secrets
token = secrets.get("secret_uid")
```

More details on other available commands/methods, and how the package works on the backend are available in the [[tutorial.ipynb|tutorial]] notebook.