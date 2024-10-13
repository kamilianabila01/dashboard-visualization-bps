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
            "Jenis Visualisasi:", ["Bar Chart"])

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
            "Jenis Visualisasi:", ["Bar Chart"])
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
            "Jenis Visualisasi:", ["Line Chart"])
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
                st.title(f"{selected_data_title}")

            # Tampilan visualisasi berdasarkan pilihan pengguna
                if selected_data_title == 'PDRB Atas Dasar Harga Berlaku Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023' and visual_type == "Line Chart":
                    st.markdown("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/PDRB Pengeluaran Publikasi Softfile/PDRB Atas Dasar Harga Berlaku Menurut Komponen Pengeluaran, Kota Mojokerto 2019-2023.xlsx'
                    df = pd.read_excel(file_path)

                    # Pastikan kolom tahun dalam format string
                    df.columns = df.columns.astype(str)

                    # Buat tabs untuk menampilkan data
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk data tabel
                    with tab1:
                        st.write(
                            "Tabel PDRB Atas Dasar Harga Berlaku Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023:")
                        st.dataframe(df)

                    # Tab 2 untuk visualisasi
                    with tab2:
                        st.write(
                            "### PDRB Atas Dasar Harga Berlaku Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023")

                        # Mengubah DataFrame menjadi format panjang untuk visualisasi
                        df_melted = df.melt(
                            id_vars=['Komponen Pengeluaran'], var_name='Tahun', value_name='Pertumbuhan')

                        # Visualisasi Pertama: Dropdown untuk memilih komponen pengeluaran
                        selected_komponen = st.selectbox(
                            "Pilih Komponen Pengeluaran:", df_melted['Komponen Pengeluaran'].unique())

                        # Filter data berdasarkan komponen yang dipilih
                        filtered_data_komponen = df_melted[df_melted['Komponen Pengeluaran']
                                                           == selected_komponen]

                        # Membuat visualisasi line chart untuk komponen yang dipilih
                        fig_komponen = px.line(
                            filtered_data_komponen,
                            x='Tahun',
                            y='Pertumbuhan',
                            title=f'Distribusi PDRB Berdasarkan {selected_komponen} (2019-2023)',
                            labels={
                                # Mengganti label menjadi Rupiah
                                'Pertumbuhan': 'Nilai PDRB (Rupiah)',
                                'Tahun': 'Tahun'
                            },
                            markers=True,  # Menambahkan marker pada setiap titik
                            template='plotly_white'
                        )

                        # Memperbarui layout untuk meningkatkan visualisasi
                        fig_komponen.update_layout(
                            # Mengganti label sumbu Y
                            yaxis_title="Nilai PDRB (Rupiah)",
                            height=400,
                            title_x=0.5
                        )

                        # Menambahkan tooltip yang informatif
                        fig_komponen.update_traces(hovertemplate='%{x}: %{y}')

                        # Menampilkan visualisasi
                        st.plotly_chart(fig_komponen)

                        # Visualisasi Kedua: Dropdown untuk memilih tahun
                        selected_tahun = st.selectbox(
                            "Pilih Tahun untuk Visualisasi:", df_melted['Tahun'].unique())

                        # Filter data berdasarkan tahun yang dipilih
                        filtered_data_tahun = df_melted[df_melted['Tahun']
                                                        == selected_tahun]

                        # Membuat visualisasi line chart untuk tahun yang dipilih
                        fig_tahun = px.line(
                            filtered_data_tahun,
                            x='Komponen Pengeluaran',
                            y='Pertumbuhan',
                            title=f'Distribusi PDRB pada Tahun {selected_tahun}',
                            labels={
                                # Mengganti label menjadi Rupiah
                                'Pertumbuhan': 'Nilai PDRB (Rupiah)',
                                'Komponen Pengeluaran': 'Komponen Pengeluaran'
                            },
                            markers=True,  # Menambahkan marker pada setiap titik
                            template='plotly_white'
                        )

                        # Memperbarui layout untuk visualisasi kedua
                        fig_tahun.update_layout(
                            # Mengganti label sumbu Y
                            yaxis_title="Nilai PDRB (Rupiah)",
                            height=400,
                            title_x=0.5
                        )

                        # Menambahkan tooltip yang informatif
                        fig_tahun.update_traces(hovertemplate='%{x}: %{y}')

                        # Menampilkan visualisasi kedua
                        st.plotly_chart(fig_tahun)

                elif selected_data_title == 'Distribusi PDRB Atas Dasar Harga Berlaku Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023' and visual_type == "Line Chart":
                    st.markdown("### ")
                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/PDRB Pengeluaran Publikasi Softfile/Distribusi PDRB Atas Dasar Harga Berlaku Menurut Komponen Pengeluaran Kota Mojokerto 2019–2023.xlsx'
                    df = pd.read_excel(file_path)

                    # Pastikan kolom tahun dalam format string
                    df.columns = df.columns.astype(str)

                    # Mengubah data pertumbuhan menjadi persentase dan format sesuai permintaan
                    # Mengabaikan kolom 'Komponen Pengeluaran'
                    for column in df.columns[1:]:
                        # Mengonversi nilai ke float dan menangani kesalahan konversi
                        df[column] = df[column].apply(
                            lambda x: f"{x * 100:.2f}%" if pd.notna(x) and isinstance(x, (int, float)) else "-")

                    # Buat tabs untuk menampilkan data
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk data tabel
                    with tab1:
                        st.write(
                            "Tabel Distribusi PDRB Atas Dasar Harga Berlaku Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023:")
                        st.dataframe(df)

                   # Tab 2 untuk visualisasi
                    with tab2:
                        st.write(
                            "### Distribusi PDRB Atas Dasar Harga Berlaku Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023")

                        # Mengubah DataFrame menjadi format panjang untuk visualisasi
                        df_melted = df.melt(
                            id_vars=['Komponen Pengeluaran'], var_name='Tahun', value_name='Pertumbuhan')

                        # Visualisasi Pertama: Dropdown untuk memilih komponen pengeluaran
                        selected_komponen = st.selectbox(
                            "Pilih Komponen Pengeluaran:", df_melted['Komponen Pengeluaran'].unique())

                        # Filter data berdasarkan komponen yang dipilih
                        filtered_data_komponen = df_melted[df_melted['Komponen Pengeluaran']
                                                           == selected_komponen]

                        # Membuat visualisasi line chart untuk komponen yang dipilih
                        fig_komponen = px.line(
                            filtered_data_komponen,
                            x='Tahun',
                            y='Pertumbuhan',
                            title=f'Distribusi PDRB Berdasarkan {selected_komponen} (2019-2023)',
                            labels={
                                'Pertumbuhan': 'Distribusi (%)', 'Tahun': 'Tahun'},
                            markers=True,  # Menambahkan marker pada setiap titik
                            template='plotly_white'
                        )

                        # Memperbarui layout untuk meningkatkan visualisasi
                        fig_komponen.update_layout(
                            yaxis_title="Distribusi (%)",
                            height=400,
                            title_x=0.5
                        )

                        # Menambahkan tooltip yang informatif
                        fig_komponen.update_traces(hovertemplate='%{x}: %{y}')

                        # Menampilkan visualisasi
                        st.plotly_chart(fig_komponen)

                        # Visualisasi Kedua: Dropdown untuk memilih tahun
                        selected_tahun = st.selectbox(
                            "Pilih Tahun untuk Visualisasi:", df_melted['Tahun'].unique())

                        # Filter data berdasarkan tahun yang dipilih
                        filtered_data_tahun = df_melted[df_melted['Tahun']
                                                        == selected_tahun]

                        # Membuat visualisasi line chart untuk tahun yang dipilih
                        fig_tahun = px.line(
                            filtered_data_tahun,
                            x='Komponen Pengeluaran',
                            y='Pertumbuhan',
                            title=f'Distribusi PDRB pada Tahun {selected_tahun}',
                            labels={
                                'Pertumbuhan': 'Distribusi (%)', 'Komponen Pengeluaran': 'Komponen Pengeluaran'},
                            markers=True,  # Menambahkan marker pada setiap titik
                            template='plotly_white'
                        )

                        # Memperbarui layout untuk visualisasi kedua
                        fig_tahun.update_layout(
                            yaxis_title="Distribusi (%)",
                            height=400,
                            title_x=0.5
                        )

                        # Menambahkan tooltip yang informatif
                        fig_tahun.update_traces(hovertemplate='%{x}: %{y}')

                        # Menampilkan visualisasi kedua
                        st.plotly_chart(fig_tahun)

                elif selected_data_title == 'Laju Pertumbuhan PDRB ADHK 2010 Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023' and visual_type == "Bar Chart":
                    st.markdown("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/PDRB Pengeluaran Publikasi Softfile/Laju Pertumbuhan PDRB ADHK 2010 Menurut Komponen Pengeluaran Kota Mojokerto, 2019- 2023.xlsx'
                    df = pd.read_excel(file_path)

                    # Pastikan kolom tahun dalam format string
                    df.columns = df.columns.astype(str)

                    # Mengubah data pertumbuhan menjadi persentase dan format sesuai permintaan
                    # Mengabaikan kolom 'Komponen Pengeluaran'
                    for column in df.columns[1:]:
                        # Mengonversi nilai ke float dan menangani kesalahan konversi
                        df[column] = df[column].apply(
                            lambda x: f"{x * 100:.2f}%" if pd.notna(x) and isinstance(x, (int, float)) else "-")

                    # Buat tabs untuk menampilkan data
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk data tabel
                    with tab1:
                        st.write(
                            "Tabel Laju Pertumbuhan PDRB ADHK 2010 Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023:")
                        st.dataframe(df)

                    # Tab 2 untuk visualisasi
                    with tab2:
                        st.write(
                            "### Laju Pertumbuhan PDRB ADHK 2010 Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023")

                        # Mengubah DataFrame menjadi format panjang untuk visualisasi
                        df_melted = df.melt(
                            id_vars=['Komponen Pengeluaran'], var_name='Tahun', value_name='Pertumbuhan')

                        # Visualisasi Pertama: Dropdown untuk memilih komponen pengeluaran
                        selected_komponen = st.selectbox(
                            "Pilih Komponen Pengeluaran:", df_melted['Komponen Pengeluaran'].unique())

                        # Filter data berdasarkan komponen yang dipilih
                        filtered_data_komponen = df_melted[df_melted['Komponen Pengeluaran']
                                                           == selected_komponen]

                        # Membuat visualisasi bar chart untuk komponen yang dipilih
                        fig_komponen = px.bar(
                            filtered_data_komponen,
                            x='Tahun',
                            y='Pertumbuhan',
                            title=f'Laju Pertumbuhan PDRB ADHK 2010 untuk {selected_komponen}',
                            labels={
                                'Pertumbuhan': 'Laju Pertumbuhan (%)', 'Tahun': 'Tahun'},
                            text='Pertumbuhan',  # Menampilkan nilai di atas batang
                            template='plotly_white'
                        )

                        # Memperbarui layout untuk meningkatkan visualisasi
                        fig_komponen.update_layout(
                            yaxis_title="Laju Pertumbuhan (%)",
                            height=400,
                            title_x=0.5
                        )

                        # Menambahkan tooltip yang informatif
                        fig_komponen.update_traces(hovertemplate='%{x}: %{y}')

                        # Menampilkan visualisasi
                        st.plotly_chart(fig_komponen)

                        # Visualisasi Kedua: Dropdown untuk memilih tahun
                        selected_tahun = st.selectbox(
                            "Pilih Tahun untuk Visualisasi:", df_melted['Tahun'].unique())

                        # Filter data berdasarkan tahun yang dipilih
                        filtered_data_tahun = df_melted[df_melted['Tahun']
                                                        == selected_tahun]

                        # Membuat visualisasi bar chart untuk tahun yang dipilih
                        fig_tahun = px.bar(
                            filtered_data_tahun,
                            x='Komponen Pengeluaran',
                            y='Pertumbuhan',
                            title=f'Laju Pertumbuhan PDRB ADHK 2010 pada Tahun {selected_tahun}',
                            labels={
                                'Pertumbuhan': 'Laju Pertumbuhan (%)', 'Komponen Pengeluaran': 'Komponen Pengeluaran'},
                            text='Pertumbuhan',  # Menampilkan nilai di atas batang
                            template='plotly_white'
                        )

                        # Memperbarui layout untuk visualisasi kedua
                        fig_tahun.update_layout(
                            yaxis_title="Laju Pertumbuhan (%)",
                            height=400,
                            title_x=0.5
                        )

                        # Menambahkan tooltip yang informatif
                        fig_tahun.update_traces(hovertemplate='%{x}: %{y}')

                        # Menampilkan visualisasi kedua
                        st.plotly_chart(fig_tahun)

                elif selected_data_title == 'Indeks Implisit PDRB Menurut Pengeluaran Kota Mojokerto, 2019-2023' and visual_type == "Line Chart":
                    st.markdown("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/PDRB Pengeluaran Publikasi Softfile/Indeks Implisit PDRB Menurut Pengeluaran Kota Mojokerto, 2019-2023.xlsx'
                    df = pd.read_excel(file_path)

                    # Pastikan kolom tahun dalam format string
                    df.columns = df.columns.astype(str)

                    # Buat tabs untuk menampilkan data
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk data tabel
                    with tab1:
                        st.write(
                            "Tabel Indeks Implisit PDRB Menurut Pengeluaran Kota Mojokerto, 2019-2023:")
                        st.dataframe(df)

                    # Tab 2 untuk visualisasi
                    with tab2:
                        st.write(
                            "### Indeks Implisit PDRB Menurut Pengeluaran Kota Mojokerto, 2019-2023")

                        # Mengubah DataFrame menjadi format panjang untuk visualisasi
                        df_melted = df.melt(
                            id_vars=['Komponen Pengeluaran'], var_name='Tahun', value_name='Pertumbuhan')

                        # Visualisasi Pertama: Dropdown untuk memilih komponen pengeluaran
                        selected_komponen = st.selectbox(
                            "Pilih Komponen Pengeluaran:", df_melted['Komponen Pengeluaran'].unique())

                        # Filter data berdasarkan komponen yang dipilih
                        filtered_data_komponen = df_melted[df_melted['Komponen Pengeluaran']
                                                           == selected_komponen]

                        # Membuat visualisasi line chart untuk komponen yang dipilih
                        fig_komponen = px.line(
                            filtered_data_komponen,
                            x='Tahun',
                            y='Pertumbuhan',
                            title=f'Indeks Implisit PDRB untuk {selected_komponen}',
                            labels={'Pertumbuhan': 'Indeks Pertumbuhan',
                                    'Tahun': 'Tahun'},
                            markers=True,  # Menambahkan marker pada setiap titik data
                            template='plotly_white'
                        )

                        # Memperbarui layout untuk meningkatkan visualisasi
                        fig_komponen.update_layout(
                            xaxis_title="Tahun",
                            yaxis_title="Indeks Pertumbuhan",
                            height=400,
                            title_x=0.5
                        )

                        # Menambahkan tooltip yang informatif
                        fig_komponen.update_traces(
                            hovertemplate='%{x}: %{y:.2f} Indeks')

                        # Menampilkan visualisasi
                        st.plotly_chart(fig_komponen)

                        # Visualisasi Kedua: Dropdown untuk memilih tahun
                        selected_tahun = st.selectbox(
                            "Pilih Tahun untuk Visualisasi:", df_melted['Tahun'].unique())

                        # Filter data berdasarkan tahun yang dipilih
                        filtered_data_tahun = df_melted[df_melted['Tahun']
                                                        == selected_tahun]

                        # Membuat visualisasi line chart untuk tahun yang dipilih
                        fig_tahun = px.line(
                            filtered_data_tahun,
                            x='Komponen Pengeluaran',
                            y='Pertumbuhan',
                            title=f'Indeks Implisit PDRB pada Tahun {selected_tahun}',
                            labels={'Pertumbuhan': 'Indeks Pertumbuhan',
                                    'Komponen Pengeluaran': 'Komponen Pengeluaran'},
                            markers=True,  # Menambahkan marker pada setiap titik data
                            template='plotly_white'
                        )

                        # Memperbarui layout untuk visualisasi kedua
                        fig_tahun.update_layout(
                            xaxis_title="Komponen Pengeluaran",
                            yaxis_title="Indeks Pertumbuhan",
                            height=400,
                            title_x=0.5
                        )

                        # Menambahkan tooltip yang informatif
                        fig_tahun.update_traces(
                            hovertemplate='%{x}: %{y:.2f} Indeks')

                        # Menampilkan visualisasi kedua
                        st.plotly_chart(fig_tahun)

                elif selected_data_title == 'Pertumbuhan Indeks Implisit PDRB Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023' and visual_type == "Bar Chart":
                    st.markdown("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/PDRB Pengeluaran Publikasi Softfile/Pertumbuhan Indeks Implisit PDRB Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023.xlsx'
                    df = pd.read_excel(file_path)

                    # Pastikan kolom tahun dalam format string
                    df.columns = df.columns.astype(str)

                    # Buat tabs untuk menampilkan data
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk data tabel
                    with tab1:
                        st.write(
                            "Tabel Pertumbuhan Indeks Implisit PDRB Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023:")
                        st.dataframe(df)

                    # Tab 2 untuk visualisasi
                    with tab2:
                        st.write(
                            "### Pertumbuhan Indeks Implisit PDRB Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023")

                        # Mengubah DataFrame menjadi format panjang untuk visualisasi
                        df_melted = df.melt(
                            id_vars=['Komponen Pengeluaran'], var_name='Tahun', value_name='Pertumbuhan')

                        # Visualisasi Pertama: Dropdown untuk memilih komponen pengeluaran
                        selected_komponen = st.selectbox(
                            "Pilih Komponen Pengeluaran:", df_melted['Komponen Pengeluaran'].unique())

                        # Filter data berdasarkan komponen yang dipilih
                        filtered_data_komponen = df_melted[df_melted['Komponen Pengeluaran']
                                                           == selected_komponen]

                        # Membuat visualisasi bar chart untuk komponen yang dipilih
                        fig_komponen = px.bar(
                            filtered_data_komponen,
                            x='Tahun',
                            y='Pertumbuhan',
                            title=f'Pertumbuhan Indeks Implisit PDRB untuk {selected_komponen}',
                            labels={'Pertumbuhan': 'Indeks Pertumbuhan',
                                    'Tahun': 'Tahun'},
                            color='Tahun',
                            template='plotly_white',
                            text='Pertumbuhan',  # Menampilkan nilai di atas bar
                        )

                        # Memperbarui layout untuk meningkatkan visualisasi
                        fig_komponen.update_layout(
                            xaxis_title="Tahun",
                            yaxis_title="Indeks Pertumbuhan",
                            legend_title="Tahun",
                            height=400,
                            title_x=0.5
                        )

                        # Menambahkan tooltip untuk menunjukkan nilai dengan satuan
                        fig_komponen.update_traces(
                            hovertemplate='%{x}: %{y:.2f} Indeks')

                        # Menampilkan visualisasi
                        st.plotly_chart(fig_komponen)

                        # Visualisasi Kedua: Dropdown untuk memilih tahun
                        selected_tahun = st.selectbox(
                            "Pilih Tahun untuk Visualisasi:", df_melted['Tahun'].unique())

                        # Filter data berdasarkan tahun yang dipilih
                        filtered_data_tahun = df_melted[df_melted['Tahun']
                                                        == selected_tahun]

                        # Membuat visualisasi bar chart untuk tahun yang dipilih
                        fig_tahun = px.bar(
                            filtered_data_tahun,
                            x='Komponen Pengeluaran',
                            y='Pertumbuhan',
                            title=f'Pertumbuhan Indeks Implisit PDRB pada Tahun {selected_tahun}',
                            labels={'Pertumbuhan': 'Indeks Pertumbuhan',
                                    'Komponen Pengeluaran': 'Komponen Pengeluaran'},
                            color='Komponen Pengeluaran',
                            template='plotly_white',
                            text='Pertumbuhan',  # Menampilkan nilai di atas bar
                        )

                        # Memperbarui layout untuk visualisasi kedua
                        fig_tahun.update_layout(
                            xaxis_title="Komponen Pengeluaran",
                            yaxis_title="Indeks Pertumbuhan",
                            legend_title="Komponen Pengeluaran",
                            height=400,
                            title_x=0.5
                        )

                        # Menambahkan tooltip untuk menunjukkan nilai dengan satuan
                        fig_tahun.update_traces(
                            hovertemplate='%{x}: %{y:.2f} Indeks')

                        # Menampilkan visualisasi kedua
                        st.plotly_chart(fig_tahun)

                elif selected_data_title == 'Perkembangan Komponen Konsumsi Rumah Tangga Kota Mojokerto, 2019-2023' and visual_type == "Line Chart":
                    st.markdown("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/PDRB Pengeluaran Publikasi Softfile/Perkembangan Komponen Konsumsi Rumah Tangga Kota Mojokerto, 2019-2023.xlsx'
                    df = pd.read_excel(file_path)

                    # Pastikan kolom tahun dalam format string
                    df.columns = df.columns.astype(str)

                    # Opsional: Ganti nama kolom untuk kemudahan akses
                    df.rename(columns={'U r a i a n': 'Uraian'}, inplace=True)

                    # Tambahkan kolom satuan berdasarkan nama kolom atau isi data
                    satuan_mapping = {
                        'Total Konsumsi Rumah Tangga (Juta Rp.)': 'Juta Rp.',
                        'a. ADHB': 'Juta Rp.',
                        'b. ADHK 2010 (Juta Rp.)': 'Juta Rp.',
                        'Proporsi terhadap PDRB ADHB': '%',
                        'Rata-rata Konsumsi per Kapita /tahun (Ribu Rp.)': 'Ribu Rp.',
                        'a. ADHB': 'Ribu Rp.',
                        'b. ADHK 2010': 'Ribu Rp.',
                        'Pertumbuhan: a. Total konsumsi Rumah': '%',
                        'Pertumbuhan: b. Per kapita': '%',
                        'Jumlah Penduduk (jiwa)': 'jiwa',
                    }

                    # Buat kolom satuan yang sesuai dengan Uraian
                    df['Satuan'] = df['Uraian'].apply(
                        lambda x: satuan_mapping.get(x, 'unknown'))

                    # Buat tabs untuk menampilkan data
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk data tabel
                    with tab1:
                        st.write(
                            "Tabel Perkembangan Komponen Konsumsi Rumah Tangga Kota Mojokerto, 2019-2023:")
                        st.dataframe(df)

                    # Tab 2 untuk visualisasi
                    with tab2:
                        st.write(
                            "### Visualisasi Perkembangan Komponen Konsumsi Rumah Tangga Kota Mojokerto, 2019-2023")

                        # Mengubah DataFrame menjadi format panjang untuk visualisasi
                        df_melted = df.melt(
                            id_vars=['Uraian', 'Satuan'], var_name='Tahun', value_name='Perkembangan')

                        # Menambahkan dropdown untuk memilih uraian
                        selected_uraian = st.selectbox(
                            "Pilih Uraian:", df_melted['Uraian'].unique())

                        # Filter data berdasarkan uraian yang dipilih
                        filtered_data = df_melted[df_melted['Uraian']
                                                  == selected_uraian]

                        # Membuat visualisasi line chart menggunakan Plotly
                        fig = px.line(
                            filtered_data,
                            x='Tahun',
                            y='Perkembangan',
                            color='Uraian',
                            markers=True,
                            title='Perkembangan Komponen Konsumsi Rumah Tangga Kota Mojokerto, 2019-2023',
                            labels={
                                # Tampilkan satuan yang sesuai
                                'Perkembangan': f'Perkembangan ({filtered_data["Satuan"].unique()[0]})',
                                'Tahun': 'Tahun'
                            },
                            template='plotly_white'
                        )

                        # Memperbarui layout untuk meningkatkan visualisasi
                        fig.update_layout(
                            xaxis_title="Tahun",
                            # Tampilkan satuan pada sumbu Y
                            yaxis_title=f'Perkembangan ({filtered_data["Satuan"].unique()[0]})',
                            legend_title="Uraian",
                            hovermode="x unified",
                            height=600,
                            title_x=0.5
                        )

                        # Menambahkan tooltip satuan pada hover
                        fig.update_traces(
                            hovertemplate='%{x}: %{y:.2f} ' + filtered_data["Satuan"].unique()[0])

                        # Menampilkan visualisasi
                        st.plotly_chart(fig)

                        # Visualisasi Kedua (jika diperlukan)
                        # Menambahkan dropdown untuk memilih tahun
                        selected_year = st.selectbox(
                            "Pilih Tahun:", df_melted['Tahun'].unique())

                        # Filter data berdasarkan tahun yang dipilih
                        filtered_data_year = df_melted[df_melted['Tahun']
                                                       == selected_year]

                        # Membuat visualisasi line chart menggunakan Plotly untuk tahun tertentu
                        fig_year = px.line(
                            filtered_data_year,
                            x='Uraian',  # Menggunakan kolom 'Uraian' yang sudah diganti namanya
                            y='Perkembangan',
                            color='Tahun',
                            markers=True,
                            title='Perkembangan Komponen Konsumsi Rumah Tangga Kota Mojokerto, 2019-2023 (per Tahun)',
                            labels={
                                # Tampilkan satuan yang sesuai
                                'Perkembangan': f'Perkembangan ({filtered_data_year["Satuan"].unique()[0]})',
                                'Uraian': 'Uraian'
                            },
                            template='plotly_white'
                        )

                        # Memperbarui layout untuk visualisasi kedua
                        fig_year.update_layout(
                            xaxis_title="Uraian",
                            # Tampilkan satuan pada sumbu Y
                            yaxis_title=f'Perkembangan ({filtered_data_year["Satuan"].unique()[0]})',
                            legend_title="Tahun",
                            hovermode="x unified",
                            height=600,
                            title_x=0.5
                        )

                        # Menambahkan tooltip satuan pada hover
                        fig_year.update_traces(
                            hovertemplate='%{x}: %{y:.2f} ' + filtered_data_year["Satuan"].unique()[0])

                        # Menampilkan visualisasi kedua
                        st.plotly_chart(fig_year)

                elif selected_data_title == 'Perkembangan Pengeluaran Konsumsi Akhir Pemerintah Kota Mojokerto, 2019-2023' and visual_type == "Line Chart":
                    st.markdown("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/PDRB Pengeluaran Publikasi Softfile/Perkembangan Pengeluaran Konsumsi Akhir Pemerintah Kota Mojokerto, 2019-2023.xlsx'
                    df = pd.read_excel(file_path)

                    # Pastikan kolom tahun dalam format string
                    df.columns = df.columns.astype(str)

                    # Opsional: Ganti nama kolom untuk kemudahan akses
                    df.rename(columns={'U r a i a n': 'Uraian'}, inplace=True)

                    # Tambahkan kolom satuan berdasarkan nama kolom atau isi data
                    satuan_mapping = {
                        'Total Konsumsi Rumah Tangga (Juta Rp.)': 'Juta Rp.',
                        'a. ADHB': 'Juta Rp.',
                        'b. ADHK 2010 (Juta Rp.)': 'Juta Rp.',
                        'Proporsi terhadap PDRB ADHB': '%',
                        'Rata-rata Konsumsi per Kapita /tahun (Ribu Rp.)': 'Ribu Rp.',
                        'a. ADHB': 'Ribu Rp.',
                        'b. ADHK 2010': 'Ribu Rp.',
                        'Pertumbuhan: a. Total konsumsi Rumah': '%',
                        'Pertumbuhan: b. Per kapita': '%',
                        'Jumlah Penduduk (jiwa)': 'jiwa',
                    }

                    # Buat kolom satuan yang sesuai dengan Uraian
                    df['Satuan'] = df['Uraian'].apply(
                        lambda x: satuan_mapping.get(x, 'unknown'))

                    # Buat tabs untuk menampilkan data
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk data tabel
                    with tab1:
                        st.write(
                            "Tabel Perkembangan Konsumsi Rumah Tangga Kota Mojokerto, 2019-2023:")
                        st.dataframe(df)

                    # Tab 2 untuk visualisasi
                    with tab2:
                        st.write(
                            "### Visualisasi Perkembangan Konsumsi Rumah Tangga Kota Mojokerto, 2019-2023")

                        # Mengubah DataFrame menjadi format panjang untuk visualisasi
                        df_melted = df.melt(
                            id_vars=['Uraian', 'Satuan'], var_name='Tahun', value_name='Perkembangan')

                        # Menambahkan dropdown untuk memilih uraian
                        selected_uraian = st.selectbox(
                            "Pilih Uraian:", df_melted['Uraian'].unique())

                        # Filter data berdasarkan uraian yang dipilih
                        filtered_data = df_melted[df_melted['Uraian']
                                                  == selected_uraian]

                        # Membuat visualisasi line chart menggunakan Plotly
                        fig = px.line(
                            filtered_data,
                            x='Tahun',
                            y='Perkembangan',
                            color='Uraian',
                            markers=True,
                            title='Perkembangan Konsumsi Rumah Tangga Kota Mojokerto, 2019-2023',
                            labels={
                                # Tampilkan satuan yang sesuai
                                'Perkembangan': f'Perkembangan ({filtered_data["Satuan"].unique()[0]})',
                                'Tahun': 'Tahun'
                            },
                            template='plotly_white'
                        )

                        # Memperbarui layout untuk meningkatkan visualisasi
                        fig.update_layout(
                            xaxis_title="Tahun",
                            # Tampilkan satuan pada sumbu Y
                            yaxis_title=f'Perkembangan ({filtered_data["Satuan"].unique()[0]})',
                            legend_title="Uraian",
                            hovermode="x unified",
                            height=600,
                            title_x=0.5
                        )

                        # Menambahkan tooltip satuan pada hover
                        fig.update_traces(
                            hovertemplate='%{x}: %{y:.2f} ' + filtered_data["Satuan"].unique()[0])

                        # Menampilkan visualisasi
                        st.plotly_chart(fig)

                        # Visualisasi Kedua (jika diperlukan)
                        # Menambahkan dropdown untuk memilih tahun
                        selected_year = st.selectbox(
                            "Pilih Tahun:", df_melted['Tahun'].unique())

                        # Filter data berdasarkan tahun yang dipilih
                        filtered_data_year = df_melted[df_melted['Tahun']
                                                       == selected_year]

                        # Membuat visualisasi line chart menggunakan Plotly untuk tahun tertentu
                        fig_year = px.line(
                            filtered_data_year,
                            x='Uraian',  # Menggunakan kolom 'Uraian' yang sudah diganti namanya
                            y='Perkembangan',
                            color='Tahun',
                            markers=True,
                            title='Perkembangan Konsumsi Rumah Tangga Kota Mojokerto, 2019-2023 (per Tahun)',
                            labels={
                                # Tampilkan satuan yang sesuai
                                'Perkembangan': f'Perkembangan ({filtered_data_year["Satuan"].unique()[0]})',
                                'Uraian': 'Uraian'
                            },
                            template='plotly_white'
                        )

                        # Memperbarui layout untuk visualisasi kedua
                        fig_year.update_layout(
                            xaxis_title="Uraian",
                            # Tampilkan satuan pada sumbu Y
                            yaxis_title=f'Perkembangan ({filtered_data_year["Satuan"].unique()[0]})',
                            legend_title="Tahun",
                            hovermode="x unified",
                            height=600,
                            title_x=0.5
                        )

                        # Menambahkan tooltip satuan pada hover
                        fig_year.update_traces(
                            hovertemplate='%{x}: %{y:.2f} ' + filtered_data_year["Satuan"].unique()[0])

                        # Menampilkan visualisasi kedua
                        st.plotly_chart(fig_year)

                elif selected_data_title == 'Laju Indeks Harga Implisit PDRB Kota Mojokerto Menurut Pengeluaran 2011-2023' and visual_type == "Line Chart":
                    st.markdown("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/PDRB Pengeluaran Yang Ada/PDRB Laju Indeks Harga Implisit PDRB Kota Mojokerto Menurut Pengeluaran 2011-2023.xlsx'
                    df = pd.read_excel(file_path)

                    # Pastikan kolom tahun dalam format string
                    df.columns = df.columns.astype(str)

                    # Buat tabs untuk menampilkan data
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk data tabel
                    with tab1:
                        st.write(
                            "Tabel Laju Indeks Harga Implisit PDRB Kota Mojokerto Menurut Pengeluaran 2011-2023:")
                        st.dataframe(df)
                    # Tab 2 untuk visualisasi
                    with tab2:
                        st.write(
                            "### Visualisasi Laju Indeks Harga Implisit PDRB Kota Mojokerto Menurut Pengeluaran 2011-2023")

                        # Mengubah DataFrame menjadi format panjang untuk visualisasi
                        df_melted = df.melt(
                            id_vars=['Jenis Pengeluaran'], var_name='Tahun', value_name='Laju Indeks')

                        # Menambahkan dropdown untuk memilih tahun
                        selected_pengeluaran = st.selectbox(
                            "Pilih Jenis Pengeluaran:", df_melted['Jenis Pengeluaran'].unique())

                        # Filter data berdasarkan tahun yang dipilih
                        filtered_data = df_melted[df_melted['Jenis Pengeluaran']
                                                  == selected_pengeluaran]

                        # Membuat visualisasi line chart menggunakan Plotly
                        fig = px.line(
                            filtered_data,
                            x='Tahun',
                            y='Laju Indeks',
                            color='Jenis Pengeluaran',
                            markers=True,
                            title='Laju Indeks Harga Implisit PDRB Kota Mojokerto Menurut Pengeluaran 2011-2023',
                            labels={
                                'Laju Indeks': 'Laju Indeks Harga Implisit (%)', 'Tahun': 'Tahun'},
                            template='plotly_white'
                        )

                        # Memperbarui layout untuk meningkatkan visualisasi
                        fig.update_layout(
                            xaxis_title="Tahun",
                            yaxis_title="Laju Indeks Harga Implisit (%)",
                            legend_title="Jenis Pengeluaran",
                            hovermode="x unified",
                            height=600,
                            title_x=0.5
                        )

                        # Menambahkan tooltip persentase pada hover
                        fig.update_traces(hovertemplate='%{x}: %{y:.2f}%')

                        # Menampilkan visualisasi
                        st.plotly_chart(fig)

                        # Visualisasi Kedua
                        # Menambahkan dropdown untuk memilih tahun
                        selected_year = st.selectbox(
                            "Pilih Tahun:", df_melted['Tahun'].unique())

                        # Filter data berdasarkan tahun yang dipilih
                        filtered_data = df_melted[df_melted['Tahun']
                                                  == selected_year]

                        # Membuat visualisasi line chart menggunakan Plotly
                        fig = px.line(
                            filtered_data,
                            x='Jenis Pengeluaran',
                            y='Laju Indeks',
                            color='Tahun',
                            markers=True,
                            title='Laju Indeks Harga Implisit PDRB Kota Mojokerto Menurut Pengeluaran 2011-2023',
                            labels={
                                'Laju Indeks': 'Laju Indeks Harga Implisit (%)', 'Tahun': 'Tahun'},
                            template='plotly_white'
                        )

                        # Memperbarui layout untuk meningkatkan visualisasi
                        fig.update_layout(
                            xaxis_title="Jenis Pengeluaran",
                            yaxis_title="Laju Indeks Harga Implisit (%)",
                            legend_title="Tahun",
                            hovermode="x unified",
                            height=600,
                            title_x=0.5
                        )

                        # Menambahkan tooltip persentase pada hover
                        fig.update_traces(hovertemplate='%{x}: %{y:.2f}%')

                        # Menampilkan visualisasi
                        st.plotly_chart(fig)

                elif selected_data_title == 'Distribusi PDRB Kota Mojokerto Atas Dasar Harga Berlaku Menurut Pengeluaran 2010-2023' and visual_type == "Bar Chart":
                    st.markdown("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/PDRB Pengeluaran Publikasi Softfile/Distribusi PDRB Kota Mojokerto Atas Dasar Harga Berlaku Menurut Pengeluaran 2010-2023.xlsx'
                    df = pd.read_excel(file_path)

                    # Pastikan kolom tahun dalam format string
                    df.columns = df.columns.astype(str)

                    # Buat tabs untuk menampilkan data
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk data tabel
                    with tab1:
                        st.write(
                            "Tabel Distribusi PDRB Kota Mojokerto Atas Dasar Harga Berlaku Menurut Pengeluaran 2010-2023:")

                        # Mengubah data persentase ke format yang tepat tanpa menghilangkan desimal
                        df_percentage = df.copy()

                        # Mengubah semua kolom kecuali kolom pertama (yang berisi Lapangan Usaha) ke format persentase dengan 2 desimal
                        df_percentage.iloc[:, 1:] = df_percentage.iloc[:, 1:].applymap(
                            lambda x: f"{x:.2f}%")

                        # Menampilkan tabel dengan persentase yang tidak dibulatkan
                        st.dataframe(df_percentage)

                    # Tab 2 untuk visualisasi
                    with tab2:
                        st.write(
                            "### Visualisasi Distribusi PDRB Kota Mojokerto Atas Dasar Harga Berlaku Menurut Pengeluaran 2010-2023")

                        # Memodifikasi kolom 'Lapangan Usaha/Industry' untuk memotong nama sebelum tanda miring
                        df['Jenis Pengeluaran'] = df['Jenis Pengeluaran'].apply(
                            lambda x: x.split('/')[0].strip())

                        # Mengubah DataFrame menjadi format panjang untuk visualisasi
                        df_melted = df.melt(
                            id_vars=['Jenis Pengeluaran'], var_name='Tahun', value_name='Persentase')

                        # Menambahkan dropdown untuk memilih tahun
                        selected_year = st.selectbox(
                            "Pilih Tahun:", df_melted['Tahun'].unique())

                        # Filter data berdasarkan tahun yang dipilih
                        filtered_data = df_melted[df_melted['Tahun']
                                                  == selected_year]

                        # Membuat visualisasi stacked bar chart menggunakan plotly
                        fig = px.bar(
                            filtered_data,
                            x='Jenis Pengeluaran',
                            y='Persentase',
                            color='Jenis Pengeluaran',
                            text='Persentase',  # Menampilkan nilai persentase pada bar
                            title=f'Distribusi PDRB Kota Mojokerto Atas Dasar Harga Berlaku Menurut Pengeluaran ({selected_year})',
                            labels={
                                'Persentase': 'Persentase (%)', 'Jenis Pengeluaran': 'Jenis Pengeluaran'},
                        )

                        # Update sumbu x agar miring dan tidak terlalu panjang, serta memperkecil font di sumbu x
                        fig.update_layout(
                            xaxis_tickangle=-45,
                            xaxis_title='Jenis Pengeluaran',
                            yaxis_title='Persentase (%)',
                            legend_title='Jenis Pengeluaran',
                            legend=dict(
                                orientation="v",  # Menampilkan legend secara vertikal
                                yanchor="top",
                                y=1,
                                xanchor="left",
                                x=1.05,  # Menempatkan legend di sebelah kanan
                                title_text="Jenis Pengeluaran",
                                itemsizing='constant'  # Menjamin ukuran legend tetap proporsional
                            ),
                            height=600,
                            title_x=0.5,
                        )

                        # Memastikan semua legend ditampilkan
                        fig.update_traces(
                            texttemplate='%{text:.2f}%', textposition='outside')

                        # Tampilkan plot
                        st.plotly_chart(fig)

                        # visualisasi kedua
                        # Menambahkan dropdown untuk memilih jenis pengeluaran
                        selected_jenis = st.selectbox(
                            "Pilih Jenis Pengeluaran:", df_melted['Jenis Pengeluaran'].unique())

                        # Filter data berdasarkan tahun yang dipilih
                        filtered_data = df_melted[df_melted['Jenis Pengeluaran']
                                                  == selected_jenis]

                        # Membuat visualisasi stacked bar chart menggunakan plotly
                        fig = px.bar(
                            filtered_data,
                            x='Tahun',
                            y='Persentase',
                            color='Tahun',
                            text='Persentase',  # Menampilkan nilai persentase pada bar
                            title=f'Distribusi PDRB Kota Mojokerto Atas Dasar Harga Berlaku Menurut Pengeluaran ({selected_jenis})',
                            labels={
                                'Persentase': 'Persentase (%)', 'Tahun': 'Tahun'},
                        )

                        # Update sumbu x agar miring dan tidak terlalu panjang, serta memperkecil font di sumbu x
                        fig.update_layout(
                            xaxis_tickangle=-45,
                            xaxis_title='Tahun',
                            yaxis_title='Persentase (%)',
                            legend_title='Tahun',
                            legend=dict(
                                orientation="v",  # Menampilkan legend secara vertikal
                                yanchor="top",
                                y=1,
                                xanchor="left",
                                x=1.05,  # Menempatkan legend di sebelah kanan
                                title_text="Tahun",
                                itemsizing='constant'  # Menjamin ukuran legend tetap proporsional
                            ),
                            height=600,
                            title_x=0.5,
                        )

                        # Memastikan semua legend ditampilkan
                        fig.update_traces(
                            texttemplate='%{text:.2f}%', textposition='outside')

                        # Tampilkan plot
                        st.plotly_chart(fig)

                elif selected_data_title == 'Distribusi Persentase Produk Domestik Regional Bruto Kota Mojokerto Atas Dasar Harga Berlaku Menurut Lapangan Usaha, 2019─2023' and visual_type == "Stacked Bar Chart":
                    st.markdown("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/PDRB Lapangan Usaha Publikasi Softfile/Distribusi Persentase Produk Domestik Regional Bruto Kota Mojokerto Atas Dasar Harga Berlaku Menurut Lapangan Usaha, 2019─2023.xlsx'
                    df = pd.read_excel(file_path)

                    # Pastikan kolom tahun dalam format string
                    df.columns = df.columns.astype(str)

                    # Buat tabs untuk menampilkan data
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk data tabel
                    with tab1:
                        st.write(
                            "Tabel Distribusi Persentase PDRB Kota Mojokerto:")

                        # Mengubah data persentase ke format yang tepat tanpa menghilangkan desimal
                        df_percentage = df.copy()

                        # Mengubah semua kolom kecuali kolom pertama (yang berisi Lapangan Usaha) ke format persentase dengan 2 desimal
                        df_percentage.iloc[:, 1:] = df_percentage.iloc[:, 1:].applymap(
                            lambda x: f"{x:.2f}%")

                        # Menampilkan tabel dengan persentase yang tidak dibulatkan
                        st.dataframe(df_percentage)

                    # Tab 2 untuk visualisasi
                    with tab2:
                        st.write(
                            "### Visualisasi Distribusi Persentase PDRB Kota Mojokerto")

                        # Memodifikasi kolom 'Lapangan Usaha/Industry' untuk memotong nama sebelum tanda miring
                        df['Lapangan Usaha/Industry'] = df['Lapangan Usaha/Industry'].apply(
                            lambda x: x.split('/')[0].strip())

                        # Mengubah DataFrame menjadi format panjang untuk visualisasi
                        df_melted = df.melt(
                            id_vars=['Lapangan Usaha/Industry'], var_name='Tahun', value_name='Persentase')

                        # Menambahkan dropdown untuk memilih tahun
                        selected_year = st.selectbox(
                            "Pilih Tahun:", df_melted['Tahun'].unique())

                        # Filter data berdasarkan tahun yang dipilih
                        filtered_data = df_melted[df_melted['Tahun']
                                                  == selected_year]

                        # Membuat visualisasi stacked bar chart menggunakan plotly
                        fig = px.bar(
                            filtered_data,
                            x='Lapangan Usaha/Industry',
                            y='Persentase',
                            color='Lapangan Usaha/Industry',
                            text='Persentase',  # Menampilkan nilai persentase pada bar
                            title=f'Distribusi Persentase PDRB Kota Mojokerto ({selected_year})',
                            labels={
                                'Persentase': 'Persentase (%)', 'Lapangan Usaha/Industry': 'Lapangan Usaha'},
                        )

                        # Update sumbu x agar miring dan tidak terlalu panjang, serta memperkecil font di sumbu x
                        fig.update_layout(
                            xaxis_tickangle=-45,
                            xaxis_title='Lapangan Usaha',
                            yaxis_title='Persentase (%)',
                            legend_title='Lapangan Usaha',
                            legend=dict(
                                orientation="v",  # Menampilkan legend secara vertikal
                                yanchor="top",
                                y=1,
                                xanchor="left",
                                x=1.05,  # Menempatkan legend di sebelah kanan
                                title_text="Lapangan Usaha",
                                itemsizing='constant'  # Menjamin ukuran legend tetap proporsional
                            ),
                            height=600,
                            title_x=0.5,
                        )

                        # Memastikan semua legend ditampilkan
                        fig.update_traces(
                            texttemplate='%{text:.2f}%', textposition='outside')

                        # Tampilkan plot
                        st.plotly_chart(fig)

                        # visualisasi kedua
                        # Menambahkan dropdown untuk memilih jenis Lapangan Usaha/Industry
                        selected_jenis = st.selectbox(
                            "Pilih Lapangan Usaha/Industry:", df_melted['Lapangan Usaha/Industry'].unique())

                        # Filter data berdasarkan tahun yang dipilih
                        filtered_data = df_melted[df_melted['Lapangan Usaha/Industry']
                                                  == selected_jenis]

                        # Membuat visualisasi stacked bar chart menggunakan plotly
                        fig = px.bar(
                            filtered_data,
                            x='Tahun',
                            y='Persentase',
                            color='Tahun',
                            text='Persentase',  # Menampilkan nilai persentase pada bar
                            title=f'Distribusi Persentase PDRB Kota Mojokerto ({selected_jenis})',
                            labels={
                                'Persentase': 'Persentase (%)', 'Tahun': 'Tahun'},
                        )

                        # Update sumbu x agar miring dan tidak terlalu panjang, serta memperkecil font di sumbu x
                        fig.update_layout(
                            xaxis_tickangle=-45,
                            xaxis_title='Tahun',
                            yaxis_title='Persentase (%)',
                            legend_title='Tahun',
                            legend=dict(
                                orientation="v",  # Menampilkan legend secara vertikal
                                yanchor="top",
                                y=1,
                                xanchor="left",
                                x=1.05,  # Menempatkan legend di sebelah kanan
                                title_text="Tahun",
                                itemsizing='constant'  # Menjamin ukuran legend tetap proporsional
                            ),
                            height=600,
                            title_x=0.5,
                        )

                        # Memastikan semua legend ditampilkan
                        fig.update_traces(
                            texttemplate='%{text:.2f}%', textposition='outside')

                        # Tampilkan plot
                        st.plotly_chart(fig)

                elif selected_data_title == 'Laju Pertumbuhan Produk Domestik Regional Bruto Atas Dasar Harga Konstan 2010 Kota Mojokerto Menurut Lapangan Usaha (persen), 2019─2023' and visual_type == "Bar Chart":
                    st.markdown("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/PDRB Lapangan Usaha Publikasi Softfile/Laju Pertumbuhan Produk Domestik Regional Bruto Atas Dasar Harga Konstan 2010 Kota Mojokerto Menurut Lapangan Usaha (persen), 2019─2023.xlsx'
                    df = pd.read_excel(file_path)

                    # Pastikan kolom tahun dalam format string
                    df.columns = df.columns.astype(str)

                    # Buat tabs untuk menampilkan data
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk data tabel
                    with tab1:
                        st.write(
                            "Tabel Laju Pertumbuhan Produk Domestik Regional Bruto Atas Dasar Harga Konstan 2010 Kota Mojokerto Menurut Lapangan Usaha (persen), 2019─2023:")

                        # Mengubah data persentase ke format yang tepat tanpa menghilangkan desimal
                        df_percentage = df.copy()

                        # Mengubah semua kolom kecuali kolom pertama (yang berisi Lapangan Usaha) ke format persentase dengan 2 desimal
                        df_percentage.iloc[:, 1:] = df_percentage.iloc[:, 1:].applymap(
                            lambda x: f"{x:.2f}%")

                        # Menampilkan tabel dengan persentase yang tidak dibulatkan
                        st.dataframe(df_percentage)

                    # Tab 2 untuk visualisasi
                    with tab2:
                        st.write(
                            "### Visualisasi Laju Pertumbuhan PDRB Menurut Lapangan Usaha (2019-2023)")

                        # Memodifikasi kolom 'Lapangan Usaha/Industry' untuk memotong nama sebelum tanda miring
                        df['Lapangan Usaha/Industry'] = df['Lapangan Usaha/Industry'].apply(
                            lambda x: x.split('/')[0].strip())

                        # Mengubah DataFrame menjadi format panjang untuk visualisasi
                        df_melted = df.melt(
                            id_vars=['Lapangan Usaha/Industry'], var_name='Tahun', value_name='Persentase')

                        # Menambahkan dropdown untuk memilih tahun
                        selected_year = st.selectbox(
                            "Pilih Tahun:", df_melted['Tahun'].unique())

                        # Filter data berdasarkan tahun yang dipilih
                        filtered_data = df_melted[df_melted['Tahun']
                                                  == selected_year]

                        # Membuat visualisasi stacked bar chart menggunakan plotly
                        fig = px.bar(
                            filtered_data,
                            x='Lapangan Usaha/Industry',
                            y='Persentase',
                            color='Lapangan Usaha/Industry',
                            text='Persentase',  # Menampilkan nilai persentase pada bar
                            title=f' Laju Pertumbuhan Produk Domestik Regional Bruto Atas Dasar Harga Konstan 2010 ({selected_year})',
                            labels={
                                'Persentase': 'Persentase (%)', 'Lapangan Usaha/Industry': 'Lapangan Usaha'},
                        )

                        # Update sumbu x agar miring dan tidak terlalu panjang, serta memperkecil font di sumbu x
                        fig.update_layout(
                            xaxis_tickangle=-45,
                            xaxis_title='Lapangan Usaha',
                            yaxis_title='Persentase (%)',
                            legend_title='Lapangan Usaha',
                            legend=dict(
                                orientation="v",  # Menampilkan legend secara vertikal
                                yanchor="top",
                                y=1,
                                xanchor="left",
                                x=1.05,  # Menempatkan legend di sebelah kanan
                                title_text="Lapangan Usaha",
                                itemsizing='constant'  # Menjamin ukuran legend tetap proporsional
                            ),
                            height=600,
                            title_x=0.5,
                        )

                        # Memastikan semua legend ditampilkan
                        fig.update_traces(
                            texttemplate='%{text:.2f}%', textposition='outside')

                        # Tampilkan plot
                        st.plotly_chart(fig)

                        # visualisasi kedua
                        # Menambahkan dropdown untuk memilih jenis Lapangan Usaha/Industry
                        selected_jenis = st.selectbox(
                            "Pilih Lapangan Usaha/Industry:", df_melted['Lapangan Usaha/Industry'].unique())

                        # Filter data berdasarkan tahun yang dipilih
                        filtered_data = df_melted[df_melted['Lapangan Usaha/Industry']
                                                  == selected_jenis]

                        # Membuat visualisasi stacked bar chart menggunakan plotly
                        fig = px.bar(
                            filtered_data,
                            x='Tahun',
                            y='Persentase',
                            color='Tahun',
                            text='Persentase',  # Menampilkan nilai persentase pada bar
                            title=f'Laju Pertumbuhan Produk Domestik Regional Bruto Atas Dasar Harga Konstan 2010 ({selected_jenis})',
                            labels={
                                'Persentase': 'Persentase (%)', 'Tahun': 'Tahun'},
                        )

                        # Update sumbu x agar miring dan tidak terlalu panjang, serta memperkecil font di sumbu x
                        fig.update_layout(
                            xaxis_tickangle=-45,
                            xaxis_title='Tahun',
                            yaxis_title='Persentase (%)',
                            legend_title='Tahun',
                            legend=dict(
                                orientation="v",  # Menampilkan legend secara vertikal
                                yanchor="top",
                                y=1,
                                xanchor="left",
                                x=1.05,  # Menempatkan legend di sebelah kanan
                                title_text="Tahun",
                                itemsizing='constant'  # Menjamin ukuran legend tetap proporsional
                            ),
                            height=600,
                            title_x=0.5,
                        )

                        # Memastikan semua legend ditampilkan
                        fig.update_traces(
                            texttemplate='%{text:.2f}%', textposition='outside')

                        # Tampilkan plot
                        st.plotly_chart(fig)

                elif selected_data_title == 'Penduduk, Distribusi Persentase Penduduk, Kepadatan Penduduk, Rasio Jenis Kelamin Penduduk Menurut Kecamatan di Kota Mojokerto, 2023' and visual_type == "Stacked Bar Chart":
                    st.markdown("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/Kependudukan Publikasi Softfile/Penduduk, Distribusi Persentase Penduduk, Kepadatan Penduduk, Rasio Jenis Kelamin Penduduk Menurut Kecamatan di Kota Mojokerto, 2023.xlsx'
                    df = pd.read_excel(file_path)

                    # Memformat kolom 'Persentase Penduduk' dengan simbol %
                    if 'Persentase Penduduk' in df.columns:
                        df['Persentase Penduduk'] = df['Persentase Penduduk'].apply(
                            lambda x: f"{x:.2f} %")

                    # Memisahkan data untuk kecamatan yang diminta
                    kecamatan_target = [
                        'PRAJURIT KULON', 'MAGERSARI', 'KRANGGAN']
                    df_kecamatan_target = df[df['Kecamatan'].isin(
                        kecamatan_target)]

                    # Memisahkan data Kota Mojokerto
                    df_kota_mojokerto = df[df['Kecamatan'] == 'Kota Mojokerto']

                    # Buat tabs untuk menampilkan data
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk data tabel
                    with tab1:
                        st.write(
                            "Tabel Penduduk, Distribusi Persentase Penduduk, Kepadatan Penduduk, Rasio Jenis Kelamin Penduduk Menurut Kecamatan di Kota Mojokerto, 2023:")
                        st.dataframe(df)

                    # Tab 2 untuk visualisasi
                    with tab2:
                        st.write("### Visualisasi Penduduk Menurut Kecamatan")

                        # Selectbox untuk memilih kolom yang akan divisualisasikan
                        selected_column = st.selectbox(
                            'Pilih kolom yang akan divisualisasikan:',
                            options=['Penduduk', 'Persentase Penduduk',
                                     'Kepadatan Penduduk per km2', 'Rasio Jenis Kelamin Penduduk']
                        )

                        # Visualisasi untuk kecamatan PRAJURIT KULON, MAGERSARI, KRANGGAN
                        fig1 = px.bar(
                            df_kecamatan_target,
                            x='Kecamatan',
                            y=selected_column,  # Menggunakan kolom yang dipilih
                            title=f'{selected_column} di Kecamatan Tertentu di Kota Mojokerto, 2023',
                            labels={selected_column: selected_column,
                                    'Kecamatan': 'Kecamatan'},
                            text=selected_column,  # Menampilkan nilai yang sesuai di setiap bar
                        )
                        st.plotly_chart(fig1)

                        # Visualisasi Kedua untuk Kota Mojokerto
                        fig2 = px.bar(
                            df_kota_mojokerto,
                            x='Kecamatan',
                            y=selected_column,  # Menggunakan kolom yang dipilih
                            title=f'{selected_column} di Kota Mojokerto, 2023',
                            labels={selected_column: selected_column,
                                    'Kecamatan': 'Kecamatan'},
                            text=selected_column,  # Menampilkan nilai yang sesuai di setiap bar
                        )
                        st.plotly_chart(fig2)

                elif selected_data_title == 'Penduduk akhir tahun Warga Negara Indonesia menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023' and visual_type == "Bar Chart":
                    st.markdown("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/Kependudukan Publikasi Softfile/Penduduk akhir tahun Warga Negara Indonesia menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto , 2023.xlsx'
                    df = pd.read_excel(file_path)

                    # Menghapus spasi dari nilai di dalam kolom 'Laki-laki', 'Perempuan', dan 'Jumlah'
                    df['Laki-laki'] = df['Laki-laki'].apply(lambda x: str(
                        x).replace(' ', '') if isinstance(x, str) else x)
                    df['Perempuan'] = df['Perempuan'].apply(lambda x: str(
                        x).replace(' ', '') if isinstance(x, str) else x)
                    df['Jumlah'] = df['Jumlah'].apply(lambda x: str(
                        x).replace(' ', '') if isinstance(x, str) else x)

                    # Mengubah nilai kolom 'Persentase' menjadi bentuk persen, pastikan hanya memformat angka
                    df['Persentase'] = df['Persentase'].apply(
                        lambda x: f'{float(x):.2f}%' if pd.api.types.is_numeric_dtype(
                            type(x)) else x
                    )

                    # Memisahkan data Kota Mojokerto dari data Kelurahan lainnya
                    df_kota_mojokerto = df[df['Kelurahan'] == 'Kota Mojokerto']
                    df_no_kota_mojokerto = df[df['Kelurahan']
                                              != 'Kota Mojokerto']

                    # Buat tabs untuk menampilkan data
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])
                    # Tab 1 untuk data tabel
                    with tab1:
                        st.write(
                            "Tabel Penduduk akhir tahun Warga Negara Indonesia menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023:")
                        st.dataframe(df)
                    # Tab 2 untuk visualisasi
                    with tab2:
                        st.write(
                            "### Visualisasi Penduduk akhir tahun Warga Negara Indonesia menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023")

                        # Menggunakan melt untuk mengubah format dataframe agar kolom 'Laki-laki', 'Perempuan', dan 'Jumlah' bisa ditampilkan sebagai nilai
                        df_melt = df_no_kota_mojokerto.melt(id_vars='Kelurahan',
                                                            value_vars=[
                                                                'Laki-laki', 'Perempuan', 'Jumlah'],
                                                            var_name='Jenis Kelamin',
                                                            value_name='Nilai')  # Ganti 'Jumlah' dengan 'Nilai'

                        fig1 = px.bar(
                            df_melt,
                            x='Kelurahan',
                            y='Nilai',  # Menggunakan 'Nilai' sebagai sumbu y
                            color='Jenis Kelamin',
                            title='Jumlah Penduduk akhir tahun Warga Negara Indonesia menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023',
                            labels={
                                'Nilai': 'Jumlah Penduduk akhir tahun Warga Negara Indonesia', 'Kelurahan': 'Kelurahan'},
                            barmode='group',  # Menampilkan bar terpisah untuk setiap kategori
                            text_auto=True
                        )

                        # Menampilkan visualisasi 1 di Streamlit
                        st.plotly_chart(fig1)

                        # Visualisasi 2: Bar chart persentase penduduk keluar tanpa data Kota Mojokerto
                        fig2 = px.bar(
                            df_no_kota_mojokerto,
                            x='Kelurahan',
                            y='Persentase',
                            title='Persentase Penduduk akhir tahun Warga Negara Indonesia menurut Kelurahan di Kota Mojokerto, 2023',
                            labels={
                                'Persentase': 'Persentase (%)', 'Kelurahan': 'Kelurahan'},
                            text_auto=True
                        )

                        # Menampilkan visualisasi 2 di Streamlit
                        st.plotly_chart(fig2)

                        # Visualisasi 3: Bar chart khusus untuk Kota Mojokerto (Laki-laki, Perempuan, Jumlah)
                        df_melt_kota = df_kota_mojokerto.melt(id_vars='Kelurahan',
                                                              value_vars=[
                                                                  'Laki-laki', 'Perempuan', 'Jumlah'],
                                                              var_name='Jenis Kelamin',
                                                              value_name='Nilai')  # Ganti 'Jumlah' dengan 'Nilai'

                        fig3 = px.bar(
                            df_melt_kota,
                            x='Kelurahan',
                            y='Nilai',  # Menggunakan 'Nilai' sebagai sumbu y
                            color='Jenis Kelamin',
                            title='Jumlah Penduduk akhir tahun Warga Negara Indonesia di Kota Mojokerto, 2023: Laki-laki, Perempuan, Jumlah',
                            labels={
                                'Nilai': 'Jumlah Penduduk akhir tahun Warga Negara Indonesia', 'Kelurahan': 'Kelurahan'},
                            barmode='group',  # Menampilkan bar terpisah untuk setiap kategori
                            text_auto=True
                        )

                        # Menampilkan visualisasi 3 di Streamlit
                        st.plotly_chart(fig3)

                elif selected_data_title == 'Penduduk akhir tahun Warga Negara Asing menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023' and visual_type == "Bar Chart":
                    st.markdown("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/Kependudukan Publikasi Softfile/Penduduk akhir tahun Warga Negara Asing menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto 2023.xlsx'
                    df = pd.read_excel(file_path)

                    # Mengubah nilai kolom 'Persentase' menjadi bentuk persen, pastikan hanya memformat angka
                    df['Persentase'] = df['Persentase'].apply(
                        lambda x: f'{float(x):.2f}%' if pd.api.types.is_numeric_dtype(
                            type(x)) else x
                    )

                    # Memisahkan data Kota Mojokerto dari data Kelurahan lainnya
                    df_kota_mojokerto = df[df['Kelurahan'] == 'Kota Mojokerto']
                    df_no_kota_mojokerto = df[df['Kelurahan']
                                              != 'Kota Mojokerto']

                    # Buat tabs untuk menampilkan data
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk data tabel
                    with tab1:
                        st.write(
                            "Tabel Penduduk akhir tahun Warga Negara Asing menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023:")
                        st.dataframe(df)
                        # Tab 2 untuk visualisasi
                    with tab2:
                        st.write(
                            "### Visualisasi Penduduk akhir tahun Warga Negara Asing menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023")
                        # Menggunakan melt untuk mengubah format dataframe agar kolom 'Laki-laki', 'Perempuan', dan 'Jumlah' bisa ditampilkan sebagai nilai
                        df_melt = df_no_kota_mojokerto.melt(id_vars='Kelurahan',
                                                            value_vars=[
                                                                'Laki-laki', 'Perempuan', 'Jumlah'],
                                                            var_name='Jenis Kelamin',
                                                            value_name='Nilai')  # Ganti 'Jumlah' dengan 'Nilai'

                        fig1 = px.bar(
                            df_melt,
                            x='Kelurahan',
                            y='Nilai',  # Menggunakan 'Nilai' sebagai sumbu y
                            color='Jenis Kelamin',
                            title='Jumlah Penduduk akhir tahun Warga Negara Asing menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023',
                            labels={'Nilai': 'Jumlah Penduduk akhir tahun Warga Negara Asing',
                                    'Kelurahan': 'Kelurahan'},
                            barmode='group',  # Menampilkan bar terpisah untuk setiap kategori
                            text_auto=True
                        )

                        # Menampilkan visualisasi 1 di Streamlit
                        st.plotly_chart(fig1)

                        # Visualisasi 2: Bar chart persentase penduduk keluar tanpa data Kota Mojokerto
                        fig2 = px.bar(
                            df_no_kota_mojokerto,
                            x='Kelurahan',
                            y='Persentase',
                            title='Persentase Penduduk akhir tahun Warga Negara Asing menurut Kelurahan di Kota Mojokerto, 2023',
                            labels={
                                'Persentase': 'Persentase (%)', 'Kelurahan': 'Kelurahan'},
                            text_auto=True
                        )

                        # Menampilkan visualisasi 2 di Streamlit
                        st.plotly_chart(fig2)

                        # Visualisasi 3: Bar chart khusus untuk Kota Mojokerto (Laki-laki, Perempuan, Jumlah)
                        df_melt_kota = df_kota_mojokerto.melt(id_vars='Kelurahan',
                                                              value_vars=[
                                                                  'Laki-laki', 'Perempuan', 'Jumlah'],
                                                              var_name='Jenis Kelamin',
                                                              value_name='Nilai')  # Ganti 'Jumlah' dengan 'Nilai'

                        fig3 = px.bar(
                            df_melt_kota,
                            x='Kelurahan',
                            y='Nilai',  # Menggunakan 'Nilai' sebagai sumbu y
                            color='Jenis Kelamin',
                            title='Jumlah Penduduk akhir tahun Warga Negara Asing di Kota Mojokerto, 2023 di Kota Mojokerto, 2023: Laki-laki, Perempuan, Jumlah',
                            labels={'Nilai': 'Jumlah Penduduk akhir tahun Warga Negara Asing',
                                    'Kelurahan': 'Kelurahan'},
                            barmode='group',  # Menampilkan bar terpisah untuk setiap kategori
                            text_auto=True
                        )

                        # Menampilkan visualisasi 3 di Streamlit
                        st.plotly_chart(fig3)

                elif selected_data_title == 'Jumlah Kelahiran menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023' and visual_type == "Bar Chart":
                    st.markdown("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/Kependudukan Publikasi Softfile/Jumlah Kelahiran menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto , 2023.xlsx'
                    df = pd.read_excel(file_path)

                    # Mengubah nilai kolom 'Persentase' menjadi bentuk persen, pastikan hanya memformat angka
                    df['Persentase'] = df['Persentase'].apply(
                        lambda x: f'{float(x):.2f}%' if pd.api.types.is_numeric_dtype(
                            type(x)) else x
                    )

                    # Memisahkan data Kota Mojokerto dari data Kelurahan lainnya
                    df_kota_mojokerto = df[df['Kelurahan'] == 'Kota Mojokerto']
                    df_no_kota_mojokerto = df[df['Kelurahan']
                                              != 'Kota Mojokerto']

                    # Buat tabs untuk menampilkan data
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk data tabel
                    with tab1:
                        st.write(
                            "Tabel Jumlah Kelahiran menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023:")
                        st.dataframe(df)
                        # Tab 2 untuk visualisasi
                    with tab2:
                        st.write(
                            "### Visualisasi Jumlah Kelahiran menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023")

                        # Menggunakan melt untuk mengubah format dataframe agar kolom 'Laki-laki', 'Perempuan', dan 'Jumlah' bisa ditampilkan sebagai nilai
                        df_melt = df_no_kota_mojokerto.melt(id_vars='Kelurahan',
                                                            value_vars=[
                                                                'Laki-laki', 'Perempuan', 'Jumlah'],
                                                            var_name='Jenis Kelamin',
                                                            value_name='Nilai')  # Ganti 'Jumlah' dengan 'Nilai'

                        fig1 = px.bar(
                            df_melt,
                            x='Kelurahan',
                            y='Nilai',  # Menggunakan 'Nilai' sebagai sumbu y
                            color='Jenis Kelamin',
                            title='Jumlah Kelahiran menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023',
                            labels={'Nilai': 'Jumlah Kelahiran',
                                    'Kelurahan': 'Kelurahan'},
                            barmode='group',  # Menampilkan bar terpisah untuk setiap kategori
                            text_auto=True
                        )

                        # Menampilkan visualisasi 1 di Streamlit
                        st.plotly_chart(fig1)

                        # Visualisasi 2: Bar chart persentase penduduk keluar tanpa data Kota Mojokerto
                        fig2 = px.bar(
                            df_no_kota_mojokerto,
                            x='Kelurahan',
                            y='Persentase',
                            title='Persentase Jumlah Kelahiran menurut Kelurahan di Kota Mojokerto, 2023',
                            labels={
                                'Persentase': 'Persentase (%)', 'Kelurahan': 'Kelurahan'},
                            text_auto=True
                        )

                        # Menampilkan visualisasi 2 di Streamlit
                        st.plotly_chart(fig2)

                        # Visualisasi 3: Bar chart khusus untuk Kota Mojokerto (Laki-laki, Perempuan, Jumlah)
                        df_melt_kota = df_kota_mojokerto.melt(id_vars='Kelurahan',
                                                              value_vars=[
                                                                  'Laki-laki', 'Perempuan', 'Jumlah'],
                                                              var_name='Jenis Kelamin',
                                                              value_name='Nilai')  # Ganti 'Jumlah' dengan 'Nilai'

                        fig3 = px.bar(
                            df_melt_kota,
                            x='Kelurahan',
                            y='Nilai',  # Menggunakan 'Nilai' sebagai sumbu y
                            color='Jenis Kelamin',
                            title='Jumlah Kelahiran di Kota Mojokerto, 2023: Laki-laki, Perempuan, Jumlah',
                            labels={'Nilai': 'Jumlah  Kelahiran',
                                    'Kelurahan': 'Kelurahan'},
                            barmode='group',  # Menampilkan bar terpisah untuk setiap kategori
                            text_auto=True
                        )

                        # Menampilkan visualisasi 3 di Streamlit
                        st.plotly_chart(fig3)

                elif selected_data_title == 'Jumlah Kematian menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023' and visual_type == "Bar Chart":
                    st.write("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/Kependudukan Publikasi Softfile/Jumlah Kematian menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto 2023.xlsx'
                    df = pd.read_excel(file_path)

                    # Mengubah nilai kolom 'Persentase' menjadi bentuk persen, pastikan hanya memformat angka
                    df['Persentase'] = df['Persentase'].apply(
                        lambda x: f'{float(x):.2f}%' if pd.api.types.is_numeric_dtype(
                            type(x)) else x
                    )

                    # Memisahkan data Kota Mojokerto dari data Kelurahan lainnya
                    df_kota_mojokerto = df[df['Kelurahan'] == 'Kota Mojokerto']
                    df_no_kota_mojokerto = df[df['Kelurahan']
                                              != 'Kota Mojokerto']

                    # Buat tabs untuk menampilkan data
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk data tabel
                    with tab1:
                        st.write(
                            "Tabel Jumlah Kematian menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023:")
                        st.dataframe(df)
                        # Tab 2 untuk visualisasi
                    with tab2:
                        st.write(
                            "### Visualisasi Jumlah Kematian menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023")

                        # Menggunakan melt untuk mengubah format dataframe agar kolom 'Laki-laki', 'Perempuan', dan 'Jumlah' bisa ditampilkan sebagai nilai
                        df_melt = df_no_kota_mojokerto.melt(id_vars='Kelurahan',
                                                            value_vars=[
                                                                'Laki-laki', 'Perempuan', 'Jumlah'],
                                                            var_name='Jenis Kelamin',
                                                            value_name='Nilai')  # Ganti 'Jumlah' dengan 'Nilai'

                        fig1 = px.bar(
                            df_melt,
                            x='Kelurahan',
                            y='Nilai',  # Menggunakan 'Nilai' sebagai sumbu y
                            color='Jenis Kelamin',
                            title='Jumlah Kematian menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023',
                            labels={'Nilai': 'Jumlah Kematian',
                                    'Kelurahan': 'Kelurahan'},
                            barmode='group',  # Menampilkan bar terpisah untuk setiap kategori
                            text_auto=True
                        )

                        # Menampilkan visualisasi 1 di Streamlit
                        st.plotly_chart(fig1)

                        # Visualisasi 2: Bar chart persentase penduduk keluar tanpa data Kota Mojokerto
                        fig2 = px.bar(
                            df_no_kota_mojokerto,
                            x='Kelurahan',
                            y='Persentase',
                            title='Persentase Jumlah Kematian menurut Kelurahan di Kota Mojokerto, 2023',
                            labels={
                                'Persentase': 'Persentase (%)', 'Kelurahan': 'Kelurahan'},
                            text_auto=True
                        )

                        # Menampilkan visualisasi 2 di Streamlit
                        st.plotly_chart(fig2)

                        # Visualisasi 3: Bar chart khusus untuk Kota Mojokerto (Laki-laki, Perempuan, Jumlah)
                        df_melt_kota = df_kota_mojokerto.melt(id_vars='Kelurahan',
                                                              value_vars=[
                                                                  'Laki-laki', 'Perempuan', 'Jumlah'],
                                                              var_name='Jenis Kelamin',
                                                              value_name='Nilai')  # Ganti 'Jumlah' dengan 'Nilai'

                        fig3 = px.bar(
                            df_melt_kota,
                            x='Kelurahan',
                            y='Nilai',  # Menggunakan 'Nilai' sebagai sumbu y
                            color='Jenis Kelamin',
                            title='Jumlah Kematian di Kota Mojokerto, 2023: Laki-laki, Perempuan, Jumlah',
                            labels={'Nilai': 'Jumlah Kematian',
                                    'Kelurahan': 'Kelurahan'},
                            barmode='group',  # Menampilkan bar terpisah untuk setiap kategori
                            text_auto=True
                        )

                        # Menampilkan visualisasi 3 di Streamlit
                        st.plotly_chart(fig3)

                elif selected_data_title == 'Jumlah Penduduk datang menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023' and visual_type == "Bar Chart":
                    st.write("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/Kependudukan Publikasi Softfile/Jumlah Penduduk datang menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto 2023.xlsx'
                    df = pd.read_excel(file_path)

                    # Mengubah nilai kolom 'Persentase' menjadi bentuk persen
                    df['Persentase'] = df['Persentase']
                    df['Persentase'] = df['Persentase'].apply(
                        lambda x: f'{x:.2f}%')  # Memformat menjadi 2 desimal dengan simbol %

                    # Memisahkan data Kota Mojokerto dari data Kelurahan lainnya
                    df_kota_mojokerto = df[df['Kelurahan'] == 'Kota Mojokerto']
                    df_no_kota_mojokerto = df[df['Kelurahan']
                                              != 'Kota Mojokerto']

                    # Buat tabs untuk menampilkan data
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk data tabel
                    with tab1:
                        st.write(
                            "Tabel Jumlah Penduduk datang menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023:")
                        st.dataframe(df)
                        # Tab 2 untuk visualisasi
                    with tab2:
                        st.write(
                            "### Visualisasi Jumlah Penduduk Datang Menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023")

                        # Visualisasi 1: Bar chart jumlah penduduk (Laki-laki, Perempuan, dan Jumlah total) tanpa data Kota Mojokerto
                        fig1 = px.bar(
                            df_no_kota_mojokerto,
                            x='Kelurahan',
                            y=['Laki-laki', 'Perempuan', 'Jumlah'],
                            title='Jumlah Penduduk Datang Menurut Kelurahan dan Jenis Kelamin (Kecuali Kota Mojokerto)',
                            labels={'value': 'Jumlah Penduduk',
                                    'variable': 'Jenis Kelamin'},
                            barmode='group',  # Menampilkan bar terpisah untuk setiap kategori
                            text_auto=True
                        )

                        # Menampilkan visualisasi 1 di Streamlit
                        st.plotly_chart(fig1)

                        # Visualisasi 2: Bar chart persentase penduduk keluar tanpa data Kota Mojokerto
                        fig2 = px.bar(
                            df_no_kota_mojokerto,
                            x='Kelurahan',
                            y='Persentase',
                            title='Persentase Penduduk Datang Menurut Kelurahan (Kecuali Kota Mojokerto)',
                            labels={
                                'Persentase': 'Persentase (%)', 'Kelurahan': 'Kelurahan'},
                            text_auto=True
                        )

                        # Menampilkan visualisasi 2 di Streamlit
                        st.plotly_chart(fig2)

                        # Visualisasi 3: Bar chart khusus untuk Kota Mojokerto (Laki-laki, Perempuan, Jumlah)
                        st.write(
                            "### Visualisasi Jumlah Penduduk Datang Kota Mojokerto")

                        fig3 = px.bar(
                            df_kota_mojokerto,
                            x='Kelurahan',
                            y=['Laki-laki', 'Perempuan', 'Jumlah'],
                            title='Jumlah Penduduk Datang Kota Mojokerto: Laki-laki, Perempuan, Jumlah',
                            labels={'value': 'Jumlah Penduduk',
                                    'variable': 'Kategori'},
                            barmode='group',  # Menampilkan bar terpisah untuk setiap kategori
                            text_auto=True
                        )

                        # Menampilkan visualisasi 3 di Streamlit
                        st.plotly_chart(fig3)

                elif selected_data_title == 'Jumlah Penduduk keluar menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023' and visual_type == "Bar Chart":
                    st.write("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/Kependudukan Publikasi Softfile/Jumlah Penduduk keluar menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto 2023.xlsx'
                    df = pd.read_excel(file_path)

                    # Mengubah nilai kolom 'Persentase' menjadi bentuk persen
                    df['Persentase'] = df['Persentase']
                    df['Persentase'] = df['Persentase'].apply(
                        lambda x: f'{x:.2f}%')  # Memformat menjadi 2 desimal dengan simbol %

                    # Memisahkan data Kota Mojokerto dari data Kelurahan lainnya
                    df_kota_mojokerto = df[df['Kelurahan'] == 'Kota Mojokerto']
                    df_no_kota_mojokerto = df[df['Kelurahan']
                                              != 'Kota Mojokerto']

                    # Buat tabs untuk menampilkan data
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk data tabel
                    with tab1:
                        st.write(
                            "Tabel Jumlah Penduduk keluar menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023:")
                        st.dataframe(df)

                    # Tab 2 untuk visualisasi
                    with tab2:
                        st.write(
                            "### Visualisasi Jumlah Penduduk Keluar Menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023")

                        # Visualisasi 1: Bar chart jumlah penduduk (Laki-laki, Perempuan, dan Jumlah total) tanpa data Kota Mojokerto
                        fig1 = px.bar(
                            df_no_kota_mojokerto,
                            x='Kelurahan',
                            y=['Laki-laki', 'Perempuan', 'Jumlah'],
                            title='Jumlah Penduduk Keluar Menurut Kelurahan dan Jenis Kelamin (Kecuali Kota Mojokerto)',
                            labels={'value': 'Jumlah Penduduk',
                                    'variable': 'Jenis Kelamin'},
                            barmode='group',  # Menampilkan bar terpisah untuk setiap kategori
                            text_auto=True
                        )

                        # Menampilkan visualisasi 1 di Streamlit
                        st.plotly_chart(fig1)

                        # Visualisasi 2: Bar chart persentase penduduk keluar tanpa data Kota Mojokerto
                        fig2 = px.bar(
                            df_no_kota_mojokerto,
                            x='Kelurahan',
                            y='Persentase',
                            title='Persentase Penduduk Keluar Menurut Kelurahan (Kecuali Kota Mojokerto)',
                            labels={
                                'Persentase': 'Persentase (%)', 'Kelurahan': 'Kelurahan'},
                            text_auto=True
                        )

                        # Menampilkan visualisasi 2 di Streamlit
                        st.plotly_chart(fig2)

                        # Visualisasi 3: Bar chart khusus untuk Kota Mojokerto (Laki-laki, Perempuan, Jumlah)
                        st.write(
                            "### Visualisasi Jumlah Penduduk Datang Kota Mojokerto")

                        fig3 = px.bar(
                            df_kota_mojokerto,
                            x='Kelurahan',
                            y=['Laki-laki', 'Perempuan', 'Jumlah'],
                            title='Jumlah Penduduk Datang: Laki-laki, Perempuan, Jumlah',
                            labels={'value': 'Jumlah Penduduk',
                                    'variable': 'Kategori'},
                            barmode='group',  # Menampilkan bar terpisah untuk setiap kategori
                            text_auto=True
                        )

                        # Menampilkan visualisasi 3 di Streamlit
                        st.plotly_chart(fig3)

                elif selected_data_title == 'Banyaknya akte kependudukan diterbitkan menurut jenisnya menurut bulan di Kota Mojokerto, 2023' and visual_type == "Bar Chart":
                    st.write("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/Kependudukan Publikasi Softfile/Banyaknya akte kependudukan diterbitkan menurut jenisnya menurut bulan di Kota Mojokerto 2023.xlsx'
                    df = pd.read_excel(file_path)

                    # Strip whitespace from column names
                    df.columns = df.columns.str.strip()

                    # Ensure the expected columns are in the DataFrame
                    expected_columns = [
                        'Bulan', 'Kelahiran Umum', 'Kelahiran Dispensasi', 'Perkawinan', 'Perceraian', 'Kematian']
                    missing_columns = [
                        col for col in expected_columns if col not in df.columns]

                    if missing_columns:
                        st.error(
                            f"Missing columns in the DataFrame: {missing_columns}")
                    else:
                        # Mengubah data menjadi format long untuk visualisasi multi-bar plot
                        df_long = df.melt(id_vars='Bulan', value_vars=['Kelahiran Umum', 'Kelahiran Dispensasi', 'Perkawinan', 'Perceraian', 'Kematian'],
                                          var_name='Jenis Akte', value_name='Jumlah')

                        # Convert 'Jumlah' column to numeric, forcing errors to NaN
                        df_long['Jumlah'] = pd.to_numeric(
                            df_long['Jumlah'], errors='coerce')

                        # Filter data for months January to September
                        valid_months = ['Januari', 'Februari', 'Maret', 'April',
                                        'Mei', 'Juni', 'Juli', 'Agustus', 'September']
                        df_long = df_long[df_long['Bulan'].isin(valid_months)]

                        # Menentukan urutan bulan
                        bulan_order = ['Januari', 'Februari', 'Maret', 'April',
                                       'Mei', 'Juni', 'Juli', 'Agustus', 'September']
                        df_long['Bulan'] = pd.Categorical(
                            df_long['Bulan'], categories=bulan_order, ordered=True)

                        # Mengurutkan DataFrame berdasarkan kolom 'Bulan'
                        df_long = df_long.sort_values('Bulan')

                        # Buat tabs untuk menampilkan data
                        tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                        # Tab 1 untuk data tabel
                        with tab1:
                            st.write(
                                "Tabel Banyaknya akte kependudukan diterbitkan menurut jenisnya menurut bulan di Kota Mojokerto, 2023:")
                            st.dataframe(df)

                        # Tab 2 untuk visualisasi
                        with tab2:
                            st.write(
                                "### Visualisasi Banyaknya akte kependudukan diterbitkan menurut jenisnya menurut bulan di Kota Mojokerto, 2023")

                            # Visualisasi stacked bar chart
                            fig = px.bar(
                                df_long,
                                x='Bulan',
                                y='Jumlah',
                                color='Jenis Akte',
                                title='Jumlah Akte Kependudukan Diterbitkan per Jenis dan Bulan di Kota Mojokerto, 2023',
                                labels={'Jumlah': 'Total Jumlah Akte'},
                                barmode='group',  # Jika ingin grouped bar chart. Gunakan 'stack' jika ingin stacked bar chart
                                text='Jumlah'  # Menampilkan nilai jumlah di atas bar
                            )

                            # Update layout untuk membuat grafik lebih menarik
                            fig.update_layout(
                                xaxis_title='Bulan',
                                yaxis_title='Total Jumlah Akte',
                                legend_title='Jenis Akte',
                                hovermode='x unified',
                                bargap=0.15  # Mengatur jarak antar bar
                            )

                            # Menampilkan chart
                            st.plotly_chart(fig)

                            # Select box for month selection
                            selected_month = st.selectbox(
                                'Pilih bulan untuk menampilkan visualisasi:',
                                valid_months
                            )

                            # Filter data for the selected month
                            filtered_data = df_long[df_long['Bulan']
                                                    == selected_month]

                            # Check if data exists for the selected month
                            if filtered_data.empty:
                                st.write(
                                    "Tidak ada data untuk bulan yang dipilih.")
                            else:

                                # Menggunakan pivot_table untuk bar chart data
                                bar_chart_data = filtered_data.pivot(
                                    index='Bulan', columns='Jenis Akte', values='Jumlah'
                                ).reset_index()

                                # Menggunakan Plotly untuk membuat bar chart
                                fig = px.bar(
                                    bar_chart_data,
                                    x='Bulan',
                                    y=bar_chart_data.columns[1:],
                                    title=f'Banyaknya Akte Kependudukan Diterbitkan pada Bulan {selected_month} di Kota Mojokerto, 2023',
                                    labels={'value': 'Jumlah',
                                            'variable': 'Jenis'},
                                    barmode='group'  # Use 'group' mode to display bars side by side
                                )

                                st.plotly_chart(fig)

                elif selected_data_title == 'Kepadatan penduduk akhir tahun Warga Negara Indonesia menurut Kelurahan di Kota Mojokerto, 2023' and visual_type == "Heatmap":
                    st.write("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/Kependudukan Publikasi Softfile/Kepadatan penduduk akhir tahun Warga Negara Indonesia menurut Kelurahan di Kota Mojokerto 2023.xlsx'
                    df = pd.read_excel(file_path)

                    # Mengubah data menjadi format long untuk visualisasi multi-line plot
                    df_long = df.melt(id_vars='Kelurahan', value_vars=[
                                      'Kepadatan Penduduk (per Km2)'], var_name='Tahun', value_name='Kepadatan penduduk akhir tahun')

                    # Buat tabs untuk menampilkan data
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk data tabel
                    with tab1:
                        st.write(
                            "Tabel Kepadatan penduduk akhir tahun Warga Negara Indonesia menurut Kelurahan di Kota Mojokerto, 2023:")
                        st.dataframe(df)
                    # Tab 2 untuk visualisasi
                    with tab2:
                        st.write(
                            "### Visualisasi Kepadatan Penduduk akhir tahun Warga Negara Indonesia menurut Kelurahan di Kota Mojokerto, 2023")
                        # Membuat heatmap
                        fig_heatmap = px.density_heatmap(df,
                                                         x='Kelurahan',
                                                         y='Kepadatan Penduduk (per Km2)',
                                                         z='Kepadatan Penduduk (per Km2)',
                                                         title='Heatmap Kepadatan Penduduk per Kelurahan - Kota Mojokerto, 2023',
                                                         labels={
                                                             'Kelurahan': 'Kelurahan', 'Kepadatan Penduduk (per Km2)': 'Kepadatan Penduduk (per Km2)'},
                                                         color_continuous_scale='Viridis',
                                                         height=600)

                        # Menampilkan heatmap di Streamlit
                        st.plotly_chart(fig_heatmap, use_container_width=True)

                elif selected_data_title == 'Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah) 2010-2023' and visual_type == "Line Chart":
                    st.write("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/IPM Yang Ada/Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah) 2010-2023.xlsx'
                    df = pd.read_excel(file_path)

                    # Memeriksa kolom yang ada
                    print(df.columns)  # Memeriksa nama kolom

                    # Membuat DataFrame untuk Kabupaten dan Kota
                    kabupaten_df = df[df['Wilayah'].str.contains(
                        'Kabupaten', na=False)]
                    kota_df = df[df['Wilayah'].str.contains('Kota', na=False)]
                    jawa_timur_df = df[df['Wilayah'] == 'Jawa Timur']

                    # Buat tabs untuk menampilkan data
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk data tabel
                    with tab1:
                        st.subheader(
                            'Tabel Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah) 2010-2023 - Kabupaten')
                        st.write(kabupaten_df)

                        st.subheader(
                            'Tabel Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah) 2010-2023 - Kota')
                        st.write(kota_df)

                        st.subheader(
                            'Tabel Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah) 2010-2023 - Jawa Timur (Total)')
                        st.write(jawa_timur_df)

                    # Tab 2 untuk visualisasi
                    with tab2:
                        st.write(
                            "### Visualisasi Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah) 2010-2023")

                        # Mengubah DataFrame menjadi format yang lebih mudah digunakan
                        df_districts = df.melt(
                            id_vars='Wilayah', var_name='Tahun', value_name='Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah)')

                        # Buat selectbox untuk memilih kabupaten
                        selected_kabupaten = st.selectbox(
                            "Pilih Kabupaten:",
                            options=kabupaten_df['Wilayah'].unique()
                        )

                        # Buat selectbox untuk memilih kota
                        selected_kota = st.selectbox(
                            "Pilih Kota:",
                            options=kota_df['Wilayah'].unique()
                        )

                        # Filter data berdasarkan pilihan pengguna untuk kabupaten
                        kabupaten_selected_data = df_districts[df_districts['Wilayah']
                                                               == selected_kabupaten]

                        # Filter data berdasarkan pilihan pengguna untuk kota
                        kota_selected_data = df_districts[df_districts['Wilayah']
                                                          == selected_kota]

                        # Ensure there is no space after the column name
                        y_column_name = 'Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah)'

                        # Plotting Line Chart untuk kabupaten terpilih
                        st.subheader(
                            f"Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah) Disesuaikan - {selected_kabupaten}")
                        fig_kabupaten = px.line(kabupaten_selected_data,
                                                x='Tahun', y=y_column_name,
                                                title=f'Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah) - {selected_kabupaten} 2010-2023',
                                                markers=True)
                        fig_kabupaten.update_layout(
                            xaxis_title='Tahun', yaxis_title='Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah)')
                        st.plotly_chart(fig_kabupaten)

                        # Plotting Line Chart untuk kota terpilih
                        st.subheader(
                            f"Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah) Disesuaikan - {selected_kota}")
                        fig_kota = px.line(kota_selected_data,
                                           x='Tahun', y=y_column_name,  # Ensure the same y column name is used
                                           title=f'Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah) Disesuaikan - {selected_kota} 2010-2023',
                                           markers=True)
                        fig_kota.update_layout(
                            xaxis_title='Tahun', yaxis_title='Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah)')
                        st.plotly_chart(fig_kota)

                        # Buat DataFrame untuk semua wilayah
                        df_melted = df.melt(
                            id_vars='Wilayah', var_name='Tahun', value_name='Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah)')

                        # Plotting Line Chart untuk HLS Jawa Timur
                        st.subheader(
                            "Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah) - Jawa Timur (Total)")

                        # Filter data untuk Jawa Timur
                        jawa_timur_melted = df_melted[df_melted['Wilayah']
                                                      == 'Jawa Timur']

                        # Membuat line chart
                        fig_jawa_timur = px.line(jawa_timur_melted,
                                                 x='Tahun',
                                                 y='Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah)',
                                                 title='Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah) 2010-2023 - Jawa Timur (Total)',
                                                 markers=True,
                                                 line_shape='linear',
                                                 color_discrete_sequence=["#636EFA"])  # Anda dapat mengganti warna sesuai preferensi

                        # Update layout untuk tampilan yang lebih baik
                        fig_jawa_timur.update_layout(
                            xaxis_title='Tahun',
                            yaxis_title='Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah)',
                            title_x=0.5,  # Center the title
                            # Background color
                            plot_bgcolor='rgba(255, 255, 255, 0.8)',
                            yaxis_tickformat=".2f"  # Format y-axis
                        )

                        # Menambahkan hover data
                        fig_jawa_timur.update_traces(
                            hovertemplate='Tahun: %{x}<br>HLS: %{y:.2f}')

                        # Menampilkan chart di Streamlit
                        st.plotly_chart(fig_jawa_timur)

                elif selected_data_title == 'Harapan Lama Sekolah (HLS) 2010-2023' and visual_type == "Line Chart":
                    st.write("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/IPM Yang Ada/Harapan Lama Sekolah (HLS) 2010-2023.xlsx'
                    df = pd.read_excel(file_path)

                    # Memeriksa kolom yang ada
                    print(df.columns)  # Memeriksa nama kolom

                    # Membuat DataFrame untuk Kabupaten dan Kota
                    kabupaten_df = df[df['Wilayah'].str.contains(
                        'Kabupaten', na=False)]
                    kota_df = df[df['Wilayah'].str.contains('Kota', na=False)]
                    jawa_timur_df = df[df['Wilayah'] == 'Jawa Timur']

                    # Buat tabs untuk menampilkan data
                    tab1, tab2 = st.tabs(["Tabel Data", "Visualisasi"])

                    # Tab 1 untuk data tabel
                    with tab1:
                        st.subheader(
                            'Tabel Harapan Lama Sekolah (HLS) 2010-2023 - Kabupaten')
                        st.write(kabupaten_df)

                        st.subheader(
                            'Tabel Harapan Lama Sekolah (HLS) 2010-2023 - Kota')
                        st.write(kota_df)

                        st.subheader(
                            'Tabel Harapan Lama Sekolah (HLS) 2010-2023 - Jawa Timur (Total)')
                        st.write(jawa_timur_df)

                    # Tab 2 untuk visualisasi
                    with tab2:
                        st.write(
                            "### Visualisasi Harapan Lama Sekolah (HLS) 2010-2023")

                        # Mengubah DataFrame menjadi format yang lebih mudah digunakan
                        df_districts = df.melt(
                            id_vars='Wilayah', var_name='Tahun', value_name='Harapan Lama Sekolah (HLS)')

                        # Buat selectbox untuk memilih kabupaten
                        selected_kabupaten = st.selectbox(
                            "Pilih Kabupaten:",
                            options=kabupaten_df['Wilayah'].unique()
                        )

                        # Buat selectbox untuk memilih kota
                        selected_kota = st.selectbox(
                            "Pilih Kota:",
                            options=kota_df['Wilayah'].unique()
                        )

                        # Filter data berdasarkan pilihan pengguna untuk kabupaten
                        kabupaten_selected_data = df_districts[df_districts['Wilayah']
                                                               == selected_kabupaten]

                        # Filter data berdasarkan pilihan pengguna untuk kota
                        kota_selected_data = df_districts[df_districts['Wilayah']
                                                          == selected_kota]

                        # Plotting Line Chart untuk kabupaten terpilih
                        st.subheader(
                            f"Harapan Lama Sekolah (HLS) Disesuaikan - {selected_kabupaten}")
                        fig_kabupaten = px.line(kabupaten_selected_data,
                                                x='Tahun', y='Harapan Lama Sekolah (HLS)',
                                                title=f'Harapan Lama Sekolah (HLS) Disesuaikan - {selected_kabupaten} 2010-2023',
                                                markers=True)
                        fig_kabupaten.update_layout(
                            xaxis_title='Tahun', yaxis_title='Harapan Lama Sekolah (HLS)')
                        st.plotly_chart(fig_kabupaten)

                        # Plotting Line Chart untuk kota terpilih
                        st.subheader(
                            f"Harapan Lama Sekolah (HLS) Disesuaikan - {selected_kota}")
                        fig_kota = px.line(kota_selected_data,
                                           x='Tahun', y='Harapan Lama Sekolah (HLS)',
                                           title=f'Harapan Lama Sekolah (HLS) Disesuaikan - {selected_kota} 2010-2023',
                                           markers=True)
                        fig_kota.update_layout(
                            xaxis_title='Tahun', yaxis_title='Harapan Lama Sekolah (HLS)')
                        st.plotly_chart(fig_kota)

                        # Buat DataFrame untuk semua wilayah
                        df_melted = df.melt(
                            id_vars='Wilayah', var_name='Tahun', value_name='Harapan Lama Sekolah (HLS)')

                        # Plotting Line Chart untuk HLS Jawa Timur
                        st.subheader(
                            "Harapan Lama Sekolah (HLS) - Jawa Timur (Total)")

                        # Filter data untuk Jawa Timur
                        jawa_timur_melted = df_melted[df_melted['Wilayah']
                                                      == 'Jawa Timur']

                        # Membuat line chart
                        fig_jawa_timur = px.line(jawa_timur_melted,
                                                 x='Tahun',
                                                 y='Harapan Lama Sekolah (HLS)',
                                                 title='Harapan Lama Sekolah (HLS) 2010-2023 - Jawa Timur (Total)',
                                                 markers=True,
                                                 line_shape='linear',
                                                 color_discrete_sequence=["#636EFA"])  # Anda dapat mengganti warna sesuai preferensi

                        # Update layout untuk tampilan yang lebih baik
                        fig_jawa_timur.update_layout(
                            xaxis_title='Tahun',
                            yaxis_title='Harapan Lama Sekolah (HLS)',
                            title_x=0.5,  # Center the title
                            # Background color
                            plot_bgcolor='rgba(255, 255, 255, 0.8)',
                            yaxis_tickformat=".2f"  # Format y-axis
                        )

                        # Menambahkan hover data
                        fig_jawa_timur.update_traces(
                            hovertemplate='Tahun: %{x}<br>HLS: %{y:.2f}')

                        # Menampilkan chart di Streamlit
                        st.plotly_chart(fig_jawa_timur)

                elif selected_data_title == 'Angka Melek Huruf (Persen) 2016-2006' and visual_type == "Line Chart":
                    st.write("### ")

                    # Membaca data dari file Excel
                    file_path = '/workspaces/dashboard-visualization-bps/IPM Yang Ada/Angka Melek Huruf (Persen) 2016-2006.xlsx'
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
