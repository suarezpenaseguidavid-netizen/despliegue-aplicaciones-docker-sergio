from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API running correctly"}

@app.get("/db-test")
def db_test():
    return {"database": "connected", "status": "pending persistence setup"}
