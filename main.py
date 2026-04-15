from fastapi import FastAPI,Path,Query,HTTPException,Depends
from pydantic import  BaseModel,Field
from fastapi.responses import HTMLResponse,FileResponse

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

#需求：设计接口查询图书，要求携带两个查询参数：图书分类和价格
#参数具体要求：
# 图书分类：默认值为python开发，长度限制为5~255
# 价格：限制大小范围为50~100
@app.get("/book_list")
async def book_list(
id :str = Query("python开发",min_length=5,max_length=255),
price : int = Query(...,ge = 50,le = 100),
):
    return {"图书分类":id,"价格":price}

#需求：设计接口新增图书，图书信息包含：书名，作者，出版社，售价
class BookCreate(BaseModel):
    bookname:str = Field(...,min_length=2,max_length=10)
    author:  str = Field(...,min_length=2,max_length=10)
    publisher:str = Field(default="黑马出版社")
    price:float = Field(default= 0,gt = 0)

@app.post("/book_list")
async def create_book(
        book :BookCreate,
):
    return {"msg":"新增图书成功","book_info":book.dict()}
#注意接口之间的命名冲突问题

@app.get("/html",response_class=HTMLResponse)
async def html():
    return "<h1>这是一级标题</h1>"

@app.get("/file",response_class=FileResponse)
async def file():
    path = "./error.jpg"
    return FileResponse(path)

@app.middleware("http")
async def middleware(request,call_next):
    print("中间件1 start")
    response = await call_next(request)
    print("中间件1 end")
    return response

@app.middleware("http")
async def middleware(request,call_next):
    print("中间件2 start")
    response = await call_next(request)
    print("中间件2 end")
    return response


@app.get("/news/{id}")
async def news(id:int):
    id_list = [1,2,3,4,5,6]
    if id not in id_list:
        raise HTTPException(status_code=404,detail="你查找的新闻不存在")
    return {"id":id}

# 依赖注入
async def comments(
        skip:int = Query(0,le=10),
        limit:int = Query(10,le=60),
):
    return {"skip":skip,"limit":limit}


@app.get("/news")
async def news_page(common=Depends(comments)):
    return common

