# 🎥 Video to Documentation AI

A smart application that converts videos into structured documentation and allows you to chat with the content using AI.

## 📖 Overview

This tool takes any video (YouTube links or uploaded files), extracts the audio, transcribes it using AI, and generates clean, structured documentation. You can also chat with the video content using a RAG-powered chatbot.

## ✨ Features

- **Multiple Input Options**: Support for video URLs (YouTube, Vimeo, etc.) or direct file uploads
- **Smart Transcription**: Uses Faster-Whisper for accurate speech-to-text conversion
- **AI-Powered Documentation**: Automatically generates structured markdown documentation from transcripts
- **Intelligent Chat**: Ask questions about the video content with context-aware responses
- **Caching System**: Avoid reprocessing the same video multiple times
- **Vector Storage**: Uses ChromaDB for efficient semantic search and retrieval
- **Modern UI**: Clean Streamlit interface with split-screen layout

## 🛠️ Tech Stack

**Backend:**
- FastAPI - REST API framework
- Faster-Whisper - Audio transcription
- LangChain - LLM orchestration
- Google Gemini - AI model for documentation generation
- ChromaDB - Vector database for RAG
- yt-dlp - Video/audio download

**Frontend:**
- Streamlit - Web interface

## 📦 Installation

### Prerequisites
- Python 3.8+
- Google API Key (for Gemini)

### Setup Steps

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd video-2-doc
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_google_api_key_here
```

## 🚀 Usage

### Start the Backend Server

```bash
uvicorn backend.main:app --reload
```

The API will be available at `http://localhost:8000`

### Start the Frontend

In a new terminal:

```bash
streamlit run frontend/app.py
```

The web interface will open at `http://localhost:8501`

### Using the Application

1. **Choose Input Type**: Select either video URL or file upload
2. **Submit**: Paste a link or upload a video/audio file
3. **Generate**: Click "Generate Documentation" and wait for processing
4. **Review**: View the structured documentation on the left panel
5. **Chat**: Ask questions about the video content using the chat interface on the right

## 📁 Project Structure

```
video-2-doc/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── audio_handler.py    # Audio extraction and processing
│   │   ├── transcriber.py      # Whisper transcription logic
│   │   ├── chunker.py          # Text chunking for vector storage
│   │   ├── vector_store.py     # ChromaDB vector operations
│   │   ├── doc_generator.py    # Documentation generation with LLM
│   │   └── chat_engine.py      # RAG-based chatbot logic
│   └── utils/
│       └── cache.py            # Caching system for processed videos
├── frontend/
│   └── app.py                  # Streamlit UI
├── temp_audio/                 # Temporary audio file storage
├── chroma_db/                  # Vector database storage
├── cache.json                  # Processing cache
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔄 How It Works

1. **Input Processing**: Accepts video URL or uploaded file
2. **Audio Extraction**: Downloads and extracts audio using yt-dlp
3. **Transcription**: Converts audio to text using Faster-Whisper
4. **Text Chunking**: Breaks transcript into manageable chunks
5. **Vector Storage**: Stores chunks in ChromaDB with embeddings
6. **Documentation Generation**: Uses Google Gemini to create structured markdown
7. **Caching**: Saves results to avoid reprocessing
8. **RAG Chat**: Retrieves relevant chunks and generates contextual answers

## 🔑 API Endpoints

### POST `/process`
Process a video and generate documentation

**Parameters:**
- `url` (optional): Video URL
- `file` (optional): Uploaded file

**Response:**
```json
{
  "status": "success",
  "hash": "unique_hash",
  "documentation": "Generated markdown documentation"
}
```

### POST `/chat`
Ask questions about processed video content

**Request Body:**
```json
{
  "collection_name": "video_hash",
  "query": "Your question here"
}
```

**Response:**
```json
{
  "answer": "AI-generated answer with context"
}
```

## 💡 Tips

- **First Run**: The first video processing takes longer as models are loaded
- **Cache**: Reprocessing the same video is instant thanks to caching
- **Audio Quality**: Better audio quality = better transcription
- **Question Format**: Ask specific questions for better chat responses

## 🐛 Troubleshooting

**Backend won't start:**
- Check if port 8000 is available
- Verify all dependencies are installed
- Ensure `.env` file exists with valid API key

**Transcription errors:**
- Check audio quality
- Try a different video format
- Ensure sufficient disk space in `temp_audio/`

**Chat not working:**
- Verify documentation was generated successfully
- Check that the hash/collection exists in ChromaDB

## 📝 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
