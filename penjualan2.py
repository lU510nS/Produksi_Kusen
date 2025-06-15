import streamlit as st
from scipy.optimize import linprog
import math

# Judul aplikasi
st.title("Optimasi Produksi Meja dan Kursi")
st.write("PT. Satyamitra Kemas Lestari ingin memaksimalkan keuntungan dari produksi meja dan kursi.")

# Input dari user
keuntungan_meja = st.number_input("Keuntungan per Meja (Rp)", value=20000)
keuntungan_kursi = st.number_input("Keuntungan per Kursi (Rp)", value=10000)
waktu_meja = st.number_input("Waktu Produksi per Meja (menit)", value=45)
waktu_kursi = st.number_input("Waktu Produksi per Kursi (menit)", value=30)
total_waktu = st.number_input("Total Waktu Produksi per Minggu (jam)", value=48)

# Konversi jam ke menit
total_menit = total_waktu * 60

# Fungsi objektif (maksimasi → minimisasi)
c = [-keuntungan_meja, -keuntungan_kursi]

# Kendala: waktu produksi
A = [[waktu_meja, waktu_kursi]]
b = [total_menit]

# Batasan non-negatif
x_bounds = (0, None)
y_bounds = (0, None)

# Optimasi dengan linprog
result = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

# Tampilkan hasil
if result.success:
    x_real = result.x[0]
    y_real = result.x[1]
    # Bulatkan ke bawah agar tetap feasible
    x_int = math.floor(x_real)
    y_int = math.floor(y_real)
    total_profit = keuntungan_meja * x_int + keuntungan_kursi * y_int
    total_unit = x_int + y_int

    st.subheader("Hasil Optimasi Produksi:")
    st.write(f"Jumlah Meja yang diproduksi: **{x_int}** unit")
    st.write(f"Jumlah Kursi yang diproduksi: **{y_int}** unit")
    st.write(f"Total Unit Diproduksi: **{total_unit}** unit")
    st.write(f"Total Keuntungan Maksimal: **Rp {total_profit:,.0f}**")
else:
    st.error("Optimasi gagal dilakukan.")
