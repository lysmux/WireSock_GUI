import configparser
from os import getenv
from pathlib import Path

from models import Tunnel, Interface, Peer


def get_configs_dir() -> Path:
    appdata_path = getenv("LOCALAPPDATA")
    path = Path(appdata_path, "WireSock", "configs")
    path.mkdir(parents=True, exist_ok=True)

    return path.expanduser()


def load_config(config_name: str) -> Tunnel | None:
    configs_dir = get_configs_dir()
    config_path = configs_dir / f"{config_name}.conf"

    if not config_path.exists():
        return None

    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(config_path)

    if not config.has_section("Interface") or not config.has_section("Peer"):
        raise

    interface_config = {}
    peer_config = {}

    for key, value in config.items("Interface"):
        match key:
            case "PrivateKey":
                interface_config["private_key"] = value
            case "Address":
                interface_config["address"] = value
            case "DNS":
                interface_config["dns"] = list(map(lambda x: x.strip(), value.split(",")))
            case "MTU":
                interface_config["mtu"] = int(value)

    for key, value in config.items("Peer"):
        match key:
            case "PublicKey":
                peer_config["public_key"] = value
            case "PresharedKey":
                peer_config["pre_shared_key"] = value
            case "Endpoint":
                peer_config["endpoint"] = value
            case "AllowedIPs":
                peer_config["allowed_ips"] = list(map(lambda x: x.strip(), value.split(",")))
            case "AisallowedIPs":
                peer_config["disallowed_ips"] = list(map(lambda x: x.strip(), value.split(",")))
            case "AllowedApps":
                peer_config["allowed_apps"] = list(map(lambda x: x.strip(), value.split(",")))
            case "DisallowedApps":
                peer_config["disallowed_apps"] = list(map(lambda x: x.strip(), value.split(",")))
            case "PersistentKeepalive":
                peer_config["persistent_keepalive"] = int(value)

    return Tunnel(name=config_name,
                  interface=Interface(**interface_config),
                  peer=Peer(**peer_config)
                  )


def save_config(tunnel: Tunnel):
    configs_dir = get_configs_dir()
    config = configparser.ConfigParser()
    config.optionxform = str

    config.add_section("Interface")
    if tunnel.interface.private_key:
        config.set("Interface", "PrivateKey", tunnel.interface.private_key)
    if tunnel.interface.address:
        config.set("Interface", "Address", tunnel.interface.address)
    if tunnel.interface.dns:
        config.set("Interface", "DNS", ",".join(tunnel.interface.dns))
    if tunnel.interface.mtu:
        config.set("Interface", "MTU", str(tunnel.interface.mtu))

    config.add_section("Peer")
    if tunnel.peer.public_key:
        config.set("Peer", "PublicKey", tunnel.peer.public_key)
    if tunnel.peer.endpoint:
        config.set("Peer", "Endpoint", tunnel.peer.endpoint)
    if tunnel.peer.pre_shared_key:
        config.set("Peer", "PresharedKey ", tunnel.peer.pre_shared_key)
    if tunnel.peer.allowed_ips:
        config.set("Peer", "AllowedIPs", ",".join(tunnel.peer.allowed_ips))
    if tunnel.peer.disallowed_ips:
        config.set("Peer", "DisallowedIPs", ",".join(tunnel.peer.disallowed_ips))
    if tunnel.peer.allowed_apps:
        config.set("Peer", "AllowedApps", ",".join(tunnel.peer.allowed_apps))
    if tunnel.peer.disallowed_apps:
        config.set("Peer", "DisallowedApps", ",".join(tunnel.peer.disallowed_apps))
    if tunnel.peer.persistent_keepalive:
        config.set("Peer", "PersistentKeepalive", str(tunnel.peer.persistent_keepalive))

    with open(configs_dir / f"{tunnel.name}.conf", "w") as config_file:
        config.write(config_file)
