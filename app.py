import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- App Configuration ---
st.set_page_config(page_title="Corporate Tax Depreciation Engine", layout="wide")
st.title("Corporate Tax Depreciation Engine")
st.markdown("### Corporate Asset Lifecycle & Depreciation Calculator")
st.divider()

# --- Inputs ---
st.sidebar.header("Asset Details")
asset_name = st.sidebar.text_input("Asset Name", "Heavy Machinery")
cost = st.sidebar.number_input("Initial Cost ($)", min_value=0.0, value=100000.0, step=1000.0)
salvage_value = st.sidebar.number_input("Salvage Value ($)", min_value=0.0, value=10000.0, step=1000.0)
life = st.sidebar.number_input("Useful Life (Years)", min_value=1, value=5, step=1)
method = st.sidebar.selectbox("Depreciation Method", ["Straight Line", "Double Declining Balance"])

# --- Calculations ---
schedule = []
accumulated_depreciation = 0
book_value = cost
depreciable_base = cost - salvage_value

for year in range(1, int(life) + 1):
    # Determine the expense based on the chosen method
    if method == "Straight Line":
        expense = depreciable_base / life
    elif method == "Double Declining Balance":
        rate = 2 / life
        expense = book_value * rate
        
        if book_value - expense < salvage_value:
            expense = book_value - salvage_value
        
        if year == life and book_value - expense > salvage_value:
            expense = book_value - salvage_value
            
    accumulated_depreciation += expense
    book_value -= expense
    
    schedule.append({
        "Year": year,
        "Depreciation Expense": expense,
        "Accumulated Depreciation": accumulated_depreciation,
        "Ending Book Value": book_value
    })

df = pd.DataFrame(schedule)

# --- Layout & Display ---
col1, col2 = st.columns([1, 2.5])

with col1:
    st.subheader("Asset Summary")
    st.metric("Asset Name", asset_name)
    st.metric("Initial Cost", f"${cost:,.2f}")
    st.metric("Depreciable Base", f"${depreciable_base:,.2f}")

with col2:
    st.subheader(f"Depreciation Schedule: {method}")
    # Format the dataframe 
    st.dataframe(df.style.format({
        "Depreciation Expense": "${:,.2f}",
        "Accumulated Depreciation": "${:,.2f}",
        "Ending Book Value": "${:,.2f}"
    }), use_container_width=True)

st.divider()

# --- Data Visualization (Matplotlib) ---
st.subheader("Asset Value & Expense Trajectory")
fig, ax = plt.subplots(figsize=(10, 4))

# Plot Book Value as a line and Expense as a bar chart
ax.plot(df["Year"], df["Ending Book Value"], marker='o', label="Ending Book Value", color='blue', linewidth=2)
ax.bar(df["Year"], df["Depreciation Expense"], label="Depreciation Expense", color='orange', alpha=0.6)

ax.set_xlabel("Year")
ax.set_ylabel("Value ($)")
ax.set_title(f"{asset_name} Depreciation Overview")
ax.set_xticks(df["Year"])
ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.4)

# Render the plot in Streamlit
st.pyplot(fig)