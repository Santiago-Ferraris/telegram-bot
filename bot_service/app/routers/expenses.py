from typing import List
from models.expense import Expense
from database.db_config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
import uuid
from sqlalchemy.orm import Session
from datetime import datetime
from app.services import expenses_service, llm_service, users_service
from models.expense_related import IsExpenseRelatedSchema, ExpenseRelatedCategory

prefix = "expenses"
router = APIRouter(
    prefix=f"/{prefix}",
    tags=["Expenses"]
    )


@router.post("")
async def post_expense_from_message(message: dict, db: Session= Depends(get_db)):
    """Processes a message with AI and inserts it into the DB if it's an expense."""
    text_message = message.get("text", "").strip()
    user_telegram_id = message.get("user_id")
    thread_id = uuid.uuid4()

    if not text_message or not user_telegram_id:
        raise HTTPException(status_code=400, detail="Message text and user_id are required")
    # Check if user exists in the database

    user = users_service.get_user(db, str(user_telegram_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. User is not on the whitelist."
        )

    # Step 1: Determine if message is expense-related
    expense_related: IsExpenseRelatedSchema = llm_service.is_expense_related(text_message, langsmith_extra={"metadata": {"thread_id": thread_id}})
    if not expense_related.is_expense_related:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message is not expense-related."
        )
    
    if expense_related.expense_category == ExpenseRelatedCategory.ADD_EXPENSE:
        # Step 2: Extract structured expense data
        expense_data = llm_service.extract_expense_details(text_message, user.id, datetime.now().isoformat(), langsmith_extra={"metadata": {"thread_id": thread_id}})

        # Step 3: Insert into database
        expenses_service.insert_expense_to_db(expense_data, db)

        return {"message": f"{expense_data.category.value} expense added ✅"}
    elif expense_related.expense_category == ExpenseRelatedCategory.GET_EXPENSES:
        expenses: List[Expense] = expenses_service.get_expenses(db, user_id=user.id)

        json_expenses = [expense._asdict() for expense in expenses]

        expense_analysis = llm_service.analyze_expenses(text_message, datetime.now().isoformat(), json_expenses ,langsmith_extra={"metadata": {"thread_id": thread_id}})

        return {"message": expense_analysis}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not implemented."
        )
