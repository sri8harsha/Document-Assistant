from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from pypdf import PdfReader
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def process_pdf(file_path: str) -> List[Document]:
    """Process PDF file and return list of Document objects."""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        if not text.strip():
            raise ValueError("No text could be extracted from the PDF")
        
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        
        # Create Document objects
        documents = [Document(page_content=chunk) for chunk in chunks]
        return documents
    except Exception as e:
        print(f"Error in process_pdf: {str(e)}")
        raise

def summarize_document(documents: List[Document]) -> str:
    """Generate a summary of the document using LLM."""
    try:
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
        chain = load_summarize_chain(llm, chain_type="map_reduce")
        summary = chain.run(documents)
        return summary
    except Exception as e:
        print(f"Error in summarize_document: {str(e)}")
        raise

def chat_with_document(query: str, documents: List[Document]) -> str:
    """Process a query about the document using LLM."""
    try:
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
        
        # Create context from documents
        context = "\n".join([doc.page_content for doc in documents])
        
        # Create prompt
        prompt = f"""Based on the following document content, please answer the question.
        
Document content:
{context}

Question: {query}

Answer:"""
        
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"Error in chat_with_document: {str(e)}")
        raise 