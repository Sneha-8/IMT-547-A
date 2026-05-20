# 🏪 Small Business Platform — Access Methodology
## IMT 542 — Portable Information Structures (G8)

---

## 📘 About
The Small Business Platform Information Structure provides portable, machine-readable
listings of local businesses (name, category, location, rating, price tier, and contact
metadata) sourced from the Yelp Fusion API and normalized against Schema.org's
`LocalBusiness` vocabulary. The intended audience includes consumers searching for
nearby businesses, small-business owners verifying their public presence, and
third-party developers, agentic AI assistants, and civic data tools that need a clean
JSON feed. Public listing metadata is openly accessible over HTTPS without
authentication; sensitive fields (owner contact details, internal notes) are gated
behind an authorization layer. The structure is hosted behind a Flask API and exposed
to the open internet through an nGrok tunnel for class demonstration.

## 📘 Methodology
- Records are pulled from the **Yelp Fusion API** (`GET /v3/businesses/search`) using
  a team-owned API key, parameterized by `term`, `location`, and `radius_meters`.
- Each raw record is normalized into our own schema (version `1.0`) that flattens
  Yelp's nested fields and aligns names with Schema.org `LocalBusiness`.
- Phone numbers are converted to **E.164** format, addresses are split into
  `address_line_1` / `address_line_2` / `city` / `state` / `zip_code`, and prices are
  stored as both `price_tier` (integer 1–4) and `price_symbol` (`$`–`$$$$`) for
  portability.
- Every record is run through a **quality_flags** pass (`has_name`, `has_rating`,
  `has_phone`, `address_line_2_missing`, `is_complete`) so consumers can filter on
  completeness without re-parsing.
- A **provenance** block (`source`, `endpoint`, `query_params`, `retrieved_at`,
  `license`, `api_key_owner`) is attached to every response so downstream users can
  trace where data came from and respect Yelp's display-only license.
- Each record carries a `data_classification` tag (`public` vs. restricted) so the
  API layer can enforce field-level access control consistent with FAIR A1.2.
- Maintenance: the dataset is refreshed on demand at request time (cache TTL ~24h)
  and re-validated against the schema; the `last_validated` and `completeness_score`
  fields in `query_summary` make freshness measurable.

## 📘 Access
- **Backend**: Start the Flask server locally — `export FLASK_APP=app.py` then
  `flask --app app.py run -p 5002`.
- **Public exposure**: Run `ngrok http http://localhost:5002` to publish a
  `https://<id>.ngrok-free.app` URL.
- **Endpoint**: `GET /businesses/search?term={term}&location={location}&radius={meters}`
  returns the normalized JSON document described in the Structure section.
- **Single record**: `GET /businesses/{id}` returns the same record shape for one
  Yelp business ID.
- **Authentication**: Public endpoints require no key; restricted fields (`contact`
  when classified as private, ownership details) require an `Authorization: Bearer
  <token>` header.
- **Client usage (Python)**:
  ```python
  import requests
  r = requests.get(
      "https://<ngrok-id>.ngrok-free.app/businesses/search",
      params={"term": "bakery", "location": "Seattle, WA", "radius": 5000},
  )
  print(r.json())
  ```
- **Errors**: standard HTTP codes — `200` success, `400` bad query, `401`
  unauthorized for restricted fields, `429` if Yelp rate limits are exceeded.

## 📘 Structure
Each response is a single JSON object with the following top-level fields:

| Field | Type | Description |
|---|---|---|
| `schema_version` | string | Internal schema version (e.g. `"1.0"`) |
| `data_classification` | string | `"public"` or `"restricted"` |
| `provenance` | object | Source, endpoint, query params, retrieval time, license |
| `query_summary` | object | Total available, returned count, `quality_summary` block |
| `businesses` | array | Array of business records |

Each `businesses[]` record:

| Field | Type | Description |
|---|---|---|
| `id` | string | Yelp business identifier |
| `name` | string | Business name |
| `yelp_url` | string | Link back to Yelp listing |
| `is_closed` | boolean | Whether the business is permanently closed |
| `categories` | array<string> | Schema.org-aligned category slugs |
| `rating` | number | 0.0–5.0 star rating |
| `review_count` | integer | Number of Yelp reviews |
| `price_tier` | integer\|null | 1–4 |
| `price_symbol` | string\|null | `$`–`$$$$` |
| `transactions` | array<string> | e.g. `"delivery"`, `"pickup"` |
| `location` | object | Address fields + `coordinates {latitude, longitude}` |
| `contact` | object | `phone_e164`, `data_classification` |
| `distance_from_query` | object | `{value, unit}` |
| `quality_flags` | object | Per-record completeness booleans + `is_complete` |

## 📘 Example

### Example Request
```
GET /businesses/search?term=bakery&location=Seattle,%20WA&radius=5000
Host: <ngrok-id>.ngrok-free.app
```

### Example Response (truncated)
```json
{
  "schema_version": "1.0",
  "data_classification": "public",
  "provenance": {
    "source": "Yelp Fusion API",
    "endpoint": "GET /v3/businesses/search",
    "query_params": {"term": "bakery", "location": "Seattle, WA", "radius_meters": 5000},
    "retrieved_at": "2026-05-19T18:00:00Z",
    "license": "Yelp Fusion API Terms of Use - display only, no redistribution",
    "api_key_owner": "team-sbp-project"
  },
  "query_summary": {
    "total_results_available": 847,
    "records_in_this_batch": 1,
    "quality_summary": {
      "records_complete": 0,
      "records_missing_price": 0,
      "records_missing_phone": 0,
      "completeness_score": 0.88,
      "last_validated": "2026-05-19T18:00:05Z"
    }
  },
  "businesses": [
    {
      "id": "gR3PmD2MXVoyoQUNu6BULA",
      "name": "Pat's Bakery",
      "yelp_url": "https://www.yelp.com/biz/pats-bakery-seattle",
      "is_closed": false,
      "categories": ["bakeries", "coffee"],
      "rating": 4.5,
      "review_count": 214,
      "price_tier": 2,
      "price_symbol": "$$",
      "transactions": ["delivery", "pickup"],
      "location": {
        "address_line_1": "1420 Pike St",
        "address_line_2": null,
        "city": "Seattle",
        "state": "WA",
        "zip_code": "98101",
        "country_code": "US",
        "coordinates": {"latitude": 47.6062, "longitude": -122.3321}
      },
      "contact": {"phone_e164": "+12065550192", "data_classification": "public"},
      "distance_from_query": {"value": 342.7, "unit": "meters"},
      "quality_flags": {
        "has_name": true, "has_rating": true, "has_price_tier": true,
        "has_address": true, "has_phone": true, "has_categories": true,
        "address_line_2_missing": true, "is_complete": false
      }
    }
  ]
}
```
