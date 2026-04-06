import traceback

try:
    from main import app
except Exception as e:
    from fastapi import FastAPI
    from fastapi.responses import PlainTextResponse
    
    app = FastAPI()
    error_msg = traceback.format_exc()
    @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"])
    async def catch_all(path_name: str):
        return PlainTextResponse(f"Initialization Error:\n{error_msg}", status_code=500)
