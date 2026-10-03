"""
fetch_data.py - Download daily climate data for 6 UAE cities from Open-Meteo.

Source : Open-Meteo Historical Weather API (ERA5 / ERA5-Land reanalysis)
         https://open-meteo.com/en/docs/historical-weather-api
Output : data/uae_climate_raw.csv

Usage  : python fetch_data.py
Needs  : Python 3.8+, internet access. No packages or API key required.

Note: values are reanalysis (model) data on a ~9-25 km grid, not readings
from a single weather station. Cite this in your README.
"""

import csv
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict

START_DATE = "2015-01-01"
END_DATE = "2025-12-31"

CITIES = {
    "Dubai": (25.2048, 55.2708),
    "Abu Dhabi": (24.4539, 54.3773),
    "Sharjah": (25.3463, 55.4209),
    "Al Ain": (24.2075, 55.7447),
    "Fujairah": (25.1288, 56.3265),
    "Ras Al Khaimah": (25.6741, 55.9804),
}

BASE_URL = "https://archive-api.open-meteo.com/v1/archive"
OUT_PATH = os.path.join("data", "uae_climate_raw.csv")
FIELDS = ["date", "city", "temp_max_c", "temp_min_c", "temp_mean_c",
          "humidity_mean_pct", "precip_mm"]


def get_json(params, retries=5):
    url = BASE_URL + "?" + urllib.parse.urlencode(params)
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=60) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                wait = 15 * attempt
                print(f"  HTTP {e.code}, retrying in {wait}s...")
                time.sleep(wait)
            else:
                body = e.read().decode("utf-8", errors="replace")
                raise RuntimeError(f"HTTP {e.code}: {body}") from e
        except urllib.error.URLError as e:
            print(f"  Network error ({e.reason}), retrying...")
            time.sleep(5 * attempt)
    raise RuntimeError("Gave up after repeated failures")


def fetch_daily(lat, lon):
    """Try daily humidity first; fall back to aggregating hourly humidity."""
    common = {
        "latitude": lat, "longitude": lon,
        "start_date": START_DATE, "end_date": END_DATE,
        "timezone": "Asia/Dubai",
    }
    daily_vars = ["temperature_2m_max", "temperature_2m_min",
                  "temperature_2m_mean", "precipitation_sum"]

    try:
        data = get_json({**common, "daily": ",".join(daily_vars + ["relative_humidity_2m_mean"])})
        d = data["daily"]
        return [
            (d["time"][i], d["temperature_2m_max"][i], d["temperature_2m_min"][i],
             d["temperature_2m_mean"][i], d["relative_humidity_2m_mean"][i],
             d["precipitation_sum"][i])
            for i in range(len(d["time"]))
        ]
    except (RuntimeError, KeyError) as e:
        print(f"  Daily humidity unavailable ({str(e)[:80]}); using hourly fallback")

    data = get_json({**common, "daily": ",".join(daily_vars)})
    hourly = get_json({**common, "hourly": "relative_humidity_2m"})
    buckets = defaultdict(list)
    for ts, val in zip(hourly["hourly"]["time"], hourly["hourly"]["relative_humidity_2m"]):
        if val is not None:
            buckets[ts[:10]].append(val)
    d = data["daily"]
    rows = []
    for i, day in enumerate(d["time"]):
        vals = buckets.get(day)
        hum = round(sum(vals) / len(vals), 1) if vals else None
        rows.append((day, d["temperature_2m_max"][i], d["temperature_2m_min"][i],
                     d["temperature_2m_mean"][i], hum, d["precipitation_sum"][i]))
    return rows


def main():
    os.makedirs("data", exist_ok=True)
    total = 0
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(FIELDS)
        for city, (lat, lon) in CITIES.items():
            print(f"Fetching {city}...")
            rows = fetch_daily(lat, lon)
            for r in rows:
                writer.writerow([r[0], city, *r[1:]])
            total += len(rows)
            print(f"  {len(rows)} days")
            time.sleep(3)  # be polite to the free API
    print(f"\nDone. {total} rows written to {OUT_PATH}")


if __name__ == "__main__":
    main()
