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
                    "Determine if the content of the message IS expense related, and its category, or if it IS NOT"
                    "For a message to be expense related, EITHER OF TWO THINGS need to happen"
                    "1. The message has both a price and a description (Assume prices are always dollars.). In this case, it is ADD category"
                    "2. The message is asking some type of a conclusion taking into account their previous spendings. In this case, it is GET category"
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
def analyze_expenses(text_message: str, timestamp: datetime, expense_list: list) -> dict:
    """Extracts expense details from a message using OpenAI."""
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {   
                "role": "system",
                "content": (
                    "You are an expense list analyzer"
                    "You will receive a Message, a current Timesamp, and an Expense List."
                    "Determine the objective stated in the content of the message"
                    "To create the answer, analyze the provided list of expenses"
                    "Your answer should be an analysis that replies to the objective stated in the message"
                    "Your answer SHOULD BE DIRECTED to the user"
                    "Your answer SHOULD be text. Text-altering symbols like ** or # do NOT work."
                )
            },
            {"role": "user", "content": f"Message: {text_message}, Timestamp: {timestamp}, Expense List: {expense_list}"}
        ],
        response_format=ExpenseAnalysisSchema
    )

    analysis = response.choices[0].message.parsed
    print(f"Analysis: {analysis.text}")

    return analysis.text
