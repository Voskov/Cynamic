from typing import Iterable

from loguru import logger

from models.traffic_sample import TrafficSample
from parsers.base_parser import BaseParser


class DefaultParser(BaseParser):
    @classmethod
    def parse_batch(cls, batch: Iterable[dict]) -> Iterable[TrafficSample]:
        for raw_sample in batch:
            try:
                yield cls.parse_traffic_sample(raw_sample)
            except Exception as e:
                logger.exception(f'Failed to parse traffic sample - {e}')

    @staticmethod
    def parse_traffic_sample(data: dict) -> TrafficSample:
        return TrafficSample(
            srcip=data.get('srcip'),
            dstip=data.get('dstip'),
            srcport=data.get('srcport'),
            dstport=data.get('dstport'),
            protocol=data.get('proto'),
            numbytes=data.get('numbytes'),
            numpackets=data.get('numpackets'),
        )
