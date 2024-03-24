import json
from typing import Iterable

from handlers.file_handler import FileHandler


class JSONHandlerException(Exception):
    pass


class JSONHandler(FileHandler):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def read(file_path) -> Iterable[dict]:
        # todo consider dealing huge files and streams
        with open(file_path) as file:
            yield from json.load(file)
