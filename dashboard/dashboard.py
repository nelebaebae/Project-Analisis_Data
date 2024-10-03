import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
reviews_per_category = pd.read_csv("dashboard/reviews_per_category.csv")
payments_per_method_month_full = pd.read_csv("dashboard/filtered_payments_per_method_month.csv")
top_10_fastest_shipping = pd.read_csv("dashboard/top_10_fastest_shipping.csv")

st.title("E-commerce Analytics Dashboard")

# Plot 1: Correlation between Review Count and Customer Satisfaction
st.header("Korelasi antara Jumlah Ulasan dan Tingkat Kepuasan Pelanggan per Kategori Produk")
reviews_per_category = reviews_per_category.sort_values(by='review_id', ascending=False)
plt.figure(figsize=(12, 6))
sns.scatterplot(data=reviews_per_category, x='review_id', y='review_score', size='review_id', sizes=(40, 200), hue='review_score', palette='viridis', legend=False)
plt.title('Korelasi antara Jumlah Ulasan dan Tingkat Kepuasan Pelanggan per Kategori Produk')
plt.xlabel('Jumlah Ulasan')
plt.ylabel('Rata-rata Skor Ulasan')
plt.tight_layout()
st.pyplot(plt)
correlation_value = reviews_per_category['review_id'].corr(reviews_per_category['review_score'])
st.write(f"Korelasi antara jumlah ulasan dan skor kepuasan: {correlation_value:.3f}")

# Plot 2: Orders by Payment Method
st.header("Jumlah Pesanan per Metode Pembayaran (Per Bulan)")
payments_per_method_month_full['order_month'] = payments_per_method_month_full['order_month'].astype(str)
filtered_payments_per_method_month = payments_per_method_month_full[
    ~payments_per_method_month_full['order_month'].isin(['2018-09', '2018-10']) &
    (payments_per_method_month_full['payment_type'] != 'not_defined')
]
plt.figure(figsize=(14, 7))
sns.lineplot(data=filtered_payments_per_method_month, x='order_month', y='order_id', hue='payment_type', marker='o')
plt.title('Jumlah Pesanan per Metode Pembayaran (Per Bulan)')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Pesanan')
plt.xticks(rotation=45)
plt.legend(title='Metode Pembayaran')
plt.tight_layout()
st.pyplot(plt)

# Plot 3: Top 10 Fastest Shipping Categories
st.header("Top 10 Kategori Produk dengan Waktu Pengiriman Tercepat (6 bulan terakhir)")
fig, ax1 = plt.subplots(figsize=(12, 6))
sns.barplot(x='product_category_name', y='average_shipping_time_days', data=top_10_fastest_shipping, palette='Blues_d', ax=ax1)

ax1.set_xlabel('Kategori Produk')
ax1.set_ylabel('Waktu Pengiriman Rata-rata (Hari)')
ax1.set_title('Top 10 Kategori Produk dengan Waktu Pengiriman Tercepat')

ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90)

ax2 = ax1.twinx()
sns.lineplot(x='product_category_name', y='total_sales', data=top_10_fastest_shipping, color='orange', marker="o", ax=ax2)

ax2.set_ylabel('Total Penjualan')

ax2.legend(['Total Penjualan'], loc='upper left')
fig.tight_layout()

st.pyplot(fig)

