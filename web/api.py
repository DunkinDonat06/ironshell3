from fastapi import APIRouter, Depends
from .db import SessionLocal
from .models import ScanHistory
from .auth import get_current_user, admin_required

router = APIRouter()

@router.get("/history/")
def get_history(user=Depends(get_current_user)):
    db = SessionLocal()
    # Можно фильтровать по user['username'] для приватности
    return db.query(ScanHistory).order_by(ScanHistory.timestamp.desc()).limit(100).all()

@router.post("/rescan/{scan_id}")
def rescan(scan_id: int, user=Depends(get_current_user)):
    # Берём параметры из истории, создаём новую задачу
    return {"status": "rescan started"}

@router.delete("/history/{scan_id}")
def delete_scan(scan_id: int, user=Depends(admin_required)):
    db = SessionLocal()
    db.query(ScanHistory).filter(ScanHistory.id == scan_id).delete()
    db.commit()
    return {"status": "deleted"}