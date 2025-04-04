import os
from openai import OpenAI
from langsmith import traceable
from models.expense_related import IsExpenseRelatedSchema, ExpenseAnalysisSchema
from models.expense import ExpenseSchema
from datetime import datetime

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

@traceable(run_type="llm")
def is_expense_related(text_message: str) -> IsExpenseRelatedSchema:
    """Determines if a message is related to an expense using OpenAI."""
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {   
                "role": "system",
                "content": (
                    "You are a text message evaluator"
                    "Determine if the content of the message is expense related, and its category "
                    "For a message to be expense related, it needs to make reference to an expense"
                    "The output should be a boolean indicating true if the message is expense related, and false if not, and a category"
                    "If it is NOT expense related, the category should be None, if it IS expense related, you should identify the correct category"
                ),
            },
            {"role": "user", "content": f"Message: {text_message}"}
        ],
        response_format=IsExpenseRelatedSchema,
    )

    is_expense_related = response.choices[0].message.parsed
    print(f"Is Expense related? {is_expense_related}")
    return is_expense_related


@traceable(run_type="llm")
def extract_expense_details(text_message: str, user_id: str, timestamp: datetime) -> dict:
    """Extracts the request from the user's message from a list of expenses"""
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {   
                "role": "system",
                "content": (
                    "You are an expense list analyzer"
                    "Parse the message and extract the following properties:"
                    "- Amount"
                    "- Category"
                    "- Description"
                ),
            },
            {"role": "user", "content": f"Message: {text_message}, User ID: {user_id}, Timestamp: {timestamp}"}
        ],
        response_format=ExpenseSchema,
    )

    expense = response.choices[0].message.parsed
    print(f"Expense: {expense}")

    return expense

@traceable(run_type="llm")
def analyze_expenses(text_message: str, user_id: str, timestamp: datetime, expense_list: list) -> dict:
    """Extracts expense details from a message using OpenAI."""
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {   
                "role": "system",
                "content": (
                    "You are an expense list analyzer"
                    "You will receive a Message, a User ID, a current Timesamp, and an Expense List."
                    "Determine the objective stated in the content of the message"
                    "To create the answer, analyze the provided list of expenses"
                    "Your answer should be an analysis that replies to the objective stated in the message"
                    "Your answer SHOULD BE DIRECTED to the user"
                )
            },
            {"role": "user", "content": f"Message: {text_message}, User ID: {user_id}, Timestamp: {timestamp}, Expense List: {expense_list}"}
        ],
        response_format=ExpenseAnalysisSchema
    )

    analysis = response.choices[0].message.parsed
    print(f"Analysis: {analysis.text}")

    return analysis.text
