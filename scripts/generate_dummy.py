import pandas as pd
import random
from faker import Faker
from datetime import timedelta
import os

fake = Faker('id_ID')

# USERS
def generate_users(n=5000):
    data = []
    for i in range(1, n+1):
        gender = random.choice(['Male', 'Female'])
        name = fake.name_male() if gender == 'Male' else fake.name_female()
        age = random.randint(17, 55)
        city = random.choice(['Jakarta', 'Bandung', 'Surabaya', 'Medan', 'Makassar'])
        join_date = fake.date_between(start_date='-3y', end_date='today')
        data.append([f"U{i:05}", name, gender, age, city, join_date])
    return pd.DataFrame(data, columns=['user_id', 'name', 'gender', 'age', 'city', 'join_date'])

# PRODUCTS
def generate_products(n=500):
    categories = ['Elektronik', 'Fashion', 'Rumah Tangga', 'Kecantikan', 'Makanan & Minuman']
    data = []
    for i in range(1, n+1):
        cat = random.choice(categories)
        name = f"{fake.word().capitalize()} {cat} {random.randint(100,999)}"
        price = random.randint(25000, 3000000)
        rating = round(random.uniform(3.0, 5.0), 2)
        data.append([f"P{i:04}", name, cat, price, rating])
    return pd.DataFrame(data, columns=['product_id', 'name', 'category', 'price', 'rating'])

# ORDERS + ORDER_ITEMS + PAYMENTS
def generate_orders(users_df, products_df, n_orders=20000):
    orders, items, payments = [], [], []

    for i in range(1, n_orders+1):
        order_id = f"O{i:06}"
        user = users_df.sample(1).iloc[0]
        user_id = user['user_id']
        order_date = fake.date_between(start_date=user['join_date'], end_date='today')
        status = random.choices(['delivered', 'canceled', 'returned'], [0.85, 0.1, 0.05])[0]
        estimated = order_date + timedelta(days=random.randint(2, 7))
        orders.append([order_id, user_id, order_date, status, estimated])

        # order items
        chosen_items = products_df.sample(random.randint(1, 4))
        total_payment = 0
        for _, p in chosen_items.iterrows():
            qty = random.randint(1, 5)
            total_payment += p['price'] * qty
            items.append([order_id, p['product_id'], p['category'], qty, p['price']])

        method = random.choice(['ShopeePay', 'COD', 'Transfer Bank', 'Kartu Kredit'])
        pay_status = 'success' if status == 'delivered' else 'failed'
        payments.append([order_id, method, total_payment, pay_status])

    return (
        pd.DataFrame(orders, columns=['order_id', 'user_id', 'order_date', 'status', 'estimated_delivery']),
        pd.DataFrame(items, columns=['order_id', 'product_id', 'category', 'quantity', 'price']),
        pd.DataFrame(payments, columns=['order_id', 'payment_method', 'payment_amount', 'payment_status']),
    )

# SIMPAN SEMUA
def save_all():
    print("🔧 Membuat data dummy Shopee...")

    users = generate_users()
    products = generate_products()
    orders, order_items, payments = generate_orders(users, products)

    # Path direktori
    output_path = os.path.join("shopee-analytics", "data", "raw")
    os.makedirs(output_path, exist_ok=True)

    users.to_csv(os.path.join(output_path, "users.csv"), index=False)
    products.to_csv(os.path.join(output_path, "products.csv"), index=False)
    orders.to_csv(os.path.join(output_path, "orders.csv"), index=False)
    order_items.to_csv(os.path.join(output_path, "order_items.csv"), index=False)
    payments.to_csv(os.path.join(output_path, "payments.csv"), index=False)

    print("✅ Semua data dummy disimpan ke: shopee-analytics/data/raw")

if __name__ == "__main__":
    save_all()
