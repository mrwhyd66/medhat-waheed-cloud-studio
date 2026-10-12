# Medhat Waheed Cloud Studio — starter backend

This is a starter FastAPI service for deployment on Render. It provides health endpoints and a basic video upload endpoint.

## Important limitations
- This starter does **not** transcribe speech, create clips, generate captions, or export Premiere projects yet.
- The `/upload` endpoint writes uploads to local temporary disk. It is not suitable for reliable 5 GB production uploads or persistent storage.
- For production, use direct multipart/resumable uploads to object storage, a background job queue/worker, FFmpeg, and a transcription service such as Whisper. Add authentication, quotas, retention/deletion policies, and restrict CORS to your Blogger domain.

## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` to inspect the API.

## Deploy on Render
1. Upload these files to the root of your GitHub repository.
2. In Render, choose **New + → Blueprint** and connect the repository, or create a Docker web service from the repository.
3. After deployment, test `/health` and `/docs` on the Render URL.
