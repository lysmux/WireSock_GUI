from config_manager import get_configs_dir
from models import WGStat, Tunnel
from wiresock_manager.wg_booster import WGBooster


class WSManager:
    instance = None
    current_tunnel = None
    wg_booster = WGBooster()

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(WSManager, cls).__new__(cls)
        return cls.instance

    def connect_tunnel(self, tunnel: Tunnel) -> bool:
        configs_dir = get_configs_dir()
        config_path = configs_dir / f"{tunnel.name}.conf"

        if not self.wg_booster.create_tunnel(config_path.as_posix()):
            return False

        if not self.wg_booster.start_tunnel():
            self.wg_booster.drop_tunnel()
            return False

        self.current_tunnel = tunnel
        return True

    def disconnect_tunnel(self):
        self.wg_booster.stop_tunnel()
        self.wg_booster.drop_tunnel()
        self.current_tunnel = None

    def set_log_level(self):
        pass

    def is_active(self) -> bool:
        return self.wg_booster.active

    def get_stat(self) -> WGStat:
        stat = self.wg_booster.stat
        return WGStat(time_since_last_handshake=stat.time_since_last_handshake,
                      tx_bytes=stat.tx_bytes,
                      rx_bytes=stat.rx_bytes,
                      estimated_loss=stat.estimated_loss,
                      estimated_rtt=stat.estimated_rtt,
                      )
