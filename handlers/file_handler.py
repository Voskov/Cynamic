from abc import abstractmethod
from typing import Iterable

from loguru import logger

from handlers.base_handler import BaseHandler


class FileHandler(BaseHandler):
    def __init__(self) -> None:
        pass

    @staticmethod
    @abstractmethod
    def read(file_path) -> Iterable[dict]:
        pass
