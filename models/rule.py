from ipaddress import IPv4Address

from pydantic import BaseModel

from models.traffic_sample import TrafficSampleAttribute, TrafficSample


class Rule(BaseModel):
    allow: bool = True
    resource: TrafficSampleAttribute


class IPRule(Rule):
    ips: set[IPv4Address] | None


class PortRule(Rule):
    ports: set[int] | None


class SubnetRule(Rule):
    subnet: IPv4Address | None


class RuleFactory:
    @classmethod
    def create_rule(cls, rule_type: str, allow: bool = True, value: str | IPv4Address | int = None | list, **kwargs):
        if not hasattr(TrafficSample, rule_type):
            raise AttributeError(f"TrafficSample has no attribute {rule_type}")
        match rule_type:
            case "srcip" | "dstip":
                return cls.create_ip_rule(rule_type, allow, value)
            case "srcport" | "dstport":
                return cls.create_port_rule(rule_type, allow, value)
            case "src_subnet_class_A" | "src_subnet_class_B" | "src_subnet_class_C" | "dst_subnet_class_A" | "dst_subnet_class_B" | "dst_subnet_class_C":
                pass  # WIP

    @classmethod
    def create_ip_rule(cls,
                       rule_type: str,
                       allow: bool,
                       value: str | IPv4Address | list[IPv4Address] | list[str] | None):
        ips = set[IPv4Address]()
        if isinstance(value, list):
            for ip in value:
                if isinstance(ip, str):
                    ip = IPv4Address(ip)
                if isinstance(ip, IPv4Address):
                    ips.add(ip)
        if isinstance(value, str):
            ips.add(IPv4Address(value))
        if isinstance(value, IPv4Address):
            ips.add(value)

        return IPRule(allow=allow, resource=rule_type, ips=ips)

    @classmethod
    def create_port_rule(cls, rule_type: str, allow: bool, value: int | list[int] | None):
        ports = set[int]()
        if isinstance(value, range):
            # sure, it's faster to check whether something in range.
            # but the range of ports isn't that big, and I don't want to add MORE complexity to this code.
            value = list(value)
        if isinstance(value, list):
            for port in value:
                if isinstance(port, int):
                    ports.add(port)
        if isinstance(value, int):
            ports.add(value)

        return PortRule(allow=allow, resource=rule_type, ports=ports)
