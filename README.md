# Northstar Self-Serve Customer Dashboard

A Streamlit-based customer support deflection tool that helps customers find answers before opening a support ticket.

## Features

- 📦 **Order Status** - Check order status, tracking, and delivery dates
- 🔄 **Returns & Refunds** - View return status and refund information
- 📊 **Stock Availability** - Check if products are in stock with restock dates
- ❓ **FAQ** - Common questions answered instantly

## Project Structure

```
.
├── app.py                 # Main Streamlit application
├── orders.csv            # Orders data
├── stock.csv             # Stock/inventory data
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── .gitignore            # Git ignore rules
```

## Installation

### Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt
```

### Using System Python

```bash
pip install -r requirements.txt
```

## Running the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Usage

1. **Home Page** - See quick links to all features
2. **My Orders** - Enter Order ID (e.g. NS-1001) to check status
3. **Returns & Refunds** - Track return requests and refund amounts
4. **Stock Check** - Search products by name or ID
5. **FAQ** - Browse common questions

## Requirements

- Python 3.8+
- Streamlit
- Pandas

See `requirements.txt` for exact versions.

## Data Files

- `orders.csv` - Customer orders with status and return info
- `stock.csv` - Product inventory with restock dates

## Author

Created for Northstar Retail support deflection MVP.

## License

Proprietary

## LIVE DEMO LINK
 https://xhu2firo5tjgh4bswoz342.streamlit.app/
