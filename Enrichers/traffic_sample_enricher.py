from datetime import datetime
from ipaddress import IPv4Address, IPv4Network

from models.traffic_sample import TrafficSample


class TrafficSampleEnricher:
    @classmethod
    def enrich(cls, traffic_sample: TrafficSample) -> TrafficSample:
        cls.enrich_with_subnet_classes(traffic_sample)
        cls.enrich_with_process_time(traffic_sample)
        return traffic_sample

    @classmethod
    def enrich_with_subnet_classes(cls, traffic_sample: TrafficSample) -> TrafficSample:
        traffic_sample.src_subnet_class_A = cls.get_subnet(traffic_sample.srcip, 8)
        traffic_sample.src_subnet_class_B = cls.get_subnet(traffic_sample.srcip, 16)
        traffic_sample.src_subnet_class_C = cls.get_subnet(traffic_sample.srcip, 24)
        traffic_sample.dst_subnet_class_A = cls.get_subnet(traffic_sample.dstip, 8)
        traffic_sample.dst_subnet_class_B = cls.get_subnet(traffic_sample.dstip, 16)
        traffic_sample.dst_subnet_class_C = cls.get_subnet(traffic_sample.dstip, 24)
        return traffic_sample

    @staticmethod
    def enrich_with_process_time(traffic_sample: TrafficSample) -> TrafficSample:
        traffic_sample.processing_time = datetime.now().isoformat()
        return traffic_sample

    @classmethod
    def get_subnet(cls, ip_address: IPv4Address, prefixlen: int) -> IPv4Address:
        network = IPv4Network(str(ip_address) + f'/{prefixlen}', strict=False)
        return network.network_address
