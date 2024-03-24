import csv
from pathlib import Path
from typing import Iterable

from handlers.file_handler import FileHandler


class CSVHandler(FileHandler):
    @staticmethod
    def read(file_path: Path) -> Iterable[dict]:
        with open(file_path) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            yield from [row for row in csv_reader]
