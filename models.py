from dataclasses import dataclass, field


@dataclass
class Interface:
    private_key: str = field(default="")
    address: list[str] = field(default_factory=lambda: [])
    dns: list[str] = field(default_factory=lambda: [])
    mtu: int = field(default=1280)


@dataclass
class Peer:
    public_key: str = field(default="")
    pre_shared_key: str = field(default="")
    endpoint: str = field(default="")
    allowed_ips: list[str] = field(default_factory=lambda: [])
    disallowed_ips: list[str] = field(default_factory=lambda: [])
    allowed_apps: list[str] = field(default_factory=lambda: [])
    disallowed_apps: list[str] = field(default_factory=lambda: [])
    persistent_keepalive: int = field(default=25)


@dataclass
class Tunnel:
    name: str = field(default="Tunnel")
    interface: Interface = Interface()
    peer: Peer = Peer()


@dataclass
class WGStat:
    latest_handshake: int = field(default=0)
    tx_bytes: int = field(default=0)
    rx_bytes: int = field(default=0)
    estimated_loss: float = field(default=0)
    estimated_rtt: int = field(default=0)
