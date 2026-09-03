from datetime import datetime, timezone
from app.database import SessionLocal
from app.models.user import User
from sqlalchemy.exc import SqlAlchemyError

import sys
from pathlib import Path

root_dir = Path("app/scripts/purge_users.py").resolve().parents[2]
sys.path.append(str(root_dir))


def purge_users():
    with SessionLocal as db:
        now=datetime.now(timezone.utc)
        
        try:
            expired_users=db.query(User).filter(
                User.is_deleted==True,
                User.schedule_delete_at<=now
            ).all()
            
            if not expired_users:
                return
            
            for user in expired_users:
                db.delete(user)
                
            db.commit()
        
        except SqlAlchemyError as e:
            db.rollback()
            print(f"Error purging users {e}")