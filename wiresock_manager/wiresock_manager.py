import logging

import resources
from config_manager import get_configs_dir
from models import WGStat, Tunnel
from wiresock_manager.wg_booster import WGBooster, LogLevel

logger = logging.getLogger("wire_sock")
logger.setLevel(logging.INFO)


class WSManager:
    instance = None
    current_tunnel = None

    wg_booster = WGBooster()
    _handle = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(WSManager, cls).__new__(cls)
        return cls.instance

    def connect_tunnel(self, tunnel: Tunnel, log_level=resources.LEVEL_ALL) -> bool:
        configs_dir = get_configs_dir()
        config_path = configs_dir / f"{tunnel.name}.conf"

        if self._handle is None:
            self._handle = self.wg_booster.get_handle(
                log_func=lambda msg: logger.info(msg.decode("utf8")),
                log_level=log_level
            )

        if self._handle is None:
            return False

        if not self.wg_booster.create_tunnel(self._handle, config_path.as_posix()):
            self._handle = None
            return False

        if not self.wg_booster.start_tunnel(self._handle):
            self.wg_booster.drop_tunnel(self._handle)
            self._handle = None
            return False

        self.current_tunnel = tunnel
        return True

    def disconnect_tunnel(self):
        if self._handle is not None:
            self.wg_booster.stop_tunnel(self._handle)
            self.wg_booster.drop_tunnel(self._handle)
            self.current_tunnel = None

    def set_log_level(self, log_level: str):
        if self._handle is not None:
            match log_level:
                case resources.LEVEL_INFO:
                    level = LogLevel.info
                case resources.LEVEL_ALL:
                    level = LogLevel.all
                case _:
                    level = LogLevel.error

            self.wg_booster.set_log_level(self._handle, level)

    def set_va_mode(self, va_mode: bool):
        if self._handle is not None:
            raise RuntimeError("Disconnect from tunnel before change va_mode")
        self.wg_booster.va_mode = va_mode

    def is_active(self) -> bool:
        if self._handle is not None:
            return self.wg_booster.is_active(self._handle)
        return False

    def get_stat(self) -> WGStat:
        if self._handle is not None:
            stat = self.wg_booster.get_stat(self._handle)
            return WGStat(latest_handshake=stat.latest_handshake,
                          tx_bytes=stat.tx_bytes,
                          rx_bytes=stat.rx_bytes,
                          estimated_loss=stat.estimated_loss,
                          estimated_rtt=stat.estimated_rtt,
                          )
        return WGStat()
