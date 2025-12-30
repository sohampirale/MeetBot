from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from database import init_database
from routes.user import router as user_router

app = FastAPI(
    title="MeetBot API",
    description="API for MeetBot voice AI agents platform",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_router)

# Optionally enable this for DB init on startup
# @app.on_event("startup")
# async def startup_event():
#     """Initialize database on application startup."""
#     # await init_database()

@app.get("/")
async def root():
    """Root endpoint for API health check."""
    return {"message": "MeetBot API is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent format."""
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected server errors."""
    return JSONResponse(status_code=500, content={"message": "Internal server error"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
