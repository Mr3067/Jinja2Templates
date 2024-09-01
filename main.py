from fastapi import FastAPI, HTTPException, Request, Form
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory='templates')
app = FastAPI()


class User(BaseModel):
    id: int
    username: str
    age: int


users_db = []


@app.get('/')
async def get_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users_db})


@app.get(path='/users/{user_id}')
async def get_users(request: Request, user_id: int) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "user": users_db[user_id-1]})


@app.post('/')
async def post_user(request: Request, name: str = Form(), age: str = Form()) -> HTMLResponse:

    if len(users_db) == 0:
        id = 1
    else:
        id = users_db[-1].id + 1
    # username = data_str.split(',')[0]
    # age = int(data_str.split(',')[1])
    username = name
    age = int(age)
    users_db.append(User(id = id, username = username, age= age))
    return templates.TemplateResponse("users.html", {"request": request, "users": users_db})


@app.put('/user/{user_id}/{username}/{age}')
async def put_user(user_id: int, username: str, age: int):
    user_ok = False
    for _ in range(len(users_db)):
        if users_db[_].id == user_id:
            user_ok = True
            users_db[_].username = username
            users_db[_].age = age
    if not user_ok:
        raise HTTPException(status_code=404, detail='User was not found"')


@app.delete('/user/{user_id}')
async def del_user(user_id: int):
    user_ok = False
    for _ in range(len(users_db)):
        if users_db[_].id == user_id:
            user_ok = True
            users_db.pop(_)
            return
    if not user_ok:
        raise HTTPException(status_code=404, detail='User was not found"')
