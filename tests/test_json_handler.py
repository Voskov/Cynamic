import types
from pathlib import Path

import pytest

from handlers.json_handler import JSONHandler
from tests.test_file_handler import TestFileHandler


class TestJSONHandler(TestFileHandler):
    @pytest.fixture(autouse=True)
    def handler(self) -> JSONHandler:
        return JSONHandler()

    @pytest.fixture(autouse=True)
    def sample_data_path(self) -> Path:
        return Path(__file__).parent / ".." / "sample_data" / "sample_data.json"

    def test_read(self, handler: JSONHandler, sample_data_path: Path):
        res = handler.read(sample_data_path)
        assert isinstance(res, types.GeneratorType)
        assert len(list(res)) == 500
        assert all(isinstance(row, dict) for row in res)
