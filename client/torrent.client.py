import time
import os
import libtorrent as lt

class TorrentClient:
    def __init__(self, listen_port=6881):
        self.ses = lt.session()
        self.ses.listen_on(listen_port, listen_port+10)

    def add_torrent(self, torrent_path: str, save_path: str):
        info = lt.torrent_info(torrent_path)
        params = {
            'ti': info,
            'save_path': save_path,
            'storage_mode': lt.storage_mode_t(2),
        }
        h = self.ses.add_torrent(params)
        return h, info.info_hash().to_string()

    def make_torrent(self, file_path: str, tracker_url: str, out_path: str):
        fs = lt.file_storage()
        lt.add_files(fs, file_path)
        t = lt.create_torrent(fs)
        t.add_tracker(tracker_url)
        t.set_creator("p2p-python")
        lt.set_piece_hashes(t, os.path.dirname(file_path))
        torrent = lt.bencode(t.generate())
        with open(out_path, 'wb') as f:
            f.write(torrent)
        info = lt.torrent_info(out_path)
        return info.info_hash().to_string()

    def seed(self, torrent_path: str, save_path: str):
        h, ih = self.add_torrent(torrent_path, save_path)
        print("Seeding...", ih)
        while True:
            s = h.status()
            print(f"state={s.state}, up={s.total_upload}, down={s.total_download}")
            time.sleep(2)