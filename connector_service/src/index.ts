import express, { RequestHandler } from "express";
import axios from "axios";
import dotenv from "dotenv";

dotenv.config();

const app = express();
app.use(express.json());

const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const TELEGRAM_API_URL = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}`;
const BOT_SERVICE_URL = process.env.BOT_SERVICE_URL;

interface TelegramMessage {
  message?: {
    chat: { id: number };
    text: string;
  };
}

// Webhook endpoint to receive Telegram messages
const webhookHandler: RequestHandler = async (req, res) => {
  const body: TelegramMessage = req.body;

  console.log(body);

  if (!body.message || !body.message.text) {
    res.sendStatus(400);
    return;
  }

  const chatId = body.message.chat.id;
  const text = body.message.text;

  console.log(`Received message: ${text}`);

  try {
    // Send message to bot service
    const botServiceResponse = await axios.post(BOT_SERVICE_URL!, {
      text: text,
      user_id: chatId
    });
    
    // Log the response from bot service
    console.log("Bot service response:", botServiceResponse.data);
    
    // Send response back to the user with the status from bot service
    await axios.post(`${TELEGRAM_API_URL}/sendMessage`, {
      chat_id: chatId,
      text: botServiceResponse.data.status
    });
  } catch (error: any) {
    console.error("Error:", error.response?.data || error.message);
    
    // If the error is a 403 (unauthorized), ignore the message
    if (error.response?.status === 403) {
      console.log(`Unauthorized user (${chatId}) attempted to use the service`);
      // Don't send any response back to the user
    }
  }

  res.sendStatus(200);
};

app.post("/webhook", webhookHandler);

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Connector service running on port ${PORT}`));
