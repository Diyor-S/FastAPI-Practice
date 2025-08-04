from fastapi import FastAPI
from items import router as items_router
from users.views import router as users_router
import uvicorn

# Annotated -> set some rules, conditions to the data

app = FastAPI()
app.include_router(items_router)
# app.include_router(items_router, prefix="items-views") # we can redefine the prefix here
app.include_router(users_router)

@app.get('/')
def hello_index():
    return {
        "message": "Hello index!",
    }
    
@app.get("/hello/")
def hello(name: str = "World"):
    name = name.strip().title()
    return {"message": f"Hello {name}!"}



@app.post("/calc/add")
def add(a: int, b: int):
    return {
        "a": a,
        "b": b,
        "result": a + b,
    }




if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)