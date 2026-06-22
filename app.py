from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bs4 import BeautifulSoup
import requests

app = FastAPI(
    title="MCD Booking/Unbooking API",
    version="1.0.0",
    description="Unofficial API Wrapper for MCD Property Booking/Unbooking Search"
)

BASE_URL = "https://mcdonline.nic.in/portal/fetchBookingUnbookingList"
SEARCH_URL = "https://mcdonline.nic.in/portal/bookingUnbookingList"

ZONES = {
    "CENTRAL ZONE": "52db43e5-48f7-4dc3-a2b6-fcd91a3afdce",
    "CITY S.P. ZONE": "06bf604c-a677-42ed-be8d-d9f7b7904d0f",
    "CIVIL LINE ZONE": "03e863f9-a61b-4594-bbc7-24869c2addc1",
    "KAROL BAGH ZONE": "4b1ed2cd-5f0d-4bb9-9880-3b771ec3ce8e",
    "KESHAVPURAM ZONE": "b1db8ee6-0014-4ff0-b7fc-19d77b809ef1",
    "NAJAFGARH ZONE": "ea957092-5254-48dc-9174-543df5954efc",
    "NARELA ZONE": "4b421c65-9d34-44b8-b1be-30a2dc56180d",
    "ROHINI ZONE": "148065e0-d1d2-4075-8f33-25325ab20b55",
    "SHAHDARA NORTH ZONE": "04ac2578-2b4a-4566-8465-6353824b412d",
    "SHAHDARA SOUTH ZONE": "2561e57e-7bde-4bd6-8842-d888bcdbdff6",
    "SOUTH ZONE": "77107bec-25e6-406a-9710-cad530be35cb",
    "WEST ZONE": "872fe807-1b5d-43dd-b22a-3458860d66dc"
}


class SearchRequest(BaseModel):
    zone_id: str
    address: str
    property_type: str = "booked"


@app.get("/")
def root():
    return {
        "message": "MCD Booking/Unbooking API",
        "docs": "/docs"
    }


@app.get("/zones")
def get_zones():
    return [
        {
            "name": name,
            "id": zone_id
        }
        for name, zone_id in ZONES.items()
    ]


@app.post("/search")
def search(req: SearchRequest):
    try:
        if not req.address.strip():
            raise HTTPException(
                status_code=400,
                detail="Address is required"
            )

        session = requests.Session()

        session.get(
            BASE_URL,
            timeout=30
        )

        payload = {
            "zoneName": req.zone_id,
            "colonyName": "",
            "commonParam": req.address,
            "bookedp": req.property_type
        }

        response = session.post(
            SEARCH_URL,
            data=payload,
            timeout=30
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        rows = soup.select(
            "#bookinglicenseTable tbody tr"
        )

        results = []

        for row in rows:
            cols = [
                td.get_text(" ", strip=True)
                for td in row.select("td")
            ]

            if len(cols) < 7:
                continue

            results.append({
                "booking_id": cols[1],
                "booking_file_number": cols[2],
                "owner_name": cols[3],
                "address": cols[4],
                "booking_date": cols[5],
                "unbooking_date": cols[6]
            })

        return {
            "count": len(results),
            "results": results
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )