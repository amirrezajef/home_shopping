# URL Parsing Feature Implementation Plan

## Overview

This document outlines the implementation plan for adding URL parsing functionality to automatically extract product information when adding new options.

## Backend Implementation

### 1. URL Parser Utility

Create a new utility function in `api/utils/url_parser.py` that can parse product information from popular e-commerce sites:

```python
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

def parse_product_url(url):
    """
    Parse product information from a URL

    Args:
        url (str): The product URL to parse

    Returns:
        dict: Parsed product information
    """
    try:
        # Validate URL format
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Invalid URL format")

        # Make request to get page content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Initialize result dictionary
        result = {
            'brand': None,
            'model_name': None,
            'price': None,
            'store': None,
            'features': None,
            'rating': None,
            'warranty_months': None
        }

        # Extract domain for site-specific parsing
        domain = parsed_url.netloc.lower()

        # Site-specific parsing logic
        if 'digikala' in domain:
            result = _parse_digikala(soup)
        elif 'amazon' in domain:
            result = _parse_amazon(soup)
        elif 'torob' in domain:
            result = _parse_torob(soup)
        else:
            # Generic parsing for unknown sites
            result = _parse_generic(soup)

        # Add URL to result
        result['link'] = url

        return result

    except Exception as e:
        raise Exception(f"Failed to parse URL: {str(e)}")

def _parse_digikala(soup):
    """Parse Digikala product page"""
    result = {}

    # Extract brand
    brand_elem = soup.find('span', {'class': 'product-brand-title'})
    if brand_elem:
        result['brand'] = brand_elem.get_text().strip()

    # Extract model name
    title_elem = soup.find('h1', {'class': 'product-title'})
    if title_elem:
        result['model_name'] = title_elem.get_text().strip()

    # Extract price
    price_elem = soup.find('div', {'class': 'product-price'})
    if price_elem:
        price_text = price_elem.get_text()
        # Extract numeric value from price text
        price_match = re.search(r'[\d,]+', price_text)
        if price_match:
            result['price'] = float(price_match.group().replace(',', ''))

    # Set store
    result['store'] = 'Digikala'

    return result

def _parse_amazon(soup):
    """Parse Amazon product page"""
    result = {}

    # Extract brand
    brand_elem = soup.find('a', {'id': 'bylineInfo'})
    if brand_elem:
        result['brand'] = brand_elem.get_text().replace('Visit the', '').replace('Store', '').strip()

    # Extract model name
    title_elem = soup.find('span', {'id': 'productTitle'})
    if title_elem:
        result['model_name'] = title_elem.get_text().strip()

    # Extract price
    price_elem = soup.find('span', {'class': 'a-price-whole'})
    if price_elem:
        price_text = price_elem.get_text()
        result['price'] = float(price_text.replace(',', ''))

    # Set store
    result['store'] = 'Amazon'

    return result

def _parse_torob(soup):
    """Parse Torob product page"""
    result = {}

    # Extract brand
    brand_elem = soup.find('div', {'class': 'product-brand'})
    if brand_elem:
        result['brand'] = brand_elem.get_text().strip()

    # Extract model name
    title_elem = soup.find('h1', {'class': 'product-title'})
    if title_elem:
        result['model_name'] = title_elem.get_text().strip()

    # Extract price
    price_elem = soup.find('div', {'class': 'price'})
    if price_elem:
        price_text = price_elem.get_text()
        # Extract numeric value from price text
        price_match = re.search(r'[\d,]+', price_text)
        if price_match:
            result['price'] = float(price_match.group().replace(',', ''))

    # Set store
    result['store'] = 'Torob'

    return result

def _parse_generic(soup):
    """Generic parsing for unknown sites"""
    result = {}

    # Try to extract title
    title_elem = soup.find('title') or soup.find('h1')
    if title_elem:
        result['model_name'] = title_elem.get_text().strip()

    # Try to extract price from common price patterns
    price_patterns = [
        re.compile(r'price.*?([\d,]+\.?\d*)', re.IGNORECASE),
        re.compile(r'[\d,]+\.?\d*', re.IGNORECASE)
    ]

    for pattern in price_patterns:
        price_elem = soup.find(string=pattern)
        if price_elem:
            price_match = pattern.search(price_elem)
            if price_match:
                try:
                    result['price'] = float(price_match.group(1).replace(',', ''))
                    break
                except:
                    continue

    return result
```

