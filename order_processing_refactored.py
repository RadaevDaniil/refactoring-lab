DEFAULT_CURRENCY = "USD"
TAX_RATE = 0.21
COUPON_DISCOUNTS = {
    "SAVE10": 0.10,
    "SAVE20": {"threshold": 200, "high": 0.20, "low": 0.05},
    "VIP": {"default": 50, "under_100": 10}
}

def parse_request(request):
    return (
        request.get("user_id"),
        request.get("items"),
        request.get("coupon"),
        request.get("currency")
    )

def validate_request(user_id, items, currency):
    if user_id is None:
        raise ValueError("user_id is required")
    if items is None:
        raise ValueError("items is required")
    
    currency = currency or DEFAULT_CURRENCY
    
    if not isinstance(items, list):
        raise ValueError("items must be a list")
    if len(items) == 0:
        raise ValueError("items must not be empty")
    
    return currency

def validate_items(items):
    for item in items:
        if "price" not in item or "qty" not in item:
            raise ValueError("item must have price and qty")
        if item["price"] <= 0:
            raise ValueError("price must be positive")
        if item["qty"] <= 0:
            raise ValueError("qty must be positive")

def calculate_subtotal(items):
    return sum(item["price"] * item["qty"] for item in items)

def calculate_discount(coupon, subtotal):
    if not coupon:
        return 0
    
    if coupon == "SAVE10":
        return int(subtotal * COUPON_DISCOUNTS["SAVE10"])
    
    elif coupon == "SAVE20":
        if subtotal >= COUPON_DISCOUNTS["SAVE20"]["threshold"]:
            return int(subtotal * COUPON_DISCOUNTS["SAVE20"]["high"])
        else:
            return int(subtotal * COUPON_DISCOUNTS["SAVE20"]["low"])
    
    elif coupon == "VIP":
        if subtotal < 100:
            return COUPON_DISCOUNTS["VIP"]["under_100"]
        return COUPON_DISCOUNTS["VIP"]["default"]
    
    else:
        raise ValueError("unknown coupon")

def calculate_tax(amount):
    return int(amount * TAX_RATE)

def generate_order_id(user_id, items_count):
    return f"{user_id}-{items_count}-X"

def process_checkout(request):
    user_id, items, coupon, currency = parse_request(request)
    
    currency = validate_request(user_id, items, currency)
    validate_items(items)
    
    subtotal = calculate_subtotal(items)
    discount = calculate_discount(coupon, subtotal)
    
    total_after_discount = max(subtotal - discount, 0)
    tax = calculate_tax(total_after_discount)
    total = total_after_discount + tax
    
    order_id = generate_order_id(user_id, len(items))
    
    return {
        "order_id": order_id,
        "user_id": user_id,
        "currency": currency,
        "subtotal": subtotal,
        "discount": discount,
        "tax": tax,
        "total": total,
        "items_count": len(items),
    }
