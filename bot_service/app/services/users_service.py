from models.user import User
from sqlalchemy.orm import Session

        

def check_user(db: Session, telegram_id: str) -> bool:
    """Checks if a user with the given telegram_id exists in the database.
    
    Args:
        db: Database session
        telegram_id: Telegram ID of the user to check
        
    Returns:
        True if the user exists, False otherwise
    """
    try:
        
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        return user is not None
    except Exception as e:
        print(f"Error checking user in database: {str(e)}")
        return False