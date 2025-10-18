from fastapi import FastAPI
from src.routes import review,auth,laptop
import uvicorn


app = FastAPI(title="Laptop Comparison API")

app.include_router(review.router,prefix = "/reviews")
app.include_router(auth.router,prefix = "/auth")
app.include_router(laptop.router,prefix = "/laptops")


if __name__ == "__main__":

    uvicorn.run("src.main:app", host="localhost", port = 8000)
