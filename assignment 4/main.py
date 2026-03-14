from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="FastAPI — Day 5 Assignment (Cart System)")

# ==========================================
# INITIAL DATA & IN-MEMORY DB
# ==========================================
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True}
]

cart = []
orders = []
order_counter = 1

# Pydantic model for Checkout
class CheckoutRequest(BaseModel):
    customer_name: str
    delivery_address: str

# ==========================================
# CART SYSTEM ENDPOINTS
# ==========================================

# --- Q1, Q3, Q4: Add Items to the Cart & Handle Stock/Duplicates ---
@app.post('/cart/add')
def add_to_cart(product_id: int, quantity: int = 1):
    # Check if product exists
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check stock (Q3 Requirement)
    if not product['in_stock']:
        raise HTTPException(status_code=400, detail=f"{product['name']} is out of stock")
    
    # Check if already in cart to update quantity (Q4 Requirement)
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += quantity
            item['subtotal'] = item['quantity'] * item['unit_price']
            return {"message": "Cart updated", "cart_item": item}
    
    # Add new item to cart
    new_item = {
        "product_id": product['id'],
        "product_name": product['name'],
        "quantity": quantity,
        "unit_price": product['price'],
        "subtotal": product['price'] * quantity
    }
    cart.append(new_item)
    return {"message": "Added to cart", "cart_item": new_item}


# --- Q2: View the Cart and Verify the Total ---
@app.get('/cart')
def view_cart():
    # Return empty message if cart is empty
    if not cart:
        return {"message": "Cart is empty"}
    
    grand_total = sum(item['subtotal'] for item in cart)
    return {
        "items": cart,
        "item_count": len(cart),
        "grand_total": grand_total
    }


# --- Q5: Remove an Item ---
@app.delete('/cart/{product_id}')
def remove_from_cart(product_id: int):
    for i, item in enumerate(cart):
        if item['product_id'] == product_id:
            removed = cart.pop(i)
            return {"message": f"{removed['product_name']} removed from cart"}
    
    raise HTTPException(status_code=404, detail="Item not found in cart")


# --- Q5 & Bonus: Checkout Flow ---
@app.post('/cart/checkout')
def checkout(req: CheckoutRequest):
    global order_counter
    
    # Bonus: Checkout with Empty Cart check
    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty — add items first")
    
    grand_total = sum(item['subtotal'] for item in cart)
    orders_placed_this_session = []
    
    # Convert cart items to orders
    for item in cart:
        new_order = {
            "order_id": order_counter,
            "customer_name": req.customer_name,
            "delivery_address": req.delivery_address,
            "product": item['product_name'],
            "quantity": item['quantity'],
            "total_price": item['subtotal']
        }
        orders.append(new_order)
        orders_placed_this_session.append(new_order)
        order_counter += 1
        
    # Empty the cart after successful checkout
    cart.clear()
    
    return {
        "message": "Checkout successful",
        "orders_placed": len(orders_placed_this_session),
        "grand_total": grand_total,
        "receipt": orders_placed_this_session
    }


# --- Q5 & Q6: View All Checked-out Orders ---
@app.get('/orders')
def get_orders():
    return {
        "orders": orders,
        "total_orders": len(orders)
    }