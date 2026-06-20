from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
import hashlib
from langchain_pinecone import Pinecone
import site
import os
class AgentServices:
    def __init__(self,llm_model,llm_api_key,embedding_model,pinecone_api_key,pinecone_index_name,chunk_size=100,chunk_overlap=1000):
        self.llm_model = llm_model
        self.llm_api_key = llm_api_key
        self.embedding_model = embedding_model
        self.pinecone_api_key = pinecone_api_key
        self.pinecone_index_name = pinecone_index_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embbeder=GoogleGenerativeAIEmbeddings(model=self.embedding_model, api_key=self.llm_api_key)
        self.get_vector_store()

    def process_pdf(self, pdf_blob: bytes):
        try: 
            chunks=self.create_chunks(pdf_blob)
            print(f"Chunks created: {len(chunks)}")
            result = self.store_as_vector(chunks)
            return result
        except Exception as e:
            print(f"Error occurred while processing PDF: {e}")
            return {"message": "Error occurred while processing PDF"}
        # Placeholder for PDF processing logic
        return {"message": "PDF processed successfully"}
    def create_chunks(self, pdf_data):
        doc_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        chunks = doc_splitter.split_documents(pdf_data)
        return chunks
    def store_as_vector(self, chunks):
        try:
            ids = [
                hashlib.md5(f"{doc.metadata.get('source')}_{doc.page_content}".encode()).hexdigest()
                for doc in chunks
            ]

            vector = Pinecone.from_documents(
                documents=chunks,
                embedding=self.embbeder,
                index_name=self.pinecone_index_name,
                # api_key=self.pinecone_api_key,
                namespace="pdf_chunks",
                ids=ids
            )

            if vector:
                return {"message": "Embeddings created and stored successfully"}
        except Exception as e:
            print(f"Error occurred while storing embeddings: {e}")
            
        
        return {"message": "Embeddings not created successfully"}
    def get_vector_store(self):
        try:
            vector_store = Pinecone(
                index_name=self.pinecone_index_name,
                embedding=self.embbeder,
                namespace="pdf_chunks",
                # api_key=self.pinecone_api_key
            )
            return vector_store
        except Exception as e:
            print(f"Error occurred while retrieving vector store: {e}")
            return None
    def retrive_from_vector(self,query):
        vector_store = self.get_vector_store()
        if not vector_store:
            return {"message": "Vector store not available"}
        try:
            docs = vector_store.similarity_search(query)
            if not docs:
                return {"message": "No relevant documents found"}
            print (f"Retrieved documents: {len(docs)}")
            return docs
        except Exception as e:
            print(f"Error occurred while retrieving documents: {e}")
            return {"message": "Error occurred while retrieving documents"}
    
    def prepare_context_and_ask_query(self, query):
        docs = self.retrive_from_vector(query)
        if not docs:
            return {"message": "No relevant documents found"}
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        context_parts = []
        sources = []
        for doc in docs:
            context_parts.append(doc.page_content)
            sources.append(doc.metadata.get("source"))
            sources.append(doc.metadata.get("source"))
        context="\n".join(context_parts)
        sources="\n".join(sources)
        prompt = f"""You are an assistant that answers questions based on the following context extracted from a PDF document. Use the context to provide a concise and accurate answer to the user's question. If the context does not contain enough information, say you don't know.
            Context:
            {context}
            Sources:
            {sources}
            Question: {query}
            Answer:"""
        response = llm.invoke([prompt])  
        # formatted_response= {
        #  "answer": response.content.strip(), "sources": sources,"Input_tokens": response.usage_metadata.input_tokens,"output_token":response.usage_metadata.output_tokens
        # } 
        return {
     
        "content": response.content,
        "input_tokens": response.usage_metadata.get("input_tokens", 0),
        "output_tokens": response.usage_metadata.get("output_tokens", 0),
        "total_tokens": response.usage_metadata.get("total_tokens", 0),
    
    "sources":os.path.basename(doc.metadata.get("source", ""))

}
#         {
#     "answer": response.content.strip(),
#     "sources": sources,
#     "Input_tokens": response.usage_metadata.get("input_tokens", 0),
#     "output_token": response.usage_metadata.get("output_tokens", 0)
# }