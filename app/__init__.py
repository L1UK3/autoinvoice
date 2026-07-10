import os
from dotenv import load_dotenv
from fastapi import FastAPI


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
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("app:app", host="[IP_ADDRESS]", port=8000, reload=True)