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


  
### ✅ FastAPI Assignment 3: Full CRUD Operations (Date: 12-03-2026)
**Folder:** `IN226026002_FASTAPI/ASSIGNMENT 3/`
**File:** `main.py`

**Description:** Built out a complete CRUD (Create, Read, Update, Delete) lifecycle for an e-commerce inventory system, emphasizing proper HTTP status codes and route hierarchy.
* **Q1: POST Operations:** Implemented product creation with auto-incrementing IDs and 400 Bad Request error handling for duplicate entries.
* **Q2: PUT Operations (Single):** Designed a partial-update endpoint utilizing `Optional` typing to allow independent field updates (price and stock status).
* **Q3: DELETE Operations:** Created secure deletion logic that successfully removes items or returns a 404 Not Found error if the ID does not exist.
* **Q4: Full CRUD Lifecycle:** Successfully navigated a complete testing workflow (Add -> Verify -> Update -> Verify -> Delete -> Verify) using Swagger UI.
* **Q5: Fixed Route Priority:** Built a `GET /products/audit` dashboard, properly routing it above dynamic ID paths to prevent URL conflicts, calculating total stock values and top-tier items.
* **Bonus: PUT Operations (Bulk):** Engineered a multi-item update endpoint utilizing query parameters to apply mathematical percentage discounts across specific target categories.


### ✅ FastAPI Assignment 4: State Management & Cart System (Date: 15-03-2026)
**Folder:** `IN226026002_FASTAPI/ASSIGNMENT 4/`
**File:** `main.py`

**Description:** Designed a fully integrated Shopping Cart and Order Management system testing state retention across multiple endpoints.
* **Q1: Add to Cart Logic:** Implemented a `/cart/add` endpoint to populate an in-memory cart array with dynamic subtotals.
* **Q2: Cart Overview:** Built a `/cart` viewer that calculates real-time `grand_total` and item counts.
* **Q3: Inventory Validation:** Added strict stock-checking logic that rejects out-of-stock items returning an HTTP 400 Bad Request.
* **Q4: Duplicate Item Handling:** Engineered loop detection to update existing cart quantities rather than creating duplicate product entries.
* **Q5: Checkout Workflow:** Connected `DELETE` endpoints for cart manipulation with a structured `/cart/checkout` endpoint that empties the user's session cart and transfers data to a persistent `/orders` log.
* **Q6: Multi-Session Testing:** Verified the cart integrity handling consecutive checkout lifecycles for multiple users.
* **Bonus: Graceful Error Handling:** Implemented edge-case protection to block checkout requests when the cart is empty.
