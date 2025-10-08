import argparse
import json
import os
import requests
from rich import print
from .config import API_BASE, TOKEN_FILE
from .torrent_client import TorrentClient
from .player import open_file

session = requests.Session()

def save_token(tok: str):
    with open(TOKEN_FILE, 'w') as f:
        f.write(tok)

def load_token():
    if not os.path.exists(TOKEN_FILE):
        return None
    return open(TOKEN_FILE).read().strip()

def auth_header():
    t = load_token()
    return {"Authorization": f"Bearer {t}"}

# Commands

def cmd_login(args):
    r = session.post(f"{API_BASE}/auth/login", json={"username": args.username, "password": args.password})
    r.raise_for_status()
    tok = r.json()["access_token"]
    save_token(tok)
    print("[green]Login ok[/green]")


def cmd_list(args):
    r = session.get(f"{API_BASE}/files/", headers=auth_header())
    r.raise_for_status()
    for f in r.json():
        print(f"#{f['id']:>3} | {f['title']:<40} | access>={f['min_role_weight']} | {f['size_bytes']/1e6:.2f} MB")


def cmd_search(args):
    r = session.post(f"{API_BASE}/search/", headers=auth_header(), json={"q": args.q})
    r.raise_for_status()
    for f in r.json():
        print(f"#{f['id']:>3} | {f['title']}")


def cmd_download(args):
    tc = TorrentClient()
    h, ih = tc.add_torrent(args.torrent, args.dest)
    print("Baixando...", ih)
    last_down = 0
    while not h.is_seed():
        s = h.status()
        cur_down = s.total_download
        delta = max(0, cur_down - last_down)
        last_down = cur_down
        # report chunk to server (best-effort)
        try:
            session.post(f"{API_BASE}/stats/download", headers=auth_header(), params={"bytes": delta})
        except Exception:
            pass
        print(f"progress={s.progress*100:.1f}% down={s.total_download/1e6:.2f}MB up={s.total_upload/1e6:.2f}MB")
    print("[green]Download completo[/green]")
    # tenta abrir arquivo principal (heurística)
    files = h.get_torrent_info().files()
    if files.num_files() == 1:
        path = os.path.join(args.dest, files.file_path(0))
        open_file(path)


def cmd_seed(args):
    tc = TorrentClient()
    ih = tc.make_torrent(args.path, args.tracker, args.out)
    print(".torrent criado com infohash:", ih)


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("login"); s.add_argument("--username"); s.add_argument("--password"); s.set_defaults(func=cmd_login)
    s = sub.add_parser("list"); s.set_defaults(func=cmd_list)
    s = sub.add_parser("search"); s.add_argument("--q", required=True); s.set_defaults(func=cmd_search)
    s = sub.add_parser("download"); s.add_argument("--torrent", required=True); s.add_argument("--dest", default="./downloads"); s.set_defaults(func=cmd_download)
    s = sub.add_parser("seed"); s.add_argument("--path", required=True); s.add_argument("--tracker", default="http://localhost:8000/tracker/announce"); s.add_argument("--out", default="./out.torrent"); s.set_defaults(func=cmd_seed)

    args = p.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()