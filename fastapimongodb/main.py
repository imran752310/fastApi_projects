from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router # type: ignore

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router)


# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from pymongo import MongoClient


# MONGO_URI="mongodb+srv://muhammadimran752310:<db_password>@cluster0.mwme6.mongodb.net/?appName=Cluster0"
# client = MongoClient(MONGO_URI)
# database = client.your_database_name
# collection = database.your_collection_name

# app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")

# templates = Jinja2Templates(directory="templates")


# @app.get("/", response_class=HTMLResponse)
# async def read_item(request: Request,):
#     return templates.TemplateResponse(
#        "index.html", {"request": request}
#     )

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str | None = None):
#     return {"item_id": item_id, "q" : q}
    

