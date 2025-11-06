"""Helper functions."""

from typing import Any, Generator

import xxhash

# Minimum data size hashed is 4KiB, maximum is 4GiB
OFFSETS = [0x10**i for i in range(3, 9)]


def incremental_hash(
    data: bytes, offsets=OFFSETS, from_start_of_file: bool = True
) -> Generator[tuple[int, str], Any, None]:
    """Generates incremental hashes of the given data at specified offsets.

    Args:
        data (bytes): The input data to hash.
        offsets (list[int]): A list of integer offsets at which to compute the hash.
        from_start_of_file (bool): Whether to hash from the start (or end) of file.

    Yields:
        Generator[tuple[int, str], Any, None]: A generator that yields tuples containing the current offset and the
        corresponding hash value as a hexadecimal string.

    Example:
        >>> data = b"example data"
        >>> offsets = [4, 8, 12]

        >>> # hashes data[:4], data[:8], data[:12]
        >>> for offset, hash_value in incremental_hash(data, offsets):
        ...     print(f"Offset: {offset}, Hash: {hash_value}")

        >>> # hashes data[-4:], data[-8:], data[-12:]
        >>> for offset, hash_value in incremental_hash(data, offsets, False):
        ...     print(f"Offset: {offset}, Hash: {hash_value}")
    """
    last_size = 0
    digest = xxhash.xxh3_64()

    for current_size in offsets:
        if current_size > len(data):
            break

        if from_start_of_file:
            # Take hash of data slice up to current_size
            chunk = data[last_size:current_size]
            digest.update(chunk)

            yield (current_size, digest.hexdigest())
            # Prepare for next iteration
            last_size = current_size
        else:
            yield (current_size, xxhash.xxh3_64(data[-1 * current_size :]).hexdigest())


def should_opt_out(data: bytes, minimum_size: int = 0) -> bool:
    """Determine whether to opt-out from file."""
    # Require minimum filesize
    return len(data) < minimum_size
