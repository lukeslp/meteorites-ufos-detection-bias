#!/usr/bin/env python3
"""
Meteorites & UFOs: Detection Bias Study

Merges witnessed meteorite falls with UFO sighting data to explore
detection patterns - both phenomena involve sky-watching, so when/where
do people see real astronomical events vs report anomalous ones?

Sources:
- Witnessed Meteorite Falls (Meteoritical Bulletin, via NASA)
- UFO Sightings by Year (NUFORC)
- UFO Sightings by State (NUFORC)

Author: Luke Steuber
"""

import json
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

# Source paths
METEORITES = Path.home() / 'datasets/witnessed-meteorite-falls/witnessed_meteorite_falls.json'
UFO_BY_YEAR = Path.home() / 'html/datavis/data_trove/data/quirky/ufo_by_year.json'
UFO_BY_STATE = Path.home() / 'html/datavis/data_trove/data/quirky/ufo_by_state.json'
OUTPUT_DIR = Path(__file__).parent


def assign_us_state(lat, lng):
    """Rough US state assignment from coordinates using bounding boxes.
    Only covers CONUS - returns None for non-US or ambiguous locations."""
    if lat is None or lng is None:
        return None
    if not (24.0 < lat < 50.0 and -125.0 < lng < -66.0):
        return None

    # Simplified state centroids for assignment (nearest centroid wins)
    # Only the most populous/largest states for reasonable coverage
    state_centroids = {
        'CA': (36.78, -119.42), 'TX': (31.97, -99.90), 'FL': (27.66, -81.52),
        'NY': (42.17, -74.95), 'PA': (41.20, -77.19), 'IL': (40.63, -89.40),
        'OH': (40.42, -82.91), 'GA': (32.16, -82.90), 'NC': (35.76, -79.02),
        'MI': (44.31, -85.60), 'NJ': (40.06, -74.41), 'VA': (37.43, -78.66),
        'WA': (47.75, -120.74), 'AZ': (34.05, -111.09), 'MA': (42.41, -71.38),
        'TN': (35.52, -86.58), 'IN': (40.27, -86.13), 'MO': (38.57, -92.60),
        'MD': (39.05, -76.64), 'WI': (43.78, -88.79), 'CO': (39.55, -105.78),
        'MN': (46.73, -94.69), 'SC': (34.00, -81.03), 'AL': (32.32, -86.90),
        'LA': (30.98, -91.96), 'KY': (37.84, -84.27), 'OR': (43.80, -120.55),
        'OK': (35.47, -97.52), 'CT': (41.60, -72.76), 'UT': (39.32, -111.09),
        'IA': (41.88, -93.10), 'NV': (38.80, -116.42), 'AR': (35.20, -91.83),
        'MS': (32.35, -89.40), 'KS': (38.53, -98.77), 'NM': (34.52, -105.87),
        'NE': (41.49, -99.90), 'ID': (44.07, -114.74), 'WV': (38.60, -80.45),
        'ME': (45.25, -69.45), 'MT': (46.88, -110.36), 'ND': (47.55, -101.00),
        'SD': (43.97, -99.90), 'WY': (43.08, -107.29), 'VT': (44.56, -72.58),
        'NH': (43.19, -71.57), 'DE': (38.91, -75.53), 'RI': (41.58, -71.48),
    }

    min_dist = float('inf')
    closest = None
    for state, (slat, slng) in state_centroids.items():
        d = (lat - slat)**2 + (lng - slng)**2
        if d < min_dist:
            min_dist = d
            closest = state
    return closest


def build_temporal_comparison(meteorites, ufo_by_year):
    """Build year-by-year comparison of meteorite falls vs UFO sightings."""
    # Count meteorite falls by year
    met_by_year = Counter()
    for m in meteorites:
        date = m.get('date', '')
        if date and len(date) >= 4 and date[:4].isdigit():
            year = int(date[:4])
            if 1900 <= year <= 2025:
                met_by_year[year] += 1

    # UFO sightings by year
    ufo_years = {}
    for entry in ufo_by_year:
        year = entry.get('year')
        count = entry.get('count', 0)
        if year and 1900 <= year <= 2025:
            ufo_years[int(year)] = count

    # Build combined timeline
    all_years = sorted(set(list(met_by_year.keys()) + list(ufo_years.keys())))
    timeline = []
    for year in all_years:
        timeline.append({
            'year': year,
            'meteorite_falls': met_by_year.get(year, 0),
            'ufo_sightings': ufo_years.get(year, 0),
        })

    return timeline


