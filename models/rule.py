from abc import abstractmethod
from ipaddress import IPv4Address
from typing import Iterable

from pydantic import BaseModel

from models.traffic_sample import TrafficSampleAttribute, TrafficSample


class Rule(BaseModel):
    allow: bool = True
    resource: TrafficSampleAttribute

    @abstractmethod
    def enforce(self, traffic_sample: TrafficSample) -> bool:
        pass


class GeneralRule(Rule):
    values: set | None

    def enforce(self, traffic_sample: TrafficSample) -> bool:
        if self.values is None:
            return self.allow
        if sample_data := getattr(traffic_sample, self.resource):
            if sample_data in self.values:
                return self.allow
        return not self.allow


class IPRule(Rule):
    ips: set[IPv4Address] | None

    def enforce(self, traffic_sample: TrafficSample) -> bool:
        if self.ips is None:
            return self.allow
        if sample_data := getattr(traffic_sample, self.resource):
            if sample_data in self.ips:
                return self.allow
        return not self.allow


class PortRule(Rule):
    ports: set[int] | None

    def enforce(self, traffic_sample: TrafficSample) -> bool:
        if self.ports is None:
            return self.allow
        if sample_port := getattr(traffic_sample, self.resource):
            if sample_port in self.ports:
                return self.allow
        return not self.allow


class RuleFactory:

    @classmethod
    def create_parse_rule_string(cls, rule_string: str) -> list[Rule]:
        if ':' not in rule_string:
            allow_str = rule_string.split(' ')[0] == 'ALLOW'
            # TODO
            return [GeneralRule(allow=allow_str, resource=rule_string.split(' ')[1], values=None)]  # placeholder
        allow_str, rule_literal = rule_string.split(':')
        allow = allow_str == 'ALLOW'

    @classmethod
    def create_general_rule(cls, rule_type: str, allow: bool, values):
        if isinstance(values, Iterable):
            values = set(values)
        else:
            values = {values}
        return GeneralRule(allow=allow, resource=rule_type, values=values)
