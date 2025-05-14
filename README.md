# LLM-Powered Internal Assistant

A Gradio-based interface for internal teams to summarize documents and interact with LLM workflows. This project provides an intuitive interface for document processing and AI-powered interactions.

## Features

- Document summarization using LLMs
- Interactive chat interface
- PDF document processing
- Clean and intuitive UI
- Fast I/O integration with LangChain

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
4. Run the application:
   ```bash
   python app.py
   ```

## Usage

1. Launch the application
2. Upload a PDF document for summarization
3. Use the chat interface to interact with the document
4. Get AI-powered insights and summaries

## Project Structure

- `app.py`: Main application file with Gradio interface
- `utils.py`: Utility functions for document processing
- `requirements.txt`: Project dependencies
- `.env`: Environment variables (create this file with your API key) 