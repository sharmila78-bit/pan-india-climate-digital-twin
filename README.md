# 🛰️ Pan-India AI Climate Digital Twin (ISRO BAH 2026)

An interactive geospatial AI digital twin platform simulating climate anomalies, SCS-CN hydrological surface runoff, and automated multi-sector SOP advisories across all 28 Indian States and 8 Union Territories.

## 🌟 Key Features
- **Pan-India Geospatial Coverage:** Complete telemetry integration for all 36 States & UTs with soil matrix and baseline elevation indexing.
- **Live Earth Observation Sync:** Real-time API telemetry pipeline with automated fallback buffers.
- **What-If Scenario Sandbox:** Dynamic stress-testing for thermal anomalies (-5°C to +7°C) and precipitation variance.
- **Hydrological Engine:** SCS-CN runoff volume and watershed inflow modeling in Million Cubic Meters (MCM).
- **Automated SOP Intelligence:** Context-aware advisories for Agriculture, Dam Spillway Control, and SDMA Disaster Response.
- **Telemetry Audit Export:** On-the-fly scenario export to CSV for administrative decision support.

## 🛠️ Tech Stack
- **Frontend / Framework:** Streamlit
- **Geospatial GIS:** Folium, Streamlit-Folium, OpenStreetMap
- **Data Analytics & Charts:** Plotly Graph Objects, Pandas, NumPy
- **ML / Modeling:** Scikit-Learn (Random Forest Ensemble)

## 🚀 Installation & Local Execution
```bash
# Clone the repository
git clone [https://github.com/sharmila78-bit/pan-india-climate-digital-twin.git](https://github.com/sharmila78-bit/pan-india-climate-digital-twin.git)

# Install dependencies
pip install -r requirements.txt

# Launch Dashboard
python -m streamlit run app.py
