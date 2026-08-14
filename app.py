"""
Northstar Self-Serve Customer Dashboard
A customer-first support deflection tool that answers the most common questions
before a support ticket is ever opened.

Features:
  - Quick order status lookups
  - Returns/refunds information
  - Real-time stock availability
  - FAQ section
"""

import pandas as pd
import streamlit as st
from pathlib import Path

# Configuration
DATA_DIR = Path(__file__).parent

st.set_page_config(
    page_title="Northstar Support — Self-Serve",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better UX
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .subheader-text {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load orders and stock data from CSV files with error handling."""
    try:
        orders = pd.read_csv(DATA_DIR / "orders.csv")
        stock = pd.read_csv(DATA_DIR / "stock.csv")
        return orders, stock
    except FileNotFoundError as e:
        st.error(f"Error loading data files: {e}")
        st.stop()
    except Exception as e:
        st.error(f"Unexpected error loading data: {e}")
        st.stop()


# Load data
orders_df, stock_df = load_data()

# Page Header
col_title, col_support = st.columns([3, 1])
with col_title:
    st.markdown('<div class="main-header">🛍️ Northstar Customer Support</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader-text">Find answers instantly — Check your order, returns, and inventory before contacting us</div>', unsafe_allow_html=True)
with col_support:
    st.markdown("""
    <div style="text-align: right; padding-top: 1rem;">
        <p><strong>Need help?</strong><br>
        <small>Contact us if you can't find your answer</small></p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Sidebar - Quick Links
with st.sidebar:
    st.markdown("### ⚡ Quick Navigation")
    st.markdown("---")
    navigation = st.radio(
        "Choose a topic:",
        ["🏠 Home", "📦 My Orders", "🔄 Returns & Refunds", "📊 Stock Check", "❓ FAQ"],
        label_visibility="collapsed"
    )


# HOME / LANDING PAGE

if navigation == "🏠 Home":
    st.markdown("## Welcome! Let us help you find answers")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 📦 **Check Your Order**")
            st.write("Find order status, tracking info, and estimated delivery")
            if st.button("Look up order", key="btn_order"):
                st.session_state.page = "📦 My Orders"
                st.rerun()
    
    with col2:
        with st.container(border=True):
            st.markdown("### 🔄 **Returns & Refunds**")
            st.write("See return status, refund amounts, and next steps")
            if st.button("Check return status", key="btn_return"):
                st.session_state.page = "🔄 Returns & Refunds"
                st.rerun()
    
    with col3:
        with st.container(border=True):
            st.markdown("### 📊 **Check Stock**")
            st.write("See if a product is available for purchase")
            if st.button("Search inventory", key="btn_stock"):
                st.session_state.page = "📊 Stock Check"
                st.rerun()
    
    st.divider()
    st.markdown("### 🎯 Common Questions Answered")
    
    col_faq1, col_faq2 = st.columns(2)
    with col_faq1:
        st.markdown("**How can I track my order?**")
        st.caption("Use the 'My Orders' section above with your Order ID")
        
        st.markdown("**What if I never received my order?**")
        st.caption("Check order status first. If marked delivered but not received, contact support.")
    
    with col_faq2:
        st.markdown("**How long do returns take?**")
        st.caption("Returns typically process within 5-7 business days after we receive it")
        
        st.markdown("**When will X product be back in stock?**")
        st.caption("Check the Stock Check tool for restock dates")

# PAGE: MY ORDERS

elif navigation == "📦 My Orders":
    st.markdown("## 📦 Order Status Lookup")
    st.write("Enter your Order ID to see the current status of your order")
    
    col_input, col_example = st.columns([3, 1])
    with col_input:
        order_id = st.text_input(
            "Order ID",
            placeholder="e.g. NS-1001",
            label_visibility="visible"
        ).strip().upper()
    with col_example:
        st.caption("Format: NS-####")
    
    if st.button("Search Order", use_container_width=True, type="primary"):
        if not order_id:
            st.warning("🔍 Please enter an Order ID to search")
        else:
            match = orders_df[orders_df["order_id"] == order_id]
            if match.empty:
                st.error(f"❌ Order '{order_id}' not found")
                st.info("💡 **Tip:** Check your confirmation email for your Order ID. It starts with 'NS-'")
            else:
                row = match.iloc[0]
                
                # Status indicator with color
                status = row.order_status
                if status == "Delivered":
                    status_color = "🟢"
                elif status == "Shipped":
                    status_color = "🟡"
                else:
                    status_color = "🔵"
                
                st.success(f"{status_color} Order **{row.order_id}** — {status}")
                
                # Order Details
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Item", row['item'])
                col2.metric("Quantity", row['quantity'])
                col3.metric("Order Date", row['order_date'])
                col4.metric("Status", row['order_status'])
                
                st.divider()
                
                # Next Steps
                if status == "Processing":
                    st.info("📋 Your order is being prepared. You'll get a shipping notification soon!")
                elif status == "Shipped":
                    st.info("📬 Your order is on its way! Check your email for tracking details.")
                elif status == "Delivered":
                    st.success("✅ Your order has been delivered. Enjoy your purchase!")

# PAGE: RETURNS & REFUNDS

elif navigation == "🔄 Returns & Refunds":
    st.markdown("## 🔄 Returns & Refunds Status")
    st.write("Check the status of your return or refund request")
    
    col_input, col_example = st.columns([3, 1])
    with col_input:
        order_id = st.text_input(
            "Order ID",
            placeholder="e.g. NS-1004",
            label_visibility="visible",
            key="return_input"
        ).strip().upper()
    with col_example:
        st.caption("Format: NS-####")
    
    if st.button("Search Return Status", use_container_width=True, type="primary"):
        if not order_id:
            st.warning("🔍 Please enter an Order ID to search")
        else:
            match = orders_df[orders_df["order_id"] == order_id]
            if match.empty:
                st.error(f"❌ Order '{order_id}' not found")
            else:
                row = match.iloc[0]
                
                if row.return_status == "Not Requested":
                    st.info(f"ℹ️ No return has been requested for order **{row.order_id}**")
                    st.write("If you want to return this item, please contact support.")
                else:
                    st.success(f"✅ Return found for order **{row.order_id}**")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Item", row['item'])
                    col2.metric("Return Status", row['return_status'])
                    col3.metric("Refund Amount", f"${row['refund_amount']:.2f}")
                    
                    st.divider()
                    st.write(f"**Return Reason:** {row['return_reason']}")
                    
                    if row.return_status == "Requested":
                        st.info("📦 Return was requested. Wait for shipping label/instructions.")
                    elif row.return_status == "In Transit":
                        st.info("📬 Your return is on its way to us. We'll process it when received.")
                    elif row.return_status == "Received":
                        st.warning("✏️ We received your return. Processing refund...")
                    elif row.return_status == "Completed":
                        st.success(f"💰 Refund completed! Check your account for ${row.refund_amount:.2f}")

# PAGE: STOCK CHECK

elif navigation == "📊 Stock Check":
    st.markdown("## 📊 Check Product Availability")
    st.write("Search for a product to see current stock levels")
    
    col_input, col_tip = st.columns([3, 1])
    with col_input:
        product_query = st.text_input(
            "Product Name or ID",
            placeholder="e.g. Yoga Mat or P-2001",
            label_visibility="visible"
        ).strip()
    with col_tip:
        st.caption("Search by name or ID")
    
    if st.button("Check Availability", use_container_width=True, type="primary"):
        if not product_query:
            st.warning("🔍 Please enter a product name or ID")
        else:
            # Search by ID
            match = stock_df[
                stock_df["product_id"].str.upper() == product_query.upper()
            ]
            # Search by name
            if match.empty:
                match = stock_df[
                    stock_df["product_name"].str.contains(
                        product_query, case=False, na=False
                    )
                ]
            
            if match.empty:
                st.error(f"❌ No product found matching '{product_query}'")
                st.info("💡 Try searching by product ID (e.g. P-2001) or full product name")
            else:
                for _, row in match.iterrows():
                        if row['quantity_in_stock'] == 0:
                            st.error(
                                f"🚫 **{row['product_name']}** ({row['product_id']})\n\n"
                                f"Currently **out of stock** — Expected restock: **{row['restock_date']}**"
                            )
                        elif row['quantity_in_stock'] <= row['reorder_threshold']:
                            st.warning(
                                f"⚠️ **{row['product_name']}** ({row['product_id']})\n\n"
                                f"Only **{row['quantity_in_stock']} in stock** (low inventory)"
                            )
                        else:
                            st.success(
                                f"✅ **{row['product_name']}** ({row['product_id']})\n\n"
                                f"**{row['quantity_in_stock']} available** — Ready to ship!"
                            )

# PAGE: FAQ

elif navigation == "❓ FAQ":
    st.markdown("## ❓ Frequently Asked Questions")
    
    faq_items = {
        "📦 How can I track my order?": 
            "Use the 'My Orders' section and enter your Order ID. You'll see current status and estimated delivery.",
        
        "🔄 How do returns work?": 
            "Check 'Returns & Refunds' with your Order ID. Once we receive your item, we'll process your refund within 5-7 business days.",
        
        "💰 How long until I get my refund?":
            "Refunds are processed 5-7 business days after we receive your return. Check the 'Returns & Refunds' section for current status.",
        
        "📊 When will X product be in stock?":
            "Use 'Stock Check' to search for the product. We'll show the expected restock date if it's currently out of stock.",
        
        "What if I never received my order?":
            "Check 'My Orders' first. If it shows 'Delivered' but you haven't received it, contact support with your Order ID.",
        
        "Can I change my order?":
            "Contact support as soon as possible with your Order ID. We may be able to help if your order hasn't shipped yet.",
        
        "How do I know my return was received?":
            "Check 'Returns & Refunds' with your Order ID. Status will update to 'Received' when we get it.",
        
        "Is this product available?":
            "Use 'Stock Check' to search for any product and see real-time availability and restock dates.",
    }
    
    for question, answer in faq_items.items():
        with st.expander(question):
            st.write(answer)
    
    st.divider()
    st.markdown("### Still have questions?")
    st.info("💬 If you can't find the answer above, please contact our support team. We're here to help!")


st.divider()
st.caption("🛍️ Northstar Customer Support — Available 24/7")

