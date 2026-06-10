# Ethno-Profiler

A Python tool for systematic ethnopharmacological literature profiling of traditional herbal formulas.

## What it does

Given a list of botanical ingredients (e.g., a traditional formula), Ethno-Profiler:

1. Searches PubMed for each ingredient across multiple pharmacological dimensions (gastric, anti-inflammatory, antioxidant, neural, etc.)
2. Generates an evidence level matrix (Strong/Moderate/Weak/None)
3. Creates a publication-ready heatmap visualization
4. Identifies research gaps
5. Outputs a structured report

## Why this exists

Tools like VOSviewer and CiteSpace analyze citation networks at the paper level, but **no existing tool analyzes a traditional formula at the ingredient × pharmacology level**. Ethno-Profiler fills this gap for ethnopharmacology researchers.

## Quick start

```python
from ethno_profiler import Profiler

# Define your formula
formula = [
    ("Apium graveolens", "Celery"),
    ("Zingiber officinale", "Ginger"),
    ("Cinnamomum cassia", "Cinnamon"),
]

# Create profiler
p = Profiler()

# Run analysis
results = p.profile(formula)

# Generate heatmap
p.plot_heatmap(results, "heatmap.tiff")

# Print report
p.print_report(results)
```

## Output example

```
Evidence Matrix:
Ingredient  | Gastric | Anti-inf | Anti-ox | Neural
------------|---------|----------|---------|--------
Ginger      | Strong  | Strong   | Strong  | Strong
Celery      | Weak    | Strong   | Strong  | Strong
Cinnamon    | Strong  | Strong   | Strong  | Strong

Research Gaps:
⚠️ Cardamom: 0 gastric studies - unexplored
⚠️ Rose: 0 gastric studies - traditional use lacks evidence
```

## Installation

```bash
pip install ethno-profiler
```

## Requirements

- Python 3.9+
- requests
- matplotlib
- numpy

## PubMed rate limit

The NCBI API allows ~3 requests/second. A typical formula of 14 ingredients × 5 dimensions = 70 requests (~30 seconds).

## License

MIT
