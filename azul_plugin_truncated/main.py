"""Partially hash files to find untruncated versions."""

from azul_runner import FV, BinaryPlugin, Feature, FeatureType, Job, State, cmdline_run

from .helper import OFFSETS, incremental_hash, should_opt_out

MINIMUM_SIZE = OFFSETS[0]


class AzulPluginTruncated(BinaryPlugin):
    """Partially hash files to assist with linking truncated samples."""

    VERSION = "2025.02.14"

    FEATURES = [
        Feature(
            name="leading_partial_hash",
            desc="XX3 partial hash of n leading bytes",
            type=FeatureType.String,
        ),
        Feature(
            name="trailing_partial_hash",
            desc="XX3 partial hash of n trailing bytes",
            type=FeatureType.String,
        ),
    ]

    def execute(self, job: Job):
        """Run the plugin."""
        buf = job.get_data().read()

        if should_opt_out(buf, minimum_size=MINIMUM_SIZE):
            return State.Label.OPT_OUT

        for size, digest in incremental_hash(buf):
            self.add_feature_values("leading_partial_hash", FV(digest, label=hex(size)))
        for size, digest in incremental_hash(buf, from_start_of_file=False):
            self.add_feature_values("trailing_partial_hash", FV(digest, label=hex(size)))


def main():
    """Plugin command-line entrypoint."""
    cmdline_run(plugin=AzulPluginTruncated)


if __name__ == "__main__":
    main()
