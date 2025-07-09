import mysql.connector
import pandas as pd
import os
import math

# 🔌 Koneksi ke MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',  # ← Ganti jika pakai password
    database='shopee_analytics'
)
cursor = conn.cursor()

# 📂 Folder data
DATA_DIR = os.path.join("shopee-analytics", "data", "raw")

# 🔁 Fungsi insert batch
def insert_from_csv(table, filename, batch_size=1000):
    path = os.path.join(DATA_DIR, filename)
    df = pd.read_csv(path)

    cols = ', '.join(df.columns)
    placeholders = ', '.join(['%s'] * len(df.columns))
    sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"

    data = [tuple(row) for row in df.values]
    total = len(data)
    num_batches = math.ceil(total / batch_size)

    print(f"🔄 Insert {total} baris ke tabel '{table}' dalam {num_batches} batch...")

    for i in range(0, total, batch_size):
        batch = data[i:i + batch_size]
        cursor.executemany(sql, batch)
        conn.commit()
        print(f"✅ Batch {i // batch_size + 1}/{num_batches} berhasil")

    print(f"🎉 Semua data '{table}' berhasil dimasukkan ({total} baris)\n")

# 🚀 Eksekusi insert semua tabel
insert_from_csv('users', 'users.csv')
insert_from_csv('products', 'products.csv')
insert_from_csv('orders', 'orders.csv')
insert_from_csv('order_items', 'order_items.csv')
insert_from_csv('payments', 'payments.csv')

# 🔒 Tutup koneksi
cursor.close()
conn.close()
print("✅ Semua data selesai dimasukkan ke MySQL!")
