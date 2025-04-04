# Connector Service

This service acts as a bridge between Telegram and the Bot Service, forwarding messages from users to the processing service and returning responses.

## Features

- Express.js-based webhook server
- Telegram Bot API integration
- Message forwarding to the Bot Service
- Response handling and delivery back to users

## Prerequisites

- Node.js 16 or higher
- Telegram Bot token (from [@BotFather](https://t.me/BotFather))

## Installation

1. Clone the repository and navigate to the connector_service directory:

```bash
cd connector_service
```

2. Install dependencies:

```bash
npm install
```

3. Set up environment variables by creating a `.env` file with the following variables:

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
BOT_SERVICE_URL=http://localhost:8000/expenses
PORT=3000  # Optional, defaults to 3000
```

Alternatively, copy the provided example environment file and modify it with your values:

```bash
cp .example.env .env
# Then edit .env with your actual credentials
```

## Running the Service

To run the service in development mode:

```bash
npm run dev
```

To build and run in production mode:

```bash
npm run build
npm start
```

The service will be available at `http://localhost:3000`.

## Setting Up a Telegram Bot

1. Create a new bot through [@BotFather](https://t.me/BotFather) on Telegram and get the API token (Remember to place it in .env file)
2. Set the webhook URL for your bot (requires a public URL):

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=<YOUR_PUBLIC_URL>/webhook"

```

For local development, you can use a service like [ngrok](https://ngrok.com/) to expose your local server:

```bash
ngrok http 3000
```

Then set the webhook using the ngrok URL:

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=<YOUR_NGROK_URL>/webhook"
```

## API Endpoints

- **POST /webhook**: Receives webhook events from Telegram

## Development

- `src/index.ts`: Main application file with webhook handler and service logic 