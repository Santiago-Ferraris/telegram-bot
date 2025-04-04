from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey, String
from pydantic import BaseModel, Field
from enum import Enum
from database.db_config import Base
from models.user import User

class ExpenseCategory(str, Enum):
    HOUSING = "Housing"
    TRANSPORTATION = "Transportation"
    FOOD = "Food"
    UTILITIES = "Utilities"
    INSURANCE = "Insurance"
    MEDICAL = "Medical/Healthcare"
    SAVINGS = "Savings"
    DEBT = "Debt"
    EDUCATION = "Education"
    ENTERTAINMENT = "Entertainment"
    OTHER = "Other"


# SQLAlchemy Model (DB Representation)
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(Text, nullable=False)
    amount = Column(String, nullable=False)
    category = Column(Text, nullable=False)
    added_at = Column(TIMESTAMP, nullable=False)


# Pydantic Schema (API Representation)
class ExpenseSchema(BaseModel):
    user_id: int = Field(description="User ID that the expense belongs to")
    description: str = Field(description="Description of the expense")
    amount: str = Field(description="Amount of the expense with a prepended $")
    category: ExpenseCategory = Field(description="Category of the expense")
    added_at: str = Field(description="Timestamp when the expense was added")

    class Config:
        model_config = {
            'from_attributes': True
        }
