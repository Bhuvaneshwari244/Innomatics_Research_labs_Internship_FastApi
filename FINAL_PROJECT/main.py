from fastapi import FastAPI, Query, HTTPException, status, Response
from pydantic import BaseModel, Field
from typing import Optional, List
import math

app = FastAPI(title="FastAPI Final Project — QuickBite Food Delivery")

# ==========================================
# INITIAL DATA (Q2, Q4, Q14)
# ==========================================
menu = [
    {"id": 1, "name": "Margherita Pizza", "price": 299, "category": "Pizza", "is_available": True},
    {"id": 2, "name": "Cheese Burger", "price": 149, "category": "Burger", "is_available": True},
    {"id": 3, "name": "Coke", "price": 60, "category": "Drink", "is_available": True},
    {"id": 4, "name": "Chocolate Lava Cake", "price": 120, "category": "Dessert", "is_available": False},
    {"id": 5, "name": "Veggie Supreme Pizza", "price": 349, "category": "Pizza", "is_available": True},
    {"id": 6, "name": "Iced Tea", "price": 80, "category": "Drink", "is_available": True}
]

orders = []
order_counter = 1
cart = []

# ==========================================
# PYDANTIC MODELS (Q6, Q9, Q11, Q15)
# ==========================================
class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=20)
    delivery_address: str = Field(..., min_length=10)
    order_type: str = Field(default='delivery') # Q9 addition

class NewMenuItem(BaseModel):
    name: str = Field(..., min_length=2)
    price: int = Field(..., gt=0)
    category: str = Field(..., min_length=2)
    is_available: bool = True

class CheckoutRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    delivery_address: str = Field(..., min_length=10)

# ==========================================
# HELPER FUNCTIONS (Q7, Q9, Q10)
# ==========================================
def find_menu_item(item_id: int):
    return next((item for item in menu if item['id'] == item_id), None)

def calculate_bill(price: int, quantity: int, order_type: str = 'delivery'):
    base_total = price * quantity
    delivery_charge = 30 if order_type.lower() == 'delivery' else 0
    return base_total + delivery_charge

def filter_menu_logic(category: Optional[str] = None, max_price: Optional[int] = None, is_available: Optional[bool] = None):
    results = menu
    if category is not None:
        results = [i for i in results if i['category'].lower() == category.lower()]
    if max_price is not None:
        results = [i for i in results if i['price'] <= max_price]
    if is_available is not None:
        results = [i for i in results if i['is_available'] == is_available]
    return results

# ==========================================
# FIXED ROUTES (Must be above variable routes!)
# ==========================================

# --- Q1: Welcome Route ---
@app.get('/')
def home():
    return {'message': 'Welcome to QuickBite Food Delivery'}

# --- Q2: Get Menu ---
@app.get('/menu')
def get_menu():
    return {"menu": menu, "total": len(menu)}

# --- Q11: Add Menu Item ---
@app.post('/menu', status_code=status.HTTP_201_CREATED)
def add_menu_item(item: NewMenuItem, response: Response):
    if any(i['name'].lower() == item.name.lower() for i in menu):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Item with this name already exists"}
    
    new_id = max((i['id'] for i in menu), default=0) + 1
    new_item = {"id": new_id, "name": item.name, "price": item.price, "category": item.category, "is_available": item.is_available}
    menu.append(new_item)
    return new_item

# --- Q5: Menu Summary ---
@app.get('/menu/summary')
def get_summary():
    available = [i for i in menu if i['is_available']]
    categories = list(set(i['category'] for i in menu))
    return {
        "total_items": len(menu),
        "available_count": len(available),
        "unavailable_count": len(menu) - len(available),
        "categories": categories
    }

# --- Q10: Filter Menu ---
@app.get('/menu/filter')
def filter_menu(category: Optional[str] = None, max_price: Optional[int] = None, is_available: Optional[bool] = None):
    filtered = filter_menu_logic(category, max_price, is_available)
    return {"total_found": len(filtered), "items": filtered}

# --- Q16: Search Menu ---
@app.get('/menu/search')
def search_menu(keyword: str = Query(...)):
    results = [i for i in menu if keyword.lower() in i['name'].lower() or keyword.lower() in i['category'].lower()]
    if not results:
        return {"message": f"No items found matching '{keyword}'"}
    return {"total_found": len(results), "items": results}

# --- Q17: Sort Menu ---
@app.get('/menu/sort')
def sort_menu(sort_by: str = Query('price'), order: str = Query('asc')):
    if sort_by not in ['price', 'name', 'category']:
        return {"error": "Invalid sort_by parameter"}
    if order not in ['asc', 'desc']:
        return {"error": "Invalid order parameter"}
    
    results = sorted(menu, key=lambda x: x[sort_by], reverse=(order == 'desc'))
    return {"sort_settings": {"sort_by": sort_by, "order": order}, "items": results}

# --- Q18: Paginate Menu ---
@app.get('/menu/page')
def paginate_menu(page: int = Query(1, ge=1), limit: int = Query(3, ge=1, le=10)):
    start = (page - 1) * limit
    sliced_menu = menu[start : start + limit]
    return {
        "page": page,
        "limit": limit,
        "total": len(menu),
        "total_pages": math.ceil(len(menu) / limit),
        "items": sliced_menu
    }

