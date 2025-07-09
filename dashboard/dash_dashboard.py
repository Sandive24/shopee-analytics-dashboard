import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load data
df_users = pd.read_csv('../data/raw/users.csv')
df_orders = pd.read_csv('../data/raw/orders.csv', parse_dates=['order_date', 'estimated_delivery'])
df_products = pd.read_csv('../data/raw/products.csv')
df_payments = pd.read_csv('../data/raw/payments.csv')
df_order_items = pd.read_csv('../data/raw/order_items.csv')

# ------ Grafik Pengguna ------
fig_gender = px.histogram(df_users, x='gender', title='Distribusi Gender Pengguna')

fig_age = px.histogram(df_users, x='age', nbins=30, title='Distribusi Usia Pengguna')

top10_city = df_users['city'].value_counts().nlargest(10).index
df_top_city = df_users[df_users['city'].isin(top10_city)]
fig_city_gender = px.histogram(df_top_city, x='city', color='gender',
                               category_orders={'city': top10_city.tolist()},
                               title='Top 10 Kota Asal Pengguna (dengan Gender)')

# ------ Grafik Orders ------
fig_order_status = px.pie(df_orders, names='status', title='Status Pesanan')

df_orders['month'] = df_orders['order_date'].dt.to_period("M").astype(str)
monthly_orders = df_orders.groupby('month').size().reset_index(name='order_count')
fig_monthly = px.line(monthly_orders, x='month', y='order_count',
                      markers=True, title='Jumlah Pesanan per Bulan')

df_orders['delivery_days'] = (df_orders['estimated_delivery'] - df_orders['order_date']).dt.days
fig_delivery_days = px.histogram(df_orders, x='delivery_days', nbins=15,
                                 title='Durasi Pengiriman (Hari)')

# ------ Grafik Pembayaran ------
df_payment_counts = df_payments['payment_method'].value_counts().reset_index()
df_payment_counts.columns = ['payment_method', 'count']
fig_payment_method = px.bar(df_payment_counts, x='payment_method', y='count',
                            title='Metode Pembayaran Populer')

fig_payment_status = px.histogram(df_payments, x='payment_status',
                                  title='Distribusi Status Pembayaran')

# ------ Grafik Produk ------
top_categories = df_products['category'].value_counts().nlargest(10).reset_index()
top_categories.columns = ['category', 'count']
fig_product_cat = px.bar(top_categories, x='count', y='category', orientation='h',
                         title='Top 10 Kategori Produk')

fig_price = px.histogram(df_products, x='price', nbins=40, title='Distribusi Harga Produk')
fig_rating = px.histogram(df_products, x='rating', nbins=20, title='Distribusi Rating Produk')

# ------ Grafik Order Items ------
produk_per_order = df_order_items.groupby('order_id').size().reset_index(name='jumlah_produk')
fig_produk_per_order = px.histogram(produk_per_order, x='jumlah_produk',
                                    title='Jumlah Produk per Order')

kategori_top = df_order_items['category'].value_counts().nlargest(10).reset_index()
kategori_top.columns = ['category', 'count']
fig_kategori_dipesan = px.bar(kategori_top, x='count', y='category', orientation='h',
                              title='Kategori yang Paling Sering Dipesan')

fig_box_qty = px.box(df_order_items, x='quantity', title='Boxplot Kuantitas Produk per Order')

# ------ Layout ------
app = dash.Dash(__name__)
app.title = "Shopee Dashboard"

app.layout = html.Div([
    html.H1("📦 Shopee Analytics Dashboard", style={'textAlign': 'center'}),

    html.H2("👤 Pengguna"),
    html.Div([
        html.Div(dcc.Graph(figure=fig_gender), className='six columns'),
        html.Div(dcc.Graph(figure=fig_age), className='six columns')
    ], className='row'),
    dcc.Graph(figure=fig_city_gender),

    html.H2("🛒 Orders"),
    html.Div([
        html.Div(dcc.Graph(figure=fig_order_status), className='six columns'),
        html.Div(dcc.Graph(figure=fig_monthly), className='six columns')
    ], className='row'),
    dcc.Graph(figure=fig_delivery_days),

    html.H2("💳 Pembayaran"),
    html.Div([
        html.Div(dcc.Graph(figure=fig_payment_method), className='six columns'),
        html.Div(dcc.Graph(figure=fig_payment_status), className='six columns')
    ], className='row'),

    html.H2("📦 Produk"),
    html.Div([
        html.Div(dcc.Graph(figure=fig_product_cat), className='six columns'),
        html.Div(dcc.Graph(figure=fig_price), className='six columns')
    ], className='row'),
    dcc.Graph(figure=fig_rating),

    html.H2("🧾 Order Items"),
    html.Div([
        html.Div(dcc.Graph(figure=fig_produk_per_order), className='six columns'),
        html.Div(dcc.Graph(figure=fig_kategori_dipesan), className='six columns')
    ], className='row'),
    dcc.Graph(figure=fig_box_qty)
], style={'padding': '20px'})

# Jalankan App
if __name__ == '__main__':
    app.run(debug=True)
