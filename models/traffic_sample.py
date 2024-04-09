import ipaddress
from typing import Optional, Literal

from pydantic import BaseModel, PositiveInt, Field


class TrafficSample(BaseModel):
    srcip: Optional[ipaddress.IPv4Address] = Field(None, alias="SRC IP")
    dstip: Optional[ipaddress.IPv4Address] = Field(None, alias="DST IP")
    srcport: Optional[PositiveInt] = Field(None, alias="SRC port")
    dstport: Optional[PositiveInt] = Field(None, alias="DST port")
    protocol: Optional[PositiveInt] = Field(None, alias="Protocol")
    numbytes: Optional[PositiveInt] = Field(None, alias="NumBytes")
    numpackets: Optional[PositiveInt] = Field(None, alias="NumPackets")
    processing_time: Optional[str] = Field(None, alias="Processing Time")
    src_subnet_class_A: Optional[ipaddress.IPv4Address] = Field(None, alias="SRC Subnet class A")
    src_subnet_class_B: Optional[ipaddress.IPv4Address] = Field(None, alias="SRC Subnet class B")
    src_subnet_class_C: Optional[ipaddress.IPv4Address] = Field(None, alias="SRC Subnet class C")
    dst_subnet_class_A: Optional[ipaddress.IPv4Address] = Field(None, alias="DST Subnet class A")
    dst_subnet_class_B: Optional[ipaddress.IPv4Address] = Field(None, alias="DST Subnet class B")
    dst_subnet_class_C: Optional[ipaddress.IPv4Address] = Field(None, alias="DST Subnet class C")

    @classmethod
    def parse_attribute_string(cls, attribute_string: str) -> str:
        try:
            return {v.alias.lower(): k for k, v in cls.__fields__.items()}[attribute_string.lower()]
        except KeyError:
            raise AttributeError(f"TrafficSample has no attribute {attribute_string}")


# fields = (f.alias for f in TrafficSample.__fields__.values())
fields = (TrafficSample.__fields__.keys())
TrafficSampleAttribute = Literal[*fields]
