# 📦 Shopee Analytics Dashboard

Dashboard interaktif untuk menganalisis data e-commerce Shopee. Dibangun menggunakan **Streamlit**, **Pandas**, dan **Seaborn**, proyek ini membantu mengeksplorasi pola perilaku pelanggan, tren penjualan, performa produk, serta metode pembayaran secara visual dan informatif.

---

## 🔍 Fitur Utama

* **Analisis Pengguna**
  Distribusi gender, usia, dan kota dengan pengguna terbanyak.

* **Analisis Pesanan**
  Status pesanan, tren bulanan, dan durasi pengiriman.

* **Analisis Pembayaran**
  Distribusi metode pembayaran dan status pembayaran.

* **Analisis Produk**
  Kategori produk, distribusi harga, dan rating produk.

* **Analisis Order Items**
  Jumlah produk per pesanan, kategori populer, dan distribusi kuantitas.

---

## 📂 Struktur Proyek

```
shopee-analytics/
│
├── data/
│   └── raw/
│       ├── users.csv
│       ├── orders.csv
│       ├── products.csv
│       ├── payments.csv
│       └── order_items.csv
│
├── dashboard/
│   └── streamlit_dashboard.py
│
├── utils/
│   └── plot_helper.py         # (opsional) helper visualisasi
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Cara Menjalankan

1. **Kloning repositori:**

   ```bash
   git clone https://github.com/username/shopee-analytics.git
   cd shopee-analytics
   ```

2. **Aktifkan virtual environment:**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   ```

3. **Instal dependensi:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan aplikasi Streamlit:**

   ```bash
   streamlit run dashboard/streamlit_dashboard.py
   ```

5. **Akses dashboard:**
   Buka browser ke: [Dashboard](anikhsan.streamlit.app)

---

## 📦 Dependensi Utama

* [pandas](https://pandas.pydata.org/)
* [streamlit](https://streamlit.io/)
* [seaborn](https://seaborn.pydata.org/)
* [matplotlib](https://matplotlib.org/)

Instalasi otomatis melalui `requirements.txt`.

---

## 📝 Catatan

* File CSV harus tersedia di direktori `data/raw/`.
* Pastikan struktur dan nama kolom sesuai dengan file contoh.
* Proyek ini dikembangkan sebagai prototipe dan dapat dikembangkan lebih lanjut untuk integrasi database, deployment cloud, atau penambahan fitur interaktif.

---

## 📌 Lisensi

Proyek ini bersifat open-source dan tersedia di bawah lisensi [MIT](LICENSE).

---

## 🙌 Kontribusi

Kontribusi sangat terbuka! Silakan fork repo ini, buat branch baru, dan ajukan pull request jika ingin menambahkan fitur atau perbaikan.

---
