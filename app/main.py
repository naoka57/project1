from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.routers import search

app = FastAPI(title="Flight & Hotel Booking Tool")

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent / "static"),
    name="static",
)

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

app.include_router(search.router)


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/results")
async def results_page(request: Request):
    return templates.TemplateResponse("results.html", {"request": request})


@app.get("/booking/{booking_id}")
async def booking_page(request: Request, booking_id: str):
    return templates.TemplateResponse(
        "booking.html", {"request": request, "booking_id": booking_id}
    )
