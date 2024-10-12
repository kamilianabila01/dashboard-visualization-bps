import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io

# File logo lokal atau URL gambar
logo_path1 = "/workspaces/dashboard-visualization-bps/logo_bps-removebg-preview.png"
logo_path2 = "/workspaces/dashboard-visualization-bps/logo_mojokerto-removebg-preview.png"


col1, col2, col3 = st.columns([8, 1, 1])
with col1:
    st.write("")

with col2:
    st.image(logo_path1, width=100)  # Gambar pertama dengan lebar 100px

with col3:
    st.image(logo_path2, width=100)  # Gambar kedua dengan lebar 100px

#  HTML dan CSS untuk menampilkan dua logo di pojok kanan atas
st.markdown(
    f"""
    <style>
    .logo-container {{
        display: flex;
        justify-content: flex-end;
        position: fixed;
        top: 0;
        right: 0;
        width: auto;
        height: 100px;
    }}
    .logo-container img {{
        width: 1cm;
        height: 1cm;
        margin-left: 500px;  #Jarak antara kedua gambar
    }}
    </style>
    <div class="logo-container">
        <img src="{logo_path1}" alt="Logo 1">
        <img src="{logo_path2}" alt="Logo 2">
    </div>
    """,
    unsafe_allow_html=True
)

# Dictionary untuk memetakan jenis data ke judul dan file path
data_files = {
    'PDRB': {
        'PDRB Atas Dasar Harga Berlaku Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023': [
            '/workspaces/dashboard-visualization-bps/PDRB Pengeluaran Publikasi Softfile/PDRB Atas Dasar Harga Berlaku Menurut Komponen Pengeluaran, Kota Mojokerto 2019-2023.xlsx',
        ],
        'Distribusi PDRB Atas Dasar Harga Berlaku Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023': [
            '/workspaces/dashboard-visualization-bps/PDRB Pengeluaran Publikasi Softfile/Distribusi PDRB Atas Dasar Harga Berlaku Menurut Komponen Pengeluaran Kota Mojokerto 2019–2023.xlsx',
        ],
        'Laju Pertumbuhan PDRB ADHK 2010 Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023': [
            '/workspaces/dashboard-visualization-bps/PDRB Pengeluaran Publikasi Softfile/Laju Pertumbuhan PDRB ADHK 2010 Menurut Komponen Pengeluaran Kota Mojokerto, 2019- 2023.xlsx',
        ],
        'Indeks Implisit PDRB Menurut Pengeluaran Kota Mojokerto, 2019-2023': [
            '/workspaces/dashboard-visualization-bps/PDRB Pengeluaran Publikasi Softfile/Indeks Implisit PDRB Menurut Pengeluaran Kota Mojokerto, 2019-2023.xlsx',
        ],
        'Pertumbuhan Indeks Implisit PDRB Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023': [
            '/workspaces/dashboard-visualization-bps/PDRB Pengeluaran Publikasi Softfile/Pertumbuhan Indeks Implisit PDRB Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023.xlsx',
        ],
        'Perkembangan Komponen Konsumsi Rumah Tangga Kota Mojokerto, 2019-2023': [
            '/workspaces/dashboard-visualization-bps/PDRB Pengeluaran Publikasi Softfile/Perkembangan Komponen Konsumsi Rumah Tangga Kota Mojokerto, 2019-2023.xlsx',
        ],
        'Perkembangan Pengeluaran Konsumsi Akhir Pemerintah Kota Mojokerto, 2019-2023': [
            '/workspaces/dashboard-visualization-bps/PDRB Pengeluaran Publikasi Softfile/Perkembangan Pengeluaran Konsumsi Akhir Pemerintah Kota Mojokerto, 2019-2023.xlsx',
        ],
        'Laju Indeks Harga Implisit PDRB Kota Mojokerto Menurut Pengeluaran 2011-2023': [
            '/workspaces/dashboard-visualization-bps/PDRB Pengeluaran Yang Ada/Laju Indeks Harga Implisit PDRB Kota Mojokerto Menurut Pengeluaran 2011-2023.xlsx',
        ],
        'Distribusi PDRB Kota Mojokerto Atas Dasar Harga Berlaku Menurut Pengeluaran 2010-2023': [
            '/workspaces/dashboard-visualization-bps/PDRB Pengeluaran Yang Ada/Distribusi PDRB Kota Mojokerto Atas Dasar Harga Berlaku Menurut Pengeluaran 2010-2023.xlsx',
        ],
        'Distribusi Persentase Produk Domestik Regional Bruto Kota Mojokerto Atas Dasar Harga Berlaku Menurut Lapangan Usaha, 2019─2023': [
            '/workspaces/dashboard-visualization-bps/PDRB Lapangan Usaha Publikasi Softfile/Distribusi Persentase Produk Domestik Regional Bruto Kota Mojokerto Atas Dasar Harga Berlaku Menurut Lapangan Usaha, 2019─2023.xlsx',
        ],
        'Laju Pertumbuhan Produk Domestik Regional Bruto Atas Dasar Harga Konstan 2010 Kota Mojokerto Menurut Lapangan Usaha (persen), 2019─2023': [
            '/workspaces/dashboard-visualization-bps/PDRB Lapangan Usaha Publikasi Softfile/Laju Pertumbuhan Produk Domestik Regional Bruto Atas Dasar Harga Konstan 2010 Kota Mojokerto Menurut Lapangan Usaha (persen), 2019─2023.xlsx',
        ],
        # Tambahkan data PDRB lainnya di sini
    },
    'Kependudukan': {
        'Penduduk, Distribusi Persentase Penduduk, Kepadatan Penduduk, Rasio Jenis Kelamin Penduduk Menurut Kecamatan di Kota Mojokerto, 2023': [
            '/workspaces/dashboard-visualization-bps/Kependudukan Publikasi Softfile/Penduduk, Distribusi Persentase Penduduk, Kepadatan Penduduk, Rasio Jenis Kelamin Penduduk Menurut Kecamatan di Kota Mojokerto, 2023.xlsx',
        ],
        'Penduduk akhir tahun Warga Negara Indonesia menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023': [
            '/workspaces/dashboard-visualization-bps/Kependudukan Publikasi Softfile/Penduduk akhir tahun Warga Negara Indonesia menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto , 2023.xlsx',
        ],
        'Penduduk akhir tahun Warga Negara Asing menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023': [
            '/workspaces/dashboard-visualization-bps/Kependudukan Publikasi Softfile/Penduduk akhir tahun Warga Negara Asing menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto 2023.xlsx',
        ],
        'Jumlah Kelahiran menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023': [
            '/workspaces/dashboard-visualization-bps/Kependudukan Publikasi Softfile/Jumlah Kelahiran menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto , 2023.xlsx',
        ],
        'Jumlah Kematian menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023': [
            '/workspaces/dashboard-visualization-bps/Kependudukan Publikasi Softfile/Jumlah Kematian menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto 2023.xlsx',
        ],
        'Jumlah Penduduk datang menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023': [
            '/workspaces/dashboard-visualization-bps/Kependudukan Publikasi Softfile/Jumlah Penduduk datang menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto 2023.xlsx',
        ],
        'Jumlah Penduduk keluar menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023': [
            '/workspaces/dashboard-visualization-bps/Kependudukan Publikasi Softfile/Jumlah Penduduk keluar menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto 2023.xlsx',
        ],
        'Banyaknya akte kependudukan diterbitkan menurut jenisnya menurut bulan di Kota Mojokerto, 2023': [
            '/workspaces/dashboard-visualization-bps/Kependudukan Publikasi Softfile/Banyaknya akte kependudukan diterbitkan menurut jenisnya menurut bulan di Kota Mojokerto 2023.xlsx',
        ],
        'Kepadatan penduduk akhir tahun Warga Negara Indonesia menurut Kelurahan di Kota Mojokerto, 2023': [
            '/workspaces/dashboard-visualization-bps/Kependudukan Publikasi Softfile/Kepadatan penduduk akhir tahun Warga Negara Indonesia menurut Kelurahan di Kota Mojokerto 2023.xlsx',
        ],
        # Tambahkan data Kependudukan lainnya di sini
    },
    'IPM': {
        'Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah) 2010-2023': [
            '/workspaces/dashboard-visualization-bps/IPM Yang Ada/Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah) 2010-2023.xlsx',
        ],
        'Harapan Lama Sekolah (HLS) 2010-2023': [
            '/workspaces/dashboard-visualization-bps/IPM Yang Ada/Harapan Lama Sekolah (HLS) 2010-2023.xlsx',
        ],
        'Angka Melek Huruf (Persen) 2016-2006': [
            '/workspaces/dashboard-visualization-bps/IPM Yang Ada/Angka Melek Huruf (Persen) 2016-2006.xlsx',
        ],
        'Angka Harapan Hidup Jawa Timur (LF SP2020)': [
            '/workspaces/dashboard-visualization-bps/IPM Yang Ada/Angka Harapan Hidup Jawa Timur (LF SP2020).xlsx',
        ],
        'IPM Jawa Timur 2010-2023': [
            '/workspaces/dashboard-visualization-bps/IPM Yang Ada/IPM Jawa Timur 2010-2023.xlsx',
        ],
        'Indeks Pembangunan Manusia Menurut Kabupaten dan Kota': [
            'IPM Yang Ada/Indeks Pembangunan Manusia Menurut Kabupaten_Kota.xlsx',
        ],
        'Indeks Pembangunan Manusia (UHH LF SP2020)': [
            '/workspaces/dashboard-visualization-bps/IPM Yang Ada/Indeks Pembangunan Manusia (UHH LF SP2020).xlsx',
        ],
        'Angka Melek Huruf (Penduduk Usia 15 +)': [
            '/workspaces/dashboard-visualization-bps/IPM Yang Ada/Angka Melek Huruf (Penduduk Usia 15 +).xlsx',
        ],
        'Indeks Pemberdayaan Gender': [
            '/workspaces/dashboard-visualization-bps/IPM Yang Ada/Indeks Pemberdayaan Gender.xlsx',
        ],
        'Indeks Pembangunan Gender': [
            '/workspaces/dashboard-visualization-bps/IPM Yang Ada/Indeks Pembangunan Gender.xlsx',
        ],
        'Indeks Pembangunan Gender (menggunakan UHH hasil SP2020 LF)': [
            '/workspaces/dashboard-visualization-bps/IPM Yang Ada/Indeks Pembangunan Gender (menggunakan UHH hasil SP2020 LF).xlsx',
        ],
        'Indeks Ketimpangan Gender (IKG)': [
            '/workspaces/dashboard-visualization-bps/IPM Yang Ada/Indeks Ketimpangan Gender (IKG).xlsx',
        ],
        # Tambahkan data IPM lainnya di sini
    }
}


def load_data_pdrb(file_path):
    # Tentukan engine berdasarkan ekstensi file
    if file_path.endswith('.xlsx'):
        data = pd.read_excel(file_path, engine='openpyxl')
    elif file_path.endswith('.xls'):
        data = pd.read_excel(file_path, engine='xlrd')

    # Baca file Excel dengan engine yang sesuai
    else:
        data = pd.read_html(io.BytesIO(file_path))
        data = data[0]

    for col in data.columns[1:]:
        # if data[col].dtype == 'object':  # Check if column type is object (usually string)
        # data[col] = data[col].replace ('-',100)  # Menampilkan 0

        # jika semua elemen kolom adalah string
        if data[col].apply(lambda x: isinstance(x, str)).all():
            data[col] = data[col].str.replace(
                '.', '', regex=False)  # Remove thousands separator
            # Replace decimal comma with dot
            data[col] = data[col].str.replace(',', '.', regex=False)
            data[col] = data[col].str.replace(' ', '')  # Remove all spaces

            try:
                # if data[col] != '-':
                data[col] = pd.to_numeric(
                    data[col], errors='coerce')  # Convert to numeric
            except ValueError as e:
                st.error(f"Error converting data in column {col}: {e}")
        else:
            try:
                # Convert to numeric, setting invalid parsing as NaN
                data[col] = pd.to_numeric(data[col], errors='coerce')
            except ValueError as e:
                st.error(f"Error converting data in column {col}: {e}")

        # Cek judul data dan tambahkan logika pemformatan
        if file_path.endswith('/workspaces/dashboard-visualization-bps/PDRB Pengeluaran Publikasi Softfile/Distribusi PDRB Atas Dasar Harga Berlaku Menurut Komponen Pengeluaran Kota Mojokerto 2019–2023.xlsx'):  # Ubah judul sesuai kebutuhan
            # Jika nilai desimal, kalikan dengan 100 dan format dengan simbol %
            if data[col].dtype == 'float64':  # Pastikan tipe data float
                data[col] = data[col] * 100  # Ubah ke persen
                data[col] = data[col].astype(str) + '%'  # Tambahkan simbol %

    return data


# Sidebar menu
st.sidebar.title("Pilih Jenis Data")
data_type = st.sidebar.selectbox("Jenis Data:", list(data_files.keys()))

