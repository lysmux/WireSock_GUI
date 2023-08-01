from dataclasses import dataclass, field


@dataclass
class Interface:
    private_key: str = field(default="")
    address: list[str] = field(default_factory=list)
    dns: list[str] = field(default_factory=list)
    mtu: int = field(default=1280)


@dataclass
class Peer:
    public_key: str = field(default="")
    pre_shared_key: str = field(default="")
    endpoint: str = field(default="")
    allowed_ips: list[str] = field(default_factory=list)
    disallowed_ips: list[str] = field(default_factory=list)
    allowed_apps: list[str] = field(default_factory=list)
    disallowed_apps: list[str] = field(default_factory=list)
    persistent_keepalive: int = field(default=25)


@dataclass
class Tunnel:
    name: str = field(default="Tunnel")
    interface: Interface = Interface()
    peer: Peer = Peer()


@dataclass
class WGStat:
    time_since_last_handshake: int = field(default=0)
    tx_bytes: int = field(default=0)
    rx_bytes: int = field(default=0)
    estimated_loss: float = field(default=0)
    estimated_rtt: int = field(default=0)
