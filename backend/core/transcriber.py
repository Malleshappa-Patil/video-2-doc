from faster_whisper import WhisperModel
import os

# Initialize globally. 
# 'base' or 'small' are great for MVP speed on CPU.
# compute_type="int8" is the optimal setting for CPU, reducing memory by ~75%.
MODEL_SIZE = "base" 
print(f"Loading faster-whisper '{MODEL_SIZE}' model into memory...")

model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")

def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes audio to text.
    faster-whisper natively supports both audio (.mp3) and video (.mp4) files
    if ffmpeg is installed on the system.
    """
    print(f"Starting transcription for {audio_path}")
    
    # vad_filter=True removes silence automatically, drastically speeding up processing
    segments, info = model.transcribe(audio_path, beam_size=5, vad_filter=True)
    
    print(f"Detected language: {info.language} ({info.language_probability:.2f})")
    
    transcript_chunks = []
    # segments is a generator, so we iterate to trigger the actual processing
    for segment in segments:
        transcript_chunks.append(segment.text.strip())
        
    # Merge all segments into one continuous text block
    full_text = " ".join(transcript_chunks)
    return full_text