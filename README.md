# Telegram Expense Tracker Bot

A microservices-based Telegram bot system that helps users track their expenses using natural language processing. The system consists of two main services:

1. **Connector Service**: A TypeScript/Node.js service that handles Telegram API integration.
2. **Bot Service**: A Python/FastAPI service that processes messages using NLP and manages expense data.

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│  Telegram API   │◄──►│ Connector       │◄──►│  Bot Service    │
│                 │    │ Service (Node)  │    │  (Python)       │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
                                             ┌─────────────────┐
                                             │                 │
                                             │  Database       │
                                             │  (PostgreSQL)   │
                                             │                 │
                                             └─────────────────┘
```

## Features

- Natural language expense tracking via Telegram
- Multi-service architecture for easier maintenance and scaling
- Database persistence of expense data
- AI-powered expense categorization and analysis

## Prompt Ideas

Here are some example prompts you can try with the bot:

### Adding Expenses

- "Spent $25 on lunch today"
- "Bought groceries for $75.50 at Whole Foods"
- "Uber ride home cost me $18.23"
- "Paid $120 for electricity bill"
- "Movie tickets for $32 yesterday"
- "Coffee shop meeting $7.45"

### Analyzing Expenses

- "What did I spend on food this month?"
- "Show me my expenses for the last week"
- "How much have I spent on transportation?"
- "What category am I spending the most on?"
- "What was my biggest expense in April?"
- "Give me a summary of my monthly spending"
- "Compare my spending this month vs last month"

The bot uses AI to understand your expenses in natural language, so you don't need to use specific formats or commands. Just write how you would normally describe your expenses!

> **Disclaimer**: While the bot uses advanced AI to analyze your expenses, the information and insights provided may not be 100% accurate. Always verify important financial calculations and decisions with professional financial tools or advisors. The bot is designed as a helpful assistant, not a replacement for professional financial management.

## Getting Started

### Prerequisites

- Node.js 16 or higher
- Python 3.11 or higher
- PostgreSQL database
- Telegram Bot token (from [@BotFather](https://t.me/BotFather))
- OpenAI API key

### Setting Up the Project

1. Clone the repository:

```bash
git clone https://github.com/yourusername/telegram-expense-tracker.git
cd telegram-expense-tracker
```

2. Set up the Bot Service:

Follow the instructions in the [Bot Service README](./bot_service/README.md).

3. Set up the Connector Service:

Follow the instructions in the [Connector Service README](./connector_service/README.md).

### Running the System

1. Start the Bot Service:

```bash
cd bot_service
source venv/bin/activate
uvicorn main:app --reload
```

2. In a separate terminal, start the Connector Service:

```bash
cd connector_service
npm run dev
```

3. Set up your Telegram Bot webhook (see Connector Service README for details).

4. Start chatting with your bot on Telegram!

## Development

Each service has its own development workflow and dependencies. Please refer to the service-specific READMEs for detailed development guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 