from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(
    title="AI Business Decision Engine",
    version="v1"
)

# --- CORS CONFIGURATION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # local dev
        "https://ai-business-decision-engine.vercel.app",  # Vercel PROD
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROUTES ---
app.include_router(router)


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "AI Business Decision Engine",
        "version": "v1"
    }
