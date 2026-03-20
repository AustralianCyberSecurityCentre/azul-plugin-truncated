# Azul Plugin Truncated

Provides incremental hashes of files, intended to assist with find untruncated versions.

## Installation

```
pip install azul-plugin-truncated
```

## Usage

Usage on local files:

````
$ azul-plugin-truncated 08700246cd7fc8d637c294e2ab1e4790594938f1aec49be5c4e0bf2112124e3f
----- AzulPluginTruncated results -----
COMPLETED

events (1)

event for binary:08700246cd7fc8d637c294e2ab1e4790594938f1aec49be5c4e0bf2112124e3f:None
  {}
  output features:
     leading_partial_hash: 0x10000 - accd727f18779d9b
                           0x100000 - ea5c569218bbbad6
                           0x1000 - fbfe7c0a91d271eb
    trailing_partial_hash: 0x1000 - 4f6576191741e81b
                           0x100000 - 914b8ee053cf0302
                           0x10000 - 991c97dd9982d967

Feature key:
  leading_partial_hash:  XX3 partial hash of n leading bytes
  trailing_partial_hash:  XX3 partial hash of n trailing bytes```

Check `azul-plugin-truncated --help` for advanced usage.

````

## Dependency management

Dependencies are managed in the pyproject.toml and debian.txt file.

Version pinning is achieved using the `uv.lock` file.
Because the `uv.lock` file is configured to use a private UV registry, external developers using UV will need to delete the existing `uv.lock` file and update the project configuration to point to the publicly available PyPI registry instead.

To add new dependencies it's recommended to use uv with the command `uv add <new-package>`
    or for a dev package `uv add --dev <new-dev-package>`

The tool used for linting and managing styling is `ruff` and it is configured via `pyproject.toml`

The debian.txt file manages the debian dependencies that need to be installed on development systems and docker images.

Sometimes the debian.txt file is insufficient and in this case the Dockerfile may need to be modified directly to
install complex dependencies.
