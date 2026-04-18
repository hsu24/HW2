import streamlit as st
import sqlite3
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Taiwan Weather Forecast", page_icon="🌤️", layout="wide")
st.title("Taiwan Weather Forecast")

@st.cache_data
def get_dates():
    conn = sqlite3.connect("data.db")
    df = pd.read_sql_query("SELECT DISTINCT dataDate FROM TemperatureForecasts ORDER BY dataDate ASC", conn)
    conn.close()
    return df["dataDate"].tolist()

@st.cache_data
def get_weather_data(date):
    conn = sqlite3.connect("data.db")
    query = "SELECT regionName as city, dataDate as start_time, mint, maxt FROM TemperatureForecasts WHERE dataDate = ?"
    df = pd.read_sql_query(query, conn, params=(date,))
    conn.close()
    return df

@st.cache_data
def get_regions():
    conn = sqlite3.connect("data.db")
    df = pd.read_sql_query("SELECT DISTINCT regionName FROM TemperatureForecasts ORDER BY regionName ASC", conn)
    conn.close()
    return df["regionName"].tolist()

@st.cache_data
def get_region_trend(region):
    conn = sqlite3.connect("data.db")
    query = "SELECT dataDate, mint as MinT, maxt as MaxT FROM TemperatureForecasts WHERE regionName = ? ORDER BY dataDate ASC"
    df = pd.read_sql_query(query, conn, params=(region,))
    conn.close()
    return df

dates = get_dates()
regions = get_regions()

if dates and regions:
    tab1, tab2 = st.tabs(["🗺️ Daily Overview", "📈 Regional Trends"])
    
    with tab1:
        st.markdown("### Daily Overview")
        selected_date = st.selectbox("Select Date", dates, key="date_selector")
        
        col1, col2 = st.columns([1.2, 1], gap="medium")
        df_data = get_weather_data(selected_date)
        
        with col1:
            st.subheader("Weather Map")
            m = folium.Map(location=[23.6, 120.9], zoom_start=7, tiles="OpenStreetMap")
            
            region_coords = {
                "北部地區": [24.95, 121.50],
                "中部地區": [24.15, 120.60],
                "南部地區": [23.10, 120.30],
                "東北部地區": [24.70, 121.75],
                "東部地區": [23.80, 121.40],
                "東南部地區": [22.75, 121.10]
            }
            
            for idx, row in df_data.iterrows():
                city = row['city']
                if city in region_coords:
                    folium.CircleMarker(
                        location=region_coords[city],
                        radius=20,
                        color="#fdee00", # exact yellow
                        weight=4,
                        fill=False,
                        tooltip=f"{city}: Min {row['mint']}°C - Max {row['maxt']}°C"
                    ).add_to(m)
                    
            st_folium(m, width=650, height=450, returned_objects=[])
            
        with col2:
            st.subheader("Temperature Data")
            st.dataframe(df_data, use_container_width=True)
            
    with tab2:
        st.markdown("### Regional Trends")
        selected_region = st.selectbox("Select Region", regions, key="region_selector")
        
        df_trend = get_region_trend(selected_region)
        
        st.markdown(f"**Temperature Trends for {selected_region}**")
        df_chart = df_trend.set_index("dataDate")
        try:
            st.line_chart(df_chart[['MinT', 'MaxT']], x_label="Date", y_label="Temperature (°C)")
        except TypeError:
            # Fallback for older Streamlit versions without x_label/y_label
            st.line_chart(df_chart[['MinT', 'MaxT']])
            
        st.markdown(f"**Temperature Data for {selected_region}**")
        st.dataframe(df_trend, use_container_width=True)
else:
    st.error("No data found in the database. Please run the data ingestion script first.")
