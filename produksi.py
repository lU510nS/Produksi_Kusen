import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# Sidebar instruksi
st.sidebar.title("📘 Instruksi Penggunaan")
st.sidebar.info("""
1. Pilih model matematika dari tab di atas.
2. Masukkan parameter sesuai kebutuhan.
3. Hasil perhitungan dan grafik akan ditampilkan secara otomatis.
""")

# Tab menu utama
tab1, tab2, tab3 = st.tabs(["🧮 Optimasi Produksi", "📦 EOQ (Persediaan)", "👥 Model Antrian"])

# 1. Optimasi Produksi
with tab1:
    st.header("Model Optimasi Produksi")
    st.write("Gunakan metode *Linear Programming* untuk menentukan jumlah produk yang maksimal dengan batasan sumber daya.")

    c = [-40, -60]  # Koefisien fungsi objektif (negatif karena linprog meminimalkan)
    A = [[2, 3]]  # Koefisien kendala
    b = [100]  # Batasan kendala

    res = linprog(c, A_ub=A, b_ub=b, bounds=[(0, None), (0, None)], method='highs')
    
    if res.success:
        x, y = res.x
        st.success(f"Jumlah Blender (x): {x:.2f}")
        st.success(f"Jumlah Pemanggang Roti (y): {y:.2f}")
        st.info(f"Total Keuntungan Maksimum: Rp{(-res.fun)*1000:,.0f}")

        # Visualisasi grafik batasan
        st.subheader("Visualisasi Batasan")
        x_vals = np.linspace(0, 60, 200)
        y_vals = (100 - 2 * x_vals) / 3
        plt.figure()
        plt.plot(x_vals, y_vals, label="2x + 3y = 100")
        plt.fill_between(x_vals, 0, y_vals, alpha=0.3)
        plt.xlabel("Produk A (Blender)")
        plt.ylabel("Produk B (Pemanggang Roti)")
        plt.axhline(0)
        plt.axvline(0)
        plt.scatter(x, y, color='red', label='Solusi Optimal')
        plt.legend()
        st.pyplot(plt)

# 2. EOQ
with tab2:
    st.header("Model Persediaan EOQ")
    D = st.number_input("Permintaan tahunan (D)", value=10000)
    S = st.number_input("Biaya pemesanan (S)", value=50000)
    H = st.number_input("Biaya penyimpanan/unit/tahun (H)", value=2000)

    EOQ = np.sqrt((2 * D * S) / H)
    st.success(f"Jumlah optimal pemesanan (EOQ): {EOQ:.2f} unit")

    # Visualisasi kurva biaya total
    st.subheader("Grafik Biaya Total vs Ukuran Pesanan")
    Q = np.linspace(100, 2000, 200)
    TC = (D/Q)*S + (Q/2)*H
    plt.figure()
    plt.plot(Q, TC, label='Total Cost')
    plt.axvline(EOQ, color='red', linestyle='--', label='EOQ')
    plt.xlabel("Ukuran Pesanan")
    plt.ylabel("Biaya Total")
    plt.legend()
    st.pyplot(plt)

# 3. Antrian M/M/1
with tab3:
    st.header("Model Antrian M/M/1")
    λ = st.number_input("Rata-rata kedatangan pelanggan per jam (λ)", value=10.0)
    μ = st.number_input("Rata-rata pelayanan pelanggan per jam (μ)", value=12.0)

    if λ >= μ:
        st.error("Sistem tidak stabil! λ harus lebih kecil dari μ.")
    else:
        ρ = λ / μ
        L = ρ / (1 - ρ)
        W = 1 / (μ - λ)
        Wq = λ / (μ * (μ - λ))

        st.info(f"Tingkat Utilisasi Server (ρ): {ρ:.2f}")
        st.info(f"Rata-rata pelanggan dalam sistem (L): {L:.2f}")
        st.info(f"Rata-rata waktu dalam sistem (W): {W:.2f} jam")
        st.info(f"Rata-rata waktu tunggu dalam antrean (Wq): {Wq:.2f} jam")

        # Visualisasi utilisasi
        st.subheader("Visualisasi Utilisasi Server")
        mu_vals = np.linspace(λ + 0.1, 2*λ, 200)
        rho_vals = λ / mu_vals
        plt.figure()
        plt.plot(mu_vals, rho_vals, label="Utilisasi (ρ)")
        plt.axhline(1, color='red', linestyle='--')
        plt.xlabel("μ (Kecepatan Pelayanan)")
        plt.ylabel("ρ (Utilisasi)")
        st.pyplot(plt)
