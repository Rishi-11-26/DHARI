import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

from route_engine import find_route
from fare_engine import calculate_fare
from time_estimator import estimate_travel
from nearest_station import find_nearest_station
from service_clock import metro_service_status
from utils.data_loader import load_stations

# Try to import location service if available
try:
    from location_service import get_device_location
    gps_available = True
except ImportError:
    gps_available = False

# Page Configuration
st.set_page_config(
    page_title="Dhari - Hyderabad Metro Guide",
    page_icon="🚇",
    layout="wide"
)

# Load dynamic data
stations_df = load_stations()
station_list = sorted(stations_df["station"].unique())

# Metro line colors
line_colors = {
    "Red": "red",
    "Blue": "blue",
    "Green": "green"
}

# Multilingual Support
language = st.sidebar.selectbox(
    "Language / भाषा / భాష",
    ["English", "हिंदी", "తెలుగు"]
)

translations = {
    "English": {
        "title": "Dhari (దారి)",
        "subtitle": "Precision Hyderabad Metro Guide",
        "plan": "Plan Your Metro Journey",
        "start": "Start Station",
        "end": "Destination Station",
        "find": "Find Route",
        "stations": "Stations",
        "time": "Estimated Time",
        "fare": "Fare",
        "route": "Route",
        "map": "Hyderabad Metro Network",
        "gps": "Use My Location"
    },
    "हिंदी": {
        "title": "धारी (దారి)",
        "subtitle": "हैदराबाद मेट्रो गाइड",
        "plan": "अपनी मेट्रो यात्रा की योजना बनाएं",
        "start": "प्रारंभ स्टेशन",
        "end": "गंतव्य स्टेशन",
        "find": "मार्ग खोजें",
        "stations": "स्टेशन",
        "time": "अनुमानित समय",
        "fare": "किराया",
        "route": "मार्ग",
        "map": "हैదराबाद मेट्रो नेटवर्क",
        "gps": "मेरी लोकेशन उपयोग करें"
    },
    "తెలుగు": {
        "title": "దారి (Dhari)",
        "subtitle": "హైదరాబాద్ మెట్రో గైడ్",
        "plan": "మీ మెట్రో ప్రయాణాన్ని ప్లాన్ చేయండి",
        "start": "ప్రారంభ స్టేషన్",
        "end": "గమ్యస్థానం స్టేషన్",
        "find": "మార్గం కనుగొనండి",
        "stations": "స్టేషన్లు",
        "time": "అంచనా సమయం",
        "fare": "చార్జ్",
        "route": "మార్గం",
        "map": "హైదరాబాద్ మెట్రో నెట్‌వర్క్",
        "gps": "నా లొకేషన్ ఉపయోగించు"
    }
}

t = translations[language]

# UI Header
st.markdown(f"<h1 style='text-align:center;'>🚇 {t['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;color:gray'>{t['subtitle']}</p>", unsafe_allow_html=True)
st.markdown("---")

# Service Status
if not metro_service_status():
    st.warning("Metro service currently closed. Operating hours: 06:00 AM – 11:00 PM")

# Initialize Session State for Stations
if "start_station_val" not in st.session_state:
    st.session_state.start_station_val = station_list[0]
if "end_station_val" not in st.session_state:
    st.session_state.end_station_val = station_list[-1]

# Route Planner
st.subheader(t["plan"])
col1, col2 = st.columns(2)

with col1:
    start_station = st.selectbox(
        t["start"], 
        station_list, 
        index=station_list.index(st.session_state.start_station_val)
    )
    st.session_state.start_station_val = start_station

with col2:
    end_station = st.selectbox(
        t["end"], 
        station_list, 
        index=station_list.index(st.session_state.end_station_val)
    )
    st.session_state.end_station_val = end_station

# Action Buttons
c1, c2 = st.columns(2)
with c1:
    if st.button(t["find"], use_container_width=True):
        st.session_state["route"] = find_route(start_station, end_station)

with c2:
    if gps_available:
        if st.button(t["gps"], use_container_width=True):
            lat, lon = get_device_location()
            if lat and lon:
                station, distance = find_nearest_station(lat, lon)
                if station in station_list:
                    st.session_state.start_station_val = station
                    st.success(f"Nearest Station: {station} ({round(distance,2)} km)")
                    st.rerun()
            else:
                st.warning("Location permission denied or unavailable.")

# Display Route Results
route_coords = []
if "route" in st.session_state and st.session_state["route"]:
    route = st.session_state["route"]
    stations_count, travel_time = estimate_travel(route)
    
    total_distance = stations_count * 1.2
    fare = calculate_fare(total_distance)

    st.markdown("---")
    st.subheader("Journey Summary")
    jc1, jc2, jc3 = st.columns(3)
    jc1.metric(t["stations"], stations_count)
    jc2.metric(t["time"], f"{travel_time} min")
    jc3.metric(t["fare"], f"₹ {fare}")

    st.subheader(t["route"])
    st.success(" → ".join(route))

    for station in route:
        row = stations_df[stations_df["station"] == station]
        if not row.empty:
            route_coords.append([row.iloc[0]["lat"], row.iloc[0]["lon"]])

# Map Visualization
st.markdown("---")
st.subheader(t["map"])

map_center = [17.3850, 78.4867]
m = folium.Map(location=map_center, zoom_start=11)

for _, row in stations_df.iterrows():
    folium.Marker(
        [row["lat"], row["lon"]],
        tooltip=row["station"],
        icon=folium.Icon(color="blue", icon="train")
    ).add_to(m)

if route_coords:
    for i in range(len(route_coords) - 1):
        station_name = route[i]
        line = stations_df[stations_df["station"] == station_name].iloc[0]["line"]
        color = line_colors.get(line, "red")
        folium.PolyLine(
            [route_coords[i], route_coords[i+1]],
            color=color,
            weight=6
        ).add_to(m)

st_folium(m, width=900, height=500)

st.markdown("---")
st.subheader("Hyderabad Metro Route Map")
st.image("hyderabad_metro_map.png", use_container_width=True)

st.markdown("---")
st.caption("Fare based on Hyderabad Metro fare slabs. Actual fares may change.")

# System Status for Uptime Monitoring
st.write("---")
st.markdown("<p style='text-align:center; color: #f0f0f0; font-size: 10px;'>System Status: Online</p>", unsafe_allow_html=True)