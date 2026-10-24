"""Trend + anomaly detection for each route CSV in data/."""
import glob, json, pathlib
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

def analyze(s):
    m = s.index.month
    clim = s.groupby(m).transform("mean")      # what is normal for that month
    sd = s.groupby(m).transform("std")
    z = (s - clim) / sd                         # how unusual is this month
    slope = np.polyfit(np.arange(len(s)), (s - clim).values, 1)[0] * 120
    return z, slope                             # slope = change per decade

if __name__ == "__main__":
    results = {}
    for f in sorted(glob.glob("data/*.csv")):
        name = pathlib.Path(f).stem
        s = pd.read_csv(f, index_col="month", parse_dates=True)["ws10m"]
        z, slope = analyze(s)
        bad = z[z.abs() > 2]
        results[name] = {"trend_per_decade_ms": round(float(slope), 3),
                         "anomaly_months": [d.strftime("%Y-%m") for d in bad.index]}
        plt.figure(figsize=(8, 3)); plt.plot(s.index, s.values, lw=1.5)
        plt.scatter(bad.index, s[bad.index], c="red", zorder=3)
        plt.title(f"{name}: 10 m wind speed (NASA POWER)"); plt.ylabel("m/s")
        plt.tight_layout(); plt.savefig(f"data/{name}.png", dpi=120); plt.close()
    pathlib.Path("data/results.json").write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))
