import dataclasses


@dataclasses.dataclass
class Interface:
    private_key: str = ""
    address: list[str] = dataclasses.field(default_factory=list)
    dns: list[str] = dataclasses.field(default_factory=list)
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
    name: str = "Tunnel"
    interface: Interface = Interface()
    peer: Peer = Peer()
