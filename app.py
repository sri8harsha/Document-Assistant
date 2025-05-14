import gradio as gr
import os
from utils import process_pdf, summarize_document, chat_with_document
from typing import List
from langchain.docstore.document import Document
import tempfile
import traceback

# Global variable to store processed documents
current_documents: List[Document] = []

def process_and_summarize(file):
    """Process uploaded PDF and generate summary."""
    global current_documents
    
    if file is None:
        return "Please upload a PDF file first."
    
    try:
        # Save uploaded file to a temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file)  # file is bytes, not a file-like object
            tmp_path = tmp.name
        current_documents = process_pdf(tmp_path)
        summary = summarize_document(current_documents)
        return summary
    except Exception as e:
        with open("error_log.txt", "w") as f:
            f.write(f"Error processing file: {e}\n")
            traceback.print_exc(file=f)
        print(f"Error processing file: {e}")
        traceback.print_exc()
        return f"Error processing file: {str(e)}"

def chat_response(message, history):
    """Handle chat interactions."""
    global current_documents
    
    if not current_documents:
        return "Please upload and process a document first."
    
    try:
        response = chat_with_document(message, current_documents)
        return response
    except Exception as e:
        with open("error_log.txt", "w") as f:
            f.write(f"Error processing query: {e}\n")
            traceback.print_exc(file=f)
        print(f"Error processing query: {e}")
        traceback.print_exc()
        return f"Error processing query: {str(e)}"

# Create Gradio interface
with gr.Blocks(title="Document Assistant", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📄 Document Assistant")
    gr.Markdown("Upload a PDF document to get started with summarization and chat capabilities.")
    
    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(label="Upload PDF", file_types=[".pdf"], type="binary")
            process_btn = gr.Button("Process Document")
            summary_output = gr.Textbox(label="Document Summary", lines=10)
        
        with gr.Column(scale=1):
            chatbot = gr.ChatInterface(
                chat_response,
                title="Chat with Document",
                description="Ask questions about the uploaded document"
            )
    
    process_btn.click(
        process_and_summarize,
        inputs=[file_input],
        outputs=[summary_output]
    )

if __name__ == "__main__":
    demo.launch(share=True) 