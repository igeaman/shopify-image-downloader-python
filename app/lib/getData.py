# app/lib/getData.py
from typing import Dict, Any, List
from urllib.parse import urlparse, urlunparse

from app.schemas import URI, requestResponse
import requests

def fetch_url(url: URI) -> Dict[str, Any]:
    """Fetch Shopify product JSON for a given product URL base."""
    # code to remove any parameters
    parsed = urlparse(url.URL)
# Rebuild URL without query and fragment
    base_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))

    url_str = f"{base_url}.json"                 # use attribute access on the model
    resp = requests.get(url_str, timeout=15)
    resp.raise_for_status()
    return resp.json()

def Data(url: URI) -> requestResponse:
    """Return a requestResponse (Images, description, title) composed from Shopify JSON."""
    data = fetch_url(url)

    product = data.get("product", {})
    title: str = product.get("title", "")
    description: str = product.get("body_html", "")

    # Build list[URI] from image 'src' values
    images: List[URI] = [
        URI(URL=img["src"])
        for img in product.get("images", [])
        if isinstance(img, dict) and "src" in img
    ]

    return requestResponse(
        Images=images,           # note capital I to match your schema
        description=description,
        title=title,
    )
