# Bot Service

This service processes and analyzes messages received from the connector service, using NLP capabilities to understand and respond to user inputs.

## Features

- FastAPI-based REST API service
- Natural Language Processing using OpenAI and LangChain
- PostgreSQL database integration for data persistence
- Message classification to identify expense-related content
- Expense tracking and categorization
- Expense analysis for financial insights
- User whitelist system for controlling access

## Message Processing

The service uses an LLM model to:
1. Identify if a message is expense-related
2. Categorize expense messages into two types:
   - **ADD category**: For tracking new expenses (contains price and description)
   - **GET category**: For analyzing previous expenses and providing insights

If a message is not expense-related or from a non-whitelisted user, the service does not process it further.

## Prerequisites

- Python 3.11 or higher
- PostgreSQL database
- OpenAI API key

## Installation

1. Clone the repository and navigate to the bot_service directory:

```bash
cd bot_service
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables by creating a `.env` file with the following variables:

```
DATABASE_URL=your_postgresql_connection_string
OPENAI_API_KEY=your_openai_api_key
LANGCHAIN_TRACING_V2=true  # Optional, for LangChain tracing
LANGCHAIN_API_KEY=your_langchain_api_key  # Optional
LANGCHAIN_PROJECT=your_langchain_project  # Optional
```

Alternatively, copy the provided example environment file and modify it with your values:

```bash
cp .example.env .env
# Then edit .env with your actual credentials
```

## Running the Service

To start the service:

```bash
uvicorn main:app --reload
```

The service will be available at `http://localhost:8000`.

## API Endpoints

- **POST /expenses**: Process expense-related messages
  - Request body: `{ "text": "message text", "user_id": "user identifier" }`
  - Response: Processed message with analysis results
  - Note: Only whitelisted users' requests will be processed

## Development

- `app/routers/`: API route definitions
- `app/services/`: Business logic and services
- `models/`: Data models
- `database/`: Database connection and operations