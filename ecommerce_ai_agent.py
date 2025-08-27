# Simulated E-commerce AI Agent for SMEs
# This script runs a console-based agent that handles user queries via rule-based logic.
# No external dependencies, APIs, or installations required.
# Copy-paste and run directly in Python.
import sys
import datetime
import random
import re

# Simulated data structures (state management)
products = [
    {"id": 1, "name": "Blue Running Shoes", "price": 80, "color": "blue", "category": "shoes", "size": "US 10"},
    {"id": 2, "name": "Red T-Shirt", "price": 20, "color": "red", "category": "clothing", "size": "M"},
    {"id": 3, "name": "Wireless Headphones", "price": 150, "color": "black", "category": "electronics"},
    {"id": 4, "name": "Coffee Beans", "price": 15, "category": "grocery"},
    {"id": 5, "name": "Laptop Charger", "price": 30, "category": "electronics"},
    {"id": 6, "name": "Premium Running Shoes", "price": 120, "color": "blue", "category": "shoes", "size": "US 10"},
    {"id": 7, "name": "Organic Coffee Beans", "price": 25, "category": "grocery"}
]

cart = []  # List of product IDs in cart
orders = []  # List of dicts: {"id": str, "items": [product_ids], "date": datetime, "status": str, "tracking": str}
user_info = {"name": "John Doe", "address": "123 Main St, City, USA", "payment": "****-1234 (masked for safety)"}
query_log = []  # For business insights
subscribed_warranty = False  # Set to True if "subscribed" separately
store_policies = {
    "shipping": "Standard shipping: 5-7 business days. Free over $50.",
    "returns": "Returns allowed within 30 days of purchase. No returns on sale items.",
    "warranty": "1-year warranty on electronics. Claims require proof of purchase.",
    "cancellations": "Orders can be canceled within 24 hours of placement.",
    "faq": "Q: How do I track my order? A: Use order ID. Q: Payment options? A: Credit card, BNPL (simulated)."
}
size_conversions = {
    "shoes": {"US 10": "EU 43, UK 9"},
    "clothing": {"M": "EU 40, UK 12"}
}
next_order_id = 1

# Helper functions
def parse_query(query):
    """Basic intent parsing via keyword matching."""
    query = query.lower()
    if "dashboard" in query:
        return "dashboard"
    elif "return" in query:
        return "return"
    elif "change order" in query or "modify order" in query:
        return "change_order"
    elif "view cart" in query:
        return "view_cart"
    elif "purchase" in query or "buy" in query or "checkout" in query:
        return "purchase"
    elif "payment info" in query:
        return "payment_info"
    elif "change name" in query or "update address" in query:
        return "update_info"
    elif "cancel order" in query:
        return "cancel_order"
    elif "policy" in query or "faq" in query or "payment methods" in query or "payment options" in query or ("accepted" in query and "payment" in query):
        return "policy_faq"
    elif "warranty" in query:
        return "warranty"
    elif "payment processing" in query or "finish payment" in query:
        return "payment_process"
    elif "track order" in query or "when will my order arrive" in query:
        return "track_order"
    elif "search" in query or "show me" in query or "recommend" in query:
        return "product_search"
    elif "compare" in query:
        return "compare"
    elif re.search(r'\badd\b.*\bto\b \bcart\b', query):
        return "add_to_cart"
    elif re.search(r'\bremove\b.*\bfrom\b \bcart\b', query):
        return "remove_from_cart"
    elif "coupon" in query or "promo" in query:
        return "coupon"
    elif "size" in query or "fit" in query or "compatibility" in query:
        return "size_fit"
    elif "reorder" in query or "subscription" in query:
        return "reorder_subscription"
    elif ("query" in query or "view" in query) and ("chats" in query or "history" in query or "log" in query):
        return "view_history"
    else:
        return "unknown"

def get_product_by_id(prod_id):
    return next((p for p in products if p["id"] == prod_id), None)

def log_query(query, response):
    query_log.append({"query": query, "response": response, "timestamp": datetime.datetime.now()})

# Functionality handlers
def handle_return(query):
    # Parse order_id from query, dummy assumption
    order_id = query.split("order")[-1].strip() if "order" in query else None
    if not order_id:
        return "Please provide order ID for return."
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        return "Order not found."
    days_since = (datetime.datetime.now() - order["date"]).days
    if days_since > 30:
        return "Sorry, returns not allowed after 30 days per policy."
    # Simulate return label
    orders.remove(order)
    return "Return approved. Prepaid label: dummy_return_label.pdf. Drop off at nearest post office."

