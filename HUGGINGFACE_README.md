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
  splits:
    - name: train
      num_examples: 1279
---

# Meteorites vs UFOs: Detection Bias Study

Both meteorite falls and UFO sightings depend on someone looking up at the right time. This dataset puts them side by side, same timeframe, same geography, to see where the patterns diverge.

Three tables in one JSON file:

| Section | Records | What It Is |
|---------|---------|------------|
| `temporal_comparison` | 124 | Year-by-year meteorite falls vs UFO reports (1900-2023) |
| `state_comparison` | 58 | State-level counts and UFO-to-meteorite ratios |
| `meteorite_detail` | 1,097 | Individual witnessed falls with US state assignment |

## Dataset Structure

See `demo_notebook.ipynb` for data exploration examples.

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

| Source | License |
|--------|---------|
| Meteoritical Bulletin (via NASA) | Public Domain |
| National UFO Reporting Center (NUFORC) | Public Domain |

## License

CC0-1.0

## Author

**Luke Steuber** · [lukesteuber.com](https://lukesteuber.com) · [@lukesteuber.com](https://bsky.app/profile/lukesteuber.com)
