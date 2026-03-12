# Innomatics_Research_labs_Internship_FastApi

### ✅ FastAPI Assignment 1: Day 1 Practice Tasks (Date: 05-03-2026)
**Folder:** `IN226026002_FASTAPI/ASSIGNMENT 1/`
**File:** `main.py`

**Description:** Built a local FastAPI web server with multiple GET endpoints to manage an e-commerce product catalog. Tested and documented all API endpoints using Swagger UI.
* **Q1: Product Catalog Update:** Added new items to the inventory and returned the updated list.
* **Q2: Category Filter Endpoint:** Created dynamic routing (`/products/category/{category_name}`) to filter items.
* **Q3: In-Stock Filter:** Implemented conditional logic to return only currently available products.
* **Q4: Store Info Summary:** Aggregated data to return total counts, stock metrics, and a set of unique categories.
* **Q5: Search Products by Name:** Built a case-insensitive search endpoint to find products by keyword.
* **Bonus: Deals Endpoint:** Utilized Python's `min()` and `max()` with lambda functions to identify the cheapest and most expensive products.


### ✅ FastAPI Assignment 2: Pydantic Validation & POST Methods (Date: 10-03-2026)
**Folder:** `IN226026002_FASTAPI/ASSIGNMENT 2/`
**File:** `main.py`

**Description:** Expanded the Day 1 FastAPI application by implementing POST requests, Query parameters, and robust data validation using Pydantic models.
* **Q1: Query Parameters:** Added a `min_price` query filter to the existing `/products/filter` endpoint.
* **Q2: Path Parameters:** Built a lightweight endpoint (`/products/{product_id}/price`) to return only specific product data.
* **Q3: Pydantic Validation:** Created a `CustomerFeedback` model to validate incoming POST data, ensuring ratings remain between 1-5.
* **Q4: Business Logic Dashboard:** Implemented a `/products/summary` endpoint utilizing `min()`, `max()`, and sets to aggregate metrics.
* **Q5: Bulk Order System:** Designed complex logic using `BulkOrder` and `OrderItem` models to process arrays of data, validate stock, and return segregated pass/fail lists.
* **Bonus: Order State Management:** Implemented a multi-step order tracker using `PATCH` endpoints to transition order statuses from "pending" to "confirmed".


  
