from typing import Optional
from models.user import User
from sqlalchemy.orm import Session

        

def get_user(db: Session, telegram_id: str) -> Optional[User]:
    """Gets a user with the given telegram_id from the database.
    
    Args:
        db: Database session
        telegram_id: Telegram ID of the user to check
        
    Returns:
        User object if found, None otherwise
    """
    try:
        
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        return user
    except Exception as e:
        print(f"Error retrieving user from database: {str(e)}")
        return None