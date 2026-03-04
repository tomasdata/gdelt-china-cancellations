"""
Script 23b — GKG Theme-Based Case Discovery
=============================================
Complementa 23a (eje SOE) con un eje temático:
  1. Co-ocurrencia de temas BRI + cancelación (sin requerir SOE en orgs)
  2. Extracción de nombres de proyecto desde AllNames
  3. Búsqueda de evidencia en Quotations
  4. Gap analysis: buscar los 16 casos conocidos que el pipeline NO detectó

Output:
  data/samples/gkg_global/gkg_project_names.csv        — nombres extraídos
  data/samples/gkg_global/gkg_quotation_evidence.csv   — citas con evidencia
  data/samples/gkg_global/gkg_gap_analysis.csv         — casos no-detectados en GKG
  data/samples/gkg_global/gkg_theme_discovery_report.md — reporte
"""

import os
import re
import pandas as pd
import numpy as np
from collections import Counter, defaultdict

os.makedirs("data/samples/gkg_global", exist_ok=True)

# ── Patrones de proyectos BRI conocidos ───────────────────────────────────────
# Nombres que deberían aparecer en AllNames o URLs si el proyecto está cubierto
BRI_PROJECT_PATTERNS = [
    # Infrastructure mega-projects
    r"CPEC|China[\s-]Pakistan\s+Economic\s+Corridor",
    r"Gwadar(?:\s+Port)?",
    r"Hambantota(?:\s+Port)?",
    r"Colombo\s+Port\s+City",
    r"Kyaukphyu(?:\s+Port)?",
    r"Myitsone\s+Dam",
    r"East\s+Coast\s+Rail(?:way)?|ECRL",
    r"Jakarta[\s-]Bandung|Kereta\s+Cepat",
    r"Pokhara(?:\s+Airport)?",
    r"Diamer[\s-]?Bhasha(?:\s+Dam)?",
    r"Kra\s+Canal|Thai\s+Canal",
    r"Bagamoyo(?:\s+Port)?",
    r"Mombasa[\s-]Nairobi|Standard\s+Gauge\s+Railway|SGR",
    r"Addis[\s-]Ababa[\s-]Djibouti",
    r"Boten[\s-]Vientiane|China[\s-]Laos\s+Railway",
    r"Dara\s+Sakor",
    r"Port\s+Qasim",
    r"Thar\s+Coal",
    r"Tarbela(?:\s+Dam)?",
    r"Great\s+Stone(?:\s+Industrial)?",
    r"Sihanoukville",
    r"Piraeus(?:\s+Port)?",
    # Mining/resources
    r"Salar\s+de\s+Uyuni|Uyuni\s+Lithium",
    r"SQM|Tianqi\s+Lithium",
    r"Ramu\s+Nickel",
    r"Sicomines",
    r"Letpadaung(?:\s+Mine)?",
    # Energy
    r"Banshkhali",
    r"Sengwa(?:\s+Coal)?",
    r"Coca\s+Codo\s+Sinclair",
    r"Rampal(?:\s+Power)?",
    # Telecom
    r"Huawei\s+5G|ZTE\s+5G",
    # Finance/policy
    r"Belt\s+and\s+Road|BRI|OBOR",
    r"Silk\s+Road\s+Fund",
    r"debt[\s-]trap",
]

PROJECT_RE = re.compile("|".join(BRI_PROJECT_PATTERNS), re.IGNORECASE)

# ── Términos de cancelación en citas ──────────────────────────────────────────
CANCEL_QUOTE_RE = re.compile(
    r"\b(cancel|suspend|halt|scrap|abandon|terminate|withdraw|pull\s+out|"
    r"block|reject|ban|revoke|renegotiat|default|stall|delay|"
    r"not\s+proceed|put\s+on\s+hold|indefinitely\s+postpone)\b",
    re.IGNORECASE
)

CHINA_QUOTE_RE = re.compile(
    r"\b(China|Chinese|Beijing|BRI|Belt\s+and\s+Road|CPEC|"
    r"Huawei|ZTE|CNPC|Sinopec|COSCO|CRRC|CCCC)\b",
    re.IGNORECASE
)

