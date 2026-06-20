from pydantic import BaseModel


class PDFRequest(BaseModel):
    pdf_blob: bytes