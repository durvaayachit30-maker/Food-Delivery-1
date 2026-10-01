import streamlit as st
from food_delivery import Customer, DeliveryPartner, Restaurant, MenuItem

st.set_page_config(page_title="Food Delivery OOP", page_icon="🍔", layout="wide")

# ---------------- Session State ----------------
if "customer" not in st.session_state:
    st.session_state.customer = None

if "delivery_partner" not in st.session_state:
    st.session_state.delivery_partner = None

if "order" not in st.session_state:
    st.session_state.order = None

if "restaurant" not in st.session_state:
    r = Restaurant("Food Corner", "Main Road")
    r.add_item(MenuItem("Veg Burger", 120, True))
    r.add_item(MenuItem("Pizza", 250, True))
    r.add_item(MenuItem("Paneer Biryani", 220, True))
    r.add_item(MenuItem("Chicken Biryani", 280, False))
    r.add_item(MenuItem("French Fries", 100, True))
    st.session_state.restaurant = r

restaurant = st.session_state.restaurant

# ---------------- UI ----------------
st.title("🍔 Food Delivery System")
st.caption("OOP Food Delivery Project - Streamlit Interface")

section = st.sidebar.radio(
    "Select Section",
    [
        "Create Customer",
        "Add Wallet Balance",
        "Show Restaurant Menu",
        "Place Order",
        "Create Delivery Partner",
        "Accept Order",
        "Enter OTP & Complete Delivery",
        "Order Status",
    ],
)

# 1. Create Customer
if section == "Create Customer":
    st.header("👤 Create Customer")

    with st.form("customer_form"):
        name = st.text_input("Customer Name")
        phone = st.text_input("Phone Number")
        address = st.text_input("Address")
        submit = st.form_submit_button("Create Customer")

    if submit:
        if name and phone and address:
            st.session_state.customer = Customer(name, phone, address)
            st.success("Customer created successfully!")
        else:
            st.warning("Please fill all fields.")

# 2. Add Wallet Balance
elif section == "Add Wallet Balance":
    st.header("💰 Add Wallet Balance")

    customer = st.session_state.customer

    if customer is None:
        st.warning("Create a customer first.")
    else:
        st.write(f"Customer: **{customer._name}**")
        st.write(f"Current Balance: ₹{customer._wallet_balance:.2f}")

        amount = st.number_input("Amount", min_value=0.0, step=50.0)

        if st.button("Add Balance"):
            if amount > 0:
                customer.add_to_wallet(amount)
                st.success(f"₹{amount:.2f} added successfully!")
                st.write(
                    f"New Balance: ₹{customer._wallet_balance:.2f}"
                )
            else:
                st.warning("Enter an amount greater than 0.")

# 3. Show Restaurant Menu
elif section == "Show Restaurant Menu":
    st.header("🍽️ Restaurant Menu")
    st.subheader(restaurant._name)
    st.write(f"Location: {restaurant._location}")

    for item in restaurant.get_menu():
        food_type = "🟢 Veg" if item._is_veg else "🔴 Non-Veg"
        c1, c2, c3 = st.columns([3, 1, 1])

        with c1:
            st.write(f"**{item._name}**")
        with c2:
            st.write(f"₹{item._price}")
        with c3:
            st.write(food_type)

# 4. Place Order
elif section == "Place Order":
    st.header("🛒 Place Order")

    customer = st.session_state.customer

    if customer is None:
        st.warning("Create a customer first.")
    else:
        menu = restaurant.get_menu()

        selected_names = st.multiselect(
            "Select food items",
            [item._name for item in menu]
        )

        selected_items = [
            item for item in menu
            if item._name in selected_names
        ]

        if selected_items:
            subtotal = sum(item._price for item in selected_items)
            gst = subtotal * 0.05
            packaging = 20
            total = subtotal + gst + packaging

            st.write("### Selected Items")
            for item in selected_items:
                st.write(f"- {item._name}: ₹{item._price}")

            st.write(f"Subtotal: ₹{subtotal:.2f}")
            st.write(f"GST (5%): ₹{gst:.2f}")
            st.write(f"Packaging Fee: ₹{packaging:.2f}")
            st.write(f"### Total: ₹{total:.2f}")

            if st.button("Place Order"):
                if customer._wallet_balance >= total:
                    order = customer.place_order(
                        restaurant, selected_items
                    )
                    customer._wallet_balance -= total
                    st.session_state.order = order

                    st.success(
                        f"Order #{order.order_id} placed successfully!"
                    )
                    st.info(
                        f"Estimated time: {order.estimated_time()} minutes"
                    )
                    st.write(f"Delivery OTP: **{order.otp}**")
                else:
                    st.error("Insufficient wallet balance.")
        else:
            st.info("Select at least one food item.")

# 5. Create Delivery Partner
elif section == "Create Delivery Partner":
    st.header("🛵 Create Delivery Partner")

    with st.form("partner_form"):
        name = st.text_input("Partner Name")
        phone = st.text_input("Phone Number")
        vehicle = st.selectbox(
            "Vehicle",
            ["Bike", "Scooter", "Car"]
        )
        submit = st.form_submit_button("Create Partner")

    if submit:
        if name and phone:
            st.session_state.delivery_partner = DeliveryPartner(
                name, phone, vehicle
            )
            st.success("Delivery partner created successfully!")
        else:
            st.warning("Please fill all fields.")

# 6. Accept Order
elif section == "Accept Order":
    st.header("📦 Accept Order")

    order = st.session_state.order
    partner = st.session_state.delivery_partner

    if order is None:
        st.warning("Place an order first.")
    elif partner is None:
        st.warning("Create a delivery partner first.")
    else:
        st.write(f"Order ID: **#{order.order_id}**")
        st.write(f"Status: **{order.status}**")
        st.write(f"Partner: **{partner._name}**")

        if partner.is_available:
            if st.button("Accept Order"):
                partner.accept_order(order)
                st.success("Order accepted!")
                st.write(f"Status: **{order.status}**")
        else:
            st.info("Delivery partner is not available.")

# 7. OTP and Complete Delivery
elif section == "Enter OTP & Complete Delivery":
    st.header("🔐 Enter OTP & Complete Delivery")

    order = st.session_state.order
    partner = st.session_state.delivery_partner

    if order is None:
        st.warning("Place an order first.")
    elif partner is None:
        st.warning("Create a delivery partner first.")
    elif order.status != "Order Accepted":
        st.warning("Delivery partner must accept the order first.")
    else:
        st.write(f"Order ID: **#{order.order_id}**")
        st.write(f"Status: **{order.status}**")

        otp = st.text_input("Enter OTP", max_chars=4)

        if st.button("Complete Delivery"):
            if partner.deliver(order, otp):
                st.success("🎉 Delivery completed successfully!")
                st.write(f"Final Status: **{order.status}**")
            else:
                st.error("Invalid OTP.")

# 8. Order Status
elif section == "Order Status":
    st.header("📋 Order Status")

    order = st.session_state.order

    if order is None:
        st.info("No order placed yet.")
    else:
        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Order ID", f"#{order.order_id}")
        with c2:
            st.metric("Status", order.status)
        with c3:
            st.metric("Bill", f"₹{order.calculate_bill():.2f}")

        st.write(
            f"Estimated Delivery Time: {order.estimated_time()} minutes"
        )
