---
name: fitness
description: Fetch cycling data from intervals.icu, process with temperature/indoor-outdoor compensation, and update the post-surgery recovery chart page in the diagrams repo.
---

# Fitness — Intervals.icu Recovery Dashboard

Fetches Charlie Fuller's cycling data from intervals.icu, computes temperature-compensated PM FTP, efficiency, and heart rate metrics, and rebuilds the recovery charts page at `diagrams/fitness/post-surgery-recovery.html`.

## Credentials

- **Athlete ID:** `i257310`
- **API Key:** `1pzk4wxcx8u2jk9fm7npcf2od`
- **Base URL:** `https://intervals.icu/api/v1/athlete/i257310`
- **Auth:** Basic auth — username `API_KEY`, password is the API key

## Steps

### 1. Fetch Data

```bash
# All activities (rides + virtual rides + other sports)
curl -s -u "API_KEY:1pzk4wxcx8u2jk9fm7npcf2od" \
  "https://intervals.icu/api/v1/athlete/i257310/activities?oldest=2022-08-01&newest=$(date +%Y-%m-%d)&limit=2000" \
  > /tmp/intervals_activities_all.json

# Wellness data
curl -s -u "API_KEY:1pzk4wxcx8u2jk9fm7npcf2od" \
  "https://intervals.icu/api/v1/athlete/i257310/wellness?oldest=2022-08-01&newest=$(date +%Y-%m-%d)" \
  > /tmp/intervals_wellness_all.json
```

### 2. Process Data & Rebuild Charts

Run the Python script below. It:
1. Loads activities and merges temperature + PM FTP from raw data
2. Computes: PM FTP @22°C (slope -0.72 W/°C), HR @22°C (slope -0.09 bpm/°C), compensated efficiency (temp +0.012/°C, outdoor +0.15)
3. Rolls up weekly for outdoor rides and all rides
4. Computes % recovery vs pre-surgery baseline
5. Generates `/Users/motorthings/Documents/Vault/GitHub/diagrams/fitness/post-surgery-recovery.html`

### 3. Key Dates & Constants

- **Surgery:** 2025-05-13
- **Half dose Lopressor:** 2025-11-13
- **Off Lopressor:** 2026-05-01
- **Pre-surgery baseline window:** rides before 2025-05-13
- **PM FTP temp slope:** -0.72 W/°C
- **Avg Power temp slope:** -0.95 W/°C
- **HR temp slope:** +0.09 bpm/°C (heat raises HR)
- **Efficiency temp slope:** +0.012 W/bpm per °C
- **Outdoor efficiency penalty:** +0.15 W/bpm
- **Missing temp assumed:** 22°C
- **Chart x-axis start:** 2024-01-01

### 4. The Charts

Three full-width charts, stacked vertically:

1. **Outdoor Weekly PM FTP & Heart Rate** — PM FTP @22°C (solid), Avg HR @22°C duration-weighted (solid), Max HR (dashed). Dual y-axis.
2. **Weekly Efficiency + CTL** — Compensated efficiency (solid, filled), CTL (solid, right axis). Dual y-axis.
3. **Recovery: % of Pre-Surgery Baseline** — PM FTP % (filled) and Efficiency % (line) from surgery date onward. Single y-axis with 100% reference.

### 5. Diagrams Repo Conventions

- Page lives at: `diagrams/fitness/post-surgery-recovery.html`
- Index entry in: `diagrams/index.html` under `<details class="section"><summary>Fitness</summary>`
- Gulf Stream Racing theme: Fraunces + Source Code Pro, light/dark toggle, sticky nav, fixed backlink
- Title tag: `Fitness — Post-Surgery Cardiac Recovery`
- Meta description: "PM FTP, efficiency, and decoupling trends over 4 years of cycling data, tracking cardiac recovery after heart surgery with temperature and indoor/outdoor compensation."
- Chart colors use `var(--primary)` (orange), `var(--secondary)` (blue), `var(--violet)`, `var(--metric)` (teal), `var(--rose)` (red)

### 6. The Generation Script

```python
import json
from datetime import datetime, timedelta
from collections import defaultdict

metrics = json.load(open('/tmp/all_ride_metrics.json'))  # from prior processing
acts = json.load(open('/tmp/intervals_activities_all.json'))

# Build raw lookup for temp + pm_ftp
raw_lookup = {}
for a in acts:
    if a.get('type') not in ('Ride', 'VirtualRide'): continue
    key = (a['start_date_local'][:10], (a.get('name') or '')[:40])
    raw_lookup[key] = {
        'temp': a.get('average_temp'),
        'pm_ftp': a.get('icu_pm_ftp'),
        'type': a.get('type'),
    }

for m in metrics:
    k = (m['date'], m['name'])
    r = raw_lookup.get(k, {})
    m['temp'] = r.get('temp') if r.get('temp') is not None else 22
    m['ride_type'] = r.get('type', '?')
    m['pm_ftp'] = r.get('pm_ftp')

# Compensate
for m in metrics:
    eff = m.get('power_hr')
    m['eff_comp'] = round(eff + (m['temp'] - 22) * 0.012 + (0.15 if m.get('ride_type') == 'Ride' else 0), 3) if eff is not None else None
    m['pm_ftp_22c'] = round(m['pm_ftp'] + (m['temp'] - 22) * 0.72, 1) if m.get('pm_ftp') else None
    m['hr_22c'] = round(m['avg_hr'] - (m['temp'] - 22) * 0.09, 1) if m.get('avg_hr') else None

def week_key(d):
    return (datetime.strptime(d, '%Y-%m-%d') - timedelta(days=datetime.strptime(d, '%Y-%m-%d').weekday())).strftime('%Y-%m-%d')

# Outdoor weekly
ow = defaultdict(list)
for m in metrics:
    if m.get('ride_type') == 'Ride': ow[week_key(m['date'])].append(m)
ow_dates = sorted(ow.keys())

def wk_avg(data, key, dates):
    return [round(sum(r[key] for r in data[wk] if r.get(key) is not None)/len([r for r in data[wk] if r.get(key) is not None]), 3) if [r for r in data[wk] if r.get(key) is not None] else None for wk in dates]

# ... (full script in the reference implementation)
```

### 7. Verification

After generating:
1. Open the page in browser — all 3 charts render with data lines visible
2. Theme toggle works, chart colors adapt
3. Backlink → Index works
4. Index page has Fitness section with link
5. Stat row numbers match computed values
