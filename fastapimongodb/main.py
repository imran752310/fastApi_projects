from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.auth import router as auth_router

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")
app.state.templates = templates

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(auth_router)


# Include auth routes
app.include_router(auth_router)

# Root route - redirect to /login
@app.get("/")
def root():
    return RedirectResponse("/login")
# Remove the separate /dashboard route here because it's in auth.py


# from fastapi import FastAPI, Request
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from app.auth import router as auth_router

# app = FastAPI()

# templates = Jinja2Templates(directory="app/templates")
# app.state.templates = templates

# app.mount("/static", StaticFiles(directory="app/static"), name="static")

# app.include_router(auth_router)

# @app.get("/dashboard")
# def dashboard(request: Request):
#     return templates.TemplateResponse(
#         "dashboard.html", {"request": request, "msg": "Welcome!"}
#     )



# # from fastapi import FastAPI
# # from fastapi.staticfiles import StaticFiles
# # from app.routes import router # type: ignore

# # app = FastAPI()

# # app.mount("/static", StaticFiles(directory="app/static"), name="static")

# # app.include_router(router)


# # # from fastapi import FastAPI, Request
# # # from fastapi.responses import HTMLResponse
# # # from fastapi.staticfiles import StaticFiles
# # # from fastapi.templating import Jinja2Templates
# # # from pymongo import MongoClient


# # # MONGO_URI="mongodb+srv://muhammadimran752310:<db_password>@cluster0.mwme6.mongodb.net/?appName=Cluster0"
# # # client = MongoClient(MONGO_URI)
# # # database = client.your_database_name
# # # collection = database.your_collection_name

# # # app = FastAPI()

# # # app.mount("/static", StaticFiles(directory="static"), name="static")

# # # templates = Jinja2Templates(directory="templates")


# # # @app.get("/", response_class=HTMLResponse)
# # # async def read_item(request: Request,):
# # #     return templates.TemplateResponse(
# # #        "index.html", {"request": request}
# # #     )

# # # @app.get("/items/{item_id}")
# # # def read_item(item_id: int, q: str | None = None):
# # #     return {"item_id": item_id, "q" : q}
    

