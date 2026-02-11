import yt_dlp
import os
import shutil
import uuid
import imageio_ffmpeg

TEMP_DIR = "temp_audio"
os.makedirs(TEMP_DIR, exist_ok=True)

def process_url(url: str) -> str:
    """Extracts audio from web links using a standalone Python FFmpeg binary."""
    unique_id = str(uuid.uuid4())
    output_template = os.path.join(TEMP_DIR, f"{unique_id}.%(ext)s")
    
    # Get the exact path to the Python-installed FFmpeg binary
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': ffmpeg_path,  # <--- THIS IS THE FIX
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_template,
        'quiet': True,
        'no_warnings': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        expected_filename = ydl.prepare_filename(info)
        base, _ = os.path.splitext(expected_filename)
        final_filename = f"{base}.mp3"
        return final_filename

def save_uploaded_file(upload_file, filename: str) -> str:
    """Saves a directly uploaded video or audio file to the temp directory."""
    unique_id = str(uuid.uuid4())
    _, ext = os.path.splitext(filename)
    dest_path = os.path.join(TEMP_DIR, f"{unique_id}{ext}")
    
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
        
    return dest_path

def cleanup_file(file_path: str):
    """Deletes the temporary file after it's transcribed."""
    if file_path and os.path.exists(file_path):
        os.remove(file_path)