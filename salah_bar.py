#!/usr/bin/env python3

from datetime import date, datetime, timedelta
import json
import os
import requests
import sys

config_path = os.path.expanduser("~/.config/salah-bar/config.json")
cache_path = os.path.expanduser("~/.cache/salah-bar/cache.json")

with open(config_path) as f:
    config = json.load(f)

PRAYERS = ["fajr", "sunrise", "dhuhr", "asr", "maghrib", "isha"]

PRAYER_NAMES = {
    "fajr": "Fajr",
    "sunrise": "Sunrise",
    "dhuhr": "Dhuhr",
    "asr": "Asr",
    "maghrib": "Maghrib",
    "isha": "Isha",
}

METHOD_MAP = {
    "MuslimWorldLeague": 3,
    "NorthAmerica": 2,
    "Egyptian": 5,
    "Karachi": 1,
    "Makkah": 4,
    "Tehran": 7,
    "Shia": 0,
    "MoonsightingCommittee": 15,
}

MECCA = (21.3891, 39.8579)


def load_cache():
    if os.path.exists(cache_path):
        with open(cache_path) as f:
            return json.load(f)
    return {}


def save_cache(cache):
    today = date.today().isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    pruned = {k: v for k, v in cache.items() if k in (today, tomorrow)}
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    with open(cache_path, "w") as f:
        json.dump(pruned, f)


def fetch_prayer_times(target_date):
    method = METHOD_MAP.get(config.get("method"), 3)
    lat = config.get("latitude") or MECCA[0]
    lon = config.get("longitude") or MECCA[1]
    school = 1 if config.get("asr") == "Hanafi" else 0

    url = f"https://api.aladhan.com/v1/timings/{target_date.strftime('%d-%m-%Y')}"
    response = requests.get(
        url,
        params={"latitude": lat, "longitude": lon, "method": method, "school": school},
        timeout=5,
    )
    response.raise_for_status()

    timings = response.json()["data"]["timings"]
    return {k.lower(): v for k, v in timings.items()}


def get_prayer_times(target_date):
    key = target_date.isoformat()
    cache = load_cache()

    if key in cache:
        return cache[key]

    timings = fetch_prayer_times(target_date)
    cache[key] = timings
    save_cache(cache)
    return timings


def parse_times(raw, target_date):
    result = {}
    for key in PRAYERS:
        if key not in raw:
            continue
        h, m = map(int, raw[key].split(":"))
        result[key] = datetime(target_date.year, target_date.month, target_date.day, h, m)
    return result


def get_current_and_next(prayer_times, tomorrow_fajr):
    now = datetime.now()
    prayers = list(prayer_times.items())

    for i, (name, time) in enumerate(prayers):
        if time > now:
            current = prayers[i - 1][0] if i > 0 else "isha"
            return current, name, time

    return "isha", "fajr", tomorrow_fajr


def format_output(current, next_time, all_times):
    delta = next_time - datetime.now()
    total_minutes = int(delta.total_seconds() // 60)
    hours, minutes = divmod(total_minutes, 60)

    countdown = f"{hours}h {minutes:02d}m" if hours > 0 else f"{minutes}m"
    label = PRAYER_NAMES.get(current, current.capitalize())
    tooltip = "\n".join(
        f"{PRAYER_NAMES.get(k, k.capitalize())}: {v.strftime('%H:%M')}"
        for k, v in all_times.items()
    )
    css_class = "imminent" if total_minutes <= 15 else "upcoming"

    return json.dumps({"text": f"{label} · {countdown}", "tooltip": tooltip, "class": css_class})


if __name__ == "__main__":
    try:
        today = date.today()
        tomorrow = today + timedelta(days=1)

        raw_today = get_prayer_times(today)
        raw_tomorrow = get_prayer_times(tomorrow)

        prayer_times = parse_times(raw_today, today)
        tomorrow_fajr = parse_times(raw_tomorrow, tomorrow)["fajr"]

        current, _, next_time = get_current_and_next(prayer_times, tomorrow_fajr)
        print(format_output(current, next_time, prayer_times))
    except Exception as e:
        print(json.dumps({"text": "salah-bar error", "tooltip": str(e), "class": "error"}))
        sys.exit(1)
