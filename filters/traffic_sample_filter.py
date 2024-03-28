from typing import Iterable

from models.rule import Rule
from models.traffic_sample import TrafficSample


class TrafficSampleFilter:
    rules: Iterable[Rule]

    def __init__(self, rules: Iterable[Rule] | None = None):
        self.rules = rules

    def filter_samples_with_rules(self, samples: Iterable[TrafficSample]):
        for sample in samples:
            if self.enforce_rules(sample):
                yield sample

    def enforce_rules(self, sample: TrafficSample) -> bool:
        for rule in self.rules:
            rule.enforce(sample)
