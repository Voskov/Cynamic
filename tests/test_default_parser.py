import pickle
import shelve
from pathlib import Path
from typing import Iterable

import pytest

from handlers.json_handler import JSONHandler
from models.traffic_sample import TrafficSample
from parsers.defaultparser import DefaultParser


class TestDefaultParser:
    sample_data_path = Path(__file__).parent / ".." / "sample_data"

    @pytest.fixture(autouse=True)
    def parser(self):
        return DefaultParser()

    @pytest.fixture(autouse=True)
    def sample_data(self) -> dict:
        return {
            "srcip": "172.17.201.3",
            "dstip": "10.42.16.116",
            "srcport": 8092,
            "dstport": 37771,
            "protocol": 6,
            "numbytes": 1500,
            "numpackets": 1
        }

    @pytest.fixture()
    def expected_traffic_sample(self) -> TrafficSample:
        sample_path = self.sample_data_path / "traffic_sample.pkl"
        return pickle.load(open(sample_path, "rb"))

    @pytest.fixture()
    def sample_batch_data(self) -> Iterable[dict]:
        # assumes that the JSONHandler is working correctly
        sample_path = self.sample_data_path / "sample_data.json"
        sample_data = JSONHandler().read(sample_path)
        return sample_data

    @pytest.fixture()
    def expected_batch(self) -> list[TrafficSample]:
        sample_path = self.sample_data_path / "traffic_samples.shlv"
        with shelve.open(str(sample_path), "r") as traffic_samples:
            return list(traffic_samples.values())

    def test_parse_parse_sample(self, parser: DefaultParser, sample_data: dict, expected_traffic_sample: TrafficSample):
        res = parser.parse_traffic_sample(sample_data)
        assert res == expected_traffic_sample

    def test_parse_batch(self, parser: DefaultParser, sample_batch_data: Iterable[dict], expected_batch: list[TrafficSample]):
        res = parser.parse_batch(sample_batch_data)
        traffic_samples = list(res)
        assert len(traffic_samples) == len(expected_batch)
        assert all(sample in expected_batch for sample in traffic_samples)


