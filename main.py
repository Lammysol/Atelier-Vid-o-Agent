from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Atelier Video Agent")

@app.get("/agent/profile")
def profile():
    return {
        "name": "MyVideoAdAgent",
        "description": "Generates 30-second crypto video ads for PumpFun and Solana projects. Fast and high quality.",
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
async def execute(request):
    data = await request.json()
    brief = data.get("brief", "No brief provided")
    return {
        "result": f"30s video ad generated for brief: {brief}",
        "deliverable_url": "https://example.com/placeholder-30s-ad.mp4"
    }

@app.get("/agent/portfolio")
def portfolio():
    return {"works": []}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
