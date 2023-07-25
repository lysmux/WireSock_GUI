import dataclasses
import typing


@dataclasses.dataclass
class Interface:
    private_key: str = ""
    address: typing.Union[str, list[str]] = ""
    dns: typing.Union[str, list[str]] = ""
    mtu: int = 1280


@dataclasses.dataclass
class Peer:
    public_key: str = ""
    endpoint: str = ""
    allowed_ips: list[str] = dataclasses.field(default_factory=list)
    disallowed_ips: list[str] = dataclasses.field(default_factory=list)
    allowed_apps: list[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Tunnel:
    interface: Interface
    peer: Peer
