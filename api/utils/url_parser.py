from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import re
from urllib.parse import urlparse
from flask import current_app


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
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }

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
        
        # Use Playwright to load and parse the page
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent=headers['User-Agent'])
            page = context.new_page()
            try:
                page.goto(url, wait_until='domcontentloaded', timeout=15000)
                try:
                    page.wait_for_load_state('networkidle', timeout=15000)
                except PlaywrightTimeoutError:
                    pass

                # Site-specific parsing logic
                if 'digikala' in domain:
                    result = _parse_digikala(page)
                elif 'amazon' in domain:
                    result = _parse_amazon(page)
                elif 'torob' in domain:
                    result = _parse_torob(page)
                else:
                    # Generic parsing for unknown sites
                    result = _parse_generic(page)
            finally:
                context.close()
                browser.close()

        # Add URL to result
        result['link'] = url
        
        return result
        
    except Exception as e:
        raise Exception(f"Failed to parse URL: {str(e)}")

def _parse_digikala(page):
    """Parse Digikala product page"""
    result = {}
    try:
        brand_text = _safe_inner_text(page, 'a[data-cro-id="pdp-breadcrumb-down"]')
        if brand_text:
            result['brand'] = brand_text.strip()

        title_text = _safe_inner_text(page, 'h1[data-testid="pdp-title"]')
        if title_text:
            result['model_name'] = title_text.strip()

        price_text = _safe_inner_text(page, 'div[data-testid="buy-box"] span[data-testid="price-final"]')
        if not price_text:
            price_text = _safe_inner_text(page, 'div[data-testid="buy-box"] span[data-testid="price-no-discount"]')
        price_text = int(persian_to_english_numerals(price_text).replace(",", ""))
        if price_text:
            result['price'] = price_text
    except Exception as ex:
        current_app.logger.warning(f"Digikala parsing warning: {ex}")

    # Set store
    result['store'] = 'Digikala'
    
    return result

def _parse_amazon(page):
    """Parse Amazon product page"""
    result = {}
    try:
        brand_text = _safe_inner_text(page, '#bylineInfo')
        if brand_text:
            result['brand'] = brand_text.replace('Visit the', '').replace('Store', '').strip()

        title_text = _safe_inner_text(page, '#productTitle')
        if title_text:
            result['model_name'] = title_text.strip()

        price_text = _safe_inner_text(page, 'span.a-price-whole')
        if price_text:
            cleaned = price_text.replace(',', '').strip()
            try:
                result['price'] = float(cleaned)
            except ValueError:
                pass
    except Exception as ex:
        current_app.logger.warning(f"Amazon parsing warning: {ex}")

    # Set store
    result['store'] = 'Amazon'
    
    return result

def _parse_torob(page):
    """Parse Torob product page"""
    result = {}
    try:
        brand_text = _safe_inner_text(page, 'div.product-brand')
        if brand_text:
            result['brand'] = brand_text.strip()

        title_text = _safe_inner_text(page, 'div.Showcase_name__hrttI')
        if title_text:
            result['model_name'] = title_text.strip()

        # container = page.locator('div#cheapest-seller')
        # first_child = container.locator("div").first
        # target = first_child.locator("div[class*='Showcase_buy_box_text__']").last
        # price_text = _safe_inner_text(target)
        price_text = _safe_inner_text(page,"div#cheapest-seller >> div >> nth=0 >> div[class*='Showcase_buy_box_text__'] >> nth=-1")

        price_text = price_text.replace("تومان","")
        price_text = int(persian_to_english_numerals(price_text).replace("٫", ""))
        if price_text:
            result['price'] = price_text
    except Exception as ex:
        current_app.logger.warning(f"Torob parsing warning: {ex}")

    # Set store
    result['store'] = 'Torob'
    
    return result

def _parse_generic(page):
    """Generic parsing for unknown sites"""
    result = {}
    try:
        # Try to extract title via document.title, fallback to first h1
        try:
            title = page.title()
        except Exception:
            title = None
        if not title:
            title = _safe_inner_text(page, 'h1')
        if title:
            result['model_name'] = title.strip()

        # Try to extract price from common price patterns by scanning text content
        body_text = _safe_inner_text(page, 'body') or ''
        price_patterns = [
            re.compile(r'price[^\d]*([\d,.]+)', re.IGNORECASE),
            re.compile(r'([\d]{1,3}(?:,[\d]{3})+(?:\.[\d]+)?)'),
            re.compile(r'(\d+\.?\d*)')
        ]
        for pattern in price_patterns:
            match = pattern.search(body_text)
            if match and match.group(1):
                numeric = match.group(1).replace(',', '')
                try:
                    result['price'] = float(numeric)
                    break
                except ValueError:
                    continue
    except Exception as ex:
        current_app.logger.warning(f"Generic parsing warning: {ex}")
    
    return result

def _safe_inner_text(page, selector):
    try:
        locator = page.locator(selector).first
        if locator and locator.count() > 0:
            return locator.inner_text(timeout=2000)
        return None
    except Exception:
        return None
    
def persian_to_english_numerals(persian_number_str):
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    english_digits = '0123456789'
    translation_table = str.maketrans(persian_digits, english_digits)
    return persian_number_str.translate(translation_table)
