from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil, os, uuid

app = FastAPI(title="Medhat Waheed Cloud Studio API", version="0.1.0")
# Replace/add your exact Blogger domain before production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/tmp/mw_uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAX_BYTES = int(os.getenv("MAX_UPLOAD_BYTES", str(5 * 1024**3)))

@app.get("/")
def root():
    return {"name": "Medhat Waheed Cloud Studio API", "status": "running", "note": "Starter API only; transcription and clip rendering are not implemented yet."}

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/upload")
def upload_video(file: UploadFile = File(...)):
    allowed = {".mp4", ".mov", ".mkv", ".webm", ".m4v", ".avi"}
    suffix = Path(file.filename or "video.mp4").suffix.lower()
    if suffix not in allowed:
        raise HTTPException(status_code=400, detail="Unsupported video file type")
    file_id = uuid.uuid4().hex
    destination = UPLOAD_DIR / f"{file_id}{suffix}"
    size = 0
    try:
        with destination.open("wb") as out:
            while True:
                chunk = file.file.read(1024 * 1024)
                if not chunk:
                    break
                size += len(chunk)
                if size > MAX_BYTES:
                    out.close()
                    destination.unlink(missing_ok=True)
                    raise HTTPException(status_code=413, detail="File exceeds configured upload limit")
                out.write(chunk)
    except HTTPException:
        raise
    except Exception as exc:
        destination.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail="Upload failed") from exc
    finally:
        file.file.close()
    return {"ok": True, "file_id": file_id, "filename": file.filename, "size_bytes": size,
            "message": "Upload received. Transcription and clip processing are not implemented in this starter."}
