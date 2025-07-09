import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Setup
st.set_page_config(layout="centered", page_title="Shopee Customer Behavior Dashboard")

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
# Letakkan legend di luar plot (kanan)
ax.legend(title='Gender', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout(rect=[0, 0, 0.85, 1])  # Sisakan ruang di kanan
st.pyplot(fig)




# --------------------------------------------
# 📦 Section 2: Orders
# --------------------------------------------
st.header("🛒 Pesanan")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Status Pesanan")
    fig, ax = plt.subplots(figsize=(6, 3.5))
    sns.countplot(data=df_orders, x='status', hue='status', palette='Set1', legend=False, ax=ax)
    fig.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("Jumlah Pesanan per Bulan")
    df_orders['month'] = df_orders['order_date'].dt.to_period("M").astype(str)
    monthly_orders = df_orders.groupby('month').size().reset_index(name='order_count')

    fig, ax = plt.subplots(figsize=(6, 3.5))
    sns.lineplot(data=monthly_orders, x='month', y='order_count', marker='o', ax=ax)

    # Set setiap 5 bulan sebagai label
    step = 5
    xticks_pos = range(0, len(monthly_orders), step)
    ax.set_xticks(xticks_pos)
    ax.set_xticklabels(monthly_orders['month'].iloc[xticks_pos], rotation=30)

    fig.tight_layout()
    st.pyplot(fig)


st.subheader("Durasi Pengiriman")
df_orders['delivery_days'] = (df_orders['estimated_delivery'] - df_orders['order_date']).dt.days
fig, ax = plt.subplots(figsize=(6, 3.5))
sns.histplot(df_orders['delivery_days'], bins=10, kde=True, color='orange', ax=ax)
st.pyplot(fig)



# --------------------------------------------
# 💳 Section 3: Payments
# --------------------------------------------
st.header("💳 Pembayaran")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Metode Pembayaran")
    fig, ax = plt.subplots(figsize=(6, 3.5))
    sns.countplot(data=df_payments, x='payment_method',
                  hue='payment_method', palette='cool', legend=False, ax=ax)
    ax.set_xticks(range(len(df_payments['payment_method'].unique())))  # pastikan tick sesuai jumlah unik
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30)
    fig.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("Status Pembayaran")
    fig, ax = plt.subplots(figsize=(6, 3.5))
    sns.countplot(data=df_payments, x='payment_status',
                  hue='payment_status', palette='Set2', legend=False, ax=ax)
    fig.tight_layout()
    st.pyplot(fig)




# --------------------------------------------
# 📦 Section 4: Produk
# --------------------------------------------
st.header("📦 Produk")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Jumlah Produk/Kategori")
    # Drop kategori NaN untuk menghindari warning
    df_products_clean = df_products.dropna(subset=['category'])
    fig, ax = plt.subplots(figsize=(6, 4))
    plot = sns.countplot(
        data=df_products_clean,
        y='category',
        order=df_products_clean['category'].value_counts().index,
        palette='viridis',
        ax=ax,
        hue='category'
    )
    fig.tight_layout()
    st.pyplot(fig)


with col2:
    st.subheader("Distribusi Harga Produk")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(df_products['price'], bins=40, kde=True, color='teal', ax=ax)
    fig.tight_layout()
    st.pyplot(fig)

st.subheader("Distribusi Rating Produk")
fig, ax = plt.subplots(figsize=(6, 4))
sns.histplot(df_products['rating'], bins=20, kde=True, color='salmon', ax=ax)
st.pyplot(fig)


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
    ax.set_xlabel("Jumlah Produk per Order")
    ax.set_ylabel("Jumlah Order")
    fig.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("Produk Terpopuler")
    top_kat = df_items['category'].value_counts().nlargest(10).reset_index()
    top_kat.columns = ['category', 'count']
    # Pastikan tidak ada NaN
    top_kat = top_kat.dropna()
    fig, ax = plt.subplots(figsize=(6, 3.5))
    bar = sns.barplot(
        data=top_kat,
        x='count',
        y='category',
        palette='viridis',
        ax=ax,
        hue='category'
    )
    ax.set_xlabel("Jumlah Pembelian")
    ax.set_ylabel("Kategori Produk")
    fig.tight_layout()
    st.pyplot(fig)



st.subheader("Boxplot Kuantitas Produk per Order Line")
fig, ax = plt.subplots(figsize=(6, 3.5))
sns.boxplot(data=df_items, x='quantity', color='salmon', ax=ax)
st.pyplot(fig)



st.markdown("""
## 🗂️ Tentang Dataset

Dataset ini merupakan simulasi transaksi Shopee yang terdiri dari 5 tabel utama:  
**Users**, **Orders**, **Products**, **Payments**, dan **Order Items**.  
Analisis dilakukan untuk menggali pola perilaku pelanggan, tren penjualan, logistik, dan preferensi pembayaran.

---

## 📊 Ringkasan Temuan Utama

- **👤 Pengguna**:  
  Dominasi usia 18–35 tahun, sebaran gender merata, pengguna terkonsentrasi di kota besar (Jakarta, Surabaya, Bandung).

- **🛒 Pesanan**:  
  Mayoritas berstatus *delivered*, tren bulanan meningkat, rata-rata pengiriman 3–5 hari.

- **💳 Pembayaran**:  
  ShopeePay & COD paling populer, tingkat keberhasilan transaksi tinggi.

- **📦 Produk**:  
  Terbanyak di kategori Fashion & Elektronik, harga mayoritas < Rp1 juta, rating tinggi.

- **🧾 Order Items**:  
  Mayoritas order berisi 1–2 item, terdapat indikasi bulk purchase.

---

## 💼 Rekomendasi Strategis

1. **Fokus promosi** di kota besar & usia produktif.  
2. **Optimalkan** kategori Fashion & Elektronik.  
3. **Tingkatkan layanan** pengiriman & estimasi real-time.  
4. **Dorong penggunaan** ShopeePay & COD dengan insentif.  
5. **Fasilitasi pembelian grosir** dengan fitur & ongkir khusus.

---
""")


st.markdown("## 📊 Statistik Deskriptif Dataset")

with st.expander("🔍 Lihat Statistik Data Numerik"):
    st.markdown("### 👤 Pengguna (Users)")
    st.dataframe(df_users[['age']].describe().T.style.format("{:.2f}"))

    st.markdown("### 📦 Produk (Products)")
    st.dataframe(df_products[['price', 'rating']].describe().T.style.format("{:.2f}"))

    st.markdown("### 🧾 Order Items")
    st.dataframe(df_items[['quantity']].describe().T.style.format("{:.2f}"))

    st.markdown("### 🛒 Pesanan (Durasi Pengiriman)")
    df_orders['delivery_days'] = (df_orders['estimated_delivery'] - df_orders['order_date']).dt.days
    st.dataframe(df_orders[['delivery_days']].describe().T.style.format("{:.2f}"))

st.markdown("""
### 👨‍💻 Developer

Dashboard ini dikembangkan oleh **Ahmad Nur Ikhsan**, Data Analyst & Developer.  
📧 Email: [ahmadnurikhsan079@email.com](mailto:ahmadnurikhsan079@email.com)  
🌐 Website: [anikhsan.netlify.app](https://anikhsan.netlify.app)  
🔗 GitHub: [github.com/sandive24](https://github.com/sandive24)  
💼 LinkedIn: [linkedin.com/in/sandive24](https://linkedin.com/in/sandive24)
""")
