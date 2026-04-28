# salah-bar

Waybar module showing your current prayer period and how long until the next one.

```
Maghrib · 43m
```

Hover for the full day's schedule. When a prayer is 15 minutes out, an `imminent` CSS class gets applied — style it however you like.

---

## Dependencies

- Python 3.9+
- `requests` (`pip install requests`)
- An internet connection — times come from the [Aladhan API](https://aladhan.com) and get cached locally once a day

---

## Installation

1. Clone the repo:

```bash
git clone https://github.com/yourusername/salah-bar ~/.local/share/salah-bar
```

2. Install the dependency:

```bash
pip install requests
```

3. Copy the example config:

```bash
mkdir -p ~/.config/salah-bar
cp config.example.json ~/.config/salah-bar/config.json
```

4. Edit `~/.config/salah-bar/config.json` with your location and method.

---

## Configuration

```json
{
    "latitude": 51.5074,
    "longitude": -0.1278,
    "method": "MoonsightingCommittee",
    "asr": "Standard"
}
```

**`latitude` / `longitude`** — decimal coordinates. Falls back to Mecca if not set.

**`method`** — which calculation authority to use:

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

**`asr`** — `Standard` (Shafi/Maliki/Hanbali) or `Hanafi`.

---

## Waybar

Add to your `config.jsonc`:

```json
"custom/salah": {
    "exec": "python3 /path/to/salah-bar/salah_bar.py",
    "interval": 60,
    "return-type": "json"
},
```

Then drop `"custom/salah"` into whichever modules list you want.

### Styling

Two CSS classes:

- `.upcoming` — default state
- `.imminent` — fires when the next prayer is 15 minutes or less away

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

- Times are fetched once a day and cached at `~/.cache/salah-bar/cache.json`. Both today and tomorrow get fetched on startup so there's always a next prayer ready, including after Isha.
- If the API is down and the cache is empty, the script errors out — Waybar shows nothing rather than wrong times.