def handle_change_order(query):
    order_id = query.split("order")[-1].strip() if "order" in query else None
    if not order_id:
        return "Please provide order ID to change."
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        return "Order not found."
    # Simulate change, e.g., add item
    return "Order changed successfully. New items: [updated list]."

def handle_view_cart():
    if not cart:
        return "Your cart is empty."
    items = [get_product_by_id(pid)["name"] for pid in cart if get_product_by_id(pid)]
    return f"Cart items: {', '.join(items)}"

def handle_purchase():
    if not cart:
        return "Cart is empty. Add items first."
    global next_order_id
    order_id = str(next_order_id)
    next_order_id += 1
    order_date = datetime.datetime.now()
    orders.append({
        "id": order_id,
        "items": cart[:],
        "date": order_date,
        "status": "Processing",
        "tracking": "TRACK-" + str(random.randint(1000, 9999))
    })
    cart.clear()
    return f"Purchase complete. Order ID: {order_id}. Estimated arrival: {order_date + datetime.timedelta(days=7)}"

def handle_payment_info():
    return f"Payment information: {user_info['payment']} (never share full details)."

def handle_update_info(query):
    if "name" in query.lower():
        new_name = query.split("to")[-1].strip()
        user_info["name"] = new_name
        return f"Name updated to {new_name}."
    elif "address" in query.lower():
        new_addr = query.split("to")[-1].strip()
        user_info["address"] = new_addr
        return f"Address updated to {new_addr}."
    return "Please specify what to update (name or address)."

def handle_cancel_order(query):
    order_id = query.split("order")[-1].strip() if "order" in query else None
    if not order_id:
        return "Please provide order ID to cancel."
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        return "Order not found."
    hours_since = (datetime.datetime.now() - order["date"]).total_seconds() / 3600
    if hours_since > 24:
        return "Sorry, cancellations not allowed after 24 hours per policy."
    orders.remove(order)
    return "Order canceled successfully."

def handle_policy_faq(query):
    key = next((k for k in store_policies if k in query.lower()), None)
    if key:
        return store_policies[key]
    return "\n".join([f"{k.capitalize()}: {v}" for k, v in store_policies.items()])

def handle_warranty(query):
    if not subscribed_warranty:
        return "Warranty claims require separate subscription. Please subscribe to proceed."
    # Simulate claim
    return "Warranty claim processed. Next steps: Send item to repair center."

def handle_payment_process():
    return "Payment processing simulated. Use BNPL option? Yes/No (demo: completed). Safe options: Credit, PayPal."

def handle_track_order(query):
    order_id = query.split("order")[-1].strip() if "order" in query else None
    if not order_id:
        return "Please provide order ID."
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        return "Order not found."
    days_left = 7 - (datetime.datetime.now() - order["date"]).days
    return f"Order status: {order['status']}. Tracking: {order['tracking']}. Arrival in approx {max(0, days_left)} days."

