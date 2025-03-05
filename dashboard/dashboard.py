import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/air_quality_df.csv")
    return df

st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

custom_palette = {
    "Excellent": "#2E91E5",
    "Good": "#57C4AD",
    "Lightly Polluted": "#FFC300",
    "Moderately Polluted": "#FF5733",
    "Heavily Polluted": "#C70039",
    "Severely Polluted": "#4A0D25"
        }

def categorize_air_quality(pm25):
    if pm25 <= 15:
        return "Excellent"
    elif pm25 <= 35:
        return "Good"
    elif pm25 <= 55:
        return "Lightly Polluted"
    elif pm25 <= 75:
        return "Moderately Polluted"
    elif pm25 <= 100:
        return "Heavily Polluted"
    else:
        return "Severely Polluted"

st.sidebar.title("📌 Navigasi Halaman")

if "page" not in st.session_state:
    st.session_state["page"] = "Landing Page"

def change_page(page_name):
    st.session_state["page"] = page_name

st.sidebar.write("")
st.sidebar.button("🏠 Halaman Utama", on_click=change_page, args=("Landing Page",))
st.sidebar.button("📊 Analisis Data", on_click=change_page, args=("Analisis Data",))

page = st.session_state["page"]

df = load_data()

if page == "Landing Page":
    st.title("🌍 Air Quality Dashboard")
    st.write("")
    st.write(
        "Aplikasi ini bertujuan untuk menganalisis kualitas udara berdasarkan dataset yang tersedia. "
        "Dengan dashboard ini, pengguna dapat memahami berbagai pola dan faktor yang mempengaruhi kualitas udara."
    )
    st.write("---")

    st.write("### 📊 Jenis Analisis yang Tersedia:")
    st.markdown("✅ **Tren Polutan di Tiap Kota**: Melihat perubahan polutan seperti PM2.5, PM10, NO2, dan O3 dari waktu ke waktu.")
    st.markdown("✅ **Korelasi Faktor Cuaca & Polusi**: Menganalisis hubungan antara suhu, kelembaban, dan tingkat polusi.")
    st.markdown("✅ **Rata-rata Polusi Udara per Kota**: Menampilkan perbandingan rata-rata polusi di berbagai lokasi.")
    st.markdown("✅ **Klasifikasi Kualitas Udara**: Menggunakan kategori kualitas udara berdasarkan tingkat PM2.5 untuk mengevaluasi tingkat polusi di setiap kota.")

    st.success("Siap untuk mulai? Pilih 'Analisis Data' di sidebar! 🚀")
    st.write("")
    st.write("© 2025 Dibuat oleh Felix Rafael")

