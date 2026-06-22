# MCD Booking/Unbooking API

Unofficial FastAPI wrapper for the Municipal Corporation of Delhi (MCD) Property Booking/Unbooking Search Portal.

This API allows you to search booked/unbooked properties by zone and address and returns structured JSON instead of raw HTML.

---

## Features

- Search booked properties by address
- Search unbooked properties
- Get all available MCD zones
- Clean JSON response
- FastAPI + Swagger Documentation
- No browser automation required
- No captcha required

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/mcd-booking-api.git

cd mcd-booking-api
```

Install dependencies:

```bash
pip install fastapi uvicorn requests beautifulsoup4
```

---

## Running the API

```bash
python app.py
```

or

```bash
uvicorn app:app --reload
```

Server will start on:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Get Available Zones

### Request

```http
GET /zones
```

### Response

```json
[
  {
    "name": "SHAHDARA NORTH ZONE",
    "id": "04ac2578-2b4a-4566-8465-6353824b412d"
  },
  {
    "name": "SHAHDARA SOUTH ZONE",
    "id": "2561e57e-7bde-4bd6-8842-d888bcdbdff6"
  }
]
```

---

## Search Properties

### Request

```http
POST /search
```

### Body

```json
{
  "zone_id": "04ac2578-2b4a-4566-8465-6353824b412d",
  "address": "KARAWAL NAGAR",
  "property_type": "booked"
}
```

### Parameters

| Field | Type | Required | Description |
|---------|---------|---------|---------|
| zone_id | string | Yes | MCD Zone UUID |
| address | string | Yes | Address or locality keyword |
| property_type | string | No | booked / unbooked |

---

### Example Response

```json
{
  "count": 2,
  "results": [
    {
      "booking_id": "220626105969233",
      "booking_file_number": "67/B-II/UC/SH-N/2026",
      "owner_name": "SHAKUNTLA DEVI",
      "address": "1/4649/132 GALI NO. 2 NEW MODERN SHAHDARA RAM NAGAR SHADARA SHAHDARA NORTH ZONE",
      "booking_date": "19-06-2026",
      "unbooking_date": ""
    }
  ]
}
```

---

# Supported Zones

| Zone |
|--------|
| CENTRAL ZONE |
| CITY S.P. ZONE |
| CIVIL LINE ZONE |
| KAROL BAGH ZONE |
| KESHAVPURAM ZONE |
| NAJAFGARH ZONE |
| NARELA ZONE |
| ROHINI ZONE |
| SHAHDARA NORTH ZONE |
| SHAHDARA SOUTH ZONE |
| SOUTH ZONE |
| WEST ZONE |

---

# Example Usage (Python)

```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/search",
    json={
        "zone_id": "04ac2578-2b4a-4566-8465-6353824b412d",
        "address": "KARAWAL NAGAR",
        "property_type": "booked"
    }
)

print(response.json())
```

---

# Tech Stack

- FastAPI
- Requests
- BeautifulSoup4
- Uvicorn

---

# Data Source

Data is fetched from the official Municipal Corporation of Delhi portal:

https://mcdonline.nic.in/portal/fetchBookingUnbookingList

This project is an unofficial wrapper and is not affiliated with the Municipal Corporation of Delhi.

---

# Disclaimer

This project simply converts publicly accessible information from the MCD portal into a developer-friendly JSON API.

Users are responsible for complying with all applicable laws, regulations, and website terms of use.

---

# Author

**Raghav Sachdev**

- Portfolio: raghavsachdev.vercel.app
- GitHub: github.com/raghavsach-dev

---

If this project helped you, consider giving it a ⭐ on GitHub.