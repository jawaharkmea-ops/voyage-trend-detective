# 🚢 Voyage Trend Detective
NASA Space Apps Challenge 2026 · Challenge: *Be an Earth System Trend Detective*

Detects long-term trends and unusual months in NASA Earth data along ship routes,
and pairs them with a simulated onboard electrical-health monitor, the two kinds of
information an Electro-Technical Officer (ETO) works with.

## What it does
1. Pulls monthly NASA POWER data (10 m wind speed, a sea-state proxy) along shipping routes.
2. Finds each month's normal level, flags anomalies (|z| > 2), and measures the trend per decade.
3. Shows results in an interactive dashboard with route risk for the next 3 months.
4. Includes a simulated ship-health panel (engine temperature, vibration, voltage, current)
   with warning/critical alerts. *This panel is a simulation, not real hardware.*

## Run it
    pip install -r requirements.txt
    python fetch_nasa_power.py
    python analyze.py

Dashboard: open `dashboard/index.html` in a browser.

## Data
NASA POWER (https://power.larc.nasa.gov). More NASA datasets will be added after the
official challenge release.

## Method
Per-month climatology → z-score of each month → linear fit on deseasonalised values.

## Author
<your name>, ECE student. Built solo for NASA Space Apps 2026.