# --- Q20: The Master Browse Route ---
@app.get('/menu/browse')
def browse_menu(
    keyword: Optional[str] = Query(None),
    sort_by: str = Query('price'),
    order: str = Query('asc'),
    page: int = Query(1, ge=1),
    limit: int = Query(4, ge=1)
):
    results = menu
    
    # 1. Filter
    if keyword:
        results = [i for i in results if keyword.lower() in i['name'].lower() or keyword.lower() in i['category'].lower()]
        
    # 2. Sort
    if sort_by in ['price', 'name', 'category']:
        results = sorted(results, key=lambda x: x[sort_by], reverse=(order == 'desc'))
        
    # 3. Paginate
    total = len(results)
    start = (page - 1) * limit
    paged = results[start : start + limit]
    
    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "total_found": total,
        "total_pages": math.ceil(total / limit) if limit > 0 else 0,
        "items": paged
    }


# ==========================================
# VARIABLE ID ROUTES (Menu)
# ==========================================

# --- Q3: Get Item by ID ---
@app.get('/menu/{item_id}')
def get_item(item_id: int):
    item = find_menu_item(item_id)
    if not item:
        return {"error": "Item not found"}
    return item

# --- Q12: Update Menu Item ---
@app.put('/menu/{item_id}')
def update_item(item_id: int, response: Response, price: Optional[int] = None, is_available: Optional[bool] = None):
    item = find_menu_item(item_id)
    if not item:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Item not found"}
    
    if price is not None: item['price'] = price
    if is_available is not None: item['is_available'] = is_available
    return {"message": "Item updated", "item": item}

# --- Q13: Delete Menu Item ---
@app.delete('/menu/{item_id}')
def delete_item(item_id: int, response: Response):
    item = find_menu_item(item_id)
    if not item:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Item not found"}
    
    menu.remove(item)
    return {"message": f"Success! {item['name']} was removed from the menu."}


# ==========================================
# ORDERS AND CART ROUTES
# ==========================================

# --- Q4: Get All Orders ---
@app.get('/orders')
def get_orders():
    return {"orders": orders, "total_orders": len(orders)}

# --- Q19: Search & Sort Orders (Fixed routes above POST) ---
@app.get('/orders/search')
def search_orders(customer_name: str = Query(...)):
    results = [o for o in orders if customer_name.lower() in o['customer_name'].lower()]
    return {"total_found": len(results), "orders": results}

@app.get('/orders/sort')
def sort_orders(order: str = Query('asc')):
    results = sorted(orders, key=lambda x: x['total_bill'], reverse=(order == 'desc'))
    return {"orders": results}

# --- Q8, Q9: Place an Order ---
@app.post('/orders')
def place_order(req: OrderRequest, response: Response):
    global order_counter
    item = find_menu_item(req.item_id)
    
    if not item:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Item not found"}
    if not item['is_available']:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Item is currently unavailable"}
        
    total_bill = calculate_bill(item['price'], req.quantity, req.order_type)
    
    new_order = {
        "order_id": order_counter,
        "customer_name": req.customer_name,
        "item": item['name'],
        "quantity": req.quantity,
        "order_type": req.order_type,
        "total_bill": total_bill,
        "delivery_address": req.delivery_address,
        "status": "confirmed"
    }
    
    orders.append(new_order)
    order_counter += 1
    return new_order

# --- Q14: Add to Cart ---
@app.post('/cart/add')
def add_to_cart(item_id: int, quantity: int = 1):
    item = find_menu_item(item_id)
    if not item or not item['is_available']:
        return {"error": "Item unavailable or not found"}
        
    for c_item in cart:
        if c_item['item_id'] == item_id:
            c_item['quantity'] += quantity
            c_item['subtotal'] = c_item['quantity'] * item['price']
            return {"message": "Cart updated", "cart": cart}
            
    cart.append({
        "item_id": item_id,
        "name": item['name'],
        "price": item['price'],
        "quantity": quantity,
        "subtotal": item['price'] * quantity
    })
    return {"message": "Added to cart", "cart": cart}

# --- Q14: View Cart ---
@app.get('/cart')
def view_cart():
    grand_total = sum(i['subtotal'] for i in cart)
    return {"cart": cart, "grand_total": grand_total}

# --- Q15: Remove from Cart ---
@app.delete('/cart/{item_id}')
def remove_from_cart(item_id: int, response: Response):
    for i, item in enumerate(cart):
        if item['item_id'] == item_id:
            cart.pop(i)
            return {"message": "Item removed from cart"}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error": "Item not in cart"}

# --- Q15: Checkout Flow ---
@app.post('/cart/checkout', status_code=status.HTTP_201_CREATED)
def checkout(req: CheckoutRequest, response: Response):
    global order_counter
    if not cart:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Cart is empty"}
        
    grand_total = sum(i['subtotal'] for i in cart)
    session_orders = []
    
    for item in cart:
        new_order = {
            "order_id": order_counter,
            "customer_name": req.customer_name,
            "item": item['name'],
            "quantity": item['quantity'],
            "total_bill": item['subtotal'],
            "delivery_address": req.delivery_address,
            "status": "confirmed"
        }
        orders.append(new_order)
        session_orders.append(new_order)
        order_counter += 1
        
    cart.clear()
    return {"message": "Checkout successful", "grand_total": grand_total, "orders": session_orders}