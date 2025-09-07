# Shopify Image Downloader — Python (FastAPI)

A minimal FastAPI backend that fetches Shopify product data and returns:
- Product title
- Product HTML description
- All product images (as URLs)

It expects a Shopify product URL (without the `.json` suffix), calls `<URL>.json`, and structures the response for easy consumption by a frontend or CLI.

## Features
- FastAPI service with CORS enabled
- Health endpoints: `/health` and `/shopify/`
- POST `/shopify/` to fetch product data from `<URL>.json`
- Rotating file logs in `app.log`
- Built‑in OpenAPI docs at `/docs` and `/redoc`

## Project Structure
- `app/main.py`: FastAPI app factory, CORS, logging, router includes
- `app/routers/shopify.py`: `/shopify` routes (health + fetch)
- `app/lib/getData.py`: Data fetch/transform from Shopify JSON
- `app/schemas.py`: Pydantic models for request/response
- `app.log`: Rotating log file output

## Requirements
- Python 3.10+
- Packages: `fastapi`, `uvicorn[standard]`, `requests`

Example `requirements.txt` (optional):
```
fastapi
uvicorn[standard]
requests
```

## Quick Start
1) Create and activate a virtual environment
```
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

2) Install dependencies
```
pip install -r requirements.txt
# or
pip install fastapi uvicorn[standard] requests
```

3) Run the server
```
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4) Open the docs
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API

### Health
- `GET /health` → `{ "status": "ok" }`
- `GET /shopify/` → `{ "status": "ok" }`

### Fetch Product Data
- `POST /shopify/`
- Request body schema:
```
{
  "URL": "https://<store>.myshopify.com/products/<handle>"
}
```
- Response body schema:
```
{
  "Images": [ { "URL": "<image_url>" }, ... ],
  "description": "<body_html>",
  "title": "<product_title>"
}
```

#### cURL example
```
curl -X POST http://localhost:8000/shopify/ \
  -H 'Content-Type: application/json' \
  -d '{
        "URL": "https://examplestore.myshopify.com/products/example-product"
      }'
```

#### Python example
```
import requests

payload = {
    "URL": "https://examplestore.myshopify.com/products/example-product"
}
r = requests.post("http://localhost:8000/shopify/", json=payload, timeout=15)
r.raise_for_status()
print(r.json())
```

## Behavior Details
- The service appends `.json` to the provided `URL` and performs an HTTP GET.
- It extracts `product.title`, `product.body_html`, and all `product.images[*].src` values.
- Image URLs are returned as a list of `{ "URL": "..." }` items to match the Pydantic schema.
- CORS allows all origins by default; adjust in `app/main.py` if needed.
- Logs write to `app.log` with daily rotation (7 backups).

## Notes and Limitations
- Some Shopify stores restrict access to product JSON; you may receive 403/404 from `<URL>.json`.
- Provide the canonical product URL (e.g., `https://<store>.myshopify.com/products/<handle>`). Do not include `.json`—the server adds it.
- Network timeouts and HTTP errors are surfaced as `400` responses with details.

## Development
- Run with `--reload` for auto-reload during development.
- Type hints are included throughout the service for clarity.

## License
This project’s license is not specified. If you intend to publish or share, consider adding a license file.
