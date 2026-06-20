import os
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from controllers.botcontrollers import create_bot_router
# from services.chatbotservices import ChatbotServices
load_dotenv()

app = FastAPI(title="Multi-Documents Chatbot API")
# ChatbotServices = ChatbotServices()
app.include_router(create_bot_router(), prefix="/api/v1/bot", tags=["Chatbot API"])
if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)
