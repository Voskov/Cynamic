import types
from pathlib import Path

import pytest

from handlers.csv_handler import CSVHandler
from tests.test_file_handler import TestFileHandler


class TestCSVHandler(TestFileHandler):
    @pytest.fixture(autouse=True)
    def handler(self) -> CSVHandler:
        return CSVHandler()

    @pytest.fixture(autouse=True)
    def sample_data_path(self) -> Path:
        return Path(__file__).parent / ".." / "sample_data" / "sample_data.csv"

    def test_read(self, handler: CSVHandler, sample_data_path: Path):
        res = handler.read(sample_data_path)
        assert isinstance(res, types.GeneratorType)
        assert len(list(res)) == 500
        assert all(isinstance(row, dict) for row in res)
