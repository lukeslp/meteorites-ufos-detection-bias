---
license: cc0-1.0
task_categories:
  - feature-extraction
language:
  - en
tags:
  - meteorites
  - ufo-sightings
  - detection-bias
  - astronomy
  - nuforc
  - nasa
  - geospatial
  - observation-bias
pretty_name: Meteorites vs UFOs - Detection Bias Study
size_categories:
  - 1K<n<10K
dataset_info:
  features:
    - name: year
      dtype: int64
    - name: meteorite_falls
      dtype: int64
    - name: ufo_sightings
      dtype: int64
    - name: state
      dtype: string
    - name: ufo_per_meteorite
      dtype: float64
    - name: name
      dtype: string
    - name: latitude
      dtype: float64
    - name: longitude
      dtype: float64
    - name: mass_g
      dtype: float64
    - name: meteorite_class
      dtype: string
  splits:
    - name: train
      num_examples: 1279
---

# Meteorites vs UFOs: Detection Bias Study

[![License: CC0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)
[![Kaggle](https://img.shields.io/badge/Kaggle-Dataset-20BEFF)](https://www.kaggle.com/datasets/lucassteuber/meteorites-ufos-detection-bias)
[![Records](https://img.shields.io/badge/records-1,279-green)]()

Both meteorite falls and UFO sightings depend on someone looking up at the right time. This dataset puts them side by side -- same timeframe, same geography -- to see where the patterns diverge.

## What's Inside

Three tables in one JSON file:

| Section | Records | What It Is |
|---------|---------|------------|
| `temporal_comparison` | 124 | Year-by-year meteorite falls vs UFO reports (1900-2023) |
| `state_comparison` | 58 | State-level counts and UFO-to-meteorite ratios |
| `meteorite_detail` | 1,097 | Individual witnessed falls with US state assignment |

## The Question

Meteorite falls are real astronomical events. UFO sightings are... something else. But both require a human witness looking at the sky. So what drives the difference?

- Population density? More people = more reports of both.
- Cultural factors? Some states report far more UFOs per real sky event.
- Time trends? UFO reports exploded after the 1990s. Meteorite documentation stayed steady.

## Record Structure

Temporal comparison:
```json
{
  "year": 2012,
  "meteorite_falls": 7,
  "ufo_sightings": 7781
}
```

State comparison:
```json
{
  "state": "CA",
  "meteorite_falls": 4,
  "ufo_sightings": 12457,
  "ufo_per_meteorite": 3114.2
}
```

Meteorite detail:
```json
{
  "name": "Murchison",
  "latitude": 44.8833,
  "longitude": -93.2,
  "date": "1969-09-28",
  "mass_g": 100000,
  "meteorite_class": "CM2",
  "us_state": null,
  "is_us": false
}
```

## Usage

```python
import json

with open('meteorites_ufos_detection_bias.json') as f:
    data = json.load(f)

# Year-by-year comparison
for row in data['temporal_comparison'][-10:]:
    print(f"{row['year']}: {row['meteorite_falls']} falls, {row['ufo_sightings']:,} UFO reports")

# Which states have the highest UFO-to-meteorite ratios?
ranked = sorted(
    [s for s in data['state_comparison'] if s['ufo_per_meteorite']],
    key=lambda x: x['ufo_per_meteorite'],
    reverse=True
)
for s in ranked[:5]:
    print(f"{s['state']}: {s['ufo_per_meteorite']:,.0f} UFO reports per meteorite fall")
```

## Sources

| Source | License | URL |
|--------|---------|-----|
| Meteoritical Bulletin (via NASA) | Public Domain | https://www.lpi.usra.edu/meteor/ |
| National UFO Reporting Center | Public Domain | https://nuforc.org/ |

## Distribution

- **GitHub**: [lukeslp/meteorites-ufos-detection-bias](https://github.com/lukeslp/meteorites-ufos-detection-bias)
- **HuggingFace**: [lukeslp/meteorites-ufos-detection-bias](https://huggingface.co/datasets/lukeslp/meteorites-ufos-detection-bias)
- **Kaggle**: [lucassteuber/meteorites-ufos-detection-bias](https://www.kaggle.com/datasets/lucassteuber/meteorites-ufos-detection-bias)

## Author

**Luke Steuber**
- Website: [lukesteuber.com](https://lukesteuber.com)
- Bluesky: [@lukesteuber.com](https://bsky.app/profile/lukesteuber.com)

## Structured Data (JSON-LD)

```json
{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "name": "Meteorites vs UFOs: Detection Bias Study",
  "description": "Side-by-side comparison of witnessed meteorite falls (NASA) and UFO sighting reports (NUFORC) across time and US states, exploring observation bias in sky-watching phenomena.",
  "url": "https://www.kaggle.com/datasets/lucassteuber/meteorites-ufos-detection-bias",
  "license": "https://creativecommons.org/publicdomain/zero/1.0/",
  "creator": {
    "@type": "Person",
    "name": "Luke Steuber",
    "url": "https://lukesteuber.com"
  },
  "keywords": ["meteorites", "UFO sightings", "detection bias", "NUFORC", "NASA", "observation bias"],
  "temporalCoverage": "1900/2023",
  "spatialCoverage": {
    "@type": "Place",
    "name": "United States (state comparison), Global (meteorite detail)"
  }
}
```
