from pydantic import BaseModel, Field
from enum import Enum

class ExpenseRelatedCategory(str, Enum):
    ADD_EXPENSE = "ADD"
    GET_EXPENSES = "GET"

class IsExpenseRelatedSchema(BaseModel):
    is_expense_related: bool = Field(description="Property that determines if a message is expense related or not")
    expense_category: ExpenseRelatedCategory = Field(None, description="Property that determines the category of an expense")

class ExpenseAnalysisSchema(BaseModel):
    text: str = Field(description="Property that determines the analysis of a list of expenses based on a message that had an objective")

