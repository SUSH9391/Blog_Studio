from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import traceback

app = FastAPI()

try:
    from main import app as real_app
    app = real_app
except Exception as e:
    error_msg = traceback.format_exc()
    @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"])
    async def catch_all(path_name: str):
        return PlainTextResponse(f"Initialization Error:\n{error_msg}", status_code=500)
