from fastapi import FastAPI,Path

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/user/hello")
async def study():
    return{"msg":"我正在学习fastapi..."}

@app.get("/user/{id}")
async def constudy(id:int):
    return{"id":id,"用户名称":f"普通用户{id}"}

@app.get("/新闻分类/{id}")
async def study01(id:int = Path(...,ge = 1,le = 100)):
    return {f"这是第{id}种新闻"}

@app.get("/新闻分类01/{name}")
async def study02(name:str = Path(...,min_length = 2,max_length = 10)):
    return {f"这个新闻分类是{name}"}