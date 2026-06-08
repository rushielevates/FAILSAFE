from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.connection import init_db
import traceback
import sys

def exception_handler(exc_type, exc_value, exc_traceback):
    print("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))

sys.excepthook = exception_handler
# Create the FastAPI app
app = FastAPI(
    title="FAILSAFE API",
    description="Early Warning System for At-Risk Students",
    version="1.0.0"
)

# Create tables on startup
@app.on_event("startup")
def startup_event():
    init_db()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Allow frontend to connect (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint - health check
@app.get("/")
def root():
    return {
        "message": "FAILSAFE API is running!",
        "status": "healthy",
        "version": "1.0.0"
    }

# Import and include route files (we'll create these next)
from routes import predict, auth

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(predict.router, prefix="/api", tags=["Predictions"])