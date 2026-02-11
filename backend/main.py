from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

from backend.utils.cache import generate_hash, check_cache, save_to_cache
from backend.core.audio_handler import process_url, save_uploaded_file, cleanup_file
from backend.core.transcriber import transcribe_audio
from backend.core.chunker import chunk_text
from backend.core.vector_store import store_chunks
from backend.core.doc_generator import generate_documentation
from backend.core.chat_engine import ask_chatbot

app = FastAPI(title="Video to Doc AI API")

class ChatRequest(BaseModel):
    collection_name: str
    query: str

@app.post("/process")
async def process_video(
    url: str = Form(None),
    file: UploadFile = File(None)
):
    """Handles both URL links and direct file uploads."""
    if not url and not file:
        raise HTTPException(status_code=400, detail="Must provide either a URL or a file.")

    temp_path = None

    # 1. Generate Hash & Check Cache
    if url:
        input_hash = generate_hash(url, is_file=False)
    else:
        # Save temp file immediately so we can hash its contents
        temp_path = save_uploaded_file(file, file.filename)
        input_hash = generate_hash(temp_path, is_file=True)

    cached_data = check_cache(input_hash)
    if cached_data:
        print("Cache hit! Returning existing documentation.")
        if temp_path: cleanup_file(temp_path)
        return {
            "status": "success", 
            "hash": input_hash, 
            "documentation": cached_data["documentation"]
        }

    # 2. Process Audio
    audio_path = None
    try:
        print("Cache miss. Starting processing pipeline...")
        if url:
            audio_path = process_url(url)
        else:
            audio_path = temp_path # Already saved locally

        # 3. Transcribe Audio -> Text
        transcript = transcribe_audio(audio_path)
        
        # 4. Chunk Text & Store in Vector DB
        chunks = chunk_text(transcript)
        store_chunks(chunks, collection_name=input_hash)
        
        # 5. Generate Final Markdown Documentation
        documentation = generate_documentation(chunks)
        
        # 6. Save to Cache
        save_to_cache(input_hash, {
            "documentation": documentation, 
            "collection_name": input_hash
        })
        
        return {"status": "success", "hash": input_hash, "documentation": documentation}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 7. Cleanup temp audio files regardless of success or failure
        if audio_path:
            cleanup_file(audio_path)

@app.post("/chat")
async def chat_with_video(request: ChatRequest):
    """Endpoint for the Streamlit chatbot."""
    try:
        answer = ask_chatbot(request.collection_name, request.query)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))