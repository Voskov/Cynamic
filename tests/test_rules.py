import pickle
import shelve
from ipaddress import IPv4Address
from pathlib import Path
from typing import Iterable

import pytest

from models.rule import RuleFactory
from models.traffic_sample import TrafficSample


class TestRules:
    sample_data_path = Path(__file__).parent / ".." / "sample_data"

    @pytest.fixture(autouse=True)
    def rule_factory(self):
        return RuleFactory()

    @pytest.fixture()
    def traffic_sample(self) -> TrafficSample:
        sample_path = self.sample_data_path / "traffic_sample.pkl"
        return pickle.load(open(sample_path, "rb"))

    class TestSingleRule:
        def test_rule_enforce_allow(self, traffic_sample: TrafficSample, rule_factory: RuleFactory) -> None:
            rule = rule_factory.create_general_rule('srcip', allow=True, values={traffic_sample.srcip})
            assert rule.enforce(traffic_sample)

        def test_rule_enforce_deny(self, traffic_sample: TrafficSample, rule_factory: RuleFactory) -> None:
            rule = rule_factory.create_general_rule('srcip', allow=False, values={traffic_sample.srcip})
            assert not rule.enforce(traffic_sample)

        def test_rule_enforce_allow_port(self, traffic_sample: TrafficSample, rule_factory: RuleFactory) -> None:
            rule = rule_factory.create_general_rule('dstport', allow=True, values={traffic_sample.dstport})
            assert rule.enforce(traffic_sample)

        def test_rule_enforce_deny_port(self, traffic_sample: TrafficSample, rule_factory: RuleFactory) -> None:
            rule = rule_factory.create_general_rule('dstport', allow=False, values={traffic_sample.dstport})
            assert not rule.enforce(traffic_sample)

        def test_rule_enforce_deny_different_ip(self, traffic_sample: TrafficSample, rule_factory: RuleFactory) -> None:
            rule = rule_factory.create_general_rule('srcip', allow=True, values=IPv4Address('192.168.1.1'))
            assert not rule.enforce(traffic_sample)

        def test_rule_enforce_allow_different_ip(self, traffic_sample: TrafficSample,
                                                 rule_factory: RuleFactory) -> None:
            rule = rule_factory.create_general_rule('srcip', allow=False, values=IPv4Address('192.168.1.1'))
            assert rule.enforce(traffic_sample)

        def test_rule_enforce_allow_several_ports(self, traffic_sample: TrafficSample,
                                                  rule_factory: RuleFactory) -> None:
            rule = rule_factory.create_general_rule('dstport', allow=True, values=[37770, 37771, 37772])
            assert rule.enforce(traffic_sample)

        def test_rule_enforce_deny_several_ports(self, traffic_sample: TrafficSample,
                                                 rule_factory: RuleFactory) -> None:
            rule = rule_factory.create_general_rule('dstport', allow=False, values=[37770, 37771, 37772])
            assert not rule.enforce(traffic_sample)

    class TestLiteralRule:
        def test_literal_rule_src_allow(self, rule_factory: RuleFactory) -> None:
            rule_str = "ALLOW: Src Subnet Class A == 10.0.0.0"
            expected = rule_factory.create_general_rule('src_subnet_class_A', allow=True,
                                                        values=IPv4Address('10.0.0.0'))
            rule = RuleFactory.create_parse_rule_string(rule_str)[0]
            assert rule == expected