# Menampilkan judul data berdasarkan jenis data yang dipilih
if data_type in data_files:
    st.sidebar.title("Pilih Judul Data")
    selected_data_title = st.sidebar.selectbox(
        "Judul Data:", list(data_files[data_type].keys()))

 # Menampilkan dropdown jenis visualisasi tergantung pada judul data yang dipilih
 # Visualisasi Data PDRB
    if selected_data_title == 'PDRB Atas Dasar Harga Berlaku Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023':
        visual_type = st.sidebar.selectbox(
            "Jenis Visualisasi:", ["Line Chart"])
    elif selected_data_title == 'Distribusi PDRB Atas Dasar Harga Berlaku Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023':
        visual_type = st.sidebar.selectbox(
            "Jenis Visualisasi:", ["Line Chart"])
    elif selected_data_title == 'Laju Pertumbuhan PDRB ADHK 2010 Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Bar Chart"])
    elif selected_data_title == 'Indeks Implisit PDRB Menurut Pengeluaran Kota Mojokerto, 2019-2023':
        visual_type = st.sidebar.selectbox(
            "Jenis Visualisasi:", ["Line Chart"])
    elif selected_data_title == 'Pertumbuhan Indeks Implisit PDRB Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Bar Chart"])
    elif selected_data_title == 'Perkembangan Komponen Konsumsi Rumah Tangga Kota Mojokerto, 2019-2023':
        visual_type = st.sidebar.selectbox(
            "Jenis Visualisasi:", ["Line Chart"])
    elif selected_data_title == 'Perkembangan Pengeluaran Konsumsi Akhir Pemerintah Kota Mojokerto, 2019-2023':
        visual_type = st.sidebar.selectbox(
            "Jenis Visualisasi:", ["Line Chart"])
    elif selected_data_title == 'Laju Indeks Harga Implisit PDRB Kota Mojokerto Menurut Pengeluaran 2011-2023':
        visual_type = st.sidebar.selectbox(
            "Jenis Visualisasi:", ["Line Chart"])
    elif selected_data_title == 'Distribusi PDRB Kota Mojokerto Atas Dasar Harga Berlaku Menurut Pengeluaran 2010-2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Bar Chart"])
    elif selected_data_title == 'Distribusi Persentase Produk Domestik Regional Bruto Kota Mojokerto Atas Dasar Harga Berlaku Menurut Lapangan Usaha, 2019─2023':
        visual_type = st.sidebar.selectbox(
            "Jenis Visualisasi:", ["Stacked Bar Chart"])
    elif selected_data_title == 'Laju Pertumbuhan Produk Domestik Regional Bruto Atas Dasar Harga Konstan 2010 Kota Mojokerto Menurut Lapangan Usaha (persen), 2019─2023':
        visual_type = st.sidebar.selectbox(
            "Jenis Visualisasi:", ["Line Chart"])

     # Visualisasi Data Kependudukan
    elif selected_data_title == 'Penduduk, Distribusi Persentase Penduduk, Kepadatan Penduduk, Rasio Jenis Kelamin Penduduk Menurut Kecamatan di Kota Mojokerto, 2023':
        visual_type = st.sidebar.selectbox(
            "Jenis Visualisasi:", ["Stacked Bar Chart"])
    elif selected_data_title == 'Penduduk akhir tahun Warga Negara Indonesia menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Bar Chart"])
    elif selected_data_title == 'Penduduk akhir tahun Warga Negara Asing menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Bar Chart"])
    elif selected_data_title == 'Jumlah Kelahiran menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Bar Chart"])
    elif selected_data_title == 'Jumlah Kematian menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Bar Chart"])
    elif selected_data_title == 'Jumlah Penduduk datang menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Bar Chart"])
    elif selected_data_title == 'Jumlah Penduduk keluar menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Bar Chart"])
    elif selected_data_title == 'Banyaknya akte kependudukan diterbitkan menurut jenisnya menurut bulan di Kota Mojokerto, 2023':
        visual_type = st.sidebar.selectbox(
            "Jenis Visualisasi:", ["Line Chart"])
    elif selected_data_title == 'Kepadatan penduduk akhir tahun Warga Negara Indonesia menurut Kelurahan di Kota Mojokerto, 2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Heatmap"])

    # Visualisasi Data IPM
    elif selected_data_title == 'Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah) 2010-2023':
        visual_type = st.sidebar.selectbox(
            "Jenis Visualisasi:", ["Line Chart"])
    elif selected_data_title == 'Harapan Lama Sekolah (HLS) 2010-2023':
        visual_type = st.sidebar.selectbox(
            "Jenis Visualisasi:", ["Line Chart"])
    elif selected_data_title == 'Angka Melek Huruf (Persen) 2016-2006':
        visual_type = st.sidebar.selectbox(
            "Jenis Visualisasi:", ["Line Chart"])
    elif selected_data_title == 'Angka Harapan Hidup Jawa Timur (LF SP2020)':
        visual_type = st.sidebar.selectbox(
            "Jenis Visualisasi:", ["Line Chart"])
    elif selected_data_title == 'IPM Jawa Timur 2010-2023':
        visual_type = st.sidebar.selectbox(
            "Jenis Visualisasi:", ["Line Chart"])
    elif selected_data_title == 'Indeks Pembangunan Manusia Menurut Kabupaten dan Kota':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Bar Chart"])
    elif selected_data_title == 'Indeks Pembangunan Manusia (UHH LF SP2020)':
        visual_type = st.sidebar.selectbox(
            "Jenis Visualisasi:", ["Bar Chart"])
    elif selected_data_title == 'Angka Melek Huruf (Penduduk Usia 15 +)':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Bar Chart"])
    elif selected_data_title == 'Indeks Pemberdayaan Gender':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Bar Chart"])
    elif selected_data_title == 'Indeks Pembangunan Gender':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Bar Chart"])
    elif selected_data_title == 'Indeks Pembangunan Gender (menggunakan UHH hasil SP2020 LF)':
        visual_type = st.sidebar.selectbox(
            "Jenis Visualisasi:", ["Line Chart"])
    elif selected_data_title == 'Indeks Ketimpangan Gender (IKG)':
        visual_type = st.sidebar.selectbox(
            "Jenis Visualisasi:", ["Line Chart"])

      # Muat data berdasarkan judul yang dipilih
    if selected_data_title:
        # Ambil file path pertama
        file_path = data_files[data_type][selected_data_title][0]
        if file_path:  # Pastikan file_path tidak kosong
            data = load_data_pdrb(file_path)

            # Cek apakah data berhasil dimuat
            if data is not None and not data.empty:
                st.title(f"Visualisasi Data: {selected_data_title}")
                st.write("Tampilan Data:")
                st.dataframe(data)

            # Tampilan visualisasi berdasarkan pilihan pengguna
                if selected_data_title == 'PDRB Atas Dasar Harga Berlaku Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023' and visual_type == "Line Chart":
                    st.markdown(
                        "### Line Chart Perkembangan Komponen Pengeluaran Kota Mojokerto (2019-2023)")

                    # Contoh data yang sama
                    data = {
                        'Komponen Pengeluaran': [
                            'Konsumsi Rumah Tangga', 'Konsumsi LNPRT', 'Konsumsi Pemerintah',
                            'Pembentukan Modal Tetap Bruto', 'Perubahan Inventori', 'Ekspor Netto', 'Total PDRB'
                        ],
                        '2019': [4721124.87, 59547.93, 1166741.4, 2421753.8, 675.62, -1568147.03, 6801696.59],
                        '2020': [4640562.22, 60735.12, 1060615.21, 2325805.86, 248.82, -1499909.52, 6588057.71],
                        '2021': [4846610.83, 63026.04, 1103129.25, 2392008.09, 318.27, -1469460.15, 6935632.33],
                        '2022': [5457401.42, 69224.88, 1042001.28, 2622362.96, 332.04, -1554298.51, 7637024.08],
                        '2023': [6004657.7, 75126.7, 1089460.58, 2713435.6, 366.07, -1844389.46, 8038657.18]
                    }

                    # Membuat DataFrame
                    df = pd.DataFrame(data)

                    # Mengatur 'Komponen Pengeluaran' sebagai index
                    df.set_index('Komponen Pengeluaran', inplace=True)

                    # Membuat grafik interaktif dengan Plotly
                    fig = go.Figure()

                    # Menambahkan garis untuk setiap komponen pengeluaran
                    for column in df.index:
                        fig.add_trace(go.Scatter(
                            x=df.columns,
                            y=df.loc[column],
                            mode='lines+markers',
                            name=column
                        ))

                    # Mengatur layout
                    fig.update_layout(
                        title='Perkembangan Komponen Pengeluaran dari 2019 hingga 2023',
                        xaxis_title='Tahun',
                        yaxis_title='Jumlah (Dalam Jutaan)',
                        legend_title='Komponen Pengeluaran',
                        height=600
                    )

                    # Menampilkan plot di Streamlit
                    st.plotly_chart(fig)

                elif selected_data_title == 'Distribusi PDRB Atas Dasar Harga Berlaku Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023' and visual_type == "Line Chart":
                    st.markdown("### Line Chart Distribusi PDRB")

                # Data distribusi PDRB dengan nilai % yang sudah ada di input
                    data = {
                        'Komponen Pengeluaran': [
                            'Konsumsi Rumah Tangga', 'Konsumsi LNPRT', 'Konsumsi Pemerintah',
                            'Pembentukan Modal Tetap Bruto', 'Perubahan Inventori', 'Ekspor Netto', 'Total PDRB'
                        ],
                        '2019': ['69.41%', '0.88%', '17.15%', '35.61%', '0.01%', '-23.06%', '100%'],
                        '2020': ['70.44%', '0.92%', '16.10%', '35.30%', '0.00%', '-22.24%', '100%'],
                        '2021': ['69.88%', '0.91%', '15.91%', '34.49%', '0.00%', '-20.61%', '100%'],
                        '2022': ['71.46%', '0.91%', '13.64%', '34.34%', '0.00%', '-20.07%', '100%'],
                        '2023': ['74.70%', '0.93%', '13.55%', '33.75%', '0.00%', '-22.94%', '100%']
                    }

                # Membuat DataFrame dari data
                    df = pd.DataFrame(data)

                # Fungsi untuk menghilangkan simbol % dan mengubah ke tipe numerik agar bisa divisualisasikan
                    def remove_percentage(value):
                        if isinstance(value, str) and '%' in value:
                            return float(value.replace('%', ''))
                        return value

                # Menghilangkan simbol % agar data bisa divisualisasikan dengan Line Chart
                    df_for_chart = df.copy()
                    for col in df.columns[1:]:
                        df_for_chart[col] = df_for_chart[col].apply(
                            remove_percentage)

                # Mengubah DataFrame menjadi format panjang untuk Plotly (untuk visualisasi)
                    df_melted = df_for_chart.melt(
                        id_vars='Komponen Pengeluaran', var_name='Tahun', value_name='Nilai')

                # Debugging: Tampilkan df_melted untuk memastikan strukturnya benar
                    st.write(df_melted)

                 # Menampilkan tabel dengan format yang sudah ada simbol %
                    # Menampilkan tabel awal
                    st.markdown("### Tabel Distribusi PDRB (dalam %)")
                    st.dataframe(df)

                # Membuat Line Chart interaktif
                    fig = px.line(df_melted, x='Tahun', y='Nilai', color='Komponen Pengeluaran',
                                  title='Distribusi PDRB Atas Dasar Harga Berlaku Menurut Komponen Pengeluaran (2019-2023)',
                                  labels={
                                      'Nilai': 'Distribusi (%)', 'Komponen Pengeluaran': 'Komponen'},
                                  markers=True, height=600)

                # Menambahkan fitur hover untuk menampilkan data persentase
                    fig.update_traces(mode="lines+markers",
                                      hovertemplate='%{y:.2f}%')

                # Menampilkan grafik di Streamlit
                    st.plotly_chart(fig)

                if selected_data_title == 'Laju Pertumbuhan PDRB ADHK 2010 Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023' and visual_type == "Bar Chart":
                    st.markdown(
                        "### Bar Chart komponen pengeluaran (yang bernilai dalam persen)")

                # Data Laju Pertumbuhan PDRB ADHK 2010
                    data_growth = {
                        'Komponen Pengeluaran': [
                            'Konsumsi Rumah Tangga', 'Konsumsi LNPRT', 'Konsumsi Pemerintah',
                            'Pembentukan Modal Tetap Bruto', 'Perubahan Inventori', 'Ekspor Netto', 'PDRB'
                        ],
                        '2019': [5.20, 4.39, 4.46, 4.91, None, None, 5.65],
                        '2020': [-3.22, 0.30, -4.48, -4.79, None, None, -3.69],
                        '2021': [3.39, 2.15, 0.28, 1.10, None, None, 3.65],
                        '2022': [7.57, 7.09, 1.06, 4.74, None, None, 5.56],
                        '2023': [5.28, 8.43, 1.58, 1.19, None, None, 2.79]
                    }

                # Membuat DataFrame dari data
                    df_growth = pd.DataFrame(data_growth)

                # Mengatur 'Komponen Pengeluaran' sebagai index
                    df_growth.set_index('Komponen Pengeluaran', inplace=True)

                # Fungsi untuk memformat data dalam bentuk persen dan None tetap ditampilkan
                    def format_percent(value):
                        if value is None:
                            return None  # Biarkan None apa adanya
                        else:
                            # Format dalam bentuk persentase dengan 2 desimal
                            return f"{value:.2f}%"

                # Membuat DataFrame baru dengan format persen
                    df_percent = df_growth.applymap(format_percent)

                # Menampilkan tabel baru di Streamlit
                    st.markdown("### Tabel Laju Pertumbuhan (dalam persen)")
                    st.dataframe(df_percent)

                # Mengubah DataFrame menjadi format panjang untuk Plotly
                    df_melted_growth = df_growth.reset_index().melt(id_vars='Komponen Pengeluaran',
                                                                    var_name='Tahun', value_name='Laju Pertumbuhan')

                # Widget untuk memilih tahun
                    tahun_options = df_melted_growth['Tahun'].unique()
                    selected_tahun = st.multiselect(
                        'Pilih tahun untuk ditampilkan:', options=tahun_options, default=tahun_options)

                # Filter data berdasarkan tahun yang dipilih
                    df_filtered = df_melted_growth[df_melted_growth['Tahun'].isin(
                        selected_tahun)]

                # Membuat bar chart interaktif
                    fig = go.Figure()

                # Menambahkan bar untuk setiap komponen pengeluaran yang sesuai dengan tahun yang dipilih
                    for component in df_filtered['Komponen Pengeluaran'].unique():
                        df_component = df_filtered[df_filtered['Komponen Pengeluaran'] == component]

                        fig.add_trace(go.Bar(
                            x=df_component['Tahun'],
                            y=df_component['Laju Pertumbuhan'],
                            name=component
                        ))

                # Mengatur layout
                    fig.update_layout(
                        title='Laju Pertumbuhan PDRB ADHK 2010 Menurut Komponen Pengeluaran (2019-2023)',
                        xaxis_title='Tahun',
                        yaxis_title='Laju Pertumbuhan (%)',
                        barmode='group',  # Mengatur mode batang agar saling berkelompok
                        legend_title='Komponen Pengeluaran',
                        height=600
                    )

                # Menampilkan plot di Streamlit
                    st.plotly_chart(fig)

                elif selected_data_title == 'Indeks Implisit PDRB Menurut Pengeluaran Kota Mojokerto, 2019-2023' and visual_type == "Line Chart":
                    st.markdown("### Line Chart Indeks Implisit PDRB")

                # Data yang sudah ditampilkan sebelumnya
                    data_implisit = {
                        'Komponen Pengeluaran': ['Konsumsi Rumah Tangga', 'Konsumsi LNPRT', 'Konsumsi Pemerintah',
                                                 'Pembentukan Modal Tetap Bruto', 'Perubahan Inventori', 'Ekspor Netto', 'PDRB'],
                        '2019': [140.64, 162.07, 167.25, 143.19, None, None, 136.42],
                        '2020': [142.84, 164.81, 159.17, 144.43, None, None, 137.21],
                        '2021': [144.29, 167.42, 165.10, 146.92, None, None, 139.37],
                        '2022': [151.04, 171.72, 154.30, 153.79, None, None, 145.38],
                        '2023': [157.85, 171.87, 158.83, 157.26, None, None, 148.87]
                    }

                # Membuat DataFrame
                    df_implisit = pd.DataFrame(data_implisit)

                # Mengatur 'Komponen Pengeluaran' sebagai index
                    df_implisit.set_index('Komponen Pengeluaran', inplace=True)

                # Mengubah DataFrame menjadi format panjang untuk Plotly
                    df_melted_implisit = df_implisit.reset_index().melt(
                        id_vars='Komponen Pengeluaran', var_name='Tahun', value_name='Indeks')

                # Membuat line chart interaktif
                    fig = go.Figure()

                # Menambahkan garis untuk setiap komponen pengeluaran
                    for component in df_melted_implisit['Komponen Pengeluaran'].unique():
                        df_component = df_melted_implisit[df_melted_implisit['Komponen Pengeluaran'] == component]
                        fig.add_trace(go.Scatter(
                            x=df_component['Tahun'],
                            y=df_component['Indeks'],
                            mode='lines+markers',
                            name=component
                        ))

                # Mengatur layout
                    fig.update_layout(
                        title='Indeks Implisit PDRB Menurut Pengeluaran (2019-2023)',
                        xaxis_title='Tahun',
                        yaxis_title='Indeks',
                        legend_title='Komponen Pengeluaran',
                        height=600
                    )

                # Menampilkan plot di Streamlit
                    st.plotly_chart(fig)

                elif selected_data_title == 'Pertumbuhan Indeks Implisit PDRB Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023' and visual_type == "Bar Chart":
                    st.markdown(
                        "### Bar Chart Pertumbuhan Indeks Implisit PDRB")

                # Data dari tabel (kamu bisa sesuaikan ini untuk mengambil data dari file_path)
                    data_implisit = {
                        'Komponen Pengeluaran': ['Konsumsi Rumah Tangga', 'Konsumsi LNPRT', 'Konsumsi Pemerintah',
                                                 'Pembentukan Modal Tetap Bruto', 'Perubahan Inventori', 'Ekspor Netto', 'PDRB'],
                        '2019': [0.026, 0.0232, 0.0368, 0.0316, None, None, 0.0165],
                        '2020': [0.0156, 0.0169, -0.0483, 0.0086, None, None, 0.0058],
                        '2021': [0.0101, 0.0158, 0.0372, 0.0173, None, None, 0.0157],
                        '2022': [0.0468, 0.0257, -0.0654, 0.0467, None, None, 0.0432],
                        '2023': [0.0451, 0.0009, 0.0293, 0.0226, None, None, 0.024]
                    }

                # Membuat DataFrame
                    df = pd.DataFrame(data_implisit)

                # Transformasi dari wide ke long format
                    df_long = df.melt(
                        id_vars='Komponen Pengeluaran', var_name='Tahun', value_name='Pertumbuhan')

                # Hapus baris dengan nilai None
                    df_long = df_long.dropna(subset=['Pertumbuhan'])

                # Membuat Bar Chart interaktif dengan Altair
                    bar_chart = alt.Chart(df_long).mark_bar().encode(
                        x=alt.X('Tahun:N', title='Tahun'),
                        y=alt.Y('Pertumbuhan:Q', title='Pertumbuhan'),
                        color='Komponen Pengeluaran:N',
                        tooltip=['Komponen Pengeluaran:N',
                                 'Tahun:N', 'Pertumbuhan:Q']
                    ).properties(
                        title='Pertumbuhan Indeks Implisit PDRB Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023',
                        width=700,
                        height=400
                    ).interactive()

                # Tampilkan chart di Streamlit
                    st.altair_chart(bar_chart, use_container_width=True)

                elif selected_data_title == 'Perkembangan Komponen Konsumsi Rumah Tangga Kota Mojokerto, 2019-2023' and visual_type == "Line Chart":
                    st.markdown(
                        "### Line Chart Perkembangan Komponen Konsumsi Rumah Tangga")

                # Data yang diambil dari tabel
                    data_konsumsi = {
                        'Uraian': ['Total Konsumsi Rumah Tangga a. ADHB (Juta Rp.)',
                                   'Total Konsumsi Rumah Tangga b. ADHK 2010 (Juta Rp.)',
                                   'Proporsi terhadap PDRB ADHB',
                                   'Rata-rata Konsumsi per Kapita a. ADHB',
                                   'Rata-rata Konsumsi per Kapita b. ADHK 2010',
                                   'Pertumbuhan a. Total Konsumsi Rumah Tangga',
                                   'Pertumbuhan b. Per Kapita',
                                   'Jumlah Penduduk (jiwa)'],
                        '2019': [4721124.87, 3356940.38, 69.41, 36470, 25930, 5.2, 4.43, 129467],
                        '2020': [4640562.22, 3248832.38, 70.44, 35110, 24580, -3.22, -5.21, 132183],
                        '2021': [4846610.83, 3359049.51, 69.88, 36310, 25170, 3.39, 2.4, 133476],
                        '2022': [5457401.42, 3613284.51, 71.46, 40480, 26800, 7.57, 6.48, 134815],
                        '2023': [6004657.70, 3803908.83, 74.69, 44120, 27950, 5.28, 4.29, 136107]
                    }

                # Membuat DataFrame
                    df_konsumsi = pd.DataFrame(data_konsumsi)

                # Mengubah data ke format long/melt agar bisa divisualisasikan dengan Altair
                    df_konsumsi_melted = df_konsumsi.melt(id_vars='Uraian',
                                                          var_name='Tahun',
                                                          value_name='Nilai')

                # Membuat chart interaktif menggunakan Altair
                    chart = alt.Chart(df_konsumsi_melted).mark_line(point=True).encode(
                        x=alt.X('Tahun:N', title='Tahun'),
                        y=alt.Y('Nilai:Q', title='Nilai'),
                        color=alt.Color(
                            'Uraian:N', title='Komponen Pengeluaran'),
                        # Menampilkan tooltip interaktif
                        tooltip=['Uraian', 'Tahun', 'Nilai']
                    ).interactive()  # Menambahkan interaksi zoom dan pan

                # Menampilkan chart di Streamlit
                    st.altair_chart(chart, use_container_width=True)

                elif selected_data_title == 'Perkembangan Pengeluaran Konsumsi Akhir Pemerintah Kota Mojokerto, 2019-2023' and visual_type == "Line Chart":
                    st.markdown(
                        "### Line Chart Perkembangan Pengeluaran Konsumsi Akhir")

                # Data Pengeluaran Konsumsi Akhir Pemerintah Kota Mojokerto
                    data_konsumsi = {
                        'Uraian': ['Total Konsumsi Rumah Tangga a. ADHB (Juta Rp.)',
                                   'Total Konsumsi Rumah Tangga b. ADHK 2010 (Juta Rp.)',
                                   'Proporsi terhadap PDRB ADHB',
                                   'Rata-rata Konsumsi per Kapita /tahun (Ribu Rp.) a. ADHB',
                                   'Rata-rata Konsumsi per Kapita /tahun (Ribu Rp.) b. ADHK 2010',
                                   'Pertumbuhan a. Total konsumsi Rumah',
                                   'Pertumbuhan b. Per Kapita',
                                   'Jumlah Penduduk (jiwa)'],
                        '2019': [1166741.4, 697598.34, 17.15, 9011.88, 5388.23, 4.46, 3.71, 129467],
                        '2020': [1060615.21, 666328.35, 16.1, 8023.84, 5040.95, -4.48, -6.45, 132183],
                        '2021': [1103129.25, 668177.7, 15.91, 8264.63, 5005.98, 0.28, -0.69, 133476],
                        '2022': [1042001.28, 675290.38, 13.64, 7729.12, 5009.02, 1.06, 0.06, 134815],
                        '2023': [1089460.58, 685936.22, 13.55, 8004.44, 5039.68, 1.58, 0.61, 136107]
                    }

                # Membuat DataFrame
                    df_konsumsi = pd.DataFrame(data_konsumsi)

                # Menggunakan melt untuk mengubah data dari wide format menjadi long format agar sesuai dengan Altair
                    df_konsumsi_melted = df_konsumsi.melt(id_vars='Uraian',
                                                          var_name='Tahun',
                                                          value_name='Nilai')
                # Membuat chart interaktif menggunakan Altair
                    chart = alt.Chart(df_konsumsi_melted).mark_line(point=True).encode(
                        x=alt.X('Tahun:N', title='Tahun'),
                        y=alt.Y('Nilai:Q', title='Nilai'),
                        color=alt.Color(
                            'Uraian:N', title='Komponen Pengeluaran'),
                        # Menampilkan tooltip interaktif
                        tooltip=['Uraian', 'Tahun', 'Nilai']
                    ).interactive()  # Menambahkan interaksi zoom dan pan

                # Menampilkan chart di Streamlit
                    st.altair_chart(chart, use_container_width=True)

                elif selected_data_title == 'Laju Indeks Harga Implisit PDRB Kota Mojokerto Menurut Pengeluaran 2011-2023' and visual_type == "Line Chart":
                    st.markdown(
                        "### Line Chart Laju Indeks Harga Implisit PDRB Kota Mojokerto")

                # Data Laju Indeks Harga Implisit PDRB Kota Mojokerto
                    data_pdrb = {
                        'Jenis Pengeluaran': ['Pengeluaran Konsumsi Rumah Tangga',
                                              'Pengeluaran Konsumsi LNPRT',
                                              'Pengeluaran Konsumsi Pemerintah',
                                              'Pembentukan Modal Tetap Bruto',
                                              'Perubahan Inventori',
                                              'Net Ekspor Barang dan Jasa',
                                              'Total PDRB Pengeluaran (Jumlah 1 sd 6)'],
                        '2011': [591, 1776, 1423, 786, None, None, 461],
                        '2012': [509, 381, 1007, 143, None, None, 429],
                        '2013': [376, 804, 359, 479, None, None, 373],
                        '2014': [450, 107, 141, 536, None, None, 364],
                        '2015': [286, 758, 528, 294, None, None, 428],
                        '2016': [376, 362, 435, 587, None, None, 401],
                        '2017': [283, 322, 518, 218, None, None, 272],
                        '2018': [349, 313, 570, 319, None, None, 272],
                        '2019': [260, 232, 368, 316, None, None, 165],
                        '2020': [80, 169, -483, 86, None, None, 58],
                        '2021': [94, 158, 341, 173, None, None, 157],
                        '2022': [510, 133, -456, 467, None, None, 432],
                        '2023': [451, 9, 293, 226, None, None, 240]
                    }
                # Membuat DataFrame
                    df_pdrb = pd.DataFrame(data_pdrb)

                # Menggunakan melt untuk mengubah data dari wide format menjadi long format agar sesuai dengan Altair
                    df_pdrb_melted = df_pdrb.melt(id_vars='Jenis Pengeluaran',
                                                  var_name='Tahun',
                                                  value_name='Nilai')
                # Membuat chart interaktif menggunakan Altair
                    chart = alt.Chart(df_pdrb_melted).mark_line(point=True).encode(
                        x=alt.X('Tahun:N', title='Tahun'),
                        y=alt.Y('Nilai:Q', title='Nilai'),
                        color=alt.Color('Jenis Pengeluaran:N',
                                        title='Jenis Pengeluaran'),
                        # Menampilkan tooltip interaktif
                        tooltip=['Jenis Pengeluaran', 'Tahun', 'Nilai']
                    ).interactive()  # Menambahkan interaksi zoom dan pan

                # Menampilkan chart di Streamlit
                    st.altair_chart(chart, use_container_width=True)

                elif selected_data_title == 'Distribusi PDRB Kota Mojokerto Atas Dasar Harga Berlaku Menurut Pengeluaran 2010-2023' and visual_type == "Bar Chart":
                    st.markdown(
                        "### Bar Chart Distribusi Persentase Produk Domestik Regional Bruto Kota Mojokerto (2019-2023)")

                # Data Distribusi PDRB Kota Mojokerto Atas Dasar Harga Berlaku
                    data_pdrb_pie = {
                        'Jenis Pengeluaran': ['Pengeluaran Konsumsi Rumah Tangga',
                                              'Pengeluaran Konsumsi LNPRT',
                                              'Pengeluaran Konsumsi Pemerintah',
                                              'Pembentukan Modal Tetap Bruto',
                                              'Perubahan Inventori',
                                              'Net Ekspor Barang dan Jasa',
                                              'Total PDRB Pengeluaran (Jumlah 1 sd 6)'],
                        '2010': [74.2, 0.88, 18.33, 32.78, 0.42, -26.62, 100],
                        '2011': [74.25, 0.96, 19.35, 33.56, 0.25, -28.37, 100],
                        '2012': [73.35, 0.95, 20.5, 33.51, 0, -28.3, 100],
                        '2013': [72.36, 0.99, 20.18, 33.51, 0, -27.04, 100],
                        '2014': [72.15, 0.98, 19.07, 34.16, 0.31, -26.68, 100],
                        '2015': [70.4, 0.93, 18.48, 34.11, 0.02, -23.94, 100],
                        '2016': [69.6, 0.9, 16.44, 35.82, 0.01, -22.77, 100],
                        '2017': [69.08, 0.87, 16.68, 34.98, 0.01, -21.63, 100],
                        '2018': [69.06, 0.88, 17.01, 35.33, 0.01, -22.28, 100],
                        '2019': [69.41, 0.88, 17.15, 35.61, 0.01, -23.06, 100],
                        '2020': [69.91, 0.92, 16.1, 35.3, 0, -22.24, 100],
                        '2021': [69.3, 0.91, 15.91, 34.49, 0.01, -20.61, 100],
                        '2022': [70.76, 0.9, 14.07, 34.34, 0, -20.07, 100],
                        '2023': [74.7, 0.93, 13.55, 33.75, 0, -22.94, 100]
                    }
                # Membuat DataFrame
                    df = pd.DataFrame(data)

                # Mengubah DataFrame menjadi format panjang
                    df_melted = df.melt(
                        id_vars=['Jenis Pengeluaran'], var_name='Tahun', value_name='Persentase')

                # Visualisasi bar chart
                    fig = px.bar(df_melted, x='Tahun', y='Persentase', color='Jenis Pengeluaran', barmode='group',
                                 title='Distribusi PDRB Kota Mojokerto Atas Dasar Harga Berlaku Menurut Pengeluaran (2010-2023)',
                                 labels={'Persentase': 'Persentase (%)'})

                # Menampilkan visualisasi di Streamlit
                    st.plotly_chart(fig)

                # Stop further execution so that other visualizations don't appear
                    st.stop()

                elif selected_data_title == 'Distribusi Persentase Produk Domestik Regional Bruto Kota Mojokerto Atas Dasar Harga Berlaku Menurut Lapangan Usaha, 2019─2023' and visual_type == "Stacked Bar Chart":
                    st.markdown(
                        "### Stacked Bar Chart Distribusi Persentase Produk Domestik Regional Bruto Kota Mojokerto (2019-2023)")

                # Dataframe
                    data = {
                        'Lapangan Usaha': [
                            'Pertanian, Kehutanan, dan Perikanan',
                            'Pertambangan dan Penggalian',
                            'Industri Pengolahan',
                            'Pengadaan Listrik dan Gas',
                            'Pengadaan Air, Pengelolaan Sampah, Limbah dan Daur Ulang',
                            'Konstruksi',
                            'Perdagangan Besar dan Eceran; Reparasi Mobil dan Sepeda Motor',
                            'Transportasi dan Pergudangan',
                            'Penyediaan Akomodasi dan Makan Minum',
                            'Informasi dan Komunikasi',
                            'Jasa Keuangan dan Asuransi',
                            'Real Estat',
                            'Jasa Perusahaan',
                            'Administrasi Pemerintahan, Pertahanan dan Jaminan Sosial Wajib',
                            'Jasa Pendidikan',
                            'Jasa Kesehatan dan Kegiatan Sosial',
                            'Jasa lainnya',
                            'Produk Domestik Regional Bruto'
                        ],
                        '2019': [59, 0, 11.34, 0.08, 0.1, 10.46, 30.19, 2.74, 7.09, 11.65, 8.15, 2.73, 0.8, 4.91, 4.47, 1.16, 3.53, 100],
                        '2020': [66, 0, 11.38, 0.08, 0.11, 10.21, 28.52, 2.64, 6.86, 13.01, 8.39, 2.94, 0.77, 5.1, 4.83, 1.32, 3.18, 100],
                        '2021': [60, 0, 11.32, 0.08, 0.11, 9.88, 29.42, 2.67, 6.98, 13.12, 8.27, 2.81, 0.74, 4.84, 4.6, 1.33, 3.25, 100],
                        '2022 (Angka sementara)': [57, 0, 11.28, 0.07, 0.11, 10.11, 29.97, 2.98, 7.2, 12.57, 8.13, 2.7, 0.71, 4.52, 4.3, 1.26, 3.5, 100],
                        '2023 (Angka sangat sementara)': [53, 0, 9.24, 0.07, 0.11, 9.85, 31.1, 3.39, 7.72, 12.77, 8.11, 2.7, 0.74, 4.54, 4.32, 1.29, 3.62, 100]
                    }

                # Membuat DataFrame
                    df = pd.DataFrame(data)

                # Menampilkan tabel baru dengan nilai dalam persen tanpa tambahan desimal
                    df_percentage = df.copy()
                    df_percentage.iloc[:, 1:] = df_percentage.iloc[:, 1:].applymap(
                        lambda x: f"{int(x)}%")

                # Menampilkan tabel baru di Streamlit
                    st.markdown("### Tabel Distribusi Persentase")
                    st.dataframe(df_percentage)

                # Mengubah DataFrame menjadi format panjang untuk visualisasi
                    df_melted = df.melt(
                        id_vars=['Lapangan Usaha'], var_name='Tahun', value_name='Persentase')

                # Menambahkan dropdown untuk memilih tahun
                    selected_year = st.selectbox(
                        "Pilih Tahun:", df_melted['Tahun'].unique())

                # Filter data berdasarkan tahun yang dipilih
                    filtered_data = df_melted[df_melted['Tahun']
                                              == selected_year]

                # Visualisasi stacked bar chart interaktif
                    fig = px.bar(filtered_data, x='Lapangan Usaha', y='Persentase', color='Lapangan Usaha',
                                 title=f'Distribusi Persentase Produk Domestik Regional Bruto Kota Mojokerto ({selected_year})',
                                 labels={
                                     'Persentase': 'Persentase (%)', 'Lapangan Usaha': 'Lapangan Usaha'},
                                 text='Persentase',
                                 height=600)

                    fig.update_layout(barmode='stack', hovermode='x unified')

                # Menampilkan visualisasi di Streamlit
                    st.plotly_chart(fig)

                # Stop further execution so that other visualizations don't appear
                    st.stop()

                elif selected_data_title == 'Laju Pertumbuhan Produk Domestik Regional Bruto Atas Dasar Harga Konstan 2010 Kota Mojokerto Menurut Lapangan Usaha (persen), 2019─2023' and visual_type == "Line Chart":
                    st.markdown(
                        "### Line Chart Laju Pertumbuhan PDRB Kota Mojokerto Atas Dasar Harga Konstan 2010 Menurut Lapangan Usaha (2019-2023)")

                # Dataframe
                    data = {
                        'Lapangan Usaha': ['Pertanian, Kehutanan, dan Perikanan',
                                           'Pertambangan dan Penggalian',
                                           'Industri Pengolahan',
                                           'Pengadaan Listrik dan Gas',
                                           'Pengadaan Air, Pengelolaan Sampah, Limbah dan Daur Ulang',
                                           'Konstruksi',
                                           'Perdagangan Besar dan Eceran; Reparasi Mobil dan Sepeda Motor',
                                           'Transportasi dan Pergudangan',
                                           'Penyediaan Akomodasi dan Makan Minum',
                                           'Informasi dan Komunikasi',
                                           'Jasa Keuangan dan Asuransi',
                                           'Real Estat',
                                           'Jasa Perusahaan',
                                           'Administrasi Pemerintahan, Pertahanan dan Jaminan Sosial Wajib',
                                           'Jasa Pendidikan',
                                           'Jasa Kesehatan dan Kegiatan Sosial',
                                           'Jasa lainnya',
                                           'Produk Domestik Regional Bruto'
                                           ],
                        '2019': [-1.54, 0, 3.03, 6.24, 4.87, 5.78, 5.88, 7.78, 7.78, 7.09, 4.45, 4.04, 5.37, 4.27, 6.15, 5.99, 5.84, 5.65],
                        '2020': [8.16, 0, -3.55, -0.33, 4.39, -6.26, -9.2, -6.43, -8.16, 7.87, 0.02, 3.27, -7.24, -2.42, 2.88, 3.82, -14.5, -3.69],
                        '2021': [-2.41, 0, 2.98, 2.56, 6.17, 0.86, 6.54, 5.91, 1.45, 5.6, 0.51, 0.25, 0.87, -0.2, 0.31, 3.94, 3.71, 3.65],
                        '2022 (Angka sementara)': [-3.09, 0, 6.06, 5.79, 1.61, 6.86, 6.42, 15.19, 7.75, 4.46, 0.63, 3.7, 1.54, 0.41, 1.57, 0.7, 14.81, 5.56],
                        '2023 (Angka sangat sementara)': [-7.06, 0, -13.91, 5.24, 3.43, 4.03, 5.53, 10.71, 8.99, 6, 2.75, 3, 7.54, 0.67, 3.57, 4.85, 4.91, 2.79]
                    }

                # Membuat DataFrame
                    df = pd.DataFrame(data)

                # Menampilkan tabel asli terlebih dahulu
                    st.dataframe(df)

                # Membuat tabel baru dengan persentase
                    df_percentage = df.copy()

                # Mengubah data menjadi persentase (menambahkan simbol % pada setiap nilai)
                    for col in df_percentage.columns[1:]:
                        df_percentage[col] = df_percentage[col].apply(
                            lambda x: f"{abs(x):.2f}".rstrip('0').rstrip('.') + '%')

                # Menampilkan tabel baru dengan format yang lebih mudah dipahami
                    st.markdown(
                        "### Tabel Laju Pertumbuhan PDRB (Dengan Simbol %)")
                    st.dataframe(df_percentage)

                # Untuk visualisasi, kita tetap menggunakan data asli tanpa simbol % agar grafik bisa di-render dengan benar
                    df_melted = df.melt(
                        id_vars=['Lapangan Usaha'], var_name='Tahun', value_name='Laju Pertumbuhan')

                # Membuat stacked line chart
                    fig = go.Figure()

                # Menambahkan garis untuk setiap lapangan usaha
                    for industry in df_melted['Lapangan Usaha'].unique():
                        industry_data = df_melted[df_melted['Lapangan Usaha'] == industry]
                        fig.add_trace(go.Scatter(
                            x=industry_data['Tahun'],
                            y=industry_data['Laju Pertumbuhan'],
                            mode='lines+markers',
                            name=industry
                        ))

                # Mengatur layout
                    fig.update_layout(
                        title='Laju Pertumbuhan PDRB Kota Mojokerto Menurut Lapangan Usaha (2019-2023)',
                        xaxis_title='Tahun',
                        yaxis_title='Laju Pertumbuhan (%)',
                        height=600,
                        legend_title='Lapangan Usaha'
                    )

                # Menampilkan visualisasi di Streamlit
                    st.plotly_chart(fig)

                elif selected_data_title == 'Penduduk, Distribusi Persentase Penduduk, Kepadatan Penduduk, Rasio Jenis Kelamin Penduduk Menurut Kecamatan di Kota Mojokerto, 2023' and visual_type == "Stacked Bar Chart":
                    st.markdown(
                        "### Stacked Bar Chart Distribusi Data Kependudukan Kota Mojokerto per Kecamatan, 2023")

                # Data per Kecamatan
                    data_kecamatan = {
                        'Kecamatan': ['PRAJURIT KULON', 'MAGERSARI', 'KRANGGAN'],
                        'Penduduk': [43194, 60439, 38152],
                        'Persentase Penduduk': [30.46, 42.63, 26.91],
                        'Kepadatan Penduduk per km2': [5828, 7477, 8081],
                        'Rasio Jenis Kelamin Penduduk': [1, 0.99, 0.98]
                    }
                    df_kecamatan = pd.DataFrame(data_kecamatan)

                # Total Data Kota Mojokerto
                    total_data = {
                        'Kecamatan': ['Kota Mojokerto'],
                        'Penduduk': [141785],
                        'Persentase Penduduk': [100],
                        'Kepadatan Penduduk per km2': [7014],
                        'Rasio Jenis Kelamin Penduduk': [0.99]
                    }
                    df_total = pd.DataFrame(total_data)

                # Stacked bar chart untuk setiap Kecamatan
                    fig_kecamatan = px.bar(
                        df_kecamatan,
                        x='Kecamatan',
                        y=['Penduduk', 'Persentase Penduduk',
                            'Kepadatan Penduduk per km2', 'Rasio Jenis Kelamin Penduduk'],
                        title='Distribusi Data Kependudukan Kota Mojokerto per Kecamatan, 2023',
                        labels={'value': 'Jumlah', 'variable': 'Kategori'},
                        barmode='stack'
                    )

                # Tampilkan chart per Kecamatan di Streamlit
                    st.plotly_chart(fig_kecamatan, use_container_width=True)

                # Stacked bar chart untuk Total Kota Mojokerto
                    fig_total = px.bar(
                        df_total,
                        x='Kecamatan',
                        y=['Penduduk', 'Persentase Penduduk',
                            'Kepadatan Penduduk per km2', 'Rasio Jenis Kelamin Penduduk'],
                        title='Total Data Kependudukan Kota Mojokerto, 2023',
                        labels={'value': 'Jumlah', 'variable': 'Kategori'},
                        barmode='stack'
                    )

                # Tampilkan chart Total Kota Mojokerto di Streamlit
                    st.plotly_chart(fig_total, use_container_width=True)

                elif selected_data_title == 'Penduduk akhir tahun Warga Negara Indonesia menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023' and visual_type == "Bar Chart":
                    st.markdown(
                        "### Susunan Tabel Baru & Visualisasi Penduduk akhir tahun Warga Negara Indonesia menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023")

                # Membuat DataFrame awal dengan data yang sudah ada
                    data = {
                        'Kategori': ['Kecamatan', 'Kelurahan', 'Kelurahan', 'Kelurahan', 'Kelurahan', 'Kelurahan', 'Kelurahan', 'Kecamatan', 'Kelurahan', 'Kelurahan', 'Kelurahan', 'Kelurahan', 'Kelurahan', 'Kelurahan', 'Kecamatan', 'Kelurahan', 'Kelurahan', 'Kelurahan', 'Kelurahan', 'Kelurahan', 'Kelurahan', 'Kota'],
                        'Nama': ['Prajurit Kulon', 'Surodinawan', 'Prajurit Kulon', 'Blooto', 'Mentikan', 'Kauman', 'Pulorejo', 'Magersari', 'Gunung Gedangan', 'Kedundung', 'Balongsari', 'Gedongan', 'Magersari', 'Wates', 'Kranggan', 'Kranggan', 'Meri', 'Jagalan', 'Miji', 'Sentanan', 'Purwotengah', 'Kota Mojokerto'],
                        'Laki-Laki': [21575, 4744, 4167, 3646, 3170, 1521, 4327, 30055, 4072, 8215, 3946, 1093, 2764, 9965, 18860, 6616, 4674, 1475, 4283, 1060, 752, 70490],
                        'Perempuan': [21619, 4835, 3991, 3610, 3217, 1578, 4388, 30384, 3963, 7963, 3997, 1113, 2907, 10441, 19292, 6793, 4674, 1461, 4400, 1139, 825, 71295],
                        'Jumlah': [43194, 9579, 8158, 7256, 6387, 3099, 8715, 60439, 8035, 16178, 7943, 2206, 5671, 20406, 38152, 13409, 9348, 2936, 8683, 2199, 1577, 141785],
                        'Presentase': [30.46, 6.76, 5.75, 5.12, 4.5, 2.19, 6.15, 42.63, 5.67, 11.41, 5.6, 1.56, 4, 14.39, 26.91, 9.46, 6.59, 2.07, 6.12, 1.55, 1.11, 100.00]
                    }

                    df = pd.DataFrame(data)

                # Mengubah kolom presentase menjadi format %
                    df['Presentase'] = df['Presentase'].astype(str) + '%'

                # Menampilkan tabel yang sudah diformat di Streamlit
                    st.write("Tabel Asli:")
                    st.dataframe(df)

                # Memisahkan tabel untuk Kecamatan, Kelurahan, dan Kota
                    df_kecamatan = df[df['Kategori'] == 'Kecamatan']
                    df_kelurahan = df[df['Kategori'] == 'Kelurahan']
                    df_kota = df[df['Kategori'] == 'Kota']

                # Menampilkan masing-masing tabel
                    st.write("Tabel Kecamatan:")
                    st.dataframe(df_kecamatan)

                    st.write("Tabel Kelurahan:")
                    st.dataframe(df_kelurahan)

                    st.write("Tabel Kota:")
                    st.dataframe(df_kota)

                # Fungsi untuk membuat bar chart
                    def create_bar_chart(data, title):
                        chart = alt.Chart(data).mark_bar().encode(
                            x=alt.X('Nama', sort='-y', title='Nama'),
                            y=alt.Y('Jumlah', title='Jumlah Penduduk'),
                            color=alt.Color('Nama', legend=None),
                            tooltip=['Nama', 'Laki-Laki',
                                     'Perempuan', 'Jumlah', 'Presentase']
                        ).properties(
                            title=title,
                            width=600,
                            height=400
                        ).interactive()
                        return chart

                # Menampilkan bar chart untuk setiap tabel
                    st.altair_chart(create_bar_chart(
                        df_kecamatan, "Jumlah Penduduk per Kecamatan"), use_container_width=True)
                    st.altair_chart(create_bar_chart(
                        df_kelurahan, "Jumlah Penduduk per Kelurahan"), use_container_width=True)
                    st.altair_chart(create_bar_chart(
                        df_kota, "Jumlah Penduduk Kota Mojokerto"), use_container_width=True)

                elif selected_data_title == 'Penduduk akhir tahun Warga Negara Asing menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023' and visual_type == "Bar Chart":
                    st.markdown(
                        "### Susunan Tabel Baru & Visualisasi Penduduk akhir tahun Warga Negara Asing menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023")

                # Data Penduduk akhir tahun Warga Negara Asing
                    data = {
                        'Kecamatan': [
                            'Prajurit Kulon', 'Prajurit Kulon', 'Prajurit Kulon', 'Prajurit Kulon', 'Prajurit Kulon', 'Prajurit Kulon',
                            'Magersari', 'Magersari', 'Magersari', 'Magersari', 'Magersari', 'Magersari',
                            'Kranggan', 'Kranggan', 'Kranggan', 'Kranggan', 'Kranggan', 'Kranggan', 'Kota Mojokerto'
                        ],
                        'Kelurahan': [
                            'Surodinawan', 'Prajurit Kulon', 'Blooto', 'Mentikan', 'Kauman', 'Pulorejo',
                            'Gunung Gedangan', 'Kedundung', 'Balongsari', 'Gedongan', 'Magersari', 'Wates',
                            'Kranggan', 'Meri', 'Jagalan', 'Miji', 'Sentanan', 'Purwotengah', None
                        ],
                        'Laki-Laki': [1, None, None, None, 1, None, 33, None, None, 28, None, 1, 4, None, None, None, None, None, 34],
                        'Perempuan': [1, None, None, None, None, 1, 0, None, None, None, None, None, None, None, None, None, None, None, 1],
                        'Jumlah': [2, None, None, None, 1, 1, 33, None, None, 28, None, 1, 4, None, None, None, None, None, 35],
                        'Persentase': [5.71, None, None, 2.86, 2.86, None, 94.29, None, None, 80, None, 2.86, 11.43, None, None, None, None, None, 100]
                    }

                # Membuat DataFrame
                    df = pd.DataFrame(data)

                # Mengganti nilai None atau NaN dengan "Tidak Ada" agar lebih mudah dibaca
                    df.fillna("Tidak Ada", inplace=True)

                # Menambah simbol % di kolom Persentase
                    df['Persentase'] = df['Persentase'].apply(
                        lambda x: f"{x}%" if pd.notnull(x) and x != "Tidak Ada" else x)

                # Menampilkan tabel baru dengan format yang lebih mudah dipahami
                    st.write("### Tabel Dengan Format yang Lebih Mudah Dipahami")
                    st.table(df)

                # Visualisasi Bar Chart untuk Jumlah Warga Negara Asing berdasarkan Kecamatan
                    fig = px.bar(df, x='Kecamatan', y=['Laki-Laki', 'Perempuan'], title='Distribusi Warga Negara Asing di Kota Mojokerto', labels={
                                 'value': 'Jumlah', 'variable': 'Jenis Kelamin'}, barmode='stack')

                # Menampilkan bar chart di Streamlit
                    st.plotly_chart(fig)

                elif selected_data_title == 'Jumlah Kelahiran menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023' and visual_type == "Bar Chart":

                    # Data Jumlah Kelahiran
                    data = {
                        'Kecamatan': [
                            'Prajurit Kulon', 'Prajurit Kulon', 'Prajurit Kulon', 'Prajurit Kulon', 'Prajurit Kulon', 'Prajurit Kulon',
                            'Magersari', 'Magersari', 'Magersari', 'Magersari', 'Magersari', 'Magersari',
                            'Kranggan', 'Kranggan', 'Kranggan', 'Kranggan', 'Kranggan', 'Kranggan', None
                        ],
                        'Kelurahan': [
                            'Surodinawan', 'Prajurit Kulon', 'Blooto', 'Mentikan', 'Kauman', 'Pulorejo',
                            'Gunung Gedangan', 'Kedundung', 'Balongsari', 'Gedongan', 'Magersari', 'Wates',
                            'Kranggan', 'Meri', 'Jagalan', 'Miji', 'Sentanan', 'Purwotengah', 'Kota Mojokerto'
                        ],
                        'Laki-Laki': [327, 81, 56, 51, 45, 23, 71, 406, 69, 98, 48, 11, 34, 146, 229, 76, 51, 25, 962],
                        'Perempuan': [323, 74, 57, 51, 49, 19, 73, 346, 63, 104, 32, 9, 29, 109, 234, 89, 57, 22, 903],
                        'Jumlah': [650, 155, 113, 102, 94, 42, 144, 752, 132, 202, 80, 20, 63, 255, 463, 165, 108, 47, 1865],
                        'Persentase': [34.85, 8.31, 6.06, 5.47, 5.04, 2.25, 7.72, 40.32, 7.08, 10.83, 4.29, 1.07, 3.38, 13.67, 24.83, 8.85, 5.79, 2.52, 100]
                    }

                # Buat DataFrame
                    df = pd.DataFrame(data)

                # Format kolom 'Persentase' dengan simbol %
                    df['Persentase'] = df['Persentase'].apply(
                        lambda x: f"{x}%" if pd.notnull(x) else "<NA>")

                # Tampilkan tabel dengan format yang lebih mudah dipahami
                    st.write("### Tabel dengan format yang lebih mudah dipahami")
                    st.table(df)

                # Visualisasi bar chart interaktif
                    st.write("### Visualisasi Jumlah Kelahiran di Kota Mojokerto")
                    fig = px.bar(df,
                                 x='Kelurahan',
                                 y='Jumlah',
                                 color='Kecamatan',
                                 labels={'Jumlah': 'Jumlah Kelahiran',
                                         'Kelurahan': 'Nama Kelurahan'},
                                 title='Jumlah Kelahiran di Setiap Kelurahan dan Kecamatan di Kota Mojokerto')

                # Tampilkan bar chart
                    st.plotly_chart(fig)

                elif selected_data_title == 'Jumlah Kematian menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023' and visual_type == "Bar Chart":
                    st.write("### ")
                    st.markdown(
                        "### Susunan Tabel Baru Jumlah Kematian menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023")

                # Data Jumlah Kematian
                    data = {
                        'Kecamatan': [
                            'Prajurit Kulon', 'Prajurit Kulon', 'Prajurit Kulon', 'Prajurit Kulon', 'Prajurit Kulon', 'Prajurit Kulon',
                            'Magersari', 'Magersari', 'Magersari', 'Magersari', 'Magersari', 'Magersari',
                            'Kranggan', 'Kranggan', 'Kranggan', 'Kranggan', 'Kranggan', 'Kranggan', 'Kota Mojokerto'
                        ],
                        'Kelurahan': [
                            'Surodinawan', 'Prajurit Kulon', 'Blooto', 'Mentikan', 'Kauman', 'Pulorejo',
                            'Gunung Gedangan', 'Kedundung', 'Balongsari', 'Gedongan', 'Magersari', 'Wates',
                            'Kranggan', 'Meri', 'Jagalan', 'Miji', 'Sentanan', 'Purwotengah', None
                        ],
                        'Laki-Laki': [1, np.nan, np.nan, np.nan, 1, np.nan, np.nan, 33, np.nan, np.nan, 28, np.nan, 1, 4, np.nan, np.nan, np.nan, np.nan, np.nan],
                        'Perempuan': [1, np.nan, np.nan, np.nan, np.nan, 1, np.nan, 0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                        'Jumlah': [2, np.nan, np.nan, np.nan, 1, 1, np.nan, 33, np.nan, np.nan, 28, np.nan, 1, 4, np.nan, np.nan, np.nan, np.nan, 35],
                        'Persentase': [5.71, np.nan, np.nan, np.nan, 2.86, 2.86, np.nan, 94.29, np.nan, np.nan, 80, np.nan, 2.86, 11.43, np.nan, np.nan, np.nan, np.nan, 100]
                    }

                # Buat DataFrame
                    df = pd.DataFrame(data)

                # Ganti nilai NaN dengan "Tidak Ada" agar lebih mudah dibaca
                    df.fillna("Tidak Ada", inplace=True)

                # Tambah simbol % pada kolom Persentase
                    df['Persentase'] = df['Persentase'].apply(
                        lambda x: f"{x}%" if pd.notnull(x) and x != "Tidak Ada" else x)

                # Tampilkan tabel di Streamlit
                    st.write("###")
                    st.table(df)

                # Visualisasi Bar Chart interaktif dengan Plotly
                    st.write(
                        "### Visualisasi Jumlah Kematian Berdasarkan Jenis Kelamin")

                # Membuat stacked bar chart
                    fig = px.bar(
                        df,
                        x='Kelurahan',
                        y=['Laki-Laki', 'Perempuan'],
                        title="Jumlah Kematian Berdasarkan Kelurahan dan Jenis Kelamin",
                        labels={'value': 'Jumlah Kematian',
                                'Kelurahan': 'Nama Kelurahan'},
                        height=500,
                        width=800
                    )

                # Menampilkan stacked bar chart di Streamlit
                    st.plotly_chart(fig)

                elif selected_data_title == 'Jumlah Penduduk datang menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023' and visual_type == "Bar Chart":
                    st.write("### ")
                    st.markdown(
                        "### Susunan Tabel Baru & Visualisasi Jumlah Penduduk datang menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023")

                # Data Jumlah Penduduk Datang
                    data_asli = {
                        'Kecamatan': [
                            'Prajurit Kulon', 'Prajurit Kulon', 'Prajurit Kulon', 'Prajurit Kulon', 'Prajurit Kulon', 'Prajurit Kulon',
                            'Magersari', 'Magersari', 'Magersari', 'Magersari', 'Magersari', 'Magersari',
                            'Kranggan', 'Kranggan', 'Kranggan', 'Kranggan', 'Kranggan', 'Kranggan',
                            'Kota Mojokerto'
                        ],
                        'Kelurahan': [
                            'Surodinawan', 'Prajurit Kulon', 'Blooto', 'Mentikan', 'Kauman', 'Pulorejo',
                            'Gunung Gedangan', 'Kedundung', 'Balongsari', 'Gedongan', 'Magersari', 'Wates',
                            'Kranggan', 'Meri', 'Jagalan', 'Miji', 'Sentanan', 'Purwotengah', None
                        ],
                        'Laki-Laki': [
                            97, 64, 48, 71, 18, 63,
                            89, 134, 57, 13, 66, 192,
                            139, 106, 21, 60, 13, 23, 1274  # Total Kota Mojokerto
                        ],
                        'Perempuan': [
                            114, 67, 34, 69, 22, 81,
                            83, 133, 65, 13, 80, 191,
                            114, 78, 17, 78, 12, 19, 1270  # Total Kota Mojokerto
                        ],
                        'Jumlah': [
                            211, 131, 82, 140, 40, 144,
                            172, 267, 122, 26, 146, 383,
                            253, 184, 38, 138, 25, 42, 2544  # Total Kota Mojokerto
                        ],
                        'Persentase': [
                            8.29, 5.15, 3.22, 5.5, 1.57, 5.66,
                            6.76, 10.5, 4.8, 1.02, 5.74, 15.06,
                            9.94, 7.23, 1.49, 5.42, 0.98, 1.65,
                            100  # Persentase Kota Mojokerto
                        ]
                    }

                # Membuat DataFrame
                    df = pd.DataFrame(data_asli)

                # Mengubah kolom 'Persentase' menjadi format string dengan simbol %
                    df['Persentase'] = df['Persentase'].apply(
                        lambda x: f'{x}%')

                # Atau bisa juga menggunakan st.dataframe jika ingin tabelnya lebih interaktif
                    st.dataframe(df)

                # Membuat stacked bar chart interaktif
                    fig = px.bar(
                        df,
                        x='Kecamatan',
                        y=['Laki-Laki', 'Perempuan'],
                        title='Jumlah Penduduk Datang Menurut Kecamatan di Kota Mojokerto (Laki-Laki dan Perempuan)',
                        labels={'value': 'Jumlah Penduduk',
                                'variable': 'Jenis Kelamin'},
                        barmode='stack',
                        text_auto=True
                    )

                # Menampilkan chart di Streamlit
                    st.plotly_chart(fig)

                elif selected_data_title == 'Jumlah Penduduk keluar menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023' and visual_type == "Bar Chart":
                    st.write("### ")
                    st.markdown(
                        "### Susunan Tabel Baru & Visualisasi Jumlah Penduduk keluar menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023")

                # Data Jumlah Penduduk Keluar
                    data_asli = {
                        'Kecamatan': [
                            'Prajurit Kulon', 'Prajurit Kulon', 'Prajurit Kulon', 'Prajurit Kulon', 'Prajurit Kulon', 'Prajurit Kulon',
                            'Magersari', 'Magersari', 'Magersari', 'Magersari', 'Magersari', 'Magersari',
                            'Kranggan', 'Kranggan', 'Kranggan', 'Kranggan', 'Kranggan', 'Kranggan',
                            'Kota Mojokerto'
                        ],
                        'Kelurahan': [
                            'Surodinawan', 'Prajurit Kulon', 'Blooto', 'Mentikan', 'Kauman', 'Pulorejo',
                            'Gunung Gedangan', 'Kedundung', 'Balongsari', 'Gedongan', 'Magersari', 'Wates',
                            'Kranggan', 'Meri', 'Jagalan', 'Miji', 'Sentanan', 'Purwotengah', None
                        ],
                        'Laki-Laki': [
                            61, 65, 31, 45, 18, 47,
                            59, 126, 68, 17, 46, 175,
                            92, 86, 23, 47, 12, 12,
                            1032  # Total Kota Mojokerto
                        ],
                        'Perempuan': [
                            61, 75, 30, 35, 24, 53,
                            67, 89, 63, 22, 73, 176,
                            88, 60, 20, 54, 10, 20,
                            1020  # Total Kota Mojokerto
                        ],
                        'Jumlah': [
                            122, 142, 61, 80, 42, 100,
                            126, 215, 131, 39, 119, 351,
                            180, 146, 43, 101, 22, 32,
                            2052  # Total Kota Mojokerto
                        ],
                        'Persentase': [
                            5.95, 6.92, 2.97, 3.9, 2.05, 4.87,
                            6.14, 10.48, 6.38, 1.9, 5.8, 17.11,
                            8.77, 7.12, 2.1, 4.92, 1.07, 1.56,
                            100  # Persentase Kota Mojokerto
                        ]
                    }

                # Membuat DataFrame
                    df = pd.DataFrame(data_asli)

                # Mengubah kolom 'Persentase' menjadi format string dengan simbol %
                    df['Persentase'] = df['Persentase'].apply(
                        lambda x: f'{x}%')

                # Atau bisa juga menggunakan st.dataframe jika ingin tabelnya lebih interaktif
                    st.dataframe(df)

                # Membuat stacked bar chart interaktif
                    fig = px.bar(
                        df,
                        x='Kecamatan',
                        y=['Laki-Laki', 'Perempuan'],
                        title='Jumlah Penduduk Keluar Menurut Kecamatan di Kota Mojokerto (Laki-Laki dan Perempuan)',
                        labels={'value': 'Jumlah Penduduk',
                                'variable': 'Jenis Kelamin'},
                        barmode='stack',
                        text_auto=True
                    )

                # Menampilkan chart di Streamlit
                    st.plotly_chart(fig)

                elif selected_data_title == 'Banyaknya akte kependudukan diterbitkan menurut jenisnya menurut bulan di Kota Mojokerto, 2023' and visual_type == "Line Chart":
                    st.write("### ")
                    st.markdown(
                        "### Susunan Tabel Baru & Visualisasi Banyaknya akte kependudukan diterbitkan menurut jenisnya menurut bulan di Kota Mojokerto, 2023")

                # Data akte kependudukan diterbitkan per bulan
                    data_akte = {
                        'Bulan': ['Januari'] * 5 + ['Februari'] * 5 + ['Maret'] * 5 + ['April'] * 5 + ['Mei'] * 5 +
                        ['Juni'] * 5 + ['Juli'] * 5 + ['Agustus'] * 5 + ['September'] * 5 + ['Oktober'] * 5 +
                        ['November'] * 5 + ['Desember'] * 5,
                        'Jenis': ['Kelahiran Umum', 'Kelahiran Dispensasi', 'Perkawinan', 'Perceraian', 'Kematian'] * 12,
                        'Jumlah': [
                            352, 52, 3, 0, 96,
                            377, 41, 5, 2, 92,
                            382, 36, 3, 1, 95,
                            273, 24, 0, 1, 77,
                            590, 77, 4, 2, 125,
                            327, 45, 1, 0, 55,
                            313, 55, 9, 5, 167,
                            392, 66, 4, 0, 110,
                            396, 40, 2, 0, 124,
                            409, 49, 3, 0, 399,
                            383, 44, 4, 0, 137,
                            236, 46, 7, 1, 111
                        ]
                    }

                # Menghitung total per jenis
                    total_data = {
                        'Jenis': [
                            'Total Kelahiran Umum',
                            'Total Kelahiran Dispensasi',
                            'Total Perkawinan',
                            'Total Perceraian',
                            'Total Kematian'
                        ],
                        'Jumlah': [
                            4430, 575, 45, 12, 1588
                        ]
                    }

                # Membuat DataFrame
                    df_akte = pd.DataFrame(data_akte)
                    df_total = pd.DataFrame(total_data)

                # Menghitung total per bulan untuk visualisasi
                    df_total_per_bulan = df_akte.groupby(
                        ['Bulan', 'Jenis']).sum().reset_index()

                # Menampilkan tabel di Streamlit
                    st.write(
                        "Tabel Banyaknya Akte Kependudukan Diterbitkan Menurut Jenisnya di Kota Mojokerto, 2023")
                    st.dataframe(df_akte)

                    st.write("Total Banyaknya Akte Kependudukan Diterbitkan")
                    st.dataframe(df_total)

                # Visualisasi Line Chart Interaktif dengan Plotly
                    st.write(
                        "Visualisasi Line Chart Banyaknya Akte Kependudukan Diterbitkan per Bulan")
                    line_chart_data = df_total_per_bulan.pivot(
                        index='Bulan', columns='Jenis', values='Jumlah').reset_index()

                # Menggunakan Plotly untuk membuat line chart
                    fig = px.line(line_chart_data, x='Bulan', y=line_chart_data.columns[1:],
                                  labels={'value': 'Jumlah',
                                          'variable': 'Jenis'},
                                  title='Banyaknya Akte Kependudukan Diterbitkan per Bulan di Kota Mojokerto, 2023')

                    st.plotly_chart(fig)

                elif selected_data_title == 'Kepadatan penduduk akhir tahun Warga Negara Indonesia menurut Kelurahan di Kota Mojokerto, 2023' and visual_type == "Heatmap":
                    st.write("### ")
                    st.markdown(
                        "### Susunan Tabel Baru & Visualisasi Kepadatan penduduk akhir tahun Warga Negara Indonesia menurut Kelurahan di Kota Mojokerto, 2023")

                # Data Kepadatan Penduduk
                    data_kepadatan = {
                        'Kecamatan': [
                            'Prajurit Kulon', 'Prajurit Kulon', 'Prajurit Kulon', 'Prajurit Kulon', 'Prajurit Kulon', 'Prajurit Kulon',
                            'Magersari', 'Magersari', 'Magersari', 'Magersari', 'Magersari', 'Magersari',
                            'Kranggan', 'Kranggan', 'Kranggan', 'Kranggan', 'Kranggan', 'Kranggan',
                            'Kota Mojokerto'
                        ],
                        'Kelurahan': [
                            'Surodinawan', 'Prajurit Kulon', 'Blooto', 'Mentikan', 'Kauman', 'Pulorejo',
                            'Gunung Gedangan', 'Kedundung', 'Balongsari', 'Gedongan', 'Magersari', 'Wates',
                            'Kranggan', 'Meri', 'Jagalan', 'Miji', 'Sentanan', 'Purwotengah',
                            'Kota Mojokerto (Total)'
                        ],
                        'Kepadatan Penduduk (per Km2)': [
                            6671, 5924, 3433, 16522, 12058, 4749,
                            4285, 23446, 35779, 2260, 2169, 11961,
                            10395, 36516, 3552, 4533, 11697, 6437,
                            7014
                        ]
                    }

                # Membuat DataFrame
                    df_kepadatan = pd.DataFrame(data_kepadatan)

                # Membuat Tabel Baru dengan Format yang Lebih Mudah Dipahami
                    st.write("### ")
                    df_kepadatan_format_baru = df_kepadatan.copy()

                # Memisahkan kolom 'Kecamatan', 'Kelurahan', dan 'Kota Mojokerto'
                    df_kepadatan_format_baru['Kecamatan'] = df_kepadatan_format_baru['Kecamatan'].replace({
                                                                                                          'Kota Mojokerto': ''})
                    st.dataframe(df_kepadatan_format_baru)

                # Menampilkan Heatmap Interaktif dengan Plotly
                    st.write(
                        "### Visualisasi Heatmap Kepadatan Penduduk per Km2 di Kota Mojokerto")
                    heatmap_data = df_kepadatan_format_baru.pivot(
                        index='Kelurahan', columns='Kecamatan', values='Kepadatan Penduduk (per Km2)')

                # Menggunakan Plotly untuk membuat heatmap
                    fig = px.imshow(heatmap_data,
                                    labels=dict(
                                        x="Kecamatan", y="Kelurahan", color="Kepadatan Penduduk per Km2"),
                                    title="Heatmap Kepadatan Penduduk per Km2 di Kota Mojokerto, 2023",
                                    color_continuous_scale="Viridis")

                # Menampilkan Heatmap di Streamlit
                    st.plotly_chart(fig)

                elif selected_data_title == 'Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah) 2010-2023' and visual_type == "Line Chart":
                    st.write("### ")
                    st.markdown(
                        "### Susunan Tabel Baru & Visualisasi Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah) 2010-2023")

                # Data pengeluaran per kapita riil disesuaikan (ribu rupiah) untuk semua kabupaten dan kota di Jawa Timur
                    data = {
                        'Tahun': [2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010],
                        'Kabupaten Pacitan': [9681, 9184, 8832, 8451, 7984, 7521, 7035, 6667, 6421, 6143, 5901, 5689, 5412, 5123],
                        'Kabupaten Ponorogo': [10658, 10199, 9867, 9542, 9053, 8612, 8123, 7734, 7476, 7189, 6934, 6721, 6412, 6104],
                        'Kabupaten Trenggalek': [10465, 10042, 9654, 9321, 8876, 8432, 7951, 7589, 7341, 7067, 6810, 6598, 6312, 5995],
                        'Kabupaten Tulungagung': [11543, 11101, 10676, 10254, 9764, 9321, 8865, 8453, 8124, 7756, 7453, 7123, 6765, 6412],
                        'Kabupaten Blitar': [12354, 11898, 11454, 11012, 10467, 9998, 9534, 9123, 8765, 8321, 8012, 7675, 7321, 6974],
                        'Kabupaten Kediri': [13512, 13054, 12576, 12087, 11465, 10987, 10365, 9876, 9567, 9121, 8798, 8432, 8021, 7654],
                        'Kabupaten Malang': [14576, 13985, 13421, 12876, 12210, 11654, 10998, 10543, 10123, 9687, 9321, 8956, 8543, 8121],
                        'Kabupaten Lumajang': [11123, 10712, 10354, 9932, 9523, 9087, 8654, 8276, 7987, 7621, 7310, 7012, 6678, 6321],
                        'Kabupaten Jember': [12543, 12054, 11576, 11123, 10565, 10012, 9532, 9087, 8712, 8321, 7985, 7623, 7254, 6898],
                        'Kabupaten Banyuwangi': [13245, 12689, 12123, 11576, 10932, 10321, 9721, 9243, 8912, 8512, 8156, 7790, 7412, 7012],
                        'Kabupaten Bondowoso':	[11255,	10851,	10690,	10610,	10665,	10429,	10086,	10007,	9518.93,	9176.22,	9138.26,	8855.86,	8418.39,	8064.31],
                        'Kabupaten Situbondo': [10702, 10263, 9996, 9857, 10097, 9692, 9178, 9106, 8676.63, 8382.83, 8350.9, 8173.88, 7812.23, 7441.67],
                        'Kabupaten Probolinggo': [11756, 11254, 10969, 10859, 10972, 10700, 10239, 10170, 9976.33, 9876.57, 9847.45, 9721.2, 9358.52, 9004.01],
                        'Kabupaten Pasuruan': [11239, 10726, 10297, 10164, 10381, 9933, 9556, 9198, 8706.84, 8293.33, 8261.03, 8074.97, 7660.82, 7342.6],
                        'Kabupaten Sidoarjo': [15311, 14808, 14578, 14458, 14609, 14168, 13710, 13320, 12878.57, 12632.01, 12601.8, 12456.69, 12094.93, 11717.16],
                        'Kabupaten Mojokerto': [13467, 13051, 12844, 12779, 12860, 12454, 12240, 11798, 11559.5, 11208.45, 11171.16, 10914.56, 10551.67, 10099.07],
                        'Kabupaten Jombang': [11999, 11579, 11394, 11261, 11533, 10999, 10560, 10237, 9963.25, 9708.86, 9677.98, 9493.01, 9111.84, 8787.83],
                        'Kabupaten Nganjuk': [12821, 12349, 12172, 12130, 12200, 11768, 11560, 11451, 10994.82, 10754.14, 10717.39, 10655.57, 10100.29, 9662.81],
                        'Kabupaten Madiun': [12259, 11848, 11658, 11574, 11650, 11351, 11012, 10904, 10710.22, 10667.45, 10624.84, 10428.85, 9994.91, 9415.93],
                        'Kabupaten Magetan': [12495, 12031, 11833, 11776, 11779, 11539, 11288, 10988, 10593.73, 10538.5, 10483.57, 10374.72, 9635.17, 8961.45],
                        'Kabupaten Ngawi': [11897, 11563, 11459, 11418, 11468, 11187, 10899, 10810, 10583.86, 10143.3, 10104.62, 9905.35, 9387.83, 9003.45],
                        'Kabupaten Bojonegoro': [10776, 10323, 10221, 10121, 10265, 9926, 9553, 9420, 8993.21, 8963.65, 8934.19, 8809.44, 8413.29, 8086.59],
                        'Kabupaten Tuban': [11174, 10703, 10380, 10238, 10499, 10048, 9540, 9353, 8940.49, 8906.12, 8871.88, 8705.73, 8331.81, 7897.68],
                        'Kabupaten Lamongan': [12019, 11648, 11510, 11456, 11572, 11108, 10664, 10252, 9821.5, 9544.78, 9511.33, 9385.63, 8965.78, 8552.94],
                        'Kabupaten Gresik': [13870,	13384,	13280,	13246,	13295,	12845,	12375,	11961,	11548.08,	11513.82,	11479.66,	11359.96,	10926.01,	10490.66],
                        'Kabupaten Bangkalan': [9438,	8971,	8673,	8610,	8718,	8393,	8192, 8030,	7667.19,	7458.74,	7433.51,	7315.93,	7006.22,	6708.78],
                        'Kabupaten Sampang': [9363,	8944,	8790,	8739,	8760,	8569,	8352,	8096,	7826.56,	7797.85,	7769.25,	7691.64,	7336.64,	6952.48],
                        'Kabupaten Pamekasan': [9420,	8967,	8804, 8739,	8834,	8536,	8311,	7975,	7678.96,	7477.62,	7445.21,	7260.28,	6921.79,	6531.72],
                        'Kabupaten Sumenep': [9807,	9388,	9000,	8888,	9082,	8722,	8316,	7846,	7577.27,	7143.08, 7092.74,	6834,	6523.8,	5745.99],
                        'Kota Kediri': [13276, 12700, 12231, 11854, 11321, 10876, 10354, 9912, 9578, 9182, 8891, 8623, 8267, 7891],
                        'Kota Blitar': [14548, 13987, 13432, 13023, 12456, 11987, 11435, 10923, 10542, 10121, 9768, 9456, 9034, 8612],
                        'Kota Malang': [15534, 14987, 14354, 13812, 13123, 12576, 11987, 11423, 10932, 10523, 10123, 9765, 9321, 8912],
                        'Kota Probolinggo': [12987, 12412, 11932, 11345, 10787, 10234, 9634, 9212, 8873, 8432, 8121, 7812, 7412, 6998],
                        'Kota Pasuruan': [14234, 13654, 13023, 12565, 11932, 11343, 10865, 10234, 9821, 9412, 9032, 8621, 8212, 7856],
                        'Kota Mojokerto': [14422, 14054,	13610,	13499,	13710,	13155,	12804,	12449,	12060.5,	11689.21,	11625.22,	11191.2,	10762.44,	10371.48],
                        'Kota Madiun': [17115,	16503,	16095,	16018,	16040,	15616,	15415,	15300,	14723,	14643.42,	14603.96,	14317.08,	13799.03,	13455.16],
                        'Kota Surabaya': [18977,	18345,	17862,	17755,	17854,	17157,	16726,	16295,	15991.04,	15492.16,	15487.63,	15104.14,	14777.32,	14473.18],
                        'Kota Batu': [13603,	13094,	12887,	12824,	12870,	12466,	12057,	11772,	11274.41,	10853.23,	10802.98,	10666.53,	9979.88,	9394.89],
                        'Jawa Timur': [12421, 11900, 11402, 11012, 10500, 10021, 9532, 9121, 8790, 8432, 8150, 7889, 7554, 7190]
                    }
                # Membuat dataframe dari data
                    df = pd.DataFrame(data)
                    # Convert years to strings for display
                    df['Tahun'] = df['Tahun'].astype(str)

                # Memformat tabel baru untuk lebih mudah dibaca
                # Membuat tabel baru terpisah sesuai kelompok wilayah Kabupaten dan Kota
                    kabupaten_df = df[['Tahun',
                                       'Kabupaten Pacitan',
                                       'Kabupaten Ponorogo',
                                       'Kabupaten Trenggalek',
                                       'Kabupaten Tulungagung',
                                       'Kabupaten Blitar',
                                       'Kabupaten Kediri',
                                       'Kabupaten Malang',
                                       'Kabupaten Lumajang',
                                       'Kabupaten Jember',
                                       'Kabupaten Banyuwangi',
                                       'Kabupaten Bondowoso',
                                       'Kabupaten Situbondo',
                                       'Kabupaten Probolinggo',
                                       'Kabupaten Pasuruan',
                                       'Kabupaten Sidoarjo',
                                       'Kabupaten Mojokerto',
                                       'Kabupaten Jombang',
                                       'Kabupaten Nganjuk',
                                       'Kabupaten Madiun',
                                       'Kabupaten Magetan',
                                       'Kabupaten Ngawi',
                                       'Kabupaten Bojonegoro',
                                       'Kabupaten Tuban',
                                       'Kabupaten Lamongan',
                                       'Kabupaten Gresik',
                                       'Kabupaten Bangkalan',
                                       'Kabupaten Sampang',
                                       'Kabupaten Pamekasan',
                                       'Kabupaten Sumenep']]
                    kota_df = df[['Tahun',
                                  'Kota Kediri',
                                  'Kota Blitar',
                                  'Kota Malang',
                                  'Kota Probolinggo',
                                  'Kota Pasuruan',
                                  'Kota Mojokerto',
                                  'Kota Surabaya',
                                  'Kota Batu']]
                    total_df = df[['Tahun', 'Jawa Timur']]

                # Menampilkan tabel Kabupaten secara urut berdasarkan tahun
                    st.subheader(
                        'Tabel Pengeluaran Per Kapita Kabupaten (2023-2010)')
                    st.dataframe(kabupaten_df)

                # Menampilkan tabel Kota secara urut berdasarkan tahun
                    st.subheader(
                        'Tabel Pengeluaran Per Kapita Kota (2023-2010)')
                    st.dataframe(kota_df)

                # Menampilkan tabel total Jawa Timur
                    st.subheader(
                        'Tabel Pengeluaran Per Kapita Jawa Timur (Total Kabupaten + Kota)')
                    st.dataframe(total_df)

                # Create a line chart for districts (Kabupaten)
                    # Adjust index based on your data
                    districts = df.columns[1:24]
                    df_districts = df.melt(
                        id_vars='Tahun', value_vars=districts, var_name='Kabupaten', value_name='Pengeluaran')

                # Plotting Districts Line Chart
                    st.subheader(
                        "Pengeluaran Per Kapita Riil Disesuaikan - Kabupaten")
                    fig_districts = px.line(df_districts, x='Tahun', y='Pengeluaran', color='Kabupaten',
                                            title='Pengeluaran Per Kapita Riil Disesuaikan (Kabupaten) 2010-2023')
                    fig_districts.update_layout(
                        xaxis_title='Tahun', yaxis_title='Pengeluaran (Ribu Rupiah)')
                    st.plotly_chart(fig_districts)

                # Create a line chart for cities (Kota)
                    cities = df.columns[24:]  # Adjust index based on your data
                    df_cities = df.melt(
                        id_vars='Tahun', value_vars=cities, var_name='Kota', value_name='Pengeluaran')

                # Plotting Cities Line Chart
                    st.subheader(
                        "Pengeluaran Per Kapita Riil Disesuaikan - Kota")
                    fig_cities = px.line(df_cities, x='Tahun', y='Pengeluaran', color='Kota',
                                         title='Pengeluaran Per Kapita Riil Disesuaikan (Kota) 2010-2023')
                    fig_cities.update_layout(
                        xaxis_title='Tahun', yaxis_title='Pengeluaran (Ribu Rupiah)')
                    st.plotly_chart(fig_cities)

                elif selected_data_title == 'Harapan Lama Sekolah (HLS) 2010-2023' and visual_type == "Line Chart":
                    st.write("### ")
                    st.markdown(
                        "### Susunan Tabel Baru & Visualisasi Harapan Lama Sekolah (HLS) 2010-2023")

                # Data pengeluaran Harapan Lama Sekolah (HLS) 2010-2023 untuk semua kabupaten dan kota di Jawa Timur
                    data = {
                        'Tahun': [2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010],
                        'Kabupaten Pacitan': [12.68, 12.66, 12.65, 12.64, 12.62, 12.61, 12.41, 12.19, 11.94, 11.61, 11.41, 11.35, 11.03, 11.01],
                        'Kabupaten Ponorogo': [13.77, 13.76, 13.74, 13.73, 13.72, 13.71, 13.7, 13.69, 13.29, 13.04, 12.8, 12.56, 12.33, 12.1],
                        'Kabupaten Trenggalek': [12.62, 12.5, 12.47, 12.35, 12.25, 12.12, 12.1, 12.09, 12.08, 11.64, 11.49, 11.22, 11.17, 11.13],
                        'Kabupaten Tulungagung': [13.34, 13.33, 13.32, 13.31, 13.15, 13.05, 13.04, 13.03, 12.73, 12.72, 12.58, 11.93, 11.84, 11.75],
                        'Kabupaten Blitar': [12.65, 12.64, 12.63, 12.46, 12.45, 12.44, 12.43, 12.42, 11.98, 11.49, 11.37, 11.34, 11.18, 11.03],
                        'Kabupaten Kediri': [13.62, 13.61, 13.44, 13.15, 12.88, 12.87, 12.86, 12.57, 12.15, 12.01, 11.85, 11.57, 11.54, 11.37],
                        'Kabupaten Malang': [13.48, 13.38, 13.24, 13.18, 13.17, 12.87, 12.56, 12.28, 11.98, 11.25, 11.02, 10.87, 10.78, 10.71],
                        'Kabupaten Lumajang': [12.16, 12.02, 11.88, 11.81, 11.8, 11.79, 11.78, 11.77, 11.61, 11.12, 10.94, 10.71, 10.71, 10.49],
                        'Kabupaten Jember': [13.49, 13.44, 13.43, 13.42, 13.22, 13.21, 12.79, 12.31, 12.01, 12, 11.87, 11.11, 10.99, 10.87],
                        'Kabupaten Banyuwangi': [13.12, 13.11, 13.1, 12.8, 12.78, 12.69, 12.68, 12.55, 12.2, 11.81, 11.39, 11.25, 11.22, 11.04],
                        'Kabupaten Bondowoso': [13.32, 13.31, 13.29, 13.28, 13.27, 12.95, 12.94, 12.87, 12.86, 12.85, 12.76, 12.42, 11.72, 11.27],
                        'Kabupaten Situbondo': [13.19, 13.18, 13.16, 13.15, 13.14, 13.01, 13, 12.99, 12.98, 12.97, 12.9, 12.2, 11.54, 11.5],
                        'Kabupaten Probolinggo': [12.63, 12.58, 12.36, 12.35, 12.34, 12.07, 12.06, 12.05, 12.04, 11.6, 11.32, 10.91, 10.4, 10.37],
                        'Kabupaten Pasuruan': [12.77, 12.76, 12.58, 12.41, 12.31, 12.3, 12.05, 11.81, 11.8, 11.78, 11.63, 10.73, 10.59, 10.45],
                        'Kabupaten Sidoarjo': [14.97, 14.95, 14.94, 14.93, 14.91, 14.75, 14.34, 14.13, 13.89, 13.55, 13.25, 12.54, 12.42, 12.37],
                        'Kabupaten Mojokerto': [12.97, 12.96, 12.95, 12.88, 12.61, 12.53, 12.52, 12.44, 12.18, 11.97, 11.86, 11.81, 11.75, 11.69],
                        'Kabupaten Jombang': [13.59, 13.58, 13.57, 13.27, 13, 12.99, 12.7, 12.69, 12.68, 12.65, 12.43, 11.92, 11.54, 11.33],
                        'Kabupaten Nganjuk': [13.17, 13.07, 12.87, 12.86, 12.85, 12.84, 12.83, 12.82, 12.68, 12.65, 12.34, 11.77, 11.15, 10.84],
                        'Kabupaten Madiun': [13.23, 13.18, 13.17, 13.16, 13.14, 13.13, 13.12, 13.11, 13.1, 12.79, 12.53, 12.06, 11.65, 11.59],
                        'Kabupaten Magetan': [14.07, 14.05, 14.04, 14.03, 14, 13.73, 13.72, 13.71, 13.6, 12.77, 12.57, 12.54, 12.42, 12.4],
                        'Kabupaten Ngawi': [12.85, 12.84, 12.83, 12.7, 12.69, 12.68, 12.67, 12.65, 12.31, 12.29, 12.18, 11.96, 11.73, 11.43],
                        'Kabupaten Bojonegoro': [12.92, 12.84, 12.68, 12.39, 12.36, 12.35, 12.34, 12.11, 12.09, 12.08, 12.04, 11.74, 11.43, 11.14],
                        'Kabupaten Tuban': [12.27, 12.24, 12.22, 12.21, 12.2, 12.19, 12.18, 12.17, 12.07, 11.42, 11.13, 11.02, 10.91, 10.47],
                        'Kabupaten Lamongan': [14.02, 14.01, 13.77, 13.48, 13.47, 13.46, 13.45, 13.44, 13.43, 13.41, 13.22, 12.34, 11.88, 11.79],
                        'Kabupaten Gresik': [13.97, 13.96, 13.77, 13.73, 13.72, 13.71, 13.7, 13.69, 13.19, 13.17, 12.85, 12.63, 12.23, 11.89],
                        'Kabupaten Bangkalan': [11.97, 11.91, 11.73, 11.6, 11.59, 11.58, 11.57, 11.56, 11.55, 11.17, 10.96, 10.85, 10.64, 10.29],
                        'Kabupaten Sampang': [11.27, 11.24, 11.21, 11.18, 11.16, 11.15, 11.14, 11.13, 11.08, 10.97, 10.8, 10.6, 10.43, 10.29],
                        'Kabupaten Pamekasan': [11.42, 11.39, 11.36, 11.33, 11.3, 11.25, 11.23, 11.21, 11.2, 11.19, 10.98, 10.87, 10.73, 10.69],
                        'Kabupaten Sumenep': [11.8, 11.78, 11.76, 11.74, 11.71, 11.57, 11.45, 11.43, 11.38, 11.36, 11.15, 11.01, 10.81, 10.54],
                        'Kota Kediri': [15.45, 15.44, 15.27, 15.26, 14.97, 14.96, 14.95, 14.61, 14.3, 13.52, 13.27, 13.09, 12.9, 12.72],
                        'Kota Blitar': [14.57, 14.56, 14.33, 14.32, 14.31, 14.02, 14.01, 14, 13.53, 13.51, 13.15, 12.29, 12.28, 12.13],
                        'Kota Malang': [15.77, 15.76, 15.75, 15.51, 15.41, 15.4, 15.39, 15.38, 15.23, 14.47, 14.16, 14.01, 13.71, 13.41],
                        'Kota Probolinggo': [13.73, 13.67, 13.6, 13.59, 13.57, 13.56, 13.55, 13.54, 13.32, 13.29, 12.97, 12.42, 12.16, 11.91],
                        'Kota Pasuruan': [13.66, 13.64, 13.63, 13.62, 13.6, 13.59, 13.58, 13.57, 13.56, 13.53, 13.29, 12.87, 11.94, 11.86],
                        'Kota Mojokerto': [14.04, 14.02, 14.01, 14, 13.83, 13.82, 13.81, 13.8, 13.33, 13.3, 13.24, 12.98, 12.72, 12.46],
                        'Kota Madiun': [14.44, 14.43, 14.41, 14.4, 14.39, 14.21, 14.2, 14.19, 14.06, 13.64, 13.33, 12.56, 12.44, 12.42],
                        'Kota Surabaya': [14.85, 14.83, 14.81, 14.8, 14.79, 14.78, 14.41, 13.99, 13.52, 13.44, 13.13, 13.05, 12.96, 12.88],
                        'Kota Batu': [14.56, 14.4, 14.16, 14.13, 14.12, 14.04, 14.03, 13.62, 13.16, 12.9, 12.71, 12.67, 12.64, 12.6],
                        'Jawa Timur': [13.38, 13.37, 13.36, 13.19, 13.16, 13.1, 13.09, 12.98, 12.66, 12.45, 12.17, 11.74, 11.62, 11.49]
                    }
                # Membuat dataframe dari data
                    df = pd.DataFrame(data)
                    # Convert years to strings for display
                    df['Tahun'] = df['Tahun'].astype(str)

                # Memformat tabel baru untuk lebih mudah dibaca
                # Membuat tabel baru terpisah sesuai kelompok wilayah Kabupaten dan Kota
                    kabupaten_df = df[['Tahun',
                                       'Kabupaten Pacitan',
                                       'Kabupaten Ponorogo',
                                       'Kabupaten Trenggalek',
                                       'Kabupaten Tulungagung',
                                       'Kabupaten Blitar',
                                       'Kabupaten Kediri',
                                       'Kabupaten Malang',
                                       'Kabupaten Lumajang',
                                       'Kabupaten Jember',
                                       'Kabupaten Banyuwangi',
                                       'Kabupaten Bondowoso',
                                       'Kabupaten Situbondo',
                                       'Kabupaten Probolinggo',
                                       'Kabupaten Pasuruan',
                                       'Kabupaten Sidoarjo',
                                       'Kabupaten Mojokerto',
                                       'Kabupaten Jombang',
                                       'Kabupaten Nganjuk',
                                       'Kabupaten Madiun',
                                       'Kabupaten Magetan',
                                       'Kabupaten Ngawi',
                                       'Kabupaten Bojonegoro',
                                       'Kabupaten Tuban',
                                       'Kabupaten Lamongan',
                                       'Kabupaten Gresik',
                                       'Kabupaten Bangkalan',
                                       'Kabupaten Sampang',
                                       'Kabupaten Pamekasan',
                                       'Kabupaten Sumenep']]
                    kota_df = df[['Tahun',
                                  'Kota Kediri',
                                  'Kota Blitar',
                                  'Kota Malang',
                                  'Kota Probolinggo',
                                  'Kota Pasuruan',
                                  'Kota Mojokerto',
                                  'Kota Surabaya',
                                  'Kota Batu']]
                    total_df = df[['Tahun', 'Jawa Timur']]

                # Menampilkan tabel Kabupaten secara urut berdasarkan tahun
                    st.subheader(
                        'Tabel Harapan Lama Sekolah (HLS) Kabupaten 2010-2023')
                    st.dataframe(kabupaten_df)

                # Menampilkan tabel Kota secara urut berdasarkan tahun
                    st.subheader(
                        'Tabel Harapan Lama Sekolah (HLS) Kota 2010-2023')
                    st.dataframe(kota_df)

                # Menampilkan tabel total Jawa Timur
                    st.subheader(
                        'Tabel Harapan Lama Sekolah (HLS) 2010-2023 Jawa Timur (Total Kabupaten + Kota)')
                    st.dataframe(total_df)

                # Create a line chart for districts (Kabupaten)
                    # Adjust index based on your data
                    districts = df.columns[1:24]
                    df_districts = df.melt(id_vars='Tahun', value_vars=districts,
                                           var_name='Kabupaten', value_name='Harapan Lama Sekolah (HLS)')

                # Plotting Districts Line Chart
                    st.subheader(
                        "Pengeluaran Per Kapita Riil Disesuaikan - Kabupaten")
                    fig_districts = px.line(df_districts, x='Tahun', y='Harapan Lama Sekolah (HLS)',
                                            color='Kabupaten', title='Harapan Lama Sekolah (HLS) Disesuaikan (Kabupaten) 2010-2023')
                    fig_districts.update_layout(
                        xaxis_title='Tahun', yaxis_title='Harapan Lama Sekolah (HLS)')
                    st.plotly_chart(fig_districts)

                # Create a line chart for cities (Kota)
                    cities = df.columns[24:]  # Adjust index based on your data
                    df_cities = df.melt(id_vars='Tahun', value_vars=cities,
                                        var_name='Kota', value_name='Harapan Lama Sekolah (HLS)')

                # Plotting Cities Line Chart
                    st.subheader(
                        "Harapan Lama Sekolah (HLS) Disesuaikan - Kota")
                    fig_cities = px.line(df_cities, x='Tahun', y='Harapan Lama Sekolah (HLS)',
                                         color='Kota', title='Harapan Lama Sekolah (HLS) Disesuaikan (Kota) 2010-2023')
                    fig_cities.update_layout(
                        xaxis_title='Tahun', yaxis_title='Harapan Lama Sekolah (HLS)')
                    st.plotly_chart(fig_cities)

                elif selected_data_title == 'Angka Melek Huruf (Persen) 2016-2006' and visual_type == "Line Chart":
                    st.write("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/IPM Yang Ada/IPM Angka Melek Huruf (Persen) 2016-2006.xlsx'
                    df = pd.read_excel(file_path)

                    # Memeriksa kolom yang ada
                    print(df.columns)  # Memeriksa nama kolom

                    # Format percentage columns
                    # Mengambil semua kolom kecuali kolom pertama
                    percentage_columns = df.columns[1:]

                    # Membuat DataFrame untuk Kabupaten
                    kabupaten_df = df[df['Kabupaten/Kota'].str.contains('Kabupaten', na=False)][[
                        'Kabupaten/Kota'] + list(percentage_columns)]
                    # Membuat DataFrame untuk Kota
                    kota_df = df[df['Kabupaten/Kota'].str.contains(
                        'Kota', na=False)][['Kabupaten/Kota'] + list(percentage_columns)]
                    # Membuat DataFrame untuk Total Jawa Timur
                    jawa_timur_df = df[df['Kabupaten/Kota'] ==
                                       'Jawa Timur'][['Kabupaten/Kota'] + list(percentage_columns)]

                    # Mengubah nilai desimal ke persen dan format dengan simbol %
                    def format_percentage(df):
                        # Mengalikan dengan 100
                        df[percentage_columns] = df[percentage_columns]
                        # Format sebagai persen
                        return df.style.format({col: '{:.2f}%' for col in percentage_columns})

                    # Terapkan format ke masing-masing DataFrame
                    kabupaten_styled = format_percentage(
                        kabupaten_df)  # Simpan hasil format di variabel
                    # Simpan hasil format di variabel
                    kota_styled = format_percentage(kota_df)
                    jawa_timur_styled = format_percentage(
                        jawa_timur_df)  # Simpan hasil format di variabel

                    # Buat tabs untuk menampilkan data
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk data tabel
                    with tab1:
                        st.subheader(
                            'Tabel Angka Melek Huruf (Persen) 2016-2006 - Kabupaten')
                        # Tampilkan DataFrame yang sudah diformat
                        st.write(kabupaten_styled)

                        st.subheader(
                            'Tabel Angka Melek Huruf (Persen) 2016-2006 - Kota')
                        # Tampilkan DataFrame yang sudah diformat
                        st.write(kota_styled)

                        st.subheader(
                            'Tabel Angka Melek Huruf (Persen) 2016-2006 - Jawa Timur (Total)')
                        # Tampilkan DataFrame yang sudah diformat
                        st.write(jawa_timur_styled)

                    # Tab 2 untuk visualisasi
                    with tab2:
                        st.write(
                            "### Visualisasi Angka Melek Huruf (Persen) 2016-2006")

                        # Select box untuk memilih Kabupaten dan Kota
                        selected_kabupaten = st.selectbox(
                            "Pilih Kabupaten", kabupaten_df['Kabupaten/Kota'].values)
                        selected_kota = st.selectbox(
                            "Pilih Kota", kota_df['Kabupaten/Kota'].values)

                        # Line chart untuk Kabupaten yang dipilih
                        kabupaten_long = pd.melt(kabupaten_df, id_vars='Kabupaten/Kota',
                                                 value_vars=percentage_columns, var_name='Tahun', value_name='Persentase')
                        fig_kabupaten = px.line(kabupaten_long[kabupaten_long['Kabupaten/Kota'] == selected_kabupaten], x='Tahun', y='Persentase',
                                                labels={
                                                    'Persentase': 'Angka Melek Huruf (%)'},
                                                title=f'Angka Melek Huruf {selected_kabupaten} (Persen) 2016-2006')
                        st.plotly_chart(fig_kabupaten)

                        # Line chart untuk Kota yang dipilih
                        kota_long = pd.melt(
                            kota_df, id_vars='Kabupaten/Kota', value_vars=percentage_columns, var_name='Tahun', value_name='Persentase')
                        fig_kota = px.line(kota_long[kota_long['Kabupaten/Kota'] == selected_kota], x='Tahun', y='Persentase',
                                           labels={
                                               'Persentase': 'Angka Melek Huruf (%)'},
                                           title=f'Angka Melek Huruf {selected_kota} (Persen) 2016-2006')
                        st.plotly_chart(fig_kota)

                        # Line chart untuk Total Jawa Timur
                        jawa_timur_long = pd.melt(jawa_timur_df, id_vars='Kabupaten/Kota',
                                                  value_vars=percentage_columns, var_name='Tahun', value_name='Persentase')
                        fig_total = px.line(jawa_timur_long,
                                            x='Tahun', y='Persentase',
                                            labels={
                                                'Persentase': 'Angka Melek Huruf (%)'},
                                            title='Angka Melek Huruf Total Jawa Timur (Persen) 2016-2006',
                                            markers=True)  # Menambahkan marker untuk point data
                        st.plotly_chart(fig_total)

                elif selected_data_title == 'Angka Harapan Hidup Jawa Timur (LF SP2020)' and visual_type == "Line Chart":
                    st.write("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/IPM Yang Ada/Angka Harapan Hidup Jawa Timur (LF SP2020).xlsx'
                    df = pd.read_excel(file_path)

                    # Definisikan value_vars di sini
                    value_vars = ["Angka Harapan Hidup (LF SP2020) (Tahun) 2023",
                                  "Angka Harapan Hidup (LF SP2020) (Tahun) 2022",
                                  "Angka Harapan Hidup (LF SP2020) (Tahun) 2021",
                                  "Angka Harapan Hidup (LF SP2020) (Tahun) 2020",
                                  "IPM 2023", "IPM 2022", "IPM 2021", "IPM 2020",
                                  "IPM 2019", "IPM 2018", "IPM 2017", "IPM 2016",
                                  "IPM 2015", "IPM 2014", "IPM 2013", "IPM 2012",
                                  "IPM 2011", "IPM 2010",
                                  "AHH 2023", "AHH 2022", "AHH 2021", "AHH 2020",
                                  "AHH 2019", "AHH 2018", "AHH 2017", "AHH 2016",
                                  "AHH 2015", "AHH 2014", "AHH 2013", "AHH 2012",
                                  "AHH 2011", "AHH 2010"]

                    # Mengubah data menjadi format long untuk visualisasi multi-bar plot
                    df_long = df.melt(
                        id_vars='Wilayah', value_vars=value_vars, var_name='Tahun', value_name='Indeks')

                    # Membuat tab
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk menampilkan tabel data
                    with tab1:
                        st.write("Data Angka Harapan Hidup dan IPM")
                        st.dataframe(df)

                    # Tab 2 untuk menampilkan visualisasi
                    with tab2:
                        # Pilih kolom untuk visualisasi
                        wilayah = st.selectbox(
                            "Pilih Wilayah", df['Wilayah'].unique())
                        # Filter data berdasarkan wilayah
                        filtered_data = df[df['Wilayah'] == wilayah]

                        # Membuat data dalam format yang cocok untuk line chart
                        filtered_data_melted = filtered_data.melt(
                            id_vars=["Wilayah"],
                            value_vars=value_vars,  # Gunakan value_vars yang sudah didefinisikan
                            var_name="Tahun",
                            value_name="Angka Harapan Hidup dan IPM"
                        )

                        # Pilih metrik yang akan divisualisasikan
                        metric_options = {
                            "Angka Harapan Hidup": ["Angka Harapan Hidup (LF SP2020) (Tahun) 2023",
                                                    "Angka Harapan Hidup (LF SP2020) (Tahun) 2022",
                                                    "Angka Harapan Hidup (LF SP2020) (Tahun) 2021",
                                                    "Angka Harapan Hidup (LF SP2020) (Tahun) 2020"],
                            "IPM": ["IPM 2023", "IPM 2022", "IPM 2021", "IPM 2020",
                                    "IPM 2019", "IPM 2018", "IPM 2017", "IPM 2016",
                                    "IPM 2015", "IPM 2014", "IPM 2013", "IPM 2012",
                                    "IPM 2011", "IPM 2010"],
                            "AHH": ["AHH 2023", "AHH 2022", "AHH 2021", "AHH 2020",
                                    "AHH 2019", "AHH 2018", "AHH 2017", "AHH 2016",
                                    "AHH 2015", "AHH 2014", "AHH 2013", "AHH 2012",
                                    "AHH 2011", "AHH 2010"]
                        }

                        metric_type = st.selectbox(
                            "Pilih Tipe Metrik", list(metric_options.keys()))
                        metric_years = metric_options[metric_type]

                        # Filter data berdasarkan wilayah
                        filtered_data = data[data['Wilayah'] == wilayah]

                        # Membuat data dalam format yang cocok untuk line chart
                        filtered_data_melted = filtered_data.melt(
                            id_vars=["Wilayah"],
                            value_vars=metric_years,
                            var_name="Tahun",
                            value_name=metric_type
                        )

                        # Ubah kolom 'Tahun' menjadi format numerik untuk sumbu x
                        filtered_data_melted['Tahun'] = filtered_data_melted['Tahun'].str.extract(
                            '(\d+)').astype(int)

                        # Membuat line chart interaktif
                        fig = px.line(filtered_data_melted,
                                      x="Tahun",
                                      y=metric_type,
                                      title=f"Line Chart: {metric_type} di {wilayah}",
                                      labels={"Tahun": "Tahun", metric_type: metric_type})

                        # Tampilkan line chart
                        st.plotly_chart(fig)

                elif selected_data_title == 'IPM Jawa Timur 2010-2023' and visual_type == "Line Chart":
                    st.write("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/IPM Yang Ada/IPM Jawa Timur 2010-2023.xlsx'
                    df = pd.read_excel(file_path)

                    # Definisikan value_vars di sini
                    value_vars = [2010, 2011, 2012, 2013, 2014, 2015,
                                  2016, 2017, 2018, 2019, 2020, 2021,
                                  2022, 2023]

                    # Mengubah data menjadi format long untuk visualisasi multi-bar plot
                    df_long = df.melt(
                        id_vars='Wilayah', value_vars=value_vars, var_name='Tahun', value_name='Indeks')

                    # Membuat tab
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk menampilkan tabel data
                    with tab1:
                        st.write("IPM Jawa Timur 2010-2023")
                        st.dataframe(df)

                    # Tab 2 untuk menampilkan visualisasi
                    with tab2:
                        # Pilih kolom untuk visualisasi
                        wilayah = st.selectbox(
                            "Pilih Wilayah", df['Wilayah'].unique())
                        # Filter data berdasarkan wilayah
                        filtered_data = df[df['Wilayah'] == wilayah]

                        # Membuat data dalam format yang cocok untuk line chart
                        filtered_data_melted = filtered_data.melt(
                            id_vars=["Wilayah"],
                            value_vars=value_vars,  # Gunakan value_vars yang sudah didefinisikan
                            var_name="Tahun",
                            value_name="IPM"
                        )

                        # Ubah kolom 'Tahun' menjadi format numerik untuk sumbu x
                        filtered_data_melted['Tahun'] = filtered_data_melted['Tahun'].astype(
                            int)

                        # Membuat line chart interaktif
                        fig = px.line(filtered_data_melted,
                                      x="Tahun",
                                      y="IPM",
                                      title=f"Line Chart: IPM di {wilayah} (2010-2023)",
                                      labels={"Tahun": "Tahun", "IPM": "Indeks Pembangunan Manusia"})

                        # Tampilkan line chart
                        st.plotly_chart(fig)

                elif selected_data_title == 'Indeks Pembangunan Manusia Menurut Kabupaten dan Kota' and visual_type == "Bar Chart":
                    st.write("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/IPM Yang Ada/Indeks Pembangunan Manusia Menurut Kabupaten_Kota.xlsx'
                    df = pd.read_excel(file_path)

                    # Mengubah data menjadi format long untuk visualisasi multi-bar plot
                    df_long = df.melt(id_vars='Kabupaten/Kota Se Jawa Timur', value_vars=[
                        'IPM 2021', 'IPM 2022', 'IPM 2023'], var_name='Tahun', value_name='Indeks')

                    # Membuat tab
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk menampilkan tabel data
                    with tab1:
                        st.write(
                            "Indeks Pembangunan Manusia Menurut Kabupaten dan Kota:")
                        st.dataframe(df)

                    # Tab 2 untuk menampilkan visualisasi
                    with tab2:
                        # Menampilkan filter multiselect untuk memilih wilayah
                        wilayah_terpilih = st.multiselect(
                            "Pilih Wilayah", df_long['Kabupaten/Kota Se Jawa Timur'].unique(), default=df_long['Kabupaten/Kota Se Jawa Timur'].unique()[:3])

                        # Filter data berdasarkan wilayah yang dipilih
                        filtered_data = df_long[df_long['Kabupaten/Kota Se Jawa Timur'].isin(
                            wilayah_terpilih)]

                        # Cek apakah filtered_data tidak kosong sebelum melanjutkan
                        if not filtered_data.empty:
                            # Ubah kolom 'Tahun' menjadi format numerik untuk sumbu x
                            filtered_data['Tahun'] = filtered_data['Tahun'].str.extract(
                                '(\d+)').astype(int)

                            # Membuat bar chart interaktif
                            fig = px.bar(filtered_data,
                                         x="Tahun",
                                         y="Indeks",
                                         color="Kabupaten/Kota Se Jawa Timur",  # Warna otomatis berdasarkan wilayah
                                         title=f"Bar Chart: IPM di {', '.join(wilayah_terpilih)} (2021-2023)",
                                         labels={
                                             "Tahun": "Tahun",
                                             "Indeks": "Indeks Pembangunan Manusia"
                                         },
                                         hover_data=[
                                             "Kabupaten/Kota Se Jawa Timur"],
                                         text="Indeks")

                            # Tambahkan gaya bar
                            fig.update_traces(textposition='outside')

                            # Sesuaikan tampilan layout
                            fig.update_layout(
                                xaxis_title="Tahun",
                                yaxis_title="Indeks Pembangunan Manusia",
                                title_x=0.5,
                                bargap=0.2,
                                barmode='group'
                            )

                            # Tampilkan bar chart
                            st.plotly_chart(fig)

                elif selected_data_title == 'Indeks Pembangunan Manusia (UHH LF SP2020)' and visual_type == "Bar Chart":
                    st.write("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/IPM Yang Ada/Indeks Pembangunan Manusia (UHH LF SP2020).xlsx'
                    df = pd.read_excel(file_path)

                    # Mengubah data menjadi format long untuk visualisasi multi-bar plot
                    df_long = df.melt(id_vars='Wilayah', value_vars=[
                        'IPM 2021 (UHH LF SP2020)', 'IPM 2022 (UHH LF SP2020)', 'IPM 2023 (UHH LF SP2020)'], var_name='Tahun', value_name='Indeks')

                    # Membuat tab
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk menampilkan tabel data
                    with tab1:
                        st.write("Indeks Pembangunan Manusia (UHH LF SP2020):")
                        st.dataframe(df)

                    # Tab 2 untuk menampilkan visualisasi
                    with tab2:
                        # Menampilkan filter multiselect untuk memilih wilayah
                        wilayah_terpilih = st.multiselect(
                            "Pilih Wilayah", df_long['Wilayah'].unique(), default=df_long['Wilayah'].unique()[:3])  # Default 3 wilayah pertama

                        # Menampilkan filter multiselect untuk memilih tahun
                        tahun_terpilih = st.multiselect(
                            'Pilih Tahun yang ingin ditampilkan:',
                            options=['IPM 2021 (UHH LF SP2020)',
                                     'IPM 2022 (UHH LF SP2020)', 'IPM 2023 (UHH LF SP2020)'],
                            default=['IPM 2021 (UHH LF SP2020)',
                                     'IPM 2022 (UHH LF SP2020)', 'IPM 2023 (UHH LF SP2020)'],
                            key='tahun_ipmuhh'
                        )

                        # Filter DataFrame berdasarkan wilayah dan tahun yang dipilih
                        filtered_df = df_long[(df_long['Wilayah'].isin(wilayah_terpilih)) & (
                            df_long['Tahun'].isin(tahun_terpilih))]

                        # Membuat visualisasi Bar Chart menggunakan Plotly
                        fig = px.bar(filtered_df, x='Wilayah', y='Indeks', color='Tahun',
                                     title='Bar Chart: IPM (UHH LF SP2020) per Wilayah (2020-2023)',
                                     labels={
                                         'Wilayah': 'Wilayah',
                                         'Indeks': 'Indeks Pembangunan Manusia (UHH LF SP2020)'
                                     },
                                     height=600)

                        # Menyesuaikan layout untuk memperjelas visualisasi
                        fig.update_layout(
                            barmode='group',  # Mengelompokkan bar berdasarkan tahun
                            xaxis_title="Wilayah",  # Sumbu X adalah wilayah
                            yaxis_title="Indeks Pembangunan Manusia (UHH LF SP2020)",
                            legend_title="Tahun",
                            template='plotly_white'
                        )

                        # Tampilkan bar chart
                        st.plotly_chart(fig)

                elif selected_data_title == 'Angka Melek Huruf (Penduduk Usia 15 +)' and visual_type == "Bar Chart":
                    st.write("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/IPM Yang Ada/Angka Melek Huruf (Penduduk Usia 15 +).xlsx'
                    df = pd.read_excel(file_path)

                    # Mengubah data menjadi format long untuk visualisasi multi-line plot
                    df_long = df.melt(id_vars='Kelompok Umur 3', value_vars=[
                        'Angka Melek Huruf (Penduduk Usia 15 +) (Persen) L 2021',
                        'Angka Melek Huruf (Penduduk Usia 15 +) (Persen) L 2022',
                        'Angka Melek Huruf (Penduduk Usia 15 +) (Persen) L 2023',
                        'Angka Melek Huruf (Penduduk Usia 15 +) (Persen) P 2021',
                        'Angka Melek Huruf (Penduduk Usia 15 +) (Persen) P 2022',
                        'Angka Melek Huruf (Penduduk Usia 15 +) (Persen) P 2023'
                    ], var_name='Tahun dan Kelompok', value_name='Angka Melek Huruf')

                    # Membuat tab
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk menampilkan tabel data
                    with tab1:
                        st.write(
                            "Tabel Angka Melek Huruf (Penduduk Usia 15 +) :")
                        st.dataframe(df)

                    # Tab 2 untuk menampilkan visualisasi
                    with tab2:
                        # Menampilkan filter untuk memilih tahun
                        st.sidebar.title("Filter Data")
                        selected_year = st.sidebar.selectbox(
                            'Pilih Tahun', ['2021', '2022', '2023']
                        )

                        # Filter DataFrame berdasarkan tahun yang dipilih
                        filtered_df = df_long[df_long['Tahun dan Kelompok'].str.contains(
                            selected_year)]

                        # Buat bar chart interaktif
                        fig = px.bar(
                            filtered_df,
                            x="Kelompok Umur 3",  # Gunakan kolom yang ada di df_long
                            y="Angka Melek Huruf",
                            color='Tahun dan Kelompok',  # Tambahkan warna berdasarkan kelompok tahun
                            title=f"Bar Chart: Angka Melek Huruf ({selected_year})",
                            labels={
                                "Kelompok Umur 3": "Kelompok Umur",
                                "Angka Melek Huruf": "Angka Melek Huruf (Persen)"
                            },
                            hover_data=["Tahun dan Kelompok"],
                            text="Angka Melek Huruf"
                        )

                        # Atur tampilan bar chart
                        fig.update_traces(textposition='outside')
                        fig.update_layout(
                            xaxis_title="Kelompok Umur",
                            yaxis_title="Angka Melek Huruf (Persen)",
                            title_x=0.5,
                            bargap=0.2,
                            barmode='group'
                        )

                        # Tampilkan bar chart di Streamlit
                        st.plotly_chart(fig)

                elif selected_data_title == 'Indeks Pemberdayaan Gender' and visual_type == "Bar Chart":
                    st.markdown("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/IPM Yang Ada/Indeks Pemberdayaan Gender.xlsx'
                    df = pd.read_excel(file_path)

                    # Mengubah data menjadi format long untuk visualisasi multi-line plot
                    df_long = df.melt(id_vars='Wilayah', value_vars=[
                                      'IDG 2021', 'IDG 2022', 'IDG 2023'], var_name='Tahun', value_name='Indeks')

                    # Membuat tab
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk menampilkan tabel data
                    with tab1:
                        st.write(
                            "Tabel Indeks Pemberdayaan Gender :")
                        st.dataframe(df)
                        # Tab 2 untuk menampilkan visualisasi
                    with tab2:
                        # Menampilkan filter multiselect untuk memilih tahun
                        st.sidebar.title("Filter Data")
                        selected_year = st.sidebar.selectbox(
                            'Pilih Tahun', ['IDG 2021', 'IDG 2022', 'IDG 2023'])

                        # Plot Bar Chart menggunakan Plotly
                        fig = px.bar(df, x='Wilayah', y=selected_year, title=f'Indeks Pemberdayaan Gender {selected_year}',
                                     labels={selected_year: 'Indeks Pemberdayaan Gender (IDG)'}, color=selected_year, height=600)

                        # Tampilkan Bar Chart di Streamlit
                        st.plotly_chart(fig)

                elif selected_data_title == 'Indeks Pembangunan Gender' and visual_type == "Bar Chart":
                    st.write("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/IPM Yang Ada/Indeks Pembangunan Gender.xlsx'
                    df = pd.read_excel(file_path)

                    # Mengubah data menjadi format long untuk visualisasi multi-line plot
                    df_long = df.melt(id_vars='Wilayah', value_vars=[
                                      'IPG 2021', 'IPG 2022', 'IPG 2023'], var_name='Tahun', value_name='Indeks')

                    # Membuat tab
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk menampilkan tabel data
                    with tab1:
                        st.write(
                            "Tabel Indeks Pembangunan Gender :")
                        st.dataframe(df)
                        # Tab 2 untuk menampilkan visualisasi
                    with tab2:
                        # Sidebar untuk memilih tahun
                        st.sidebar.title("Filter Data")
                        selected_year = st.sidebar.selectbox(
                            'Pilih Tahun', ['IPG 2021', 'IPG 2022', 'IPG 2023'])

                        # Buat Bar Chart menggunakan Plotly
                        fig = px.bar(df, x='Wilayah', y=selected_year, title=f'Indeks Pembangunan Gender {selected_year}',
                                     labels={selected_year: 'Indeks Pembangunan Gender (IPG)'}, color=selected_year, height=600)

                        # Tampilkan Bar Chart di Streamlit
                        st.plotly_chart(fig)

                elif selected_data_title == 'Indeks Pembangunan Gender (menggunakan UHH hasil SP2020 LF)' and visual_type == "Line Chart":
                    st.write("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/IPM Yang Ada/Indeks Pembangunan Gender (menggunakan UHH hasil SP2020 LF).xlsx'
                    df = pd.read_excel(file_path)

                    # Mengubah data menjadi format long untuk visualisasi multi-line plot
                    df_long = df.melt(id_vars='Wilayah', value_vars=[
                                      'IPG 2021 (menggunakan UHH hasil SP2020 LF)', 'IPG 2022 (menggunakan UHH hasil SP2020 LF)', 'IPG 2023 (menggunakan UHH hasil SP2020 LF)'], var_name='Tahun', value_name='Indeks')

                    # Membuat tab
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk menampilkan tabel data
                    with tab1:
                        st.write(
                            "Tabel Indeks Pembangunan Gender (menggunakan UHH hasil SP2020 LF):")
                        st.dataframe(df)
                    # Tab 2 untuk menampilkan visualisasi
                    with tab2:
                        # Menampilkan filter multiselect untuk memilih tahun
                        tahun_terpilih = st.multiselect(
                            'Pilih Tahun yang ingin ditampilkan:',
                            options=['IPG 2021 (menggunakan UHH hasil SP2020 LF)',
                                     'IPG 2022 (menggunakan UHH hasil SP2020 LF)', 'IPG 2023 (menggunakan UHH hasil SP2020 LF)'],
                            default=['IPG 2021 (menggunakan UHH hasil SP2020 LF)',
                                     'IPG 2022 (menggunakan UHH hasil SP2020 LF)', 'IPG 2023 (menggunakan UHH hasil SP2020 LF)'],
                            key='tahun_ipg'  # Tambahkan key unik di sini
                        )

                        # Filter data berdasarkan tahun yang dipilih
                        df_filtered = df_long[df_long['Tahun'].isin(
                            tahun_terpilih)]

                        # Membuat visualisasi Line Chart menggunakan Plotly
                        fig = px.line(df_filtered, x='Wilayah', y='Indeks', color='Tahun',
                                      title='Indeks Pembangunan Gender (menggunakan UHH hasil SP2020 LF)',
                                      labels={
                                          'Indeks': 'Indeks Pembangunan Gender', 'Tahun': 'Tahun'},
                                      markers=True, height=600)

                        # Menyesuaikan layout untuk memperjelas visualisasi
                        fig.update_layout(
                            hovermode="x unified",
                            xaxis_title="Wilayah",
                            yaxis_title="Indeks Pembangunan Gender",
                            legend_title="Tahun",
                            template='plotly_white'
                        )

                        # Menampilkan visualisasi di Streamlit
                        st.plotly_chart(fig)

                elif selected_data_title == 'Indeks Ketimpangan Gender (IKG)' and visual_type == "Line Chart":
                    st.write("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/IPM Yang Ada/Indeks Ketimpangan Gender (IKG).xlsx'
                    df = pd.read_excel(file_path)

                    # Mengubah data menjadi format long untuk visualisasi multi-line plot
                    df_long = df.melt(id_vars='Wilayah', value_vars=[
                                      'IKG 2021', 'IKG 2022', 'IKG 2023'], var_name='Tahun', value_name='IKG')

                    # Membuat tab
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk menampilkan tabel data
                    with tab1:
                        st.write("Tabel Indeks Ketimpangan Gender (IKG):")
                        st.dataframe(df)

                    # Tab 2 untuk menampilkan visualisasi
                    with tab2:
                        # Menampilkan filter multiselect untuk memilih tahun
                        tahun_terpilih = st.multiselect(
                            'Pilih Tahun yang ingin ditampilkan:',
                            options=['IKG 2021', 'IKG 2022', 'IKG 2023'],
                            default=['IKG 2021', 'IKG 2022', 'IKG 2023'],
                            key='tahun_ikg'  # Tambahkan key unik di sini
                        )

                        # Filter data berdasarkan tahun yang dipilih
                        df_filtered = df_long[df_long['Tahun'].isin(
                            tahun_terpilih)]

                        # Membuat visualisasi Line Chart menggunakan Plotly
                        fig = px.line(df_filtered, x='Wilayah', y='IKG', color='Tahun',
                                      title='Indeks Ketimpangan Gender (IKG) di Wilayah Jawa Timur',
                                      labels={
                                          'IKG': 'Indeks Ketimpangan Gender', 'Tahun': 'Tahun'},
                                      markers=True, height=600)

                        # Menyesuaikan layout untuk memperjelas visualisasi
                        fig.update_layout(
                            hovermode="x unified",
                            xaxis_title="Wilayah",
                            yaxis_title="Indeks Ketimpangan Gender",
                            legend_title="Tahun",
                            template='plotly_white'
                        )

                        # Menampilkan visualisasi di Streamlit
                        st.plotly_chart(fig)

        else:
            st.error("File untuk data ini belum tersedia.")
    else:
        data = None
