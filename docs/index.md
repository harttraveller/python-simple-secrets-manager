# Overview

This package makes it easier to store and retrieve secrets. Suppose you're developing a python package that needs to access external API services. To test the package, you need to be able to load your API key, but users of your package should sign up to get their own API key. One way to circumvent this is to create something like the following directory structure:

```
my_package/
├── __init__.py
└── ...
secrets.yaml
.gitignore
```

And then in your `.gitignore` add `secrets.yaml`.

There are two main drawbacks to this approach (or any other similar approach):

1. You might accidentally commit the secrets anyways (say if you revert to a branch where `secrets.yaml` was not in the gitignore and then commit).
2. You can't access these secrets from other projects.

This package addresses both of these issues.

!!! note
    Currently this package does not offer major security benefits over simply using global environment variables, although it is ideally easier to use. Future versions will incorporate enhanced security measures, time permitting.
