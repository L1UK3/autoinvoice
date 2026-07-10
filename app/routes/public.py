

# Health Check
@app.get('/')
def health_check():
    return {"status": "ok"}