### 2. New API Endpoint

Add a new endpoint to `api/routes/options.py`:

```python
@options_bp.route('/options/parse-url', methods=['POST'])
def parse_option_url():
    """
    Parse product information from a URL

    Expected JSON input:
    {
        "url": "https://example.com/product"
    }

    Returns:
    {
        "success": true,
        "data": {
            "brand": "Example Brand",
            "model_name": "Example Model",
            "price": 123456.0,
            "store": "Example Store",
            "link": "https://example.com/product",
            ...
        }
    }
    """
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({"message": "URL الزامی است.", "success": False}), 400

        # Parse URL to extract product information
        parsed_data = parse_product_url(url)

        return jsonify({
            "message": "اطلاعات محصول با موفقیت استخراج شد.",
            "success": True,
            "data": parsed_data
        }), 200

    except Exception as e:
        return jsonify({"message": f"خطا در تجزیه URL: {str(e)}", "success": False}), 500
```

## Frontend Implementation

### 1. Add URL Input Field

Modify the option form in `frontend/src/components/ItemDetail.jsx` to include a URL input field:

```jsx
// Add to the form fields
<div className="space-y-2">
    <Label htmlFor="url">لینک محصول</Label>
    <div className="flex gap-2">
        <Input
            id="url"
            name="url"
            type="url"
            value={optionFormData.url || ""}
            onChange={handleOptionInputChange}
            placeholder="https://example.com/product"
        />
        <Button type="button" onClick={handleParseUrl} disabled={!optionFormData.url || parsingUrl}>
            {parsingUrl ? "در حال تجزیه..." : "تجزیه"}
        </Button>
    </div>
</div>
```

### 2. Add Parsing Function

Add a new function to handle URL parsing:

```jsx
const [parsingUrl, setParsingUrl] = useState(false);

const handleParseUrl = async () => {
    if (!optionFormData.url) {
        setError("لطفاً یک URL وارد کنید");
        return;
    }

    setParsingUrl(true);
    setError(null);

    try {
        const response = await axios.post("/api/options/parse-url", {
            url: optionFormData.url,
        });

        if (response.data.success) {
            // Update form data with parsed information
            setOptionFormData((prev) => ({
                ...prev,
                ...response.data.data,
            }));
        } else {
            setError(response.data.message || "خطا در تجزیه URL");
        }
    } catch (err) {
        setError(err.response?.data?.message || "خطا در تجزیه URL");
        console.error("URL parsing error:", err);
    } finally {
        setParsingUrl(false);
    }
};
```

## Error Handling

### 1. Network Errors

Handle network timeouts and connection errors gracefully.

### 2. Invalid URLs

Validate URL format before attempting to parse.

### 3. Parsing Failures

Provide meaningful error messages when parsing fails.

## Testing

### 1. Test with Sample URLs

Test the implementation with URLs from popular e-commerce sites:

-   Digikala product pages
-   Amazon product pages
-   Torob product pages
-   Generic e-commerce sites

### 2. Edge Cases

Test with:

-   Invalid URLs
-   Pages with missing information
-   Pages with dynamic content
-   Pages that require authentication

## Security Considerations

### 1. Rate Limiting

Implement rate limiting on the parsing endpoint to prevent abuse.

### 2. Input Validation

Validate all input data before processing.

### 3. User-Agent Headers

Use appropriate User-Agent headers when making requests to avoid being blocked.
