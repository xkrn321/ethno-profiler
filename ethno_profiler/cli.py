"""Command-line interface for ethno-profiler."""
import argparse
import json
from .profiler import Profiler

def main():
    parser = argparse.ArgumentParser(description="Ethnopharmacological literature profiler")
    parser.add_argument("ingredients", nargs="+", help="Scientific names of ingredients")
    parser.add_argument("--names", nargs="+", help="Display names (optional, defaults to scientific names)")
    parser.add_argument("--output", default="heatmap.tiff", help="Output heatmap path")
    parser.add_argument("--dpi", type=int, default=300, help="Heatmap DPI")

    args = parser.parse_args()
    
    names = args.names or args.ingredients
    ingredients = list(zip(args.ingredients, names))
    
    p = Profiler()
    results = p.profile(ingredients)
    p.plot_heatmap(results, args.output, dpi=args.dpi)
    p.print_report(results)

if __name__ == "__main__":
    main()
