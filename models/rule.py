from abc import abstractmethod
from ipaddress import IPv4Address, AddressValueError
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

    def __eq__(self, other):
        return self.allow == other.allow and self.resource == other.resource and self.values == other.values


class RuleFactory:
    @classmethod
    def create_parse_rule_string(cls, rule_string: str) -> list[Rule]:
        if ':' not in rule_string:
            allow_str = rule_string.split(' ')[0] == 'ALLOW'
            # TODO
            return [GeneralRule(allow=allow_str, resource=rule_string.split(' ')[1], values=None)]  # placeholder
        allow_str, rule_literal = [s.strip() for s in rule_string.split(':')]
        rule_type_str, value = [s.strip() for s in rule_literal.split('==')]
        rule_type = TrafficSample.parse_attribute_string(rule_type_str)
        allow = allow_str == 'ALLOW'
        return [cls.create_general_rule(rule_type=rule_type,
                                        allow=allow,
                                        values=value)]

    @classmethod
    def create_general_rule(cls, rule_type: str, allow: bool, values):
        # TODO - organize
        if isinstance(values, str):
            try:
                values = {IPv4Address(values)}
            except AddressValueError:
                values = {values}
        elif isinstance(values, Iterable):
            values = set(values)
        else:
            values = {values}
        return GeneralRule(allow=allow, resource=rule_type, values=values)
