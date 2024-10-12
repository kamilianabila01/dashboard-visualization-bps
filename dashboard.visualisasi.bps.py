import streamlit as st
import pandas as pd
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
        #if data[col].dtype == 'object':  # Check if column type is object (usually string)
            #data[col] = data[col].replace ('-',100)  # Menampilkan 0

        # jika semua elemen kolom adalah string
        if data[col].apply(lambda x: isinstance(x, str)).all():    
            data[col] = data[col].str.replace('.', '', regex=False)  # Remove thousands separator
            data[col] = data[col].str.replace(',', '.', regex=False)  # Replace decimal comma with dot
            data[col] = data[col].str.replace(' ', '')  # Remove all spaces
            
            try:
            #if data[col] != '-': 
                data[col] = pd.to_numeric(data[col], errors='coerce')  # Convert to numeric
            except ValueError as e:
                st.error(f"Error converting data in column {col}: {e}")
        else:
            try:
                data[col] = pd.to_numeric(data[col], errors='coerce')  # Convert to numeric, setting invalid parsing as NaN
            except ValueError as e:
                st.error(f"Error converting data in column {col}: {e}")

    return data

# Sidebar menu
st.sidebar.title("Pilih Jenis Data")
data_type = st.sidebar.selectbox("Jenis Data:", list(data_files.keys()))

