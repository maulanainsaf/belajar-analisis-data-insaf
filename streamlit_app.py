import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Analisis Penjualan",
    page_icon="",
    layout="wide"
)

# Load datasets
combined = pd.read_csv("combined_sales.csv")

# Sidebar untuk logo dan filter
st.sidebar.image("profil_insaf.jpg", use_container_width=True)  # Ganti dengan path logo
st.sidebar.header("Filter")
selected_year = st.sidebar.selectbox("Pilih Tahun:", ["Semua"] + sorted(combined['year'].unique().tolist()))

# Filter berdasarkan tahun jika dipilih
if selected_year != "Semua":
    combined = combined[combined['year'] == selected_year]

# Title
st.title("Sales Dashboard")

# Sorting Top 10
sales_by_city = combined.groupby(['customer_city', 'year'])['total_y'].sum().reset_index()
sales_by_state = combined.groupby(['customer_state', 'year'])['total_x'].sum().reset_index()

top_10_city = sales_by_city.sort_values(by="total_y", ascending=False).head(10)
top_10_state = sales_by_state.sort_values(by="total_x", ascending=False).head(10)

# Menampilkan Data
st.subheader("Sales by City")
# Filter Pencarian Kota
search_city = st.text_input("Cari Kota:")
if search_city:
    filtered_city = sales_by_city[sales_by_city["customer_city"].str.contains(search_city, case=False, na=False)]
    if not filtered_city.empty:
        st.write(f"Hasil pencarian untuk kota: {search_city}")
        st.dataframe(filtered_city)
    else:
        st.write("Tidak ada hasil yang ditemukan.")
st.dataframe(combined[['customer_city', 'year', 'total_y']])

# Visualization: Top 10 Sales by City
st.subheader("Top 10 Sales by City")
fig_city, ax_city = plt.subplots(figsize=(10, 6))
sns.barplot(data=top_10_city, x="customer_city", y="total_y", hue="year", ax=ax_city)
ax_city.set_title('Top 10 Total Sales by City')
ax_city.set_xlabel('City')
ax_city.set_ylabel('Total Sales')
st.pyplot(fig_city)

st.subheader("Sales by State")
# Filter Pencarian State
search_state = st.text_input("Cari State:")
if search_state:
    filtered_state = sales_by_state[sales_by_state["customer_state"].str.contains(search_state, case=False, na=False)]
    if not filtered_state.empty:
        st.write(f"Hasil pencarian untuk state: {search_state}")
        st.dataframe(filtered_state)
    else:
        st.write("Tidak ada hasil yang ditemukan.")
st.dataframe(combined[['customer_state', 'year', 'total_x']])

# Visualization: Top 10 Sales by State
st.subheader("Top 10 Sales by State")
fig_state, ax_state = plt.subplots(figsize=(10, 6))
sns.barplot(data=top_10_state, x='customer_state', y='total_x', hue="year", ax=ax_state)
ax_state.set_title('Top 10 Total Sales per State')
ax_state.set_xlabel('State')
ax_state.set_ylabel('Total Sales')
st.pyplot(fig_state)