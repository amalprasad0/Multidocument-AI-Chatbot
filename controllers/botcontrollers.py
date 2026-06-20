from fastapi import APIRouter, UploadFile, File

import runpy
from services.chatbotservices import ChatbotServices

def create_bot_router():
    botrouter = APIRouter()
    chatbot_services = ChatbotServices()

    # @botrouter.post("/chat")
    # async def chat_endpoint(request: dict):
    #     response = chatbot_services.process_chat_request(request)
    #     return response

    @botrouter.post("/upload-pdf")
    async def upload_pdf_endpoint(pdf_file: UploadFile = File(...)):
        pdf_bytes = await pdf_file.read()
        response = chatbot_services.handle_pdf_upload(pdf_bytes)
        return response

    @botrouter.post("/ask-question")
    async def ask_question_endpoint(question: str):
        response = chatbot_services.ask_question(question)
        return response

    return botrouter