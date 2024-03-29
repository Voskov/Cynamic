import pickle
from datetime import datetime, timedelta
from ipaddress import IPv4Address
from pathlib import Path

import pytest

from Enrichers.traffic_sample_enricher import TrafficSampleEnricher
from models.traffic_sample import TrafficSample


class TestTrafficSampleEnricher:
    sample_data_path = Path(__file__).parent / ".." / "sample_data"

    @pytest.fixture(autouse=True)
    def enricher(self):
        return TrafficSampleEnricher()

    @pytest.fixture()
    def traffic_sample(self) -> TrafficSample:
        sample_path = self.sample_data_path / "traffic_sample.pkl"
        return pickle.load(open(sample_path, "rb"))

    def test_enrich_processing_time(self, enricher: TrafficSampleEnricher, traffic_sample: TrafficSample):
        enriched_sample = enricher.enrich_with_process_time(traffic_sample)
        now = datetime.now()
        parsed_processing_time = datetime.fromisoformat(enriched_sample.processing_time)
        tolerance = timedelta(milliseconds=100)
        assert now - parsed_processing_time < tolerance

    def test_get_subnet(self, enricher: TrafficSampleEnricher, traffic_sample: TrafficSample):
        src_ip = IPv4Address('172.17.201.3')
        assert enricher.get_subnet(src_ip, 24) == IPv4Address('172.17.201.0')
        assert enricher.get_subnet(src_ip, 16) == IPv4Address('172.17.0.0')
        assert enricher.get_subnet(src_ip, 8) == IPv4Address('172.0.0.0')

    def test_enrich_with_subnet_classes(self, enricher: TrafficSampleEnricher, traffic_sample: TrafficSample):
        enriched_sample = enricher.enrich_with_subnet_classes(traffic_sample)
        assert enriched_sample.src_subnet_class_A == IPv4Address('172.0.0.0')
        assert enriched_sample.src_subnet_class_B == IPv4Address('172.17.0.0')
        assert enriched_sample.src_subnet_class_C == IPv4Address('172.17.201.0')
        assert enriched_sample.dst_subnet_class_A == IPv4Address('10.0.0.0')
        assert enriched_sample.dst_subnet_class_B == IPv4Address('10.42.0.0')
        assert enriched_sample.dst_subnet_class_C == IPv4Address('10.42.16.0')

    def test_enrich(self, enricher: TrafficSampleEnricher, traffic_sample: TrafficSample):
        enriched_sample = enricher.enrich(traffic_sample)
        now = datetime.now()
        parsed_processing_time = datetime.fromisoformat(enriched_sample.processing_time)
        tolerance = timedelta(milliseconds=100)
        assert now - parsed_processing_time < tolerance
        assert enriched_sample.src_subnet_class_A == IPv4Address('172.0.0.0')


class TestAttributeParse:
    def test_parse_attribute_string(self):
        from models.traffic_sample import TrafficSample
        sample = TrafficSample()
        assert sample.parse_attribute_string("SRC IP") == "srcip"
        assert sample.parse_attribute_string("DST IP") == "dstip"
        assert sample.parse_attribute_string("SRC port") == "srcport"
        assert sample.parse_attribute_string("DST port") == "dstport"
        assert sample.parse_attribute_string("Protocol") == "protocol"
        assert sample.parse_attribute_string("SRC Subnet class A") == "src_subnet_class_A"
        assert sample.parse_attribute_string("SRC Subnet class B") == "src_subnet_class_B"
        assert sample.parse_attribute_string("SRC Subnet class C") == "src_subnet_class_C"
        assert sample.parse_attribute_string("DST Subnet class A") == "dst_subnet_class_A"
        assert sample.parse_attribute_string("DST Subnet class B") == "dst_subnet_class_B"
        assert sample.parse_attribute_string("DST Subnet class C") == "dst_subnet_class_C"
