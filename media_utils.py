import uuid
import shutil
from pathlib import Path
from fastapi import UploadFile, HTTPException

POST_MEDIA_DIR = Path("media/post_attachments")
POST_MEDIA_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
ALLOWED_AUDIO_TYPES = {"audio/mpeg", "audio/wav", "audio/ogg", "audio/mp3"}
ALLOWED_VIDEO_TYPES = {"video/mp4", "video/webm", "video/ogg"}

ALLOWED_TYPES = ALLOWED_IMAGE_TYPES | ALLOWED_AUDIO_TYPES | ALLOWED_VIDEO_TYPES
MAX_FILE_SIZE = 50 * 1024 * 1024 # 50 MB to accommodate videos

def process_post_attachment(file: UploadFile) -> str:
    """Saves a post attachment asynchronously/semi-sync and returns the relative path."""
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")
    
    # We can perform a rough check, though relying on file size reads requires async or seek
    # For now we'll do stream saving.
    ext = file.filename.split('.')[-1].lower() if '.' in file.filename else ''
    filename = f"{uuid.uuid4().hex}.{ext}" if ext else f"{uuid.uuid4().hex}"
    filepath = POST_MEDIA_DIR / filename

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return f"/media/post_attachments/{filename}"
