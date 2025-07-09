import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Setup
st.set_page_config(layout="wide", page_title="Shopee Analytics Dashboard")

# Load data
df_users = pd.read_csv("data/raw/users.csv")
df_orders = pd.read_csv("data/raw/orders.csv", parse_dates=["order_date", "estimated_delivery"])
df_products = pd.read_csv("data/raw/products.csv")
df_payments = pd.read_csv("data/raw/payments.csv")
df_items = pd.read_csv("data/raw/order_items.csv")

st.title("📦 Shopee Analytics Dashboard")

# --------------------------------------------
# 👤 Section 1: Users
# --------------------------------------------
st.header("👤 Pengguna")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribusi Gender")
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.countplot(data=df_users, x='gender', hue='gender', palette='Set2', legend=False, ax=ax)
    st.pyplot(fig)

with col2:
    st.subheader("Distribusi Usia")
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.histplot(df_users['age'], bins=20, kde=True, color='skyblue', ax=ax)
    st.pyplot(fig)

# Top 10 Cities
st.subheader("10 Kota Pengguna Terbanyak (dengan Gender)")
top10 = df_users['city'].value_counts().nlargest(10).index
df_top = df_users[df_users['city'].isin(top10)]
fig, ax = plt.subplots(figsize=(10, 4))
sns.countplot(data=df_top, x='city', hue='gender', palette='viridis', order=top10, ax=ax)
plt.xticks(rotation=45)
# Pindahkan legend ke luar kanan plot
ax.legend(title='Gender', bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
st.pyplot(fig)


st.markdown("""
**📝 Insight Pengguna:**
- Gender pengguna cukup merata (atau dominan satu sisi).
- Mayoritas pengguna berusia produktif (18–35 tahun).
- Kota terbanyak: Jakarta, Surabaya, Bandung — menunjukkan konsentrasi pengguna di kota besar.
""")


# --------------------------------------------
# 📦 Section 2: Orders
# --------------------------------------------
st.header("🛒 Pesanan")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Status Pesanan")
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.countplot(data=df_orders, x='status', hue='status', palette='Set1', legend=False, ax=ax)
    st.pyplot(fig)

with col2:
    st.subheader("Jumlah Pesanan per Bulan")

    df_orders['month'] = df_orders['order_date'].dt.to_period("M").astype(str)
    monthly_orders = df_orders.groupby('month').size().reset_index(name='order_count')

    fig, ax = plt.subplots(figsize=(7, 3.5))
    sns.lineplot(data=monthly_orders, x='month', y='order_count', marker='o', ax=ax)

    # Tampilkan hanya setiap 5 bulan
    months = monthly_orders['month']
    ax.set_xticks(range(0, len(months), 5))
    ax.set_xticklabels(months[::5], rotation=30)

    st.pyplot(fig)

col = st.columns([1])[0]  # atau bisa [0.8] biar sempit
st.subheader("Durasi Pengiriman")
df_orders['delivery_days'] = (df_orders['estimated_delivery'] - df_orders['order_date']).dt.days
fig, ax = plt.subplots(figsize=(6, 3.5))
sns.histplot(df_orders['delivery_days'], bins=10, kde=True, color='orange', ax=ax)
st.pyplot(fig)

st.markdown("""
**📝 Insight Pesanan:**
- Status pesanan didominasi oleh _delivered_.
- Jumlah pesanan per bulan menunjukkan tren pertumbuhan stabil.
- Rata-rata durasi pengiriman 3–5 hari.
""")


# --------------------------------------------
# 💳 Section 3: Payments
# --------------------------------------------
st.header("💳 Pembayaran")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Metode Pembayaran")
    fig, ax = plt.subplots(figsize=(6, 3.5))
    sns.countplot(data=df_payments, x='payment_method', hue='payment_method', palette='cool', legend=False, ax=ax)
    plt.xticks(rotation=30)
    st.pyplot(fig)

with col2:
    st.subheader("Status Pembayaran")
    fig, ax = plt.subplots(figsize=(6, 3.5))
    sns.countplot(data=df_payments, x='payment_status', hue='payment_status', palette='Set2', legend=False, ax=ax)
    st.pyplot(fig)

st.markdown("""
**📝 Insight Pembayaran:**
- Metode paling populer: ShopeePay dan COD.
- Sebagian besar transaksi sukses. Gagal bayar berkorelasi dengan status pesanan tertentu.
""")


# --------------------------------------------
# 📦 Section 4: Produk
# --------------------------------------------
st.header("📦 Produk")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Jumlah Produk per Kategori")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(data=df_products, y='category',hue='category',
                  order=df_products['category'].value_counts().index,
                  palette='viridis', ax=ax)
    st.pyplot(fig)

with col2:
    st.subheader("Distribusi Harga Produk")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(df_products['price'], bins=40, kde=True, color='teal', ax=ax)
    st.pyplot(fig)

col = st.columns([1])[0]  # atau bisa [0.8] biar sempit
st.subheader("Distribusi Rating Produk")
fig, ax = plt.subplots(figsize=(6, 4))
sns.histplot(df_products['rating'], bins=20, kde=True, color='salmon', ax=ax)
st.pyplot(fig)

st.markdown("""
**📝 Insight Produk:**
- Produk terbanyak berasal dari kategori Fashion & Elektronik.
- Sebagian besar harga produk di bawah Rp1 juta.
- Rating produk cenderung tinggi, menunjukkan kepuasan pelanggan.
""")


# --------------------------------------------
# 🧾 Section 5: Order Items
# --------------------------------------------
st.header("🧾 Order Items")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Jumlah Produk per Order")
    produk_per_order = df_items.groupby('order_id').size().reset_index(name='jumlah_produk')
    fig, ax = plt.subplots(figsize=(6, 3.5))
    sns.histplot(produk_per_order['jumlah_produk'], bins=10, kde=True, color='skyblue', ax=ax)
    st.pyplot(fig)

with col2:
    st.subheader("Kategori Produk Terpopuler")
    top_kat = df_items['category'].value_counts().nlargest(10)
    fig, ax = plt.subplots(figsize=(6, 3.5))
    sns.barplot(x=top_kat.values, y=top_kat.index, palette='viridis', ax=ax,hue=top_kat.index)
    st.pyplot(fig)

col = st.columns([1])[0]  # atau bisa [0.8] biar sempit
st.subheader("Boxplot Kuantitas Produk per Order Line")
fig, ax = plt.subplots(figsize=(6, 3.5))
sns.boxplot(data=df_items, x='quantity', color='salmon', ax=ax)
st.pyplot(fig)

st.markdown("""
**📝 Insight Order Items:**
- Mayoritas pesanan terdiri dari 1–2 produk.
- Kategori terpopuler: Elektronik & Fashion.
- Terdapat outlier pembelian dalam jumlah besar (bulk order).
""")
