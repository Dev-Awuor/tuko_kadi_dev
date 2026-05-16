"""Main Entry Point for Sauti ya Mwananchi FastAPI Gateway."""

from fastapi import FastAPI
from src.gateway.webhooks import router as webhook_router
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sauti ya Mwananchi Gateway",
    description="Stateless Gateway for Africa's Talking Integration",
    version="1.0.0"
)

# Health Check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "sauti-ya-mwananchi"}

@app.get("/")
async def root():
    return {
        "service": "Sauti ya Mwananchi",
        "endpoints": ["/webhook/sms", "/webhook/ussd", "/webhook/whatsapp", "/health"]
    }

# Include routers
app.include_router(webhook_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
