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
