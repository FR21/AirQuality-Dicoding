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

st.sidebar.title("📌 Page Navigation")

if "page" not in st.session_state:
    st.session_state["page"] = "Landing Page"

def change_page(page_name):
    st.session_state["page"] = page_name

st.sidebar.write("")
st.sidebar.button("🏠 Home Page", on_click=change_page, args=("Landing Page",))
st.sidebar.button("📊 Data Analysis", on_click=change_page, args=("Data Analysis",))

page = st.session_state["page"]

df = load_data()

if page == "Landing Page":
    st.title("🌍 Air Quality Dashboard")
    st.write("")
    st.write(
        "This application aims to analyze air quality based on the available dataset. "
        "With this dashboard, users can understand various patterns and factors affecting air quality."
    )
    st.write("---")

    st.write("### 📊 Available Analysis Types:")
    st.markdown("✅ **Pollutant Trends in Each City**: Observing changes in pollutants such as PM2.5, PM10, NO2, and O3 over time.")
    st.markdown("✅ **Correlation Between Weather Factors & Pollution**: Analyzing the relationship between temperature, humidity, and pollution levels.")
    st.markdown("✅ **Average Air Pollution in Each City**: Comparing the average pollution levels across different locations.")
    st.markdown("✅ **Air Quality Classification**: Using air quality categories based on PM2.5 levels to evaluate pollution levels in each city.")

    st.success("Ready to start? Select 'Data Analysis' in the sidebar! 🚀")
    st.write("")
    st.write("© 2025 Created by Felix Rafael")

else: 
    st.title("📊 Data Analysis")

    tab1, tab2, tab3 = st.tabs(["Data Table", "Q1-Q3 Analysis", "Air Quality Classification"])

    with tab1:
        st.write("### 🗂️ Data Table")
        df["year"] = df["year"].astype(int).astype(str)
        station_options = ["All"] + list(df["station"].unique())
        selected_station = st.selectbox("Select City", station_options)
        
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

            st.subheader("🔹 Pollutant Trends in Each City")
            st.write("Question 1: How has air quality (PM2.5, PM10, NO2, O3) changed in three cities over the years?")

            col1, col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.lineplot(data=pollution_trend, x="year", y="PM2.5", hue="station", marker="o", ax=ax)
                ax.set_title("PM2.5 Trends Over the Years")
                ax.set_xlabel("Year")
                ax.set_ylabel("Average PM2.5")
                ax.set_xticks(available_years)
                ax.grid()
                st.pyplot(fig)

            with col2:
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.lineplot(data=pollution_trend, x="year", y="PM10", hue="station", marker="o", ax=ax)
                ax.set_title("PM10 Trends Over the Years")
                ax.set_xlabel("Year")
                ax.set_ylabel("Average PM10")
                ax.set_xticks(available_years)
                ax.grid()
                st.pyplot(fig)

            col3, col4 = st.columns(2)

            with col3:
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.lineplot(data=pollution_trend, x="year", y="NO2", hue="station", marker="o", ax=ax)
                ax.set_title("NO2 Trends Over the Years")
                ax.set_xlabel("Year")
                ax.set_ylabel("Average NO2")
                ax.set_xticks(available_years)
                ax.grid()
                st.pyplot(fig)

            with col4:
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.lineplot(data=pollution_trend, x="year", y="O3", hue="station", marker="o", ax=ax)
                ax.set_title("O3 Trends Over the Years")
                ax.set_xlabel("Year")
                ax.set_ylabel("Average O3")
                ax.set_xticks(available_years)
                ax.grid()
                st.pyplot(fig)

        st.write("---")
        
        if all(col in df.columns for col in ["PM2.5", "PM10", "NO2", "O3", "TEMP", "DEWP", "RAIN", "station"]):
            correlation_columns = ["PM2.5", "PM10", "NO2", "O3", "TEMP", "DEWP", "RAIN"]
            st.subheader("🔹 Correlation Between Weather Factors & Pollution")
            st.write("Question 2: How do temperature (TEMP), humidity (DEWP), and rainfall (RAIN) affect air pollution levels in the three cities?")
                
            col5, col6, col7 = st.columns(3)
                
            for station, col in zip(["Changping", "Gucheng", "Nongzhanguan"], [col5, col6, col7]):
                with col:
                    st.subheader(station)
                    station_df = df[df["station"] == station]
                    corr_matrix = station_df[correlation_columns].corr()
                    fig, ax = plt.subplots(figsize=(8, 6))
                    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
                    ax.set_title(f"Correlation Between Weather Factors & Air Pollution in {station}")
                    st.pyplot(fig)

        st.write("---")
        
        if all(col in df.columns for col in ["station", "PM2.5", "PM10", "NO2", "O3"]):
            st.subheader("🔹 Average Air Pollution per City")
            st.write("Question 3: Based on the available data, which city has the highest level of air pollution?")
            pollution_avg = df.groupby("station")[["PM2.5", "PM10", "NO2", "O3"]].mean()
                
            col8, col9 = st.columns(2)
                
            with col8:
                fig, ax = plt.subplots(figsize=(12, 6))
                pollution_avg.plot(kind="bar", colormap="coolwarm", edgecolor="black", ax=ax)
                ax.set_title("Average Air Pollution Levels in Each City")
                ax.set_ylabel("Average Concentration (µg/m³)")
                ax.set_xticklabels(pollution_avg.index, rotation=0)
                ax.grid(axis="y", linestyle="--", alpha=0.7)
                ax.legend(title="Pollutants")
                st.pyplot(fig)

    with tab3:
        st.subheader("📊 City Air Quality Classification Based on PM2.5 Using Clustering (Manual Grouping)")

        air_quality_avg = df.groupby(["year", "station"])["PM2.5"].mean().reset_index()
        air_quality_avg["Air_Quality_Category"] = air_quality_avg["PM2.5"].apply(categorize_air_quality)

        stations = air_quality_avg["station"].unique()
        station = st.selectbox("Select City", stations)

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

            ax.set_title(f"Air Quality (PM2.5) in {station} by Year", fontsize=14)
            ax.set_xlabel("Year", fontsize=12)
            ax.set_ylabel("Average PM2.5", fontsize=12)
            ax.tick_params(axis='x', rotation=30)
            ax.grid(axis="y", linestyle="--", alpha=0.7)
            ax.legend(title="Air Quality Category", bbox_to_anchor=(1,1))

            st.pyplot(fig)

        with col11:
            st.dataframe(city_data[["year", "PM2.5", "Air_Quality_Category"]].rename(columns={"year": "Year"}))
        
        st.markdown("""
        ### **Indicator**  

        | **Category**            | **PM2.5 Range (µg/m³)** | **Color**   | **Meaning** |
        |------------------------|------------------|------------|---------|
        | **Excellent**          | 0 - 15           |  Blue      | Very good air quality, almost no pollution. |
        | **Good**               | 16 - 35          |  Green     | Air is in good condition and safe for outdoor activities. |
        | **Lightly Polluted**   | 36 - 55          |  Yellow    | Some pollution, but still within a reasonable limit for most people. |
        | **Moderately Polluted** | 56 - 75         |  Orange    | Moderate pollution, may begin to affect sensitive groups. |
        | **Heavily Polluted**   | 76 - 100         |  Red       | Poor air quality, may cause health effects. |
        | **Severely Polluted**  | > 100            |  Dark Red  | Very dangerous, severely polluted air quality. |
        """)



