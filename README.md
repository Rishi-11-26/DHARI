# Dhari (దారి) — Hyderabad Metro Navigation System

Dhari is a lightweight, reliable, and auto-updating navigation system for the Hyderabad Metro.

## Features
- **Live Data**: Syncs with Google Sheets for real-time station and fare updates.
- **Smart Routing**: BFS-based shortest path finding between stations.
- **Fare Estimation**: Automatic calculation based on distance slabs.
- **Nearest Station**: GPS-based location finding.
- **Reliable**: Built-in caching and local fallback for maximum uptime on free hosting.

## Setup Instructions

### 1. Google Sheets Integration
To make the app auto-updating:
1. Create a Google Sheet with three tabs: `stations`, `fare_matrix`, and `interchanges`.
2. Populate them with the data from the `data/` folder.
3. In Google Sheets, go to **File > Share > Publish to web**.
4. Select each tab and choose **CSV** as the format.
5. Copy the generated URLs and paste them into `utils/data_loader.py` in the `SHEET_URLS` dictionary.

### 2. Local Installation
```bash
pip install -r requirements.txt
streamlit run app.py
```

### 3. Deployment & Keep-Alive (Render/Free Hosting)
Free hosting platforms like Render often put apps to sleep after inactivity. To prevent this:
1. Deploy your app to Render.
2. Go to [UptimeRobot](https://uptimerobot.com/).
3. Create a new "HTTP(s)" monitor.
4. Point it to your app's URL (e.g., `https://your-app-name.onrender.com`).
5. Set the monitoring interval to **10 minutes**.
6. This will keep the app "awake" and responsive for your users.

## Project Structure
- `app.py`: Main UI and application logic.
- `route_engine.py`: BFS algorithm for finding the best route.
- `fare_engine.py`: Logic for calculating ticket prices.
- `utils/data_loader.py`: Handles data fetching with caching and fallback.
- `data/`: Contains backup CSV files.
- `updater/`: Optional scripts for data maintenance.

## Disclaimer
Fares and timings are based on public information and may vary.