# ── FIPS → país (simplificado de 23a) ────────────────────────────────────────
FIPS_MAP = {
    "CI":"Chile","AR":"Argentina","BR":"Brasil","MX":"México","PE":"Perú",
    "CO":"Colombia","VE":"Venezuela","BL":"Bolivia","EC":"Ecuador",
    "PK":"Pakistan","IN":"India","CE":"Sri Lanka","NP":"Nepal","BG":"Bangladesh",
    "MY":"Malaysia","TH":"Thailand","ID":"Indonesia","VM":"Vietnam","CB":"Cambodia",
    "LA":"Laos","BM":"Myanmar","RP":"Philippines",
    "KZ":"Kazakhstan","UZ":"Uzbekistan","KG":"Kyrgyzstan","TX":"Turkmenistan","TI":"Tajikistan",
    "IR":"Iran","IS":"Israel","SA":"Saudi Arabia","AE":"UAE","TU":"Turkey","IZ":"Iraq",
    "NI":"Nigeria","KE":"Kenya","SF":"South Africa","ET":"Ethiopia","TZ":"Tanzania",
    "ZA":"Zambia","ZI":"Zimbabwe","CG":"Congo (DRC)","EG":"Egypt","AO":"Angola",
    "CM":"Cameroon","GH":"Ghana","MZ":"Mozambique","DJ":"Djibouti",
    "UK":"United Kingdom","GM":"Germany","FR":"France","IT":"Italy","GR":"Greece",
    "HU":"Hungary","PL":"Poland","BO":"Belarus","UP":"Ukraine","RS":"Russia",
    "BK":"Bosnia-Herzegovina","SR":"Serbia","MN":"Montenegro","AL":"Albania",
    "AS":"Australia","NZ":"New Zealand","PP":"Papua New Guinea","FJ":"Fiji","TN":"Tonga",
    "MG":"Mongolia","MV":"Maldives",
}

_EXCLUDE = {"US","CA","CH","TW","HK","JA","KS","KN"}


def get_countries(locs_str):
    if not locs_str or pd.isna(locs_str):
        return []
    found = set()
    for part in str(locs_str).split(";"):
        fields = part.split("#")
        if len(fields) >= 4:
            cc = fields[3].strip().upper()
            if cc in FIPS_MAP and cc not in _EXCLUDE:
                found.add(cc)
    return sorted(found)


# ── Cargar casos conocidos ────────────────────────────────────────────────────
known_cases = pd.read_csv("data/samples/final/bri_cancellations_consolidated.csv")
# Casos que el pipeline NO detectó
gap_cases = known_cases[known_cases["pipeline_detected"] == "no"].copy()
print(f"Casos conocidos: {len(known_cases)}, no detectados por pipeline: {len(gap_cases)}")

# ── Procesar GKG año por año ──────────────────────────────────────────────────
YEARS = range(2017, 2025)
project_names_found = []
quotation_evidence = []
gap_hits = defaultdict(list)  # project_name → list of (year, url, evidence)

total_articles = 0
total_with_project = 0
total_with_quote_evidence = 0

