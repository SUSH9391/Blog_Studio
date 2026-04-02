from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException
from fastapi import status

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

post: list[dict] =  [
    {"id": 1, "title": "First Post", "content": "This is the first post."},
    {"id": 2, "title": "Second Post", "content": "This is the second post."},
    {"id": 3, "title": "Third Post", "content": "This is the third post."},
]


@app.get("/", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "Home.html",
        {"posts": post, "title": "Home Page"},
    )


@app.get("/posts/{post_id}", include_in_schema=False)
def post_page(request: Request, post_id: int):
    for post_item in post:
        if post_item.get("id") == post_id:
            
            return templates.TemplateResponse(
                request,
                "post.html",
                {"post": post_item, "title": post_item.get("title", "Post")[:50]},
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.get("/api/posts")
def get_posts():
    return post


@app.get("/api/posts/{post_id}")
def get_post(post_id: int):
    for post_item in post:
        if post_item.get("id") == post_id:
            return post_item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@app.exception_handler(StarletteHTTPException)
def genral_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred while processing your request."
    )
    
    if request.url.path.startswith("/api/"):
        return JSONResponse({"detail": message}, status_code=exception.status_code)
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": f"Error {exception.status_code}",
            "message": message,
        },
    status_code=exception.status_code
    )
    
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, execption: RequestValidationError):
    message = "Invalid request data. Please check your input and try again."
    
    if request.url.path.startswith("/api/"):
        return JSONResponse({"detail": message}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "title": "Validation Error",
            "message": message,
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )