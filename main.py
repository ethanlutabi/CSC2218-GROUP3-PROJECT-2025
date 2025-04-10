from fastapi import FastAPI
from presentation.api.accounts import router as accounts_router

app = FastAPI(
    title="Simple Banking API",
    description="A simple banking application following Clean Architecture",
    version="1.0.0"
)

app.include_router(accounts_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
