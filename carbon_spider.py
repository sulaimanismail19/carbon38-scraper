import scrapy
import re


class CarbonSpider(scrapy.Spider):
    name = "carbon_spider"
    allowed_domains = ["carbon38.com"]
    start_urls = [
        "https://carbon38.com/en-in/collections/tops",
        "https://carbon38.com/en-in/collections/leggings",
        "https://carbon38.com/en-in/collections/bras",
        "https://carbon38.com/en-in/collections/pants",
        "https://carbon38.com/en-in/collections/jackets",
        "https://carbon38.com/en-in/collections/jumpsuits-rompers",
        "https://carbon38.com/en-in/collections/outerwear",
        "https://carbon38.com/en-in/collections/shorts",
        "https://carbon38.com/en-in/collections/new-arrivals",
        "https://carbon38.com/en-in/collections/all"
    ]

    def parse(self, response):
        product_links = response.css('a.ProductItem__ImageWrapper::attr(href)').getall()
        for link in product_links:
            yield response.follow(link, callback=self.parse_product)

        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        brand = "CARBON38"
        product_name = (response.xpath('//h1/text()').get() or "").strip()

        # Updated price extraction (more robust)
        price = (
            response.css('span.Price, span.price, span.product__price::text')
            .re_first(r"[\$\₹RS\.]*\s*\d+[\,\d]*")
            or response.xpath('//*[contains(text(), "$") or contains(text(), "₹")]/text()')
            .re_first(r"[\$\₹RS\.]*\s*\d+[\,\d]*")
            or ""
        ).strip()

        # Optional: Debug print
        # raw_prices = response.xpath('//text()').re(r"[\$\₹RS\.]*\s*\d+[\,\d]*")
        # print("PRICE CANDIDATES:", raw_prices)

        reviews = next(
            (
                t.strip()
                for t in response.xpath('//body//*[not(self::script or self::style)]/text()').getall()
                if "review" in t.lower() and any(char.isdigit() for char in t)
            ),
            "No Reviews",
        )

        colour = (
            response.xpath('//span[contains(@class, "swatch-selected") or contains(@class, "selected-color")]/text()')
            .get() or ""
        ).strip()

        sizes = response.xpath('//fieldset[contains(@class, "product-form__input")]/label/text()').getall()
        sizes = [s.strip() for s in sizes if s.strip()]

        description = response.xpath('//div[contains(@class, "product__description")]//text()').getall()
        description = " ".join([d.strip() for d in description if d.strip()])

        sku = response.xpath('//*[contains(text(), "SKU")]/text()').re_first(r"SKU[:\s]+([A-Z0-9\-]+)")

        product_id = re.search(r'"product_id":"(\d+)"', response.text)
        product_id = product_id.group(1) if product_id else ""

        image_urls = response.xpath('//img[contains(@src, "/cdn/shop/files")]/@src').getall()
        image_urls = [response.urljoin(url) for url in image_urls]
        primary_image_url = image_urls[0] if image_urls else ""

        breadcrumbs = ["Home", "Designers", brand, product_name]

        yield {
            "breadcrumbs": breadcrumbs,
            "primary_image_url": primary_image_url,
            "brand": brand,
            "product_name": product_name,
            "price": price,
            "reviews": reviews,
            "colour": colour,
            "sizes": sizes,
            "description": description,
            "sku": sku,
            "product_id": product_id,
            "product_url": response.url,
            "image_urls": image_urls,
        }
