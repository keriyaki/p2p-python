from sqlalchemy.orm import Session
from datetime import datetime
from ..models import Peer

class TrackerService:
    def __init__(self, db: Session):
        self.db = db

    def announce(self, info_hash: str, peer_id: str, ip: str, port: int):
        p = (
            self.db.query(Peer)
            .filter(Peer.info_hash == info_hash, Peer.peer_id == peer_id)
            .first()
        )
        if not p:
            p = Peer(info_hash=info_hash, peer_id=peer_id, ip=ip, port=port)
            self.db.add(p)
        else:
            p.ip = ip
            p.port = port
            p.last_seen = datetime.utcnow()
        # Return peer list for swarm
        peers = self.db.query(Peer).filter(Peer.info_hash == info_hash).all()
        return [{"ip": x.ip, "port": x.port} for x in peers]