else: 
    st.title("📊 Analisis Data")

    tab1, tab2, tab3 = st.tabs(["Data Table", "Q1-Q3 Analysis", "Klasifikasi Kualitas Udara"])

    with tab1:
        st.write("### 🗂️ Data Table")
        df["year"] = df["year"].astype(int).astype(str)
        station_options = ["All"] + list(df["station"].unique())
        selected_station = st.selectbox("Pilih Kota", station_options)
        
        if selected_station == "All":
            st.dataframe(df)
        else:
            st.dataframe(df[df["station"] == selected_station])
    
    with tab2:
        st.subheader("🔎 Q1-Q3 Analysis")
        
        if all(col in df.columns for col in ["year", "station", "PM2.5", "PM10", "NO2", "O3"]):
            df["year"] = df["year"].astype(int)
            available_years = sorted(df["year"].unique())
            pollution_trend = df.groupby(["year", "station"])[["PM2.5", "PM10", "NO2", "O3"]].mean().reset_index()

            st.subheader("🔹 Tren Polutan di Tiap Kota")
            st.write("Pertanyaan 1: Bagaimana pola perubahan kualitas udara (PM2.5, PM10, NO2, O3) di tiga kota dari tahun ke tahun?")

            col1, col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.lineplot(data=pollution_trend, x="year", y="PM2.5", hue="station", marker="o", ax=ax)
                ax.set_title("Tren PM2.5 dari Tahun ke Tahun")
                ax.set_xlabel("Tahun")
                ax.set_ylabel("Rata-rata PM2.5")
                ax.set_xticks(available_years)
                ax.grid()
                st.pyplot(fig)

            with col2:
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.lineplot(data=pollution_trend, x="year", y="PM10", hue="station", marker="o", ax=ax)
                ax.set_title("Tren PM10 dari Tahun ke Tahun")
                ax.set_xlabel("Tahun")
                ax.set_ylabel("Rata-rata PM10")
                ax.set_xticks(available_years)
                ax.grid()
                st.pyplot(fig)

            col3, col4 = st.columns(2)

            with col3:
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.lineplot(data=pollution_trend, x="year", y="NO2", hue="station", marker="o", ax=ax)
                ax.set_title("Tren NO2 dari Tahun ke Tahun")
                ax.set_xlabel("Tahun")
                ax.set_ylabel("Rata-rata NO2")
                ax.set_xticks(available_years)
                ax.grid()
                st.pyplot(fig)

            with col4:
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.lineplot(data=pollution_trend, x="year", y="O3", hue="station", marker="o", ax=ax)
                ax.set_title("Tren O3 dari Tahun ke Tahun")
                ax.set_xlabel("Tahun")
                ax.set_ylabel("Rata-rata O3")
                ax.set_xticks(available_years)
                ax.grid()
                st.pyplot(fig)

        st.write("---")
        
        if all(col in df.columns for col in ["PM2.5", "PM10", "NO2", "O3", "TEMP", "DEWP", "RAIN", "station"]):
            correlation_columns = ["PM2.5", "PM10", "NO2", "O3", "TEMP", "DEWP", "RAIN"]
            st.subheader("🔹Korelasi Faktor Cuaca & Polusi")
            st.write("Pertanyaan 2: Bagaimana pengaruh suhu (TEMP), kelembaban (DEWP), dan curah hujan (RAIN) terhadap tingkat polusi udara di tiga kota?")
                
            col5, col6, col7 = st.columns(3)
                
            for station, col in zip(["Changping", "Gucheng", "Nongzhanguan"], [col5, col6, col7]):
                with col:
                    st.subheader(station)
                    station_df = df[df["station"] == station]
                    corr_matrix = station_df[correlation_columns].corr()
                    fig, ax = plt.subplots(figsize=(8, 6))
                    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
                    ax.set_title(f"Korelasi Faktor Cuaca & Polusi Udara di {station}")
                    st.pyplot(fig)

        st.write("---")
        
        if all(col in df.columns for col in ["station", "PM2.5", "PM10", "NO2", "O3"]):
            st.subheader("🔹Rata-rata Polusi Udara per Kota")
            st.write("Pertanyaan 3: Berdasarkan pada data yang ada, kota manakah yang memiliki tingkat polusi udara tertinggi?")
            pollution_avg = df.groupby("station")[["PM2.5", "PM10", "NO2", "O3"]].mean()
                
            col8, col9 = st.columns(2)
                
            with col8:
                fig, ax = plt.subplots(figsize=(12, 6))
                pollution_avg.plot(kind="bar", colormap="coolwarm", edgecolor="black", ax=ax)
                ax.set_title("Rata-rata Tingkat Polusi Udara di Setiap Kota")
                ax.set_ylabel("Konsentrasi Rata-rata (µg/m³)")
                ax.set_xticklabels(pollution_avg.index, rotation=0)
                ax.grid(axis="y", linestyle="--", alpha=0.7)
                ax.legend(title="Polutan")
                st.pyplot(fig)

    with tab3:
        st.subheader("📊 Klasifikasi Kualitas Udara Kota Berdasarkan PM2.5 dengan Pendekatan Clustering (Manual Grouping)")

        air_quality_avg = df.groupby(["year", "station"])["PM2.5"].mean().reset_index()
        air_quality_avg["Air_Quality_Category"] = air_quality_avg["PM2.5"].apply(categorize_air_quality)

        stations = air_quality_avg["station"].unique()
        station = st.selectbox("Pilih Kota", stations)

        city_data = air_quality_avg[air_quality_avg["station"] == station]
        city_data["year"] = city_data["year"].astype(int).astype(str)

        col10, col11 = st.columns([1, 1])  

        with col10:
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(
                x="year", 
                y="PM2.5", 
                hue="Air_Quality_Category", 
                data=city_data, 
                palette=custom_palette,
                dodge=False,
                saturation=1,
                ax=ax
            )

            ax.set_title(f"Kualitas Udara (PM2.5) di {station} per Tahun", fontsize=14)
            ax.set_xlabel("Tahun", fontsize=12)
            ax.set_ylabel("Rata-rata PM2.5", fontsize=12)
            ax.tick_params(axis='x', rotation=30)
            ax.grid(axis="y", linestyle="--", alpha=0.7)
            ax.legend(title="Kategori Kualitas Udara", bbox_to_anchor=(1,1))

            st.pyplot(fig)

        with col11:
            st.dataframe(city_data[["year", "PM2.5", "Air_Quality_Category"]].rename(columns={"year": "Tahun"}))
        
        st.markdown("""
        ### **Keterangan**  

        | **Kategori**            | **Rentang PM2.5 (µg/m³)** | **Warna**   | **Makna** |
        |------------------------|------------------|------------|---------|
        | **Excellent**          | 0 - 15           |  Biru    | Kualitas udara sangat baik, hampir tidak ada polusi. |
        | **Good**              | 16 - 35          |  Hijau   | Udara dalam kondisi baik dan aman untuk aktivitas luar ruangan. |
        | **Lightly Polluted**  | 36 - 55          |  Kuning  | Ada sedikit polusi, tetapi masih dalam batas wajar untuk sebagian besar orang. |
        | **Moderately Polluted** | 56 - 75          |  Oranye  | Polusi sedang, dapat mulai mempengaruhi kelompok sensitif seperti anak-anak dan lansia. |
        | **Heavily Polluted**   | 76 - 100         |  Merah   | Udara dalam kondisi buruk, dapat menyebabkan efek kesehatan bagi masyarakat umum. |
        | **Severely Polluted**  | > 100            |  Merah Tua | Sangat berbahaya, kualitas udara sangat buruk dan dapat menyebabkan dampak kesehatan yang serius. |
        """)