def handle_product_search(query):
    terms = query.lower().split()
    filtered = products[:]
    reserved_terms = set()
    
    if "under" in terms:
        under_idx = terms.index("under")
        if under_idx + 1 < len(terms):
            max_price_str = terms[under_idx + 1].replace("$", "")
            validated_str = max_price_str.lstrip('-').replace('.', '', 1)
            if validated_str.isdigit():
                max_price = float(max_price_str)
                filtered = [p for p in filtered if p.get("price", float("inf")) < max_price]
                reserved_terms.add("under")
                reserved_terms.add(terms[under_idx + 1])
            else:
                return "Invalid price format. Please use a number like $100."
        else:
            return "Missing price after 'under'."
    
    if "in" in terms:
        in_idx = terms.index("in")
        if in_idx + 1 < len(terms):
            color = terms[in_idx + 1]
            filtered = [p for p in filtered if p.get("color") == color]
            reserved_terms.add("in")
            reserved_terms.add(color)
        else:
            return "Missing color after 'in'."
    
    # General keyword filtering for remaining terms
    ignore_words = {"show", "me", "search", "recommend", "for", "please"}  # Common query noise
    keywords = [t for t in terms if t not in reserved_terms and t not in ignore_words and not t.startswith('$')]
    if keywords:
        filtered = [p for p in filtered if any(
            k in p["name"].lower() or k in p.get("category", "").lower() or k in p.get("color", "").lower()
            for k in keywords
        )]
    
    if not filtered:
        return "No products found. Try different search."
    
    # Personalized recommendations based on history
    past_categories = set()
    for order in orders:
        for pid in order["items"]:
            prod = get_product_by_id(pid)
            if prod:
                past_categories.add(prod["category"])
    if past_categories:
        personalized = [p for p in filtered if p["category"] in past_categories]
        if personalized:
            filtered = personalized  # Prioritize past categories
    
    recs = random.sample(filtered, min(3, len(filtered)))
    rec_str = "\n".join([f"{p['name']} - ${p['price']}" for p in recs])
    
    # Cross-sell: suggest accessory
    electronics = [p for p in products if p["category"] == "electronics"]
    accessory = random.choice(electronics) if electronics and any(p["category"] == "shoes" for p in recs) else None
    cross_sell = f"Suggested accessory: {accessory['name']} - ${accessory['price']}" if accessory else ""
    
    # Upsell: suggest higher-margin alternative
    upsell = None
    for rec in recs:
        alternatives = [p for p in products if p["category"] == rec["category"] and p["price"] > rec["price"]]
        if alternatives:
            upsell = random.choice(alternatives)
            break
    upsell_str = f"Upsell suggestion: {upsell['name']} - ${upsell['price']} (higher quality alternative)" if upsell else ""
    
    return f"Search results/recommendations:\n{rec_str}\n{cross_sell}\n{upsell_str}"

def handle_compare(query):
    # Assume comparing products by name, handle multiple
    query_clean = query.lower().replace("compare", "").replace(",", "").strip()
    names = [n.strip() for n in query_clean.split("and")]
    if len(names) < 2:
        return "Please specify at least two products to compare, e.g., 'compare shoes and t-shirt'."
    prods = []
    for name in names:
        prod = next((p for p in products if name in p["name"].lower()), None)
        if prod:
            prods.append(prod)
    if len(prods) < 2:
        return "Not enough products found for comparison."
    # Side-by-side table (console formatted)
    headers = ["Attribute"] + [p["name"] for p in prods]
    rows = [
        ["Price", *[f"${p['price']}" for p in prods]],
        ["Category", *[p["category"] for p in prods]],
        ["Color", *[p.get("color", "N/A") for p in prods]],
        ["Size", *[p.get("size", "N/A") for p in prods]]
    ]
    table = "\n".join([" | ".join(row) for row in [headers] + rows])
    return f"Comparison:\n{table}"

def handle_add_to_cart(query):
    match = re.search(r'\badd\b\s*(.*?)\s*\bto\b \bcart\b', query.lower())
    if not match:
        return "Please specify the product to add."
    prod_name = match.group(1).strip()
    if not prod_name:
        return "Please specify the product to add."
    matches = [p for p in products if prod_name in p["name"].lower()]
    if not matches:
        return "Product not found."
    if len(matches) > 1:
        return f"Multiple matches: {', '.join([p['name'] for p in matches])}. Please specify."
    prod = matches[0]
    cart.append(prod["id"])
    return f"{prod['name']} added to cart."

def handle_remove_from_cart(query):
    match = re.search(r'\bremove\b\s*(.*?)\s*\bfrom\b \bcart\b', query.lower())
    if not match:
        return "Please specify the product to remove."
    prod_name = match.group(1).strip()
    if not prod_name:
        return "Please specify the product to remove."
    matches = [p for p in products if prod_name in p["name"].lower()]
    if not matches:
        return "Product not found."
    if len(matches) > 1:
        return f"Multiple matches: {', '.join([p['name'] for p in matches])}. Please specify."
    prod = matches[0]
    if prod["id"] not in cart:
        return "Product not in cart."
    cart.remove(prod["id"])
    return f"{prod['name']} removed from cart."

def handle_coupon():
    # Simulate best deal
    total = sum(p.get("price", 0) for p in (get_product_by_id(pid) for pid in cart) if p)
    if total > 100:
        return "Applied 10% discount. New total: [calculated]."
    return "No eligible coupons. Check eligibility: Orders over $100."

