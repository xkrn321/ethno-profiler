"""
Core profiler module
"""
import requests
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

__version__ = "1.0.0"

# Default pharmacological dimensions with PubMed query suffixes
DEFAULT_DIMENSIONS = {
    "Gastric": "gastric[Title/Abstract] OR gastroprotective[Title/Abstract] OR antiulcer[Title/Abstract]",
    "Anti-inflam": "anti-inflammatory[Title/Abstract] OR NF-kB[Title/Abstract] OR cytokine[Title/Abstract]",
    "Anti-oxid": "antioxidant[Title/Abstract] OR oxidative stress[Title/Abstract] OR Nrf2[Title/Abstract]",
    "Neural": "neuroprotective[Title/Abstract] OR brain[Title/Abstract] OR serotonin[Title/Abstract] OR GABA[Title/Abstract]",
}

# Heuristic bands for search-result counts; these are not evidence grades.
THRESHOLDS = {
    "High count": 10,
    "Medium count": 5,
    "Low count": 1,
    "No hits": 0,
}

class Profiler:
    """Exploratory PubMed publication-count profiler for ethnomedicine research."""

    def __init__(self, dimensions=None, delay=0.4):
        """
        Args:
            dimensions: dict of {name: PubMed_query_suffix}. Default = 4 dimensions.
            delay: seconds between API calls (PubMed rate limit ~3/sec).
        """
        self.dimensions = dimensions or DEFAULT_DIMENSIONS
        self.delay = delay
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    def _count_pubmed(self, query):
        """Get total PubMed publication count for a query."""
        try:
            r = requests.get(self.base_url, params={
                'db': 'pubmed', 'term': query, 'retmax': 1, 'retmode': 'json'
            }, timeout=30)
            r.raise_for_status()
            return int(r.json().get('esearchresult', {}).get('count', 0))
        except requests.RequestException:
            raise

    def profile(self, ingredients):
        """
        Profile an herbal formula.

        Args:
            ingredients: list of (scientific_name, display_name) tuples.
                         e.g. [("Zingiber officinale", "Ginger"), ...]

        Returns:
            dict with keys: 'matrix' (dict), 'raw_counts' (list), 'dimensions' (list)
        """
        dim_names = list(self.dimensions.keys())
        results = []

        for sci_name, display_name in ingredients:
            row = {"ingredient": display_name, "scientific_name": sci_name}

            # Total publications
            total_q = f'"{sci_name}"[Title/Abstract]'
            row["total"] = self._count_pubmed(total_q)
            time.sleep(self.delay)

            # Per-dimension
            for dim_name, dim_query in self.dimensions.items():
                q = f'("{sci_name}"[Title/Abstract]) AND ({dim_query})'
                row[dim_name] = self._count_pubmed(q)
                time.sleep(self.delay)

            results.append(row)

        return {
            'raw_counts': results,
            'dimensions': dim_names,
            'ingredients': [r['ingredient'] for r in results],
        }

    @staticmethod
    def classify(count):
        """Assign a simple publication-count band, not an evidence grade."""
        if count >= THRESHOLDS["High count"]:
            return "High count"
        elif count >= THRESHOLDS["Medium count"]:
            return "Medium count"
        elif count >= THRESHOLDS["Low count"]:
            return "Low count"
        return "No hits"

    def plot_heatmap(self, results, output_path="publication_counts.tiff", dpi=300):
        """Generate a heatmap of exploratory publication-count bands."""
        dims = results['dimensions']
        herbs = results['ingredients']

        # Build a numeric matrix from count bands (0=no hits, 3=high count).
        level_map = {"No hits": 0, "Low count": 1, "Medium count": 2, "High count": 3}
        matrix = []
        for row in results['raw_counts']:
            matrix.append([level_map[self.classify(row[d])] for d in dims])
        matrix = np.array(matrix)

        fig, ax = plt.subplots(figsize=(12/2.54, 14/2.54))
        im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto', vmin=0, vmax=3)

        ax.set_xticks(range(len(dims)))
        ax.set_yticks(range(len(herbs)))
        ax.set_xticklabels(dims, fontsize=7)
        ax.set_yticklabels(herbs, fontsize=6.5)

        symbols = {3: '██', 2: '▓▓', 1: '▒▒', 0: '░░'}
        for i in range(len(herbs)):
            for j in range(len(dims)):
                ax.text(j, i, symbols[matrix[i, j]], ha='center', va='center',
                       fontsize=6, color='white' if matrix[i, j] >= 2 else 'gray')

        ax.set_xlabel('Pharmacological Category', fontsize=7)
        ax.set_ylabel('Botanical Ingredient', fontsize=7)
        ax.set_title('Publication-count bands', fontsize=8)

        plt.tight_layout()
        plt.savefig(output_path, dpi=dpi, bbox_inches='tight', format='tiff')
        plt.close()
        return output_path

    def print_report(self, results):
        """Print a text report of the profiling results."""
        dims = results['dimensions']
        print("\nPublication-count bands (not evidence grades):")
        header = f"{'Ingredient':20s}" + "".join(f"{d:>12s}" for d in dims)
        print(header)
        print("-" * len(header))
        for row in results['raw_counts']:
            levels = "".join(f"{self.classify(row[d]):>12s}" for d in dims)
            print(f"{row['ingredient']:20s}{levels}")

        print("\n\nQueries with few search hits (not evidence of no effect):")
        for row in results['raw_counts']:
            for d in dims:
                c = row[d]
                if c == 0:
                    print(f"  ⚠️ {row['ingredient']}: no hits for the current PubMed query in '{d}'")
                elif c < 5:
                    print(f"  🔶 {row['ingredient']}: {c} hits for the current PubMed query in '{d}'")

    def to_markdown(self, results):
        """Generate a Markdown table of publication-count bands."""
        dims = results['dimensions']
        lines = ["| Ingredient |" + "|".join(dims) + "|"]
        lines.append("|---" * (len(dims) + 1) + "|")
        for row in results['raw_counts']:
            levs = "|".join(self.classify(row[d]) for d in dims)
            lines.append(f"|{row['ingredient']}|{levs}|")
        return "\n".join(lines)
