def secret_name(name: str) -> None:
    # secret name must be only alphanumeric and underscore, and cannot start with number
    if not len(name):
        raise ValueError("the secret name must be at least one character long")
    if name[0].isnumeric():
        raise ValueError("the secret name cannot start with a number")
    if not all([i.isalnum() or i == "_" for i in name]):
        raise ValueError(
            "the secret name can only contain alphanumeric and underscore chars"
        )
