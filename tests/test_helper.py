"""Test helper functions."""

import random
import unittest

import xxhash

from azul_plugin_truncated.helper import incremental_hash


class TestDigest(unittest.TestCase):
    """Test methods used for hashing."""

    random.seed(1)
    random_0x1000_bytes = random.randbytes(0x1000)
    random_0x50000_bytes = random.randbytes(0x50000)

    def test_small_hash_all_nulls(self):
        """Ensure consistency of result of hashing."""
        _, digest_x = next(incremental_hash(b"\x00" * 0x1000))
        _, digest_y = next(incremental_hash(b"\x00" * 0x1000, from_start_of_file=False))
        self.assertEqual(digest_x, "93d76fe148c689ba")
        self.assertEqual(digest_y, digest_y)

    def test_small_hash_high_entropy_data(self):
        """Ensure consistency of result of hashing."""

        _, digest_x = next(incremental_hash(TestDigest.random_0x1000_bytes))
        _, digest_y = next(incremental_hash(TestDigest.random_0x1000_bytes, from_start_of_file=False))
        self.assertEqual(digest_x, "3b01999a1ccca0d9")
        self.assertEqual(digest_x, digest_y)

    def test_reversed_hash_on_not_aligned_data(self):
        """Ensure offsets are calculated as expected."""
        expected_leading_hash_0x1000 = xxhash.xxh3_64(TestDigest.random_0x50000_bytes[:0x1000]).hexdigest()
        expected_leading_hash_0x10000 = xxhash.xxh3_64(TestDigest.random_0x50000_bytes[:0x10000]).hexdigest()
        expected_trailing_hash_0x1000 = xxhash.xxh3_64(TestDigest.random_0x50000_bytes[-0x1000:]).hexdigest()
        expected_trailing_hash_0x10000 = xxhash.xxh3_64(TestDigest.random_0x50000_bytes[-0x10000:]).hexdigest()
        self.assertEqual(
            [(0x1000, expected_leading_hash_0x1000), (0x10000, expected_leading_hash_0x10000)],
            list(incremental_hash(TestDigest.random_0x50000_bytes)),
        )
        self.assertEqual(
            [(0x1000, expected_trailing_hash_0x1000), (0x10000, expected_trailing_hash_0x10000)],
            list(incremental_hash(TestDigest.random_0x50000_bytes, from_start_of_file=False)),
        )

    def test_end_of_offset(self):
        """Ensure no hashing past final offset."""
        offsets_provided = [4, 8, 12, 16]
        results = list(incremental_hash(TestDigest.random_0x50000_bytes, offsets=offsets_provided))
        hashed_offsets = [t[0] for t in results]
        self.assertEqual(hashed_offsets, offsets_provided)

    def test_incremental_hashing_logic(self):
        """Ensure logic around incremental hashing gives a correct result.

        Calculating a single hash of the data should be equal to the incrementally generated hash of the same data."""
        text = b"A" * 0x100000
        total_hash = xxhash.xxh3_64(text).hexdigest()
        self.assertTrue(total_hash in [digest for size, digest in incremental_hash(text)])

    def test_hashing_limit(self):
        """Ensure hashing completes on a power of 0x10."""
        text = b"A" * 0x24321
        last_hash = xxhash.xxh3_64(text[:0x10000]).hexdigest()
        sizes_generated = [size for size, digest in incremental_hash(text)]
        hashes_generated = [digest for size, digest in incremental_hash(text)]
        self.assertTrue(sizes_generated == [0x1000, 0x10000])
        self.assertTrue(last_hash == hashes_generated[-1])
