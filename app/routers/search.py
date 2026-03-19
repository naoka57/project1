from datetime import date, timedelta
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")

# モックデータ: フライト検索結果
MOCK_FLIGHTS = [
    {
        "id": "FL001",
        "airline": "ANA",
        "airline_logo": "NH",
        "origin": "NRT",
        "destination": "LAX",
        "departure_time": "10:30",
        "arrival_time": "04:30",
        "duration": "10h 00m",
        "stops": 0,
        "price": 85000,
        "currency": "JPY",
    },
    {
        "id": "FL002",
        "airline": "JAL",
        "airline_logo": "JL",
        "origin": "NRT",
        "destination": "LAX",
        "departure_time": "17:00",
        "arrival_time": "11:00",
        "duration": "10h 00m",
        "stops": 0,
        "price": 92000,
        "currency": "JPY",
    },
    {
        "id": "FL003",
        "airline": "United Airlines",
        "airline_logo": "UA",
        "origin": "NRT",
        "destination": "LAX",
        "departure_time": "15:45",
        "arrival_time": "10:15",
        "duration": "10h 30m",
        "stops": 0,
        "price": 78000,
        "currency": "JPY",
    },
    {
        "id": "FL004",
        "airline": "Delta Air Lines",
        "airline_logo": "DL",
        "origin": "NRT",
        "destination": "LAX",
        "departure_time": "16:30",
        "arrival_time": "12:00",
        "duration": "11h 30m",
        "stops": 1,
        "price": 65000,
        "currency": "JPY",
    },
    {
        "id": "FL005",
        "airline": "Korean Air",
        "airline_logo": "KE",
        "origin": "NRT",
        "destination": "LAX",
        "departure_time": "09:00",
        "arrival_time": "06:30",
        "duration": "13h 30m",
        "stops": 1,
        "price": 58000,
        "currency": "JPY",
    },
]

MOCK_HOTELS = [
    {
        "id": "HT001",
        "name": "Hilton Los Angeles Airport",
        "rating": 4.2,
        "stars": 4,
        "area": "LAX Airport Area",
        "price_per_night": 18000,
        "currency": "JPY",
        "image": "hotel1",
        "amenities": ["Wi-Fi", "Pool", "Gym", "Restaurant"],
    },
    {
        "id": "HT002",
        "name": "Holiday Inn LAX",
        "rating": 3.8,
        "stars": 3,
        "area": "LAX Airport Area",
        "price_per_night": 12000,
        "currency": "JPY",
        "image": "hotel2",
        "amenities": ["Wi-Fi", "Shuttle", "Breakfast"],
    },
    {
        "id": "HT003",
        "name": "The Westin Bonaventure",
        "rating": 4.5,
        "stars": 4,
        "area": "Downtown LA",
        "price_per_night": 25000,
        "currency": "JPY",
        "image": "hotel3",
        "amenities": ["Wi-Fi", "Pool", "Spa", "Restaurant", "Bar"],
    },
    {
        "id": "HT004",
        "name": "Motel 6 Los Angeles",
        "rating": 3.2,
        "stars": 2,
        "area": "Hollywood",
        "price_per_night": 8000,
        "currency": "JPY",
        "image": "hotel4",
        "amenities": ["Wi-Fi", "Parking"],
    },
    {
        "id": "HT005",
        "name": "Miyako Hotel Los Angeles",
        "rating": 4.0,
        "stars": 3,
        "area": "Little Tokyo",
        "price_per_night": 15000,
        "currency": "JPY",
        "image": "hotel5",
        "amenities": ["Wi-Fi", "Japanese Breakfast", "Onsen"],
    },
]


@router.get("/api/search/combined")
async def search_combined(
    request: Request,
    origin: str = "NRT",
    destination: str = "LAX",
    departure_date: str = "",
    return_date: str = "",
    adults: int = 1,
):
    """フライト+ホテルの最安値組み合わせ検索 (モック)"""
    if not departure_date:
        departure_date = str(date.today() + timedelta(days=30))
    if not return_date:
        return_date = str(date.today() + timedelta(days=37))

    dep = date.fromisoformat(departure_date)
    ret = date.fromisoformat(return_date)
    nights = (ret - dep).days

    flights = sorted(MOCK_FLIGHTS, key=lambda f: f["price"])
    hotels = sorted(MOCK_HOTELS, key=lambda h: h["price_per_night"])

    combinations = []
    for flight in flights:
        for hotel in hotels:
            total = flight["price"] + (hotel["price_per_night"] * nights)
            combinations.append(
                {
                    "flight": flight,
                    "hotel": hotel,
                    "nights": nights,
                    "hotel_total": hotel["price_per_night"] * nights,
                    "total_price": total,
                }
            )
    combinations.sort(key=lambda x: x["total_price"])

    return {
        "origin": origin,
        "destination": destination,
        "departure_date": departure_date,
        "return_date": return_date,
        "adults": adults,
        "combinations": combinations[:10],
        "flights": flights,
        "hotels": hotels,
    }


@router.post("/api/search/results")
async def search_results_partial(request: Request):
    """HTMX用: 検索結果パーシャルを返す"""
    form = await request.form()
    origin = form.get("origin", "NRT")
    destination = form.get("destination", "LAX")
    departure_date = form.get("departure_date", str(date.today() + timedelta(days=30)))
    return_date = form.get("return_date", str(date.today() + timedelta(days=37)))
    adults = int(form.get("adults", "1"))

    dep = date.fromisoformat(departure_date)
    ret = date.fromisoformat(return_date)
    nights = (ret - dep).days if ret > dep else 1

    flights = sorted(MOCK_FLIGHTS, key=lambda f: f["price"])
    hotels = sorted(MOCK_HOTELS, key=lambda h: h["price_per_night"])

    combinations = []
    for flight in flights:
        for hotel in hotels:
            total = flight["price"] + (hotel["price_per_night"] * nights)
            combinations.append(
                {
                    "flight": flight,
                    "hotel": hotel,
                    "nights": nights,
                    "hotel_total": hotel["price_per_night"] * nights,
                    "total_price": total,
                }
            )
    combinations.sort(key=lambda x: x["total_price"])

    return templates.TemplateResponse(
        "partials/results_content.html",
        {
            "request": request,
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date,
            "return_date": return_date,
            "adults": adults,
            "combinations": combinations[:10],
            "flights": flights,
            "hotels": hotels,
        },
    )