for year in YEARS:
    path = f"data/samples/gkg_por_año/{year}/gkg_china_{year}.parquet"
    if not os.path.exists(path):
        continue

    print(f"\n{'='*60}")
    print(f"Procesando {year}...")
    df = pd.read_parquet(path)
    df["tone"] = df["V2Tone"].str.split(",").str[0].astype(float, errors="ignore")
    total_articles += len(df)
    print(f"  Artículos: {len(df):,}")

    year_projects = 0
    year_quotes = 0

    for idx, row in df.iterrows():
        url = str(row.get("DocumentIdentifier", ""))
        allnames = str(row.get("AllNames", "") or "")
        quotations = str(row.get("Quotations", "") or "")
        themes = str(row.get("V2Themes", "") or "")
        locs = row.get("V2Locations", "")
        tone = row.get("tone", 0)
        source = str(row.get("SourceCommonName", ""))

        countries = get_countries(locs)

        # ── 1. Buscar nombres de proyecto BRI en AllNames ─────────────
        project_matches = PROJECT_RE.findall(allnames)
        if not project_matches:
            # También buscar en URL
            project_matches = PROJECT_RE.findall(url)

        if project_matches:
            year_projects += 1
            for cc in (countries if countries else [""]):
                country_name = FIPS_MAP.get(cc, cc) if cc else "Unknown"
                project_names_found.append({
                    "year": year,
                    "cc": cc,
                    "country": country_name,
                    "project_match": ",".join(set(m for m in project_matches if m)),
                    "tone": tone,
                    "source": source,
                    "url": url,
                    "allnames_sample": allnames[:300],
                })

        # ── 2. Buscar evidencia en Quotations ─────────────────────────
        if quotations and quotations != "None" and len(quotations) > 10:
            # Buscar citas que mencionan China + cancelación
            has_china = bool(CHINA_QUOTE_RE.search(quotations))
            cancel_match = CANCEL_QUOTE_RE.search(quotations)

            if has_china and cancel_match:
                year_quotes += 1
                # Extraer las citas relevantes (separadas por |)
                quotes = quotations.split("|")
                relevant_quotes = []
                for q in quotes:
                    if CHINA_QUOTE_RE.search(q) and CANCEL_QUOTE_RE.search(q):
                        relevant_quotes.append(q.strip()[:300])
                    elif CANCEL_QUOTE_RE.search(q):
                        relevant_quotes.append(q.strip()[:300])

                if relevant_quotes:
                    for cc in (countries if countries else [""]):
                        country_name = FIPS_MAP.get(cc, cc) if cc else "Unknown"
                        quotation_evidence.append({
                            "year": year,
                            "cc": cc,
                            "country": country_name,
                            "tone": tone,
                            "cancel_action": cancel_match.group(),
                            "n_relevant_quotes": len(relevant_quotes),
                            "best_quote": relevant_quotes[0][:500],
                            "source": source,
                            "url": url,
                        })

        # ── 3. Gap analysis: buscar casos no detectados ───────────────
        for _, gc in gap_cases.iterrows():
            project = str(gc["project"])
            gc_country = str(gc["country"])
            # Buscar nombre del proyecto en AllNames, URL, o Quotations
            search_text = f"{allnames} {url} {quotations}"
            # Crear pattern dinámico para cada proyecto
            keywords = project.lower().split()
            # Necesita al menos 2 keywords del nombre del proyecto
            matched_kw = sum(1 for kw in keywords if len(kw) > 3 and kw in search_text.lower())
            if matched_kw >= 2:
                gap_hits[project].append({
                    "year": year,
                    "url": url,
                    "source": source,
                    "tone": tone,
                    "country_match": gc_country,
                    "keywords_matched": matched_kw,
                    "allnames_sample": allnames[:200],
                })

    total_with_project += year_projects
    total_with_quote_evidence += year_quotes
    print(f"  Proyectos BRI encontrados: {year_projects:,}")
    print(f"  Citas con evidencia cancel+China: {year_quotes:,}")

    del df

# ── Resultados ────────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print("RESULTADOS")
print(f"Total artículos: {total_articles:,}")
print(f"Con nombre de proyecto BRI: {total_with_project:,}")
print(f"Con evidencia en citas: {total_with_quote_evidence:,}")

# ── Project names ─────────────────────────────────────────────────────────────
df_projects = pd.DataFrame(project_names_found)
print(f"\n=== Nombres de proyecto BRI encontrados: {len(df_projects):,} ===")
if len(df_projects) > 0:
    # Top proyectos por frecuencia
    all_matches = Counter()
    for m in df_projects["project_match"]:
        for p in m.split(","):
            p = p.strip()
            if p:
                all_matches[p] += 1

    print("\nTop 30 menciones de proyecto:")
    for proj, n in all_matches.most_common(30):
        print(f"  {n:5d}  {proj}")

    # Por país
    print("\nProyectos por país (top 20):")
    proj_by_country = df_projects.groupby("country").size().sort_values(ascending=False)
    print(proj_by_country.head(20).to_string())

# ── Quotation evidence ────────────────────────────────────────────────────────
df_quotes = pd.DataFrame(quotation_evidence)
print(f"\n=== Evidencia en citas: {len(df_quotes):,} ===")
if len(df_quotes) > 0:
    print("\nAcciones de cancelación más frecuentes:")
    print(df_quotes["cancel_action"].value_counts().head(15).to_string())

    print("\nTop países con evidencia de citas:")
    quotes_by_country = df_quotes.groupby("country").agg(
        n=("url", "nunique"),
        avg_tone=("tone", "mean"),
    ).sort_values("n", ascending=False)
    quotes_by_country["avg_tone"] = quotes_by_country["avg_tone"].round(2)
    print(quotes_by_country.head(20).to_string())

    print("\nMejores citas (más negativas):")
    top_quotes = df_quotes.nsmallest(15, "tone")
    for _, q in top_quotes.iterrows():
        print(f"\n  [{q['country']} {q['year']}] tone={q['tone']:.1f}")
        print(f"  Action: {q['cancel_action']}")
        print(f"  Quote: {q['best_quote'][:200]}")
        print(f"  URL: {q['url'][:100]}")

