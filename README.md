# Carbon38- scraper

##  Project Overview

This project utilizes the **Scrapy** framework to extract structured product data from the [Carbon38](https://www.carbon38.com) e-commerce website. The spider specifically targets the *Activewear Tops* collection to gather relevant product details efficiently.

---

##  Extracted Fields

- **Product Name**
- **Price**
- **Product URL**

---

##  Files Included

 - `carbon38_submission.zip` – Compressed project folder for submission
- `settings.py` – Configuration file for Scrapy settings
- `products.csv` – Output data in CSV format
- `products.json` – Output data in JSON format
- `carbon_spider.py` – Contains the Scrapy spider implementation

---

##  How to Run the Spider

Ensure your environment is set up with Scrapy, then run the following command in the project directory:

```bash
scrapy crawl carbon