# Menampilkan judul data berdasarkan jenis data yang dipilih
if data_type in data_files:
    st.sidebar.title("Pilih Judul Data")
    selected_data_title = st.sidebar.selectbox("Judul Data:", list(data_files[data_type].keys()))

 # Menampilkan dropdown jenis visualisasi tergantung pada judul data yang dipilih
 # Visualisasi Data PDRB
    if selected_data_title == 'PDRB Atas Dasar Harga Berlaku Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Line Chart"])
    elif selected_data_title == 'Distribusi PDRB Atas Dasar Harga Berlaku Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Stacked Bar Chart"])
    elif selected_data_title == 'Laju Pertumbuhan PDRB ADHK 2010 Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Line Chart", "Bar Chart"])
    elif selected_data_title == 'Indeks Implisit PDRB Menurut Pengeluaran Kota Mojokerto, 2019-2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Line Chart"])
    elif selected_data_title == 'Pertumbuhan Indeks Implisit PDRB Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Bar Chart"])
    elif selected_data_title == 'Perkembangan Komponen Konsumsi Rumah Tangga Kota Mojokerto, 2019-2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Line Chart"])
    elif selected_data_title == 'Perkembangan Pengeluaran Konsumsi Akhir Pemerintah Kota Mojokerto, 2019-2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Line Chart"])
    elif selected_data_title == 'Laju Indeks Harga Implisit PDRB Kota Mojokerto Menurut Pengeluaran 2011-2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Line Chart"])
    elif selected_data_title == 'Distribusi PDRB Kota Mojokerto Atas Dasar Harga Berlaku Menurut Pengeluaran 2010-2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Pie Chart"])
    elif selected_data_title == 'Distribusi Persentase Produk Domestik Regional Bruto Kota Mojokerto Atas Dasar Harga Berlaku Menurut Lapangan Usaha, 2019─2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Stacked Bar Chart"])
    elif selected_data_title == 'Laju Pertumbuhan Produk Domestik Regional Bruto Atas Dasar Harga Konstan 2010 Kota Mojokerto Menurut Lapangan Usaha (persen), 2019─2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Line Chart"])
    
     # Visualisasi Data Kependudukan
    elif selected_data_title == 'Penduduk, Distribusi Persentase Penduduk, Kepadatan Penduduk, Rasio Jenis Kelamin Penduduk Menurut Kecamatan di Kota Mojokerto, 2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Stacked Bar Chart"])
    elif selected_data_title == 'Penduduk akhir tahun Warga Negara Indonesia menurut Kelurahan dan Jenis Kelamin di Kota Mojokerto, 2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Stacked Bar Chart"])
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
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Line Chart"]) 
    elif selected_data_title == 'Kepadatan penduduk akhir tahun Warga Negara Indonesia menurut Kelurahan di Kota Mojokerto, 2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Heatmap"]) 
    
    # Visualisasi Data IPM
    elif selected_data_title == 'Pengeluaran Per Kapita Riil Disesuaikan (Ribu Rupiah) 2010-2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Line Chart"]) 
    elif selected_data_title == 'Harapan Lama Sekolah (HLS) 2010-2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Line Chart"]) 
    elif selected_data_title == 'Angka Melek Huruf (Persen) 2016-2006':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Line Chart"]) 
    elif selected_data_title == 'Angka Harapan Hidup Jawa Timur (LF SP2020)':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Line Chart"]) 
    elif selected_data_title == 'IPM Jawa Timur 2010-2023':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Line Chart"]) 
    elif selected_data_title == 'Indeks Pembangunan Manusia Menurut Kabupaten dan Kota':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Bar Chart"]) 
    elif selected_data_title == 'Indeks Pembangunan Manusia (UHH LF SP2020)':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Line Chart"]) 
    elif selected_data_title == 'Angka Melek Huruf (Penduduk Usia 15 +)':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Bar Chart"]) 
    elif selected_data_title == 'Indeks Pemberdayaan Gender':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Bar Chart"]) 
    elif selected_data_title == 'Indeks Pembangunan Gender':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Bar Chart"]) 
    elif selected_data_title == 'Indeks Pembangunan Gender (menggunakan UHH hasil SP2020 LF)':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Line Chart"]) 
    elif selected_data_title == 'Indeks Ketimpangan Gender (IKG)':
        visual_type = st.sidebar.selectbox("Jenis Visualisasi:", ["Line Chart"]) 

      # Muat data berdasarkan judul yang dipilih
    if selected_data_title:
        file_path = data_files[data_type][selected_data_title][0]  # Ambil file path pertama
        if file_path:  # Pastikan file_path tidak kosong
            data = load_data_pdrb(file_path)
            
            # Cek apakah data berhasil dimuat
            if data is not None and not data.empty:
                st.title(f"Visualisasi Data: {selected_data_title}")
                st.write("Tampilan Data:")
                st.dataframe(data)

            # Tampilan visualisasi berdasarkan pilihan pengguna
                if selected_data_title == 'PDRB Atas Dasar Harga Berlaku Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023' and visual_type == "Line Chart":
                    st.markdown("### Line Chart")

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

                    # Set 'Komponen Pengeluaran' sebagai index
                    df.set_index('Komponen Pengeluaran', inplace=True)

                    # Menampilkan plot di Streamlit dengan matplotlib
                    st.title('Perkembangan Komponen Pengeluaran Kota Mojokerto (2019-2023)')

                    # Plot menggunakan matplotlib
                    plt.figure(figsize=(10, 6))
                    
                    # Menggunakan semua data termasuk 'Total PDRB'
                    for column in df.index:  # Tidak lagi mengecualikan 'Total PDRB'
                        plt.plot(df.columns, df.loc[column], marker='o', label=column)

                    # Menambahkan label dan judul
                    plt.title('Perkembangan Komponen Pengeluaran dari 2019 hingga 2023')
                    plt.xlabel('Tahun')
                    plt.ylabel('Jumlah (Dalam Jutaan)')
                    plt.xticks(rotation=45)
                    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
                    plt.tight_layout()

                    # Menampilkan plot di Streamlit
                    st.pyplot(plt)

                elif selected_data_title == 'Distribusi PDRB Atas Dasar Harga Berlaku Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023' and visual_type == "Bar Chart":
                    st.markdown("### Stacked Bar Chart")

                    # Membuat DataFrame dari data
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

                    df = pd.DataFrame(data)
                    df.set_index('Komponen Pengeluaran', inplace=True)

                    # Membuat figur dan axes
                    fig, ax = plt.subplots(figsize=(10, 6))

                    # Membuat stacked bar chart
                    df.T.plot(kind='bar', stacked=True, ax=ax)

                    # Menambahkan judul dan label
                    ax.set_title('Distribusi PDRB Atas Dasar Harga Berlaku Menurut Komponen Pengeluaran (2019-2023)')
                    ax.set_xlabel('Tahun')
                    ax.set_ylabel('Distribusi (%)')
                    ax.set_xticklabels(df.columns, rotation=45)

                    # Menampilkan grafik di Streamlit
                    st.pyplot(fig)

                
                elif selected_data_title == 'Laju Pertumbuhan PDRB ADHK 2010 Menurut Komponen Pengeluaran Kota Mojokerto, 2019-2023' and visual_type == "Line Chart":
                    st.markdown("### Line Chart komponen pengeluaran (yang bernilai dalam persen)")

                    # Clean up the data, removing unwanted characters and converting to numeric
                    data_clean = data.set_index('Komponen Pengeluaran')  # Setting 'Komponen Pengeluaran' as the index
                    data_clean = data_clean.replace({'%': '', '-': None}, regex=True)  # Remove % signs and handle '-'
                    data_clean = data_clean.apply(pd.to_numeric, errors='coerce')  # Convert everything to numeric

                    # Plotting data with y-axis limits for percentage-based data
                    plt.figure(figsize=(10, 6))
                    
                    for column in data_clean.columns[:-1]:  # Exclude the PDRB column
                        plt.plot(data_clean.index, data_clean[column], marker='o', label=column)
                        
                        plt.title('Laju Pertumbuhan PDRB ADHK 2010 Menurut Komponen Pengeluaran')
                        plt.xlabel('Tahun')
                        plt.ylabel('Pertumbuhan (%)')
                        plt.xticks(rotation=45)
                        plt.legend()
                        
                    # Set the y-axis limits from --0.25 to 0.76 for percentage data
                    plt.ylim(-0.25, 0.76)
                    st.pyplot(plt)

                    # Data Total PDRB
                    st.markdown("### Bar Chart total PDRB:")
                    data_pdrb = [5.65, -3.69, 3.65, 5.56, 2.79]
                    years = ['2019', '2020', '2021', '2022', '2023']  # Tahun atau kategori lain yang sesuai

                    # Buat DataFrame untuk data PDRB
                    pdrb_df = pd.DataFrame({
                        'Year': years,
                        'PDRB': data_pdrb
                    })

                    # Buat figure dan axis untuk bar chart
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.bar(pdrb_df['Year'], pdrb_df['PDRB'], color='lightblue')

                    # Tambahkan judul dan label sumbu
                    ax.set_title('Total PDRB per Tahun')
                    ax.set_xlabel('Tahun')
                    ax.set_ylabel('PDRB (%)')

                    # Tampilkan bar chart di Streamlit
                    st.pyplot(fig)


                
                # Tambahkan else-if untuk judul data lainnya dengan visualisasi yang berbeda

            else:
                st.error("Data tidak ditemukan atau kosong.")
        else:
            st.error("File untuk data ini belum tersedia.")
    else:
       data = None