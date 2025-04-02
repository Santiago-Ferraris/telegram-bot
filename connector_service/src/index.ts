import express, { RequestHandler } from "express";
import axios from "axios";
import dotenv from "dotenv";

dotenv.config();

const app = express();
app.use(express.json());

const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const TELEGRAM_API_URL = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}`;

interface TelegramMessage {
  message?: {
    chat: { id: number };
    text: string;
  };
}

// Webhook endpoint to receive Telegram messages
const webhookHandler: RequestHandler = async (req, res) => {
  const body: TelegramMessage = req.body;

  if (!body.message || !body.message.text) {
    res.sendStatus(400);
    return;
  }

  const chatId = body.message.chat.id;
  const text = body.message.text;

  console.log(`Received message: ${text}`);

  // Send the same message back to the user
  try {
    await axios.post(`${TELEGRAM_API_URL}/sendMessage`, {
      chat_id: chatId,
      text: `You said: ${text}`,
    });
  } catch (error: any) {
    console.error("Error sending message:", error.response?.data || error.message);
  }

  res.sendStatus(200);
};

app.post("/webhook", webhookHandler);

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Connector service running on port ${PORT}`));
