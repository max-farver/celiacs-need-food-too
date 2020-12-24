from fastapi import FastAPI

from routes import restaurant_routes, user_routes, review_routes

app = FastAPI()
app.include_router(restaurant_routes.router)
app.include_router(user_routes.router)
app.include_router(review_routes.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
