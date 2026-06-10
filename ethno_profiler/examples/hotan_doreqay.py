# Example: Profile Hotan Doreqay formula
from ethno_profiler import Profiler

# Define the 14 ingredients
hotan_doreqay = [
    ("Apium graveolens", "Celery"),
    ("Cinnamomum cassia", "Cinnamon"),
    ("Citrus reticulata", "Tangerine peel"),
    ("Zingiber officinale", "Ginger"),
    ("Nardostachys jatamansi", "Nardostachys"),
    ("Amomum tsaoko", "Tsaoko"),
    ("Rosa rugosa", "Rose"),
    ("Syzygium aromaticum", "Clove"),
    ("Foeniculum vulgare", "Fennel"),
    ("Pimpinella anisum", "Anise"),
    ("Amomum cardamomum", "Cardamom"),
    ("Trachyspermum ammi", "Ajwain"),
    ("Cinnamomum cassia twig", "Cinnamon twig"),
    ("Piper longum", "Long pepper"),
]

# Run profiling
p = Profiler()
results = p.profile(hotan_doreqay)

# Generate outputs
p.plot_heatmap(results, "hotan_doreqay_heatmap.tiff")
p.print_report(results)

# Save markdown table
with open("evidence_matrix.md", "w") as f:
    f.write(p.to_markdown(results))

print("Done! See hotan_doreqay_heatmap.tiff and evidence_matrix.md")
