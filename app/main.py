import uvicorn
from app import create_app

if __name__ == "__main__":
    # start the server
    app = create_app()
    uvicorn.run("app:app", host="[IP_ADDRESS]", port=8000, reload=True)