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

# Fungsi objektif untuk maksimisasi (linprog → minimisasi → dikalikan -1)
c = [-keuntungan_meja, -keuntungan_kursi]

# Kendala: waktu produksi meja dan kursi tidak boleh melebihi waktu total
A = [[waktu_meja, waktu_kursi]]
b = [total_menit]

# Batasan non-negatif
x_bounds = (0, None)
y_bounds = (0, None)

# Optimasi
result = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

# Tampilkan hasil
if result.success:
    # Hasil dari linprog
    x_real = result.x[0]
    y_real = result.x[1]

    # Bulatkan ke bawah agar tetap feasible
    x = math.floor(x_real)
    y = math.floor(y_real)

    # Hitung total waktu yang digunakan dan sisa
    waktu_digunakan = (x * waktu_meja) + (y * waktu_kursi)
    sisa_waktu = total_menit - waktu_digunakan

    # Hitung keuntungan
    profit_meja = x * keuntungan_meja
    profit_kursi = y * keuntungan_kursi
    total_profit = profit_meja + profit_kursi
    total_unit = x + y

    # Tampilkan hasil
    st.subheader("📦 Hasil Produksi Optimal")
    st.write(f"- Jumlah Meja yang diproduksi: **{x} unit**")
    st.write(f"- Jumlah Kursi yang diproduksi: **{y} unit**")
    st.write(f"- Total Unit Diproduksi: **{total_unit} unit**")
    st.write(f"- Total Waktu Digunakan: **{waktu_digunakan} menit**")
    st.write(f"- Sisa Waktu Tersedia: **{sisa_waktu} menit**")

    st.subheader("💰 Rincian Keuntungan")
    st.write(f"- Keuntungan per Meja: **Rp {keuntungan_meja:,.0f}** × {x} = **Rp {profit_meja:,.0f}**")
    st.write(f"- Keuntungan per Kursi: **Rp {keuntungan_kursi:,.0f}** × {y} = **Rp {profit_kursi:,.0f}**")
    st.success(f"🎯 Total Keuntungan Maksimal: **Rp {total_profit:,.0f}**")
else:
    st.error("Optimasi gagal dilakukan.")