# ── Gap analysis ──────────────────────────────────────────────────────────────
print(f"\n=== Gap Analysis: casos no detectados por pipeline ===")
print(f"Casos a buscar: {len(gap_cases)}")
for _, gc in gap_cases.iterrows():
    project = str(gc["project"])
    hits = gap_hits.get(project, [])
    status = f"FOUND ({len(hits)} hits)" if hits else "NOT FOUND"
    print(f"\n  {gc['country']:20s} | {project[:40]:40s} | {status}")
    if hits:
        for h in sorted(hits, key=lambda x: x["tone"])[:3]:
            print(f"    {h['year']} tone={h['tone']:.1f} {h['url'][:80]}")

# ── Guardar ───────────────────────────────────────────────────────────────────
print("\n=== Guardando ===")

if len(df_projects) > 0:
    df_projects.to_csv("data/samples/gkg_global/gkg_project_names.csv", index=False)
    print(f"  gkg_project_names.csv: {len(df_projects):,}")

if len(df_quotes) > 0:
    df_quotes.to_csv("data/samples/gkg_global/gkg_quotation_evidence.csv", index=False)
    print(f"  gkg_quotation_evidence.csv: {len(df_quotes):,}")

# Gap analysis CSV
gap_rows = []
for _, gc in gap_cases.iterrows():
    project = str(gc["project"])
    hits = gap_hits.get(project, [])
    gap_rows.append({
        "country": gc["country"],
        "project": project,
        "year": gc["year"],
        "gkg_hits": len(hits),
        "best_url": hits[0]["url"][:200] if hits else "",
        "best_tone": hits[0]["tone"] if hits else None,
    })
df_gap = pd.DataFrame(gap_rows)
df_gap.to_csv("data/samples/gkg_global/gkg_gap_analysis.csv", index=False)
print(f"  gkg_gap_analysis.csv: {len(df_gap)}")

# ── Reporte narrativo ─────────────────────────────────────────────────────────
with open("data/samples/gkg_global/gkg_theme_discovery_report.md", "w") as f:
    f.write("# GKG Theme-Based Case Discovery Report (Script 23b)\n\n")
    f.write(f"**Fecha**: {pd.Timestamp.now().strftime('%Y-%m-%d')}\n\n")

    f.write("## Resumen\n\n")
    f.write(f"- Artículos GKG procesados: {total_articles:,}\n")
    f.write(f"- Con nombre de proyecto BRI: {total_with_project:,}\n")
    f.write(f"- Con evidencia de cancelación en citas: {total_with_quote_evidence:,}\n")

    f.write("\n## Nombres de proyecto BRI detectados\n\n")
    if len(df_projects) > 0:
        f.write("| Proyecto | Menciones |\n|----------|----------|\n")
        for proj, n in all_matches.most_common(20):
            f.write(f"| {proj} | {n} |\n")

    f.write("\n## Evidencia en citas (top 20 más negativas)\n\n")
    if len(df_quotes) > 0:
        for _, q in df_quotes.nsmallest(20, "tone").iterrows():
            f.write(f"\n### {q['country']} ({q['year']}) — tone {q['tone']:.1f}\n")
            f.write(f"- Action: *{q['cancel_action']}*\n")
            f.write(f"- Quote: \"{q['best_quote'][:300]}\"\n")
            f.write(f"- Source: [{q['source']}]({q['url']})\n")

    f.write("\n## Gap Analysis: casos no detectados por pipeline\n\n")
    f.write("| País | Proyecto | Año | GKG Hits | Status |\n")
    f.write("|------|----------|-----|----------|--------|\n")
    for _, gc in df_gap.iterrows():
        status = "FOUND" if gc["gkg_hits"] > 0 else "NOT FOUND"
        f.write(f"| {gc['country']} | {gc['project'][:35]} | {gc['year']} | "
                f"{gc['gkg_hits']} | {status} |\n")

print("\n✓ Reporte: data/samples/gkg_global/gkg_theme_discovery_report.md")
print("\n=== SCRIPT 23b COMPLETO ===")
