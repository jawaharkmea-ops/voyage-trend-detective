"""Download monthly 10 m wind speed (a sea-state proxy) from NASA POWER
along each shipping route and save one CSV per route in data/."""
import pathlib, requests, pandas as pd

URL = "https://power.larc.nasa.gov/api/temporal/monthly/point"
ROUTES = {  # (lat, lon) waypoints
    "Kochi-Dubai": [(9.9, 76.2), (14.0, 70.0), (19.0, 64.0), (24.5, 57.0)],
    "Mumbai-Singapore": [(18.9, 72.8), (10.0, 78.0), (6.0, 90.0), (1.3, 103.8)],
    "Chennai-Colombo": [(13.1, 80.3), (9.0, 80.5), (6.9, 79.9)],
}

def fetch(lat, lon, start=2016, end=2025):
    r = requests.get(URL, params=dict(parameters="WS10M", community="RE",
        latitude=lat, longitude=lon, start=start, end=end, format="JSON"), timeout=60)
    r.raise_for_status()
    d = r.json()["properties"]["parameter"]["WS10M"]
    return {k: v for k, v in d.items() if not k.endswith("13") and v != -999}

if __name__ == "__main__":
    pathlib.Path("data").mkdir(exist_ok=True)
    for name, pts in ROUTES.items():
        df = pd.DataFrame({i: fetch(*p) for i, p in enumerate(pts)})
        out = df.mean(axis=1).rename("ws10m").to_frame()
        out.index = pd.to_datetime(out.index, format="%Y%m")
        out.index.name = "month"
        out.to_csv(f"data/{name}.csv")
        print("saved", name, len(out), "months")
