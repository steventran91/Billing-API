from fastapi import FastAPI
from .routers import auth

app = FastAPI(title="billing-api")
app.include_router(auth.router)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
