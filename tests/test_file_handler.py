from abc import abstractmethod
from pathlib import Path

import pytest

from handlers.file_handler import FileHandler


class TestFileHandler:
    @pytest.mark.skip
    def test_read(self, csv_handler: FileHandler, sample_data_path: Path):
        pass
