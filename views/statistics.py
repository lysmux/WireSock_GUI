import threading
import time

import flet
import humanize

import resources
from wiresock_manager.wiresock_manager import WSManager


class StatisticsView(flet.UserControl):
    def __init__(self):
        super().__init__()
        self.latest_handshake = flet.Ref[flet.Text]()
        self.rx_bytes = flet.Ref[flet.Text]()
        self.tx_bytes = flet.Ref[flet.Text]()
        self.estimated_loss = flet.Ref[flet.Text]()
        self.estimated_rtt = flet.Ref[flet.Text]()

        self.allow_update = False

        update_thread = threading.Thread(target=self.update_statistics)
        update_thread.daemon = True
        update_thread.start()

    def build(self):
        return flet.Column([
            flet.Row([
                flet.Text(resources.LATEST_HANDSHAKE),
                flet.Text(ref=self.latest_handshake)
            ]),
            flet.Row([
                flet.Text(resources.RX_BYTES),
                flet.Text(ref=self.rx_bytes)
            ]),
            flet.Row([
                flet.Text(resources.TX_BYTES),
                flet.Text(ref=self.tx_bytes)
            ]),
            flet.Row([
                flet.Text(resources.ESTIMATED_RTT),
                flet.Text(ref=self.estimated_rtt)
            ]),
            flet.Row([
                flet.Text(resources.ESTIMATED_LOSS),
                flet.Text(ref=self.estimated_loss)
            ]),
        ])

    def did_mount(self):
        self.allow_update = True

    def will_unmount(self):
        self.allow_update = False

    def update_statistics(self):
        while True:
            if self.allow_update:
                statistics = WSManager().get_stat()

                self.latest_handshake.current.value = humanize.naturaltime(statistics.latest_handshake)
                self.latest_handshake.current.update()

                self.rx_bytes.current.value = humanize.naturalsize(statistics.rx_bytes)
                self.rx_bytes.current.update()

                self.tx_bytes.current.value = humanize.naturalsize(statistics.tx_bytes)
                self.tx_bytes.current.update()

                self.estimated_rtt.current.value = f"{statistics.estimated_rtt} {resources.MILLI_SECONDS}"
                self.estimated_rtt.current.update()

                self.estimated_loss.current.value = f"{statistics.estimated_loss}%"
                self.estimated_loss.current.update()

            time.sleep(1)
