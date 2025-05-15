from fastapi import FastAPI
from database import Base, engine
from api.users_api import user_router
app = FastAPI(docs_url="/")
# первичная миграция
Base.metadata.create_all(bind=engine)
# регистрируем компонент(роутер)
app.include_router(user_router)

@app.get("/test")
async def test():
    return "OK"

# uvicorn main:app --reload