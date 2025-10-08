from fastapi import APIRouter

router = APIRouter(prefix="/tracker", tags=["tracker"])

@router.get("")   # /tracker
def tracker_root():
    return {"tracker": "ok"}

@router.get("/announce")  # /tracker/announce
def announce(info_hash: str | None = None, event: str | None = None):
    return {"announce": "received", "info_hash": info_hash, "event": event}