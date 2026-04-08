from app.api.routes import app


def main() -> None:
    import uvicorn

    uvicorn.run("app.api.routes:app", host="0.0.0.0", port=7860, reload=False)
