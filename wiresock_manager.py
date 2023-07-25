import configparser
import pathlib

from models import Tunnel, Interface, Peer


def load_config(path: pathlib.Path) -> Tunnel:
    config = configparser.ConfigParser()
    config.read(path)

    if not config.has_section("Interface") or not config.has_section("Peer"):
        raise

    interface_config = {}
    peer_config = {}

    for key, value in config.items("Interface"):
        match key:
            case "privatekey":
                interface_config["private_key"] = value
            case "address":
                interface_config["address"] = list(map(lambda x: x.strip(), value.split(",")))
            case "dns":
                interface_config["dns"] = list(map(lambda x: x.strip(), value.split(",")))
            case "mtu":
                interface_config["mtu"] = int(value)

    for key, value in config.items("Peer"):
        match key:
            case "publickey":
                peer_config["public_key"] = value
            case "endpoint":
                peer_config["endpoint"] = value
            case "allowedips":
                peer_config["allowed_ips"] = list(map(lambda x: x.strip(), value.split(",")))
            case "disallowedips":
                peer_config["disallowed_ips"] = list(map(lambda x: x.strip(), value.split(",")))
            case "allowedapps":
                peer_config["allowed_apps"] = list(map(lambda x: x.strip(), value.split(",")))

    return Tunnel(name=path.stem,
                  interface=Interface(**interface_config),
                  peer=Peer(**peer_config)
                  )
