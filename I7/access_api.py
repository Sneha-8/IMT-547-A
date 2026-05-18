"""
I7 API Access - Python Client Script
Course: IMT 542 A Sp 26 - Portable Information Structures
Author: Sneha

Description:
    Uses the requests library to call the Local Small Business Discovery API.
    Demonstrates all available GET endpoints.

How to Run:
    1. Start the server first:   flask --app app run -p 5002
    2. (Optional) Start ngrok:   ngrok http http://localhost:5002
       Then replace BASE_URL below with your ngrok HTTPS URL.
    3. Run this script:          python access_api.py
"""

import requests
import json

# Replace with your ngrok URL when tunneling
BASE_URL = "http://localhost:5002"


def sep(label):
    print("\n" + "=" * 60)
    print(f"  {label}")
    print("=" * 60)


def show(response):
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))


# 1. Health check
sep("GET / - API Health Check")
show(requests.get(f"{BASE_URL}/"))

# 2. List all businesses
sep("GET /businesses - All Businesses")
show(requests.get(f"{BASE_URL}/businesses"))

# 3. Get one business by ID
sep("GET /businesses/sb-001 - Single Business")
show(requests.get(f"{BASE_URL}/businesses/sb-001"))

# 4. Filter by category
sep("GET /businesses/category/cafe - Filter by Category")
show(requests.get(f"{BASE_URL}/businesses/category/cafe"))

# 5. Filter by ZIP code
sep("GET /businesses/zip/98101 - Filter by ZIP")
show(requests.get(f"{BASE_URL}/businesses/zip/98101"))

# 6. Filter by neighborhood
sep("GET /businesses/neighborhood/Capitol Hill - Filter by Neighborhood")
show(requests.get(f"{BASE_URL}/businesses/neighborhood/Capitol Hill"))

# 7. Keyword search
sep("GET /search?q=vegan - Keyword Search")
show(requests.get(f"{BASE_URL}/search", params={"q": "vegan"}))

# 8. List categories
sep("GET /categories - All Categories")
show(requests.get(f"{BASE_URL}/categories"))

print("\nDone!")
