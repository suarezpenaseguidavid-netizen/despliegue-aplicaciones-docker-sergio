import os

import psycopg
from fastapi import FastAPI, HTTPException

app = FastAPI()


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "db-app"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "appdb"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD", ""),
        connect_timeout=3,
    )


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API running correctly"}


@app.get("/db-test")
def db_test():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version()")
                version = cur.fetchone()[0]
        return {"database": "connected", "version": version}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"database error: {exc}")
