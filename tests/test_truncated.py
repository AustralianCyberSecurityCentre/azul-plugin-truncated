"""Test truncated files plugin."""

from azul_runner import FV, Event, JobResult, State, test_template

from azul_plugin_truncated.main import AzulPluginTruncated


class TestTruncated(test_template.TestPlugin):
    """Test truncated files logic."""

    PLUGIN_TO_TEST = AzulPluginTruncated

    def test_opt_out_on_small_file(self):
        """Test on a file that's too small."""
        data = self.load_test_file_bytes(
            "7bb6f9f7a47a63e684925af3608c059edcc371eb81188c48c9714896fb1091fd", "Benign ASCII text file."
        )
        result = self.do_execution(data_in=[("content", data)])
        self.assertJobResult(result, JobResult(state=State(State.Label.OPT_OUT)))

    def test_sufficient_small_file(self):
        """Test on a file barely large enough."""
        data = self.load_test_file_bytes(
            "c57b36912f69bb3c680d0f213a959443b2e98cd7479e595be45715e3fd5b9bb7",
            "Benign Windows 32EXE, called rundll.exe.",
        )
        result = self.do_execution(data_in=[("content", data)])
        self.assertJobResult(
            result,
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        entity_type="binary",
                        entity_id="c57b36912f69bb3c680d0f213a959443b2e98cd7479e595be45715e3fd5b9bb7",
                        features={
                            "leading_partial_hash": [FV("e9c572df647153a9", label="0x1000")],
                            "trailing_partial_hash": [FV("6408c50909f60912", label="0x1000")],
                        },
                    )
                ],
            ),
        )

    def test_incremental_hash(self):
        """Test on a larger file."""
        data = self.load_test_file_bytes(
            "1552f6a579b77b61460df56cb4b2ce0a34fe96b6176829d7916275b806edc2bb", "Windows 32EXE, without overlay."
        )
        result = self.do_execution(data_in=[("content", data)])
        self.assertJobResult(
            result,
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        sha256="1552f6a579b77b61460df56cb4b2ce0a34fe96b6176829d7916275b806edc2bb",
                        features={
                            "leading_partial_hash": [
                                FV("1c6c206e686f0828", label="0x1000"),
                                FV("e33004ee001124e2", label="0x10000"),
                            ],
                            "trailing_partial_hash": [
                                FV("30c82ca3e94d23f8", label="0x10000"),
                                FV("f8f02d9c15418e3f", label="0x1000"),
                            ],
                        },
                    )
                ],
            ),
        )

    def test_pe_with_overlay(self):
        """Test execution on pe with overlay."""
        data = self.load_test_file_bytes(
            "39af08d3477203cb8188c88db44b6dcfebe2ba901ea6b35977d814cf29e87dbf",
            "Malicious Windows 32DLL, malware family graftor.",
        )
        result = self.do_execution(data_in=[("content", data)])
        self.assertJobResult(
            result,
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        entity_type="binary",
                        entity_id="39af08d3477203cb8188c88db44b6dcfebe2ba901ea6b35977d814cf29e87dbf",
                        features={
                            "leading_partial_hash": [
                                FV("c83a9f65195a7d7a", label="0x1000"),
                                FV("a98a65ac9b8a973c", label="0x10000"),
                            ],
                            "trailing_partial_hash": [
                                FV("60e042f9aea6a75f", label="0x1000"),
                                FV("7cd67617cb96576d", label="0x10000"),
                            ],
                        },
                    )
                ],
            ),
        )
