from fastapi import FastAPI, Request
import uvicorn
import requests
import time
import jwt

app = FastAPI(title="Atelier Video Agent")

# === REPLACE THESE WITH YOUR REAL KLING KEYS ===
ACCESS_KEY = "AGgaTnBJbeQAyn34tdr3R8aKyd8NrNb4"
SECRET_KEY = "pr3eQPFdeJdMB4LgDKL3HArpteJKA4Nr"

def get_kling_jwt():
    payload = {
        "iss": ACCESS_KEY,
        "exp": int(time.time()) + 3600,
        "nbf": int(time.time()) - 10
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@app.get("/agent/profile")
def profile():
    return {
        "name": "MyVideoAdAgent",
        "description": "Generates 30-second crypto video ads using Kling AI",
        "capabilities": ["video_gen"]
    }

@app.get("/agent/services")
def services():
    return {
        "services": [
            {
                "id": "svc_1774423718114_fo5dcyjwc",
                "title": "30-Second Crypto Video Advertisement",
                "description": "High-quality 30-second promotional video ad for PumpFun or Solana memecoins.",
                "price_usd": "100.00",
                "category": "video_gen"
            }
        ]
    }

@app.post("/agent/execute")
async def execute(request: Request):
    data = await request.json()
    brief = data.get("brief", "Energetic 30s promo for new Solana memecoin")

    prompt = f"Dynamic 30-second crypto advertisement: {brief}. High energy, fast cuts, glowing charts pumping, Solana logo, text overlays 'To The Moon!' and 'Buy Now', cinematic lighting, upbeat music, 1080p, smooth motion, professional ad style, no watermark."

    try:
        token = get_kling_jwt()

        # Create task
        create_resp = requests.post(
            "https://api-singapore.klingai.com/v1/videos/text2video",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={
                "prompt": prompt,
                "duration": 30,
                "aspect_ratio": "16:9"
            }
        )
        create_resp.raise_for_status()
        task_id = create_resp.json().get("task_id")

        # Poll for completion
        video_url = None
        for _ in range(45):
            status_resp = requests.get(
                f"https://api-singapore.klingai.com/v1/videos/text2video/{task_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            status = status_resp.json()
            if status.get("status") == "completed":
                video_url = status.get("data", {}).get("url")
                break
            time.sleep(4)

        if not video_url:
            raise Exception("Video generation timed out")

        return {
            "result": "30s video generated successfully with Kling AI",
            "deliverable_url": video_url
        }

    except Exception as e:
        return {
            "result": f"Error: {str(e)}",
            "deliverable_url": "https://example.com/error.mp4"
        }

@app.get("/agent/portfolio")
def portfolio():
    return {"works": []}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
