from typing import List, Optional
from models.expense import ExpenseSchema, Expense
from sqlalchemy.orm import Session
from sqlalchemy import cast, Numeric

def get_expenses(db: Session, user_id: Optional[str] = None) -> List[Expense]:
    """Retrieves a list of expenses from the database."""
    print("Retrieving expenses")
    try:
        query = db.query(Expense)
        
        if user_id:
            query = query.filter(Expense.user_id == user_id)

        expenses = query.all()
        return expenses
    except Exception as e:
        print(f"Error retrieving expenses from database: {str(e)}")
        return []

def insert_expense_to_db(expense_data: ExpenseSchema, db: Session) -> Optional[Expense]:
    """Inserts extracted expense data into the database."""
    try:
        expense_data_dict = expense_data.model_dump() 

        new_expense = Expense(**expense_data_dict)

        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)

        return new_expense
    except Exception as e:
        print(f"Error inserting expense into database: {str(e)}")
        db.rollback()
        return None


def get_expenses(db: Session, user_id: Optional[str] = None) -> List[Expense]:
    """Retrieves a list of expenses from the database.
    Returns:
        List of Expense objects
    """
    print("Retrieving expenses")
    try:
        query = db.query(Expense).with_entities(
            Expense.id,
            Expense.user_id,
            Expense.description,
            cast(Expense.amount, Numeric(10, 2)).label("amount"),  # ✅ Cast here
            Expense.category,
            Expense.added_at
        )
        
        if user_id:
            query = query.filter(Expense.user_id == user_id)
            
        return query.all()
    except Exception as e:
        print(f"Error retrieving expenses from database: {str(e)}")
        return []