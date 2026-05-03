# salah-bar

Waybar module showing your current prayer and a countdown to the next one.

```
Maghrib · 43m
```

Hover for the full day's schedule. 15 minutes out from a prayer, the `imminent` CSS class kicks in.

---

## Dependencies

- Python 3.9+
- `requests` — `sudo pacman -S python-requests` on Arch, `pip install requests` elsewhere
- Internet on first run — times are pulled from the [Aladhan API](https://aladhan.com) and cached daily

---

## Installation

```bash
git clone https://github.com/CaptnJayce/salah-bar ~/.local/share/salah-bar
chmod +x ~/.local/share/salah-bar/salah_bar.py
sudo pacman -S python-requests
```

No config file. Everything lives in your Waybar config.

---

## Waybar

```jsonc
"custom/salah": {
    "exec": "~/.local/share/salah-bar/salah_bar.py --lat 51.5074 --lon -0.1278 --method MuslimWorldLeague --asr Standard",
    "interval": 30,
    "return-type": "json"
},
```

Add `"custom/salah"` to whichever modules list you want.

---

## Arguments

| Argument | Default | Description |
|---|---|---|
| `--lat` | `21.3891` | Latitude — defaults to Mecca |
| `--lon` | `39.8579` | Longitude — defaults to Mecca |
| `--method` | `MuslimWorldLeague` | Calculation method (see below) |
| `--asr` | `Standard` | `Standard` or `Hanafi` |

**Calculation methods:**

| Value | Authority |
|---|---|
| `MuslimWorldLeague` | Muslim World League |
| `NorthAmerica` | Islamic Society of North America |
| `Egyptian` | Egyptian General Authority of Survey |
| `Karachi` | University of Islamic Sciences, Karachi |
| `Makkah` | Umm al-Qura University |
| `Tehran` | Institute of Geophysics, Tehran |
| `Shia` | Shia Ithna Ansari |
| `MoonsightingCommittee` | Moonsighting Committee Worldwide |

---

## Styling

```css
#custom-salah {
    color: #cdd6f4;
}

#custom-salah.imminent {
    color: #e06c75;
}
```

---

## Notes

- Times are cached at `~/.cache/salah-bar/cache.json` and refreshed once a day. Today and tomorrow both get fetched on startup, so there's always a next prayer available after Isha.
- If the API is unreachable and the cache is empty, the script exits cleanly — Waybar shows nothing rather than stale or wrong times.
