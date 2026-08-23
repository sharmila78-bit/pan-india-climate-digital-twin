import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import folium
from streamlit_folium import st_folium
import requests
import datetime

# ----------------------------------------------------
# 1. ENTERPRISE PAGE CONFIGURATION
# ----------------------------------------------------
st.set_page_config(
    page_title="ISRO BAH 2026 - Pan-India AI Climate Digital Twin",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Contrast UI Theme
st.markdown("""
<style>
    .metric-box {
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        padding: 12px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 26px !important;
        font-weight: 800 !important;
        color: #0284c7 !important;
    }
    div[data-testid="stMetricLabel"] {
        font-weight: 700 !important;
        color: #1e293b !important;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. ALL 28 STATES + 8 UNION TERRITORIES OF INDIA
# ----------------------------------------------------
REGIONS = {
    # 28 States
    "Andhra Pradesh (Amaravati / Delta)": {"lat": 15.9129, "lon": 79.7400, "soil": "Coastal Alluvial", "elev": 65, "t_base": 34.0, "r_base": 12.0},
    "Arunachal Pradesh (Itanagar / Himalayas)": {"lat": 28.2180, "lon": 94.7278, "soil": "Alpine Mountain Humus", "elev": 2100, "t_base": 19.0, "r_base": 55.0},
    "Assam (Guwahati / Brahmaputra Basin)": {"lat": 26.2006, "lon": 92.9376, "soil": "Floodplain Alluvial", "elev": 85, "t_base": 29.5, "r_base": 42.0},
    "Bihar (Patna / Gangetic Plains)": {"lat": 25.0961, "lon": 85.3131, "soil": "Gangetic Silt", "elev": 53, "t_base": 32.5, "r_base": 18.0},
    "Chhattisgarh (Raipur / Mahanadi)": {"lat": 21.2787, "lon": 81.8661, "soil": "Red-Yellow Earth", "elev": 290, "t_base": 31.0, "r_base": 22.0},
    "Goa (Panaji / Konkan Coast)": {"lat": 15.2993, "lon": 74.1240, "soil": "Coastal Laterite", "elev": 30, "t_base": 30.0, "r_base": 45.0},
    "Gujarat (Gandhinagar / Kutch Basin)": {"lat": 22.2587, "lon": 71.1924, "soil": "Saline & Alluvial", "elev": 90, "t_base": 35.5, "r_base": 8.0},
    "Haryana (Chandigarh / Yamuna Basin)": {"lat": 29.0588, "lon": 76.0856, "soil": "Sandy Loam", "elev": 220, "t_base": 33.5, "r_base": 9.0},
    "Himachal Pradesh (Shimla / Western Hills)": {"lat": 31.1048, "lon": 77.1734, "soil": "Podzolic Forest", "elev": 2200, "t_base": 18.0, "r_base": 32.0},
    "Jharkhand (Ranchi / Chota Nagpur)": {"lat": 23.6102, "lon": 85.2799, "soil": "Red Micaceous", "elev": 650, "t_base": 30.0, "r_base": 24.0},
    "Karnataka (Bengaluru / Deccan Plateau)": {"lat": 15.3173, "lon": 75.7139, "soil": "Red Sandy Loam", "elev": 600, "t_base": 28.5, "r_base": 18.0},
    "Kerala (Thiruvananthapuram / Western Ghats)": {"lat": 10.8505, "lon": 76.2711, "soil": "Laterite Basin", "elev": 450, "t_base": 29.0, "r_base": 48.0},
    "Madhya Pradesh (Bhopal / Narmada Valley)": {"lat": 22.9734, "lon": 78.6569, "soil": "Medium Black Basaltic", "elev": 420, "t_base": 32.0, "r_base": 20.0},
    "Maharashtra (Mumbai / Vidarbha Basin)": {"lat": 19.7515, "lon": 75.7139, "soil": "Black Regur", "elev": 550, "t_base": 31.5, "r_base": 26.0},
    "Manipur (Imphal / Valley)": {"lat": 24.6637, "lon": 93.9063, "soil": "Lacustrine Silt", "elev": 790, "t_base": 26.0, "r_base": 35.0},
    "Meghalaya (Shillong / Rain Belt)": {"lat": 25.4670, "lon": 91.3662, "soil": "Acidic Hill Loam", "elev": 1500, "t_base": 20.5, "r_base": 65.0},
    "Mizoram (Aizawl / Lushai Hills)": {"lat": 23.1645, "lon": 92.9376, "soil": "Terraced Clay", "elev": 1000, "t_base": 24.0, "r_base": 38.0},
    "Nagaland (Kohima / Naga Range)": {"lat": 26.1584, "lon": 94.5624, "soil": "Brown Forest Earth", "elev": 1400, "t_base": 22.5, "r_base": 34.0},
    "Odisha (Bhubaneswar / Coastal Belt)": {"lat": 20.9517, "lon": 85.0985, "soil": "Deltaic Alluvial", "elev": 45, "t_base": 32.0, "r_base": 32.0},
    "Punjab (Chandigarh / Indus Basin)": {"lat": 31.1471, "lon": 75.3412, "soil": "Deep Rich Alluvial", "elev": 230, "t_base": 32.5, "r_base": 12.0},
    "Rajasthan (Jaipur / Thar Desert)": {"lat": 27.0238, "lon": 74.2179, "soil": "Arid Desert Sand", "elev": 225, "t_base": 38.5, "r_base": 4.0},
    "Sikkim (Gangtok / Teesta Basin)": {"lat": 27.5330, "lon": 88.5122, "soil": "High Mountain Humus", "elev": 1900, "t_base": 17.5, "r_base": 45.0},
    "Tamil Nadu (Chennai / Cauvery Basin)": {"lat": 11.1271, "lon": 78.6569, "soil": "Clay Loam & Coastal Silt", "elev": 120, "t_base": 33.5, "r_base": 14.0},
    "Telangana (Hyderabad / Deccan)": {"lat": 18.1124, "lon": 79.0193, "soil": "Red Chalkas", "elev": 500, "t_base": 33.0, "r_base": 15.0},
    "Tripura (Agartala / Barak Basin)": {"lat": 23.9408, "lon": 91.9882, "soil": "Red Loamy Clay", "elev": 60, "t_base": 28.5, "r_base": 36.0},
    "Uttar Pradesh (Lucknow / Gangetic)": {"lat": 26.8467, "lon": 80.9462, "soil": "Deep Alluvial Silt", "elev": 125, "t_base": 33.0, "r_base": 16.0},
    "Uttarakhand (Dehradun / Garhwal)": {"lat": 30.0668, "lon": 79.0193, "soil": "Mountain Hill Soil", "elev": 1600, "t_base": 22.0, "r_base": 38.0},
    "West Bengal (Kolkata / Delta)": {"lat": 22.9868, "lon": 87.8550, "soil": "Deltaic Alluvial & Mangrove", "elev": 35, "t_base": 32.0, "r_base": 30.0},
    
    # 8 Union Territories
    "Andaman & Nicobar (Port Blair / Bay of Bengal)": {"lat": 11.6234, "lon": 92.7265, "soil": "Marine Tropical Clay", "elev": 16, "t_base": 30.0, "r_base": 55.0},
    "Chandigarh UT (Capital Region)": {"lat": 30.7333, "lon": 76.7794, "soil": "Alluvial Loam", "elev": 320, "t_base": 33.0, "r_base": 11.0},
    "Dadra & Nagar Haveli and Daman & Diu": {"lat": 20.3974, "lon": 72.8328, "soil": "Coastal Regur", "elev": 25, "t_base": 31.0, "r_base": 30.0},
    "Delhi NCR (National Capital Region)": {"lat": 28.7041, "lon": 77.1025, "soil": "Alluvial / Urban Surface", "elev": 215, "t_base": 34.5, "r_base": 10.0},
    "Jammu & Kashmir UT (Srinagar / Valley)": {"lat": 33.7782, "lon": 76.5762, "soil": "Karewa Glacial Loam", "elev": 1850, "t_base": 20.0, "r_base": 20.0},
    "Ladakh UT (Leh / Cold Desert Plateau)": {"lat": 34.1526, "lon": 77.5771, "soil": "Arid Skeletal Gravel", "elev": 3500, "t_base": 12.0, "r_base": 2.0},
    "Lakshadweep (Kavaratti / Coral Atoll)": {"lat": 10.5667, "lon": 72.6417, "soil": "Coral Sand", "elev": 4, "t_base": 30.5, "r_base": 42.0},
    "Puducherry UT (Coromandel Coast)": {"lat": 11.9416, "lon": 79.8083, "soil": "Coastal Alluvial", "elev": 15, "t_base": 32.0, "r_base": 16.0}
}

# ----------------------------------------------------
# 3. LIVE EARTH OBSERVATION INGESTION ENGINE
# ----------------------------------------------------
@st.cache_data(ttl=1800)
def fetch_satellite_telemetry(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max,surface_pressure_mean&hourly=relativehumidity_2m&timezone=Asia%2FKolkata"
    try:
        res = requests.get(url, timeout=4)
        if res.status_code == 200:
            return res.json(), True
    except Exception:
        pass
    return None, False

# ----------------------------------------------------
# 4. SIDEBAR - CONTROLS & TWIN STRESS SANDBOX
# ----------------------------------------------------
st.sidebar.markdown("### 🛰️ ISRO BAH 2026 Telemetry")
st.sidebar.caption("Project: **Pan-India Climate Digital Twin** | Team: **Code Rocketeers**")

selected_region = st.sidebar.selectbox("🎯 Target Sector (All 36 States & UTs)", list(REGIONS.keys()))
region_meta = REGIONS[selected_region]

# Telemetry Sync
telemetry_data, is_live = fetch_satellite_telemetry(region_meta["lat"], region_meta["lon"])

if is_live and "daily" in telemetry_data:
    raw_dates = telemetry_data["daily"]["time"]
    api_temp = telemetry_data["daily"]["temperature_2m_max"]
    api_rain = telemetry_data["daily"]["precipitation_sum"]
    st.sidebar.success("🟢 Live Earth Observation Synchronized")
else:
    raw_dates = [(datetime.date.today() + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    api_temp = [region_meta["t_base"] + np.random.uniform(-1.2, 1.5) for _ in range(7)]
    api_rain = [region_meta["r_base"] + np.random.uniform(-3.0, 5.0) for _ in range(7)]
    st.sidebar.warning("🟡 Calibrated Base Climate Mode Active")

st.sidebar.markdown("---")
st.sidebar.subheader("🎛️ Real-Time Environment Modifiers")
curr_humidity = st.sidebar.slider("Ambient Relative Humidity (%)", 15, 100, 65)
curr_wind = st.sidebar.slider("Surface Wind Velocity (km/h)", 2, 70, 18)

st.sidebar.markdown("---")
st.sidebar.subheader("🔬 Digital Twin 'What-If' Stress Sandbox")
temp_mod = st.sidebar.slider("Simulated Thermal Delta (°C)", -5.0, 7.0, 0.0, 0.5)
rain_mod_pct = st.sidebar.slider("Simulated Precipitation Variance (%)", -60, 150, 0, 10)
land_cover = st.sidebar.selectbox(
    "Land Surface / Canopy Classification",
    ["Pristine Natural Forest", "Mixed Agricultural Farmland", "High-Density Urban Concrete"]
)

# ----------------------------------------------------
# 5. MATHEMATICAL & HYDROLOGICAL COMPUTATION MATRIX
# ----------------------------------------------------
# Weather adjustments based on physics
humidity_temp_offset = (curr_humidity - 50) * -0.04
sim_temp = [round(t + temp_mod + humidity_temp_offset, 1) for t in api_temp]
sim_rain = [round(max(0.0, (r * (curr_humidity / 50.0)) * (1 + (rain_mod_pct / 100.0))), 1) for r in api_rain]

# Hydrological Runoff Modeling (SCS Runoff Coefficient)
runoff_coeff = 0.30 if land_cover == "Pristine Natural Forest" else (0.55 if land_cover == "Mixed Agricultural Farmland" else 0.88)
peak_rain = max(sim_rain)
runoff_volume_mm = round(peak_rain * runoff_coeff, 1)
inflow_mcm = round((runoff_volume_mm * 1.6), 2)  # Million Cubic Meters

avg_temp = round(float(np.mean(sim_temp)), 1)
tot_rain = round(float(np.sum(sim_rain)), 1)

# Multi-Tier Risk Classification
if avg_temp >= 38.0 or max(sim_temp) >= 42.0:
    alert_status = "CRITICAL: Severe Heatwave (IMD Red Alert)"
    status_theme = "red"
elif peak_rain >= 50.0 or runoff_volume_mm >= 35.0:
    alert_status = "CRITICAL: Flood Inundation & Cloudburst Hazard"
    status_theme = "red"
elif tot_rain <= 4.0 and avg_temp >= 33.0:
    alert_status = "MODERATE: Agricultural Drought & Aridity"
    status_theme = "orange"
else:
    alert_status = "NOMINAL: Climate State in Equilibrium"
    status_theme = "green"

# ----------------------------------------------------
# 6. MAIN DASHBOARD VISUALS
# ----------------------------------------------------
st.title("🛰️ AI-Powered Climate Digital Twin of India")
st.caption(f"Spatial Sector: **{selected_region}** | Baseline Elevation: `{region_meta['elev']} m` | Soil Substrate: `{region_meta['soil']}`")

# KPI Summary Row
k1, k2, k3, k4 = st.columns(4)
k1.metric("Simulated Mean Temp", f"{avg_temp} °C", delta=f"{temp_mod:+.1f} °C" if temp_mod != 0 else None)
k2.metric("7-Day Projected Rain", f"{tot_rain} mm", delta=f"{rain_mod_pct:+d}%" if rain_mod_pct != 0 else None)
k3.metric("Peak Surface Runoff", f"{runoff_volume_mm} mm/day", help="Calculated using land cover infiltration dynamics.")
k4.metric("Twin Operational Risk", alert_status.split(":")[0])

st.markdown("---")

# Analytics & GIS Mapping Row
col_map, col_graph = st.columns([1, 1])

with col_map:
    st.subheader("🗺️ Geospatial Hazard & Telemetry GIS")
    
    # Layered OpenStreetMap Folium Radar
    map_obj = folium.Map(
        location=[region_meta["lat"], region_meta["lon"]],
        zoom_start=6,
        tiles="OpenStreetMap"
    )
    
    marker_color = "red" if avg_temp > 35 else ("blue" if tot_rain > 45 else "green")
    
    folium.Circle(
        location=[region_meta["lat"], region_meta["lon"]],
        radius=55000,
        popup=f"<b>Sector:</b> {selected_region}<br><b>Avg Temp:</b> {avg_temp}°C<br><b>Peak Rain:</b> {peak_rain}mm<br><b>Runoff:</b> {runoff_volume_mm}mm/day",
        color=marker_color,
        fill=True,
        fill_opacity=0.4
    ).add_to(map_obj)
    
    folium.Marker(
        location=[region_meta["lat"], region_meta["lon"]],
        tooltip=f"Active ISRO/IMD Node: {selected_region}",
        icon=folium.Icon(color="blue", icon="cloud")
    ).add_to(map_obj)
    
    st_folium(map_obj, width=540, height=360)

with col_graph:
    st.subheader("📊 7-Day Dual Predictive Dynamics")
    fig = go.Figure()
    
    # Temperature Line
    fig.add_trace(go.Scatter(
        x=raw_dates, y=sim_temp,
        name="Max Temperature (°C)",
        mode='lines+markers',
        line=dict(color='#ea580c', width=3),
        yaxis='y1'
    ))
    
    # Rainfall Volume Bar
    fig.add_trace(go.Bar(
        x=raw_dates, y=sim_rain,
        name="Precipitation (mm)",
        marker_color='#0284c7',
        opacity=0.7,
        yaxis='y2'
    ))
    
    fig.update_layout(
        height=360,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
        yaxis=dict(title=dict(text="Temperature (°C)", font=dict(color="#ea580c"))),
        yaxis2=dict(
            title=dict(text="Precipitation (mm)", font=dict(color="#0284c7")),
            overlaying='y',
            side='right'
        )
    )
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------
# 7. AUTOMATED SECTORAL DECISION INTELLIGENCE (SOPs)
# ----------------------------------------------------
st.markdown("### ⚡ Automated Sector Decision Intelligence & SOP Advisory")
s1, s2, s3 = st.columns(3)

with s1:
    st.markdown("#### 🌾 Agriculture & Crop Health")
    if avg_temp > 35:
        st.error("• Severe thermal transpiration: Trigger emergency drip irrigation & mulching.")
    elif tot_rain > 50:
        st.warning("• Waterlogging Risk: Expedite crop furrow drainage channels immediately.")
    else:
        st.success("• Soil moisture & vegetative indices remain optimal.")

with s2:
    st.markdown("#### 🌊 Hydrology & Dam Operations")
    st.write(f"• Estimated Watershed Inflow: **{inflow_mcm} MCM**")
    if runoff_volume_mm > 28:
        st.error("• Sluice Gate Alert: Initiate regulated spillway release protocol.")
    else:
        st.info("• Reservoir capacity securely buffered within rule curve.")

with s3:
    st.markdown("#### 🛡️ State Disaster Response (SDMA)")
    if "CRITICAL" in alert_status:
        st.error("• Red Alert: Mobilize emergency response teams and regional advisories.")
    elif "MODERATE" in alert_status:
        st.warning("• Yellow Watch: Monitor dry spells and water tanker reserves.")
    else:
        st.success("• Standard Readiness: Telemetry normal.")

# ----------------------------------------------------
# 8. HACKATHON DEMO AUDIT LOG & EXPORT ENGINE
# ----------------------------------------------------
st.markdown("---")
with st.expander("📥 View Telemetry Audit Log & Export Report (Demo Ready)"):
    df_export = pd.DataFrame({
        "Date": raw_dates,
        "Simulated_Temp_C": sim_temp,
        "Simulated_Rain_mm": sim_rain,
        "Runoff_Yield_mm": [round(r * runoff_coeff, 1) for r in sim_rain],
        "Sector": [selected_region] * len(raw_dates)
    })
    st.dataframe(df_export, use_container_width=True)
    
    csv_data = df_export.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📄 Download Scenario Simulation CSV",
        data=csv_data,
        file_name=f"Climate_Twin_{selected_region.split()[0]}_Scenario.csv",
        mime="text/csv"
    )