def handle_size_fit(query):
    prod_name = query.lower().split("for")[-1].strip() if "for" in query else ""
    prod = next((p for p in products if prod_name in p["name"].lower()), None)
    if not prod or "size" not in prod:
        return "No size info available."
    conv = size_conversions.get(prod["category"], {}).get(prod["size"], "No conversion")
    return f"Recommended size: {prod['size']}. Conversions: {conv}. Compatibility: Fits standard."

def handle_reorder_subscription(query):
    if not orders:
        return "No previous orders."
    last_order = orders[-1]
    items = [p.get("name", "Unknown") for p in (get_product_by_id(pid) for pid in last_order["items"]) if p]
    # Simulate reorder
    cart.extend(last_order["items"])
    return f"Reordered: {', '.join(items)}. Subscription: Monthly (pause/cancel via 'subscription pause')."

def handle_view_history():
    if not query_log:
        return "No query history available yet."
    history_str = "\n".join([
        f"{q['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}: {q['query']} - {q['response']}"
        for q in query_log
    ])
    return f"Query History:\n{history_str}"

def handle_unknown():
    if cart:
        return "Abandoned cart reminder: You have items in cart. Proceed to checkout? Also, redirecting to human support."
    return "Sorry, I can't handle this. Redirecting to human support with history."

# Dashboard for owners/admins
def handle_dashboard():
    print("Entering Admin Dashboard. Type 'exit' to leave.")
    while True:
        try:
            admin_query = input("Admin: ")
        except EOFError:
            print("End of input in dashboard. Exiting.")
            break
        if admin_query.lower() == "exit":
            break
        elif "change plan" in admin_query.lower():
            print("Plan changed. New features: [configured].")
        elif "configure features" in admin_query.lower():
            print("Features configured. Added subscriptions.")
        elif "insights" in admin_query.lower():
            # Summarize logs
            common_queries = {}
            for q in query_log:
                intent = parse_query(q["query"])
                common_queries[intent] = common_queries.get(intent, 0) + 1
            print("Customer Insights:")
            for k, v in sorted(common_queries.items(), key=lambda x: x[1], reverse=True):
                print(f"- {k}: {v} queries")
            print("Trending: Frequent searches for shoes.")
            print("Alerts: Out-of-stock mentions (simulated).")
            print("Automated Campaign: 'Flash sale on shoes! Buy now.'")
        elif "guardrails" in admin_query.lower():
            print("Guardrails: PII masked, refunds auto-approved under $50 (enforced).")
        else:
            print("Unknown admin command. Options: change plan, configure features, insights, guardrails.")

# Main agent loop
print("Welcome to E-commerce AI Agent. Type 'quit' to exit.")
while True:
    try:
        user_query = input("You: ")
    except EOFError:
        print("End of input reached. Exiting.")
        sys.exit(0)
    if user_query.lower() == "quit":
        sys.exit(0)
    intent = parse_query(user_query)
   
    try:
        if intent == "dashboard":
            handle_dashboard()
            response = "Exited dashboard."
        elif intent == "return":
            response = handle_return(user_query)
        elif intent == "change_order":
            response = handle_change_order(user_query)
        elif intent == "view_cart":
            response = handle_view_cart()
        elif intent == "purchase":
            response = handle_purchase()
        elif intent == "payment_info":
            response = handle_payment_info()
        elif intent == "update_info":
            response = handle_update_info(user_query)
        elif intent == "cancel_order":
            response = handle_cancel_order(user_query)
        elif intent == "policy_faq":
            response = handle_policy_faq(user_query)
        elif intent == "warranty":
            response = handle_warranty(user_query)
        elif intent == "payment_process":
            response = handle_payment_process()
        elif intent == "track_order":
            response = handle_track_order(user_query)
        elif intent == "product_search":
            response = handle_product_search(user_query)
        elif intent == "compare":
            response = handle_compare(user_query)
        elif intent == "add_to_cart":
            response = handle_add_to_cart(user_query)
        elif intent == "remove_from_cart":
            response = handle_remove_from_cart(user_query)
        elif intent == "coupon":
            response = handle_coupon()
        elif intent == "size_fit":
            response = handle_size_fit(user_query)
        elif intent == "reorder_subscription":
            response = handle_reorder_subscription(user_query)
        elif intent == "view_history":
            response = handle_view_history()
        else:
            response = handle_unknown()
    except Exception as e:
        response = f"An unexpected error occurred: {str(e)}. Please rephrase your query and try again."
    log_query(user_query, response)
    print("Agent:", response)