def build_geographic_comparison(meteorites, ufo_by_state):
    """Build state-level comparison of meteorite falls vs UFO sightings."""
    # Assign US states to meteorites
    met_by_state = Counter()
    us_meteorites = 0
    for m in meteorites:
        state = assign_us_state(m.get('latitude'), m.get('longitude'))
        if state:
            met_by_state[state] += 1
            us_meteorites += 1

    # UFO sightings by state
    ufo_states = {}
    for entry in ufo_by_state:
        state = entry.get('state', '')
        count = entry.get('count', 0)
        if state and len(state) == 2:
            ufo_states[state] = count

    # Build combined state comparison
    all_states = sorted(set(list(met_by_state.keys()) + list(ufo_states.keys())))
    state_comparison = []
    for state in all_states:
        met = met_by_state.get(state, 0)
        ufo = ufo_states.get(state, 0)
        ratio = round(ufo / met, 1) if met > 0 else None
        state_comparison.append({
            'state': state,
            'meteorite_falls': met,
            'ufo_sightings': ufo,
            'ufo_per_meteorite': ratio,
        })

    return state_comparison, us_meteorites


def build_meteorite_detail(meteorites):
    """Clean meteorite records with state assignment."""
    records = []
    for m in meteorites:
        date = m.get('date', '')
        year = None
        if date and len(date) >= 4 and date[:4].isdigit():
            year = int(date[:4])

        state = assign_us_state(m.get('latitude'), m.get('longitude'))

        records.append({
            'name': m.get('name'),
            'latitude': m.get('latitude'),
            'longitude': m.get('longitude'),
            'date': date if date else None,
            'year': year,
            'mass_g': m.get('mass_g'),
            'meteorite_class': m.get('meteorite_class'),
            'fall_type': m.get('fall_type'),
            'us_state': state,
            'is_us': state is not None,
        })
    return records


def main():
    print("=" * 60)
    print("METEORITES & UFOs: DETECTION BIAS STUDY")
    print("=" * 60)

    # Load sources
    with open(METEORITES) as f:
        meteorites = json.load(f)
    with open(UFO_BY_YEAR) as f:
        ufo_by_year = json.load(f)
    with open(UFO_BY_STATE) as f:
        ufo_by_state = json.load(f)

    print(f"Meteorite falls: {len(meteorites):,}")
    print(f"UFO year entries: {len(ufo_by_year)}")
    print(f"UFO state entries: {len(ufo_by_state)}")

    # Build temporal comparison
    timeline = build_temporal_comparison(meteorites, ufo_by_year)
    print(f"\nTemporal records (1900-2025): {len(timeline)}")

    # Build geographic comparison
    state_data, us_meteorites = build_geographic_comparison(meteorites, ufo_by_state)
    print(f"State records: {len(state_data)}")
    print(f"US meteorite falls: {us_meteorites}")

    # Build detailed meteorite records
    met_detail = build_meteorite_detail(meteorites)
    us_count = sum(1 for m in met_detail if m['is_us'])
    print(f"Meteorite detail records: {len(met_detail)} ({us_count} US)")

    # Combined output
    dataset = {
        'metadata': {
            'title': 'Meteorites & UFOs: Detection Bias Study',
            'description': 'Comparing witnessed meteorite falls with UFO sighting reports to explore detection bias patterns. Both phenomena involve sky-watching, revealing how location, population density, and cultural factors affect what gets reported.',
            'created': datetime.now().strftime('%Y-%m-%d'),
            'sources': {
                'meteorite_falls': {
                    'source': 'Meteoritical Bulletin (via NASA)',
                    'url': 'https://www.lpi.usra.edu/meteor/',
                    'records': len(meteorites),
                    'license': 'Public Domain'
                },
                'ufo_sightings': {
                    'source': 'National UFO Reporting Center (NUFORC)',
                    'url': 'https://nuforc.org/',
                    'records': sum(e.get('count', 0) for e in ufo_by_state),
                    'license': 'Public Domain'
                }
            },
            'record_counts': {
                'temporal_comparison': len(timeline),
                'state_comparison': len(state_data),
                'meteorite_detail': len(met_detail),
            }
        },
        'temporal_comparison': timeline,
        'state_comparison': state_data,
        'meteorite_detail': met_detail,
    }

    # Save
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

    output_path = OUTPUT_DIR / 'meteorites_ufos_detection_bias.json'
    with open(output_path, 'w') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    size_mb = output_path.stat().st_size / 1024 / 1024
    print(f"\nSaved to: {output_path}")
    print(f"File size: {size_mb:.2f} MB")

    # Print some interesting findings
    print(f"\n{'='*60}")
    print("INTERESTING FINDINGS:")
    print(f"{'='*60}")

    # Peak years for each
    if timeline:
        peak_met = max(timeline, key=lambda x: x['meteorite_falls'])
        peak_ufo = max(timeline, key=lambda x: x['ufo_sightings'])
        print(f"Peak meteorite year: {peak_met['year']} ({peak_met['meteorite_falls']} falls)")
        print(f"Peak UFO year: {peak_ufo['year']} ({peak_ufo['ufo_sightings']:,} sightings)")

    # States with most UFOs per meteorite
    ranked = sorted([s for s in state_data if s['ufo_per_meteorite'] is not None],
                    key=lambda x: x['ufo_per_meteorite'], reverse=True)
    if ranked:
        print(f"\nHighest UFO-to-meteorite ratios:")
        for s in ranked[:5]:
            print(f"  {s['state']}: {s['ufo_per_meteorite']:,.0f} UFOs per meteorite fall")


if __name__ == '__main__':
    main()
