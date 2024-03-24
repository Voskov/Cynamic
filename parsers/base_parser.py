from abc import ABC, abstractmethod
from typing import Iterable

from models.traffic_sample import TrafficSample


class BaseParser(ABC):
    @staticmethod
    @abstractmethod
    def parse_batch(self, batch: Iterable[dict]) -> Iterable[TrafficSample]:
        pass

    @staticmethod
    @abstractmethod
    def parse_traffic_sample(data: dict) -> TrafficSample:
        pass

