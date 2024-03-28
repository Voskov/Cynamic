import ipaddress
from typing import Optional, Literal

from pydantic import BaseModel, PositiveInt


class TrafficSample(BaseModel):
    srcip: Optional[ipaddress.IPv4Address] = None
    dstip: Optional[ipaddress.IPv4Address] = None
    srcport: Optional[PositiveInt] = None
    dstport: Optional[PositiveInt] = None
    protocol: Optional[PositiveInt] = None
    numbytes: Optional[PositiveInt] = None
    numpackets: Optional[PositiveInt] = None
    processing_time: Optional[str] = None
    src_subnet_class_A: Optional[ipaddress.IPv4Address] = None
    src_subnet_class_B: Optional[ipaddress.IPv4Address] = None
    src_subnet_class_C: Optional[ipaddress.IPv4Address] = None
    dst_subnet_class_A: Optional[ipaddress.IPv4Address] = None
    dst_subnet_class_B: Optional[ipaddress.IPv4Address] = None
    dst_subnet_class_C: Optional[ipaddress.IPv4Address] = None


fields = tuple(TrafficSample.__annotations__.keys())
TrafficSampleAttribute = Literal[*fields]
