# Taiwan Weather Forecast Dashboard (HW2)

A data-driven web application that automates the extraction of weather data from the CWA API, persists it into a local SQLite3 database, and visualizes Taiwan's regional weather forecast through an interactive Streamlit dashboard.

## 🟢 Live Demo Snapshot

You can view a working static snapshot of the UI deployed on Streamlit Community Cloud here:
👉 **[Live Streamlit Dashboard](https://github.com/hsu24/HW2)**

*(Add your dashboard screenshot below)*
<br>
<img src="https://docs.streamlit.io/logo.svg" alt="App Dashboard Screenshot" width="600"/>

---

## ✨ Features

- **Data Pipeline**: Automated extraction of Taiwan weather forecasts via `fetch_weather.py` and persistent storage using local SQLite3 architecture (`data.db`).
- **🗺️ Daily Overview Tab**: Select a specific date to view regional temperature data side-by-side with an interactive map visualization (built with Folium).
- **📈 Regional Trends Tab**: Select a specific region to view a 7-day temperature trend line chart, complete with dynamically generated data tables.
- **Beautiful UI**: Redesigned Streamlit UI featuring native components, tabs for improved readability, and color-coded map markers.

## 🚀 Getting Started

### 1. Install Dependencies
Ensure you have Python installed, then install the required packages:
```bash
pip install streamlit pandas folium streamlit-folium
```

### 2. Run Data Ingestion
Gather the latest weather forecasting data into the local database:
```bash
python fetch_weather.py
```

### 3. Launch the App
Start the Streamlit web server:
```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` in your browser to view the dashboard!

## 📁 Repository Structure

- `app.py`: The main Streamlit dashboard application.
- `data.db`: SQLite database for storing forecast data.
- `database_operations.py`: Helper functions for database management.
- `fetch_weather.py`: Script to download data from the external API.
- `taiwan.geojson` / `download_geojson.py`: Mapping data used for Folium boundaries.
- `index.html` & `style.css`: Alternative vanilla web markup files for custom layouts.

---
*Created for HW2. Built with Python & Streamlit.*
