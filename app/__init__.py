import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.routes import auth, protected


def create_app():
    """
    Application factory function to create and configure the FastAPI application.
    """
    load_dotenv()
    app = FastAPI(
        title="Auto Invoice",
        description="Auto Invoice",
        version="1.0.0" 
    )
    
    app.include_router(auth.router)
    app.include_router(protected.router)
    return app
