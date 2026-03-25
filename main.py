from fastapi import FastAPI, Request
import uvicorn
import requests
import time
import jwt  # We'll add this to requirements
import os
from datetime import datetime, timedelta

app = FastAPI(title="Atelier Video Agent")

# === YOUR KEYS ===
ACCESS_KEY = "AGgaTnBJbeQAyn34tdr3R8aKyd8NrNb4"   # ← Paste your Access Key
SECRET_KEY = "pr3eQPFdeJdMB4LgDKL3HArpteJKA4Nr"   # ← Paste your Secret Key

def get_kling_jwt():
    payload = {
        "iss": ACCESS_KEY,
        "exp": int(time.time()) + 3600,  # 1 hour expiry
        "nbf": int(time.time()) - 5
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

@app.get("/agent/profile")
def profile():
    return {
        "name": "MyVideoAdAgent",
        "description": "Generates 30-second crypto video ads for PumpFun and Solana projects using Kling AI.",
        "capabilities": ["video_gen"]
    }

@app.get("/agent/services")
def services():
    return {
        "services": [
            {
                "id": "svc_1774423718114_fo5dcyjwc",
                "title": "30-Second Crypto Video Advertisement",
                "description": "High-quality 30-second promotional video ad for PumpFun or Solana memecoins. Includes text overlays, music, and dynamic visuals.",
                "price_usd": "100.00",
                "category": "video_gen"
            }
        ]
    }

@app.post("/agent/execute")
async def execute(request: Request):
    data = await request.json()
    brief = data.get("brief", "Create an energetic 30-second promo for a new Solana memecoin")

    prompt = f"30-second high-energy crypto advertisement video: {brief}. Fast cuts, glowing Solana charts pumping up, text overlays 'To The Moon!', 'Buy Now on PumpFun', cinematic lighting, upbeat electronic music vibe, smooth camera moves, 1080p, no watermark, professional ad quality."

    try:
        jwt_token = get_kling_jwt()

        # Create task (Kling 2.6+ style - adjust if your dashboard shows different base URL)
        create_resp = requests.post(
            "https://api.klingai.com/v1/videos/text2video",   # Common base; some use api-singapore.klingai.com
            headers={
                "Authorization": f"Bearer {jwt_token}",
                "Content-Type": "application/json"
            },
            json={
                "model": "kling-2.6-pro",   # or "kling-2.6-standard" for cheaper
                "prompt": prompt,
                "duration": 30,
                "aspect_ratio": "16:9"
            },
            timeout=60
        )
        create_resp.raise_for_status()
        task_id = create_resp.json().get("task_id")

        # Poll for completion (up to ~3 minutes)
        video_url = None
        for _ in range(45):
            status_resp = requests.get(
                f"https://api.klingai.com/v1/videos/status/{task_id}",
                headers={"Authorization": f"Bearer {jwt_token}"}
            )
            status_data = status_resp.json()
            if status_data.get("status") == "completed":
                video_url = status_data.get("data", {}).get("url")
                break
            time.sleep(4)

        if not video_url:
            raise Exception("Video generation timed out or failed")

        return {
            "result": "30s video ad generated successfully with Kling AI",
            "deliverable_url": video_url
        }

    except Exception as e:
        return {
            "result": f"Error: {str(e)}",
            "deliverable_url": "https://example.com/error-placeholder.mp4"
        }

@app.get("/agent/portfolio")
def portfolio():
    return {"works": []}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
