
from agentservices.agentservices import AgentServices
import tempfile
from langchain_community.document_loaders import PyPDFLoader
import os
class ChatbotServices:
    def __init__(self):
        self.agentServices=AgentServices(
            llm_model=os.getenv("LLM_MODEL"),
            llm_api_key=os.getenv("GOOGLE_API_KEY"),
            embedding_model=os.getenv("LLM_EMbEDDING_MODEL"),
            pinecone_api_key=os.getenv("PINECONE_API_KEY"),
            pinecone_index_name=os.getenv("PINECONE_INDEX_NAME"),
            chunk_size=int(os.getenv("CHUNK_SIZE", 1000)),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP", 200))
        )

    def process_chat_request(self, request):
        # Placeholder for processing chat requests
        return {"response": "This is a response from the chatbot."}
    
    def handle_pdf_upload(self, pdf_blob):
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_pdf:

            temp_pdf.write(pdf_blob)
            temp_path = temp_pdf.name

        loader = PyPDFLoader(temp_path)
        pdf_data=loader.load()
        
        data=self.agentServices.process_pdf(pdf_data)
        print(f"Data processed: {data}")

        
        
        return {"message": "PDF uploaded and processed successfully"}

    def ask_question(self, question):
        response = self.agentServices.prepare_context_and_ask_query(question)
        if not response:
            return {"answer": "No answer found for the question."}
        return {"answer": response}