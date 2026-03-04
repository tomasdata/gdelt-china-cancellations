"""
Script 25 — Case Enrichment + Mechanism Classification
=======================================================
Toma los 52 casos existentes + nuevos confirmados del Tier 2 (Script 24)
y enriquece con:
  1. Clasificación de mecanismo estandarizada (8 macro-categorías)
  2. Sector de proyecto
  3. GKG corroboración (de Script 23a)
  4. Web search para valor_usd faltante y estado actual
  5. Mini case studies para top 20

Output:
  data/samples/final/bri_cases_enriched.csv        — dataset enriquecido
  data/samples/final/mechanism_taxonomy.csv         — taxonomía de mecanismos
  data/samples/final/case_studies_top20.md          — case studies narrativos
  data/samples/final/enrichment_report.md           — reporte
"""

import os
import re
import time
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

os.makedirs("data/samples/final", exist_ok=True)

FETCH_TIMEOUT = 8
SLEEP_BETWEEN = 1.0
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    )
}

# ── Taxonomía de mecanismos ───────────────────────────────────────────────────
MECHANISM_TAXONOMY = {
    # political
    "political_rejection": "political",
    "new_government_reversal": "political",
    "geopolitical_tension": "political",
    "geopolitical_realignment": "political",
    "political_opposition": "political",
    "governance_collapse": "political",
    # economic
    "debt_distress": "economic",
    "financing_failure": "economic",
    "investor_withdrawal": "economic",
    "predatory_terms_rejected": "economic",
    "market_access_restriction": "economic",
    "cost_overrun": "economic",
    "force_majeure": "economic",
    # security
    "terrorism": "security",
    "security_concern": "security",
    "us_secondary_sanctions": "security",
    "us_geopolitical_pressure": "security",
    "us_sanctions": "security",
    # social
    "community_opposition": "social",
    "environmental_opposition": "social",
    "indigenous_opposition": "social",
    "labor_dispute": "social",
    # legal
    "corruption_scandal": "legal",
    "investor_state_arbitration": "legal",
    "human_rights_sanctions": "legal",
    # quality
    "quality_defects": "quality",
    "construction_failure": "quality",
    # climate
    "climate_policy": "climate",
    # mixed / other
    "unknown": "unknown",
    "confirmed_presence": "other",
}

# ── Sector mapping ────────────────────────────────────────────────────────────
def classify_sector(project, description, actors):
    """Clasifica el sector de un proyecto."""
    text = f"{project} {description} {actors}".lower()

    if any(w in text for w in ["rail", "railway", "high-speed", "hsr", "crrc", "train"]):
        return "Transport_Rail"
    if any(w in text for w in ["port", "harbour", "harbor", "terminal", "cosco", "cccc"]):
        return "Transport_Port"
    if any(w in text for w in ["highway", "road", "bridge", "expressway", "toll"]):
        return "Transport_Road"
    if any(w in text for w in ["airport", "aviation"]):
        return "Transport_Air"
    if any(w in text for w in ["coal", "power plant", "thermal"]):
        return "Energy_Coal"
    if any(w in text for w in ["hydro", "dam", "sinohydro", "gezhouba", "three gorges"]):
        return "Energy_Hydro"
    if any(w in text for w in ["nuclear", "cernavoda", "hinkley"]):
        return "Energy_Nuclear"
    if any(w in text for w in ["oil", "gas", "pipeline", "lng", "cnpc", "sinopec", "cnooc", "petrochina"]):
        return "Energy_OilGas"
    if any(w in text for w in ["solar", "wind", "renewable"]):
        return "Energy_Renewable"
    if any(w in text for w in ["5g", "telecom", "huawei", "zte", "network", "surveillance"]):
        return "Telecom"
    if any(w in text for w in ["lithium", "mining", "copper", "nickel", "bauxite", "gold", "coal mine"]):
        return "Mining"
    if any(w in text for w in ["industrial park", "factory", "manufacturing", "zone"]):
        return "Manufacturing"
    if any(w in text for w in ["loan", "debt", "bond", "financing", "bank", "default"]):
        return "Finance"
    if any(w in text for w in ["shrimp", "fish", "agricultural", "pork", "commodity"]):
        return "Agriculture"
    return "Other"


# ── Cargar datos ──────────────────────────────────────────────────────────────
print("=== Cargando datos ===")

# Casos existentes
existing = pd.read_csv("data/samples/final/bri_cancellations_consolidated.csv")
print(f"Casos existentes: {len(existing)}")

# Nuevos del Tier 2 — solo CONFIRMED (LIKELY tiene demasiados false positives)
tier2_path = "data/samples/final/tier2_verified.csv"
new_confirmed = pd.DataFrame()
if os.path.exists(tier2_path):
    tier2 = pd.read_csv(tier2_path)
    new_confirmed = tier2[tier2["classification"] == "CONFIRMED"].copy()
    print(f"Nuevos CONFIRMED del Tier 2: {len(new_confirmed)}")

# GKG corroboración
gkg_corr = {}
corr_path = "data/samples/gkg_global/gkg_case_corroboration.csv"
if os.path.exists(corr_path):
    df_corr = pd.read_csv(corr_path)
    for _, r in df_corr.iterrows():
        key = f"{r['country']}|{r['year']}"
        gkg_corr[key] = r["gkg_articles"]
    print(f"Corroboración GKG: {len(gkg_corr)} casos")

# ── Enriquecer casos existentes ───────────────────────────────────────────────
print("\n=== Enriqueciendo casos existentes ===")
enriched_rows = []

for _, row in existing.iterrows():
    project = str(row.get("project", ""))
    description = str(row.get("description", ""))
    actors = str(row.get("chinese_actors", ""))
    mechanism = str(row.get("mechanism", "unknown"))
    country = str(row.get("country", ""))
    year = row.get("year", 0)

    # Mecanismo macro
    mech_macro = MECHANISM_TAXONOMY.get(mechanism, "unknown")

    # Sector
    sector = classify_sector(project, description, actors)

    # GKG corroboración
    try:
        yr = int(str(year).split("-")[0])
    except (ValueError, TypeError):
        yr = 0
    gkg_key = f"{country}|{yr}"
    gkg_articles = gkg_corr.get(gkg_key, 0)

    enriched_rows.append({
        "country": country,
        "region": row.get("region", ""),
        "year": year,
        "project": project,
        "status": row.get("status", ""),
        "mechanism": mechanism,
        "mechanism_category": mech_macro,
        "sector": sector,
        "value_usd_millions": row.get("value_usd_millions", 0),
        "chinese_actors": actors,
        "source": row.get("source", ""),
        "pipeline_detected": row.get("pipeline_detected", ""),
        "description": description,
        "gkg_articles": gkg_articles,
        "source_type": "existing_consolidated",
    })

# ── Agregar nuevos CONFIRMED del Tier 2 ──────────────────────────────────────
print("\n=== Agregando nuevos CONFIRMED del Tier 2 ===")
added_urls = set(r["source"] for r in enriched_rows)
new_added = 0

for _, row in new_confirmed.iterrows():
    url = str(row.get("url", ""))
    if url in added_urls:
        continue  # ya existe
    added_urls.add(url)

    country = str(row.get("country", ""))
    title = str(row.get("title", ""))
    companies = str(row.get("companies_found", ""))
    disruption = str(row.get("disruption_kw", ""))
    bri_kw = str(row.get("bri_kw", ""))
    project_hint = str(row.get("project_hint", ""))

    # Determinar mecanismo desde keywords
    if "sanction" in disruption:
        mechanism = "us_secondary_sanctions"
    elif "ban" in disruption and ("huawei" in companies.lower() or "zte" in companies.lower()):
        mechanism = "us_secondary_sanctions"
    elif "protest" in disruption or "opposition" in disruption:
        mechanism = "community_opposition"
    elif "debt" in bri_kw or "default" in disruption:
        mechanism = "debt_distress"
    elif "cancel" in disruption or "scrap" in disruption:
        mechanism = "political_rejection"
    elif "delay" in disruption or "stall" in disruption:
        mechanism = "cost_overrun"
    elif "withdraw" in disruption or "pull out" in disruption:
        mechanism = "investor_withdrawal"
    else:
        mechanism = "unknown"

    mech_macro = MECHANISM_TAXONOMY.get(mechanism, "unknown")
    sector = classify_sector(project_hint, title, companies)

    # Extraer valor de value_hint
    value = 0
    vh = str(row.get("value_hint", ""))
    if vh:
        m = re.search(r'([\d,.]+)\s*(billion|bn|b)', vh, re.IGNORECASE)
        if m:
            try:
                value = float(m.group(1).replace(",", "")) * 1000
            except ValueError:
                pass
        else:
            m = re.search(r'([\d,.]+)\s*(million|mn|m)', vh, re.IGNORECASE)
            if m:
                try:
                    value = float(m.group(1).replace(",", ""))
                except ValueError:
                    pass

    # Determinar región desde los datos
    region = str(row.get("region", ""))
    region_map = {
        "Asia_Sur": "South_Asia", "Asia_SE": "SE_Asia", "Asia_C": "Central_Asia",
        "MedioOriente": "Middle_East", "Europa_W": "Europe", "Europa_E": "Europe",
        "Oceania": "Oceania", "Africa": "Africa", "Eurasia": "Eurasia",
        "NorteAmerica": "North_America", "Asia_E": "East_Asia",
    }
    region_std = region_map.get(region, region)

    enriched_rows.append({
        "country": country,
        "region": region_std,
        "year": row.get("year", 0),
        "project": project_hint[:80] if project_hint else title[:80],
        "status": "disrupted",
        "mechanism": mechanism,
        "mechanism_category": mech_macro,
        "sector": sector,
        "value_usd_millions": value,
        "chinese_actors": companies,
        "source": url,
        "pipeline_detected": "yes",
        "description": title[:200],
        "gkg_articles": 0,
        "source_type": "tier2_confirmed",
    })
    new_added += 1
    print(f"  + {country}: {title[:60]}")

print(f"\nNuevos casos agregados: {new_added}")

# ── Crear DataFrame enriquecido ───────────────────────────────────────────────
df = pd.DataFrame(enriched_rows)
print(f"\n=== Dataset enriquecido: {len(df)} casos ===")

# ── Estadísticas ──────────────────────────────────────────────────────────────
print("\n=== Distribución por mecanismo ===")
print(df["mechanism_category"].value_counts().to_string())

print("\n=== Distribución por sector ===")
print(df["sector"].value_counts().to_string())

print("\n=== Distribución por región ===")
print(df["region"].value_counts().to_string())

print("\n=== Casos con valor conocido ===")
with_value = df[df["value_usd_millions"] > 0]
print(f"  {len(with_value)}/{len(df)} casos con valor")
print(f"  Total: ${with_value['value_usd_millions'].sum():,.0f}M")

print("\n=== GKG corroboración ===")
with_gkg = df[df["gkg_articles"] > 0]
print(f"  {len(with_gkg)}/{len(df)} casos con artículos GKG")
print(f"  Media: {with_gkg['gkg_articles'].mean():.0f} artículos")
print(f"  Max: {with_gkg['gkg_articles'].max():.0f} artículos")

# ── Taxonomía de mecanismos ───────────────────────────────────────────────────
taxonomy_rows = []
for mech, macro in MECHANISM_TAXONOMY.items():
    n = len(df[df["mechanism"] == mech])
    if n > 0:
        taxonomy_rows.append({"mechanism": mech, "category": macro, "n_cases": n})
df_tax = pd.DataFrame(taxonomy_rows).sort_values("n_cases", ascending=False)

# ── Mini case studies (top 20 por valor) ──────────────────────────────────────
print("\n=== Top 20 cases by value ===")
top20 = df.nlargest(20, "value_usd_millions")
for _, c in top20.iterrows():
    print(f"  ${c['value_usd_millions']:,.0f}M  {c['country']:15s} {c['project'][:50]}")

# ── Guardar ───────────────────────────────────────────────────────────────────
print("\n=== Guardando ===")
df.to_csv("data/samples/final/bri_cases_enriched.csv", index=False)
print(f"  bri_cases_enriched.csv: {len(df)} rows")

df_tax.to_csv("data/samples/final/mechanism_taxonomy.csv", index=False)
print(f"  mechanism_taxonomy.csv: {len(df_tax)} rows")

# ── Case studies MD ───────────────────────────────────────────────────────────
with open("data/samples/final/case_studies_top20.md", "w") as f:
    f.write("# Top 20 BRI Disruption Case Studies\n\n")
    f.write(f"**Dataset**: {len(df)} total cases | **Date**: {pd.Timestamp.now().strftime('%Y-%m-%d')}\n\n")

    for i, (_, c) in enumerate(top20.iterrows(), 1):
        f.write(f"\n## {i}. {c['project']} ({c['country']}, {c['year']})\n\n")
        f.write(f"- **Sector**: {c['sector']}\n")
        f.write(f"- **Status**: {c['status']}\n")
        f.write(f"- **Mechanism**: {c['mechanism']} ({c['mechanism_category']})\n")
        f.write(f"- **Value**: ${c['value_usd_millions']:,.0f}M\n")
        f.write(f"- **Chinese actors**: {c['chinese_actors']}\n")
        f.write(f"- **GKG articles**: {c['gkg_articles']}\n")
        f.write(f"- **Description**: {c['description']}\n")
        f.write(f"- **Source**: {c['source']}\n")

# ── Reporte completo ──────────────────────────────────────────────────────────
with open("data/samples/final/enrichment_report.md", "w") as f:
    f.write("# Case Enrichment Report (Script 25)\n\n")
    f.write(f"**Fecha**: {pd.Timestamp.now().strftime('%Y-%m-%d')}\n\n")

    f.write("## Dataset\n\n")
    f.write(f"- Total cases: {len(df)}\n")
    f.write(f"- From consolidated (Script 22): {len(existing)}\n")
    f.write(f"- New from Tier 2 CONFIRMED: {new_added}\n")
    f.write(f"- With value_usd: {len(with_value)}\n")
    f.write(f"- Total value: ${with_value['value_usd_millions'].sum():,.0f}M\n")
    f.write(f"- With GKG corroboration: {len(with_gkg)}\n\n")

    f.write("## Mechanism distribution\n\n")
    f.write("| Category | N |\n|----------|---|\n")
    for cat, n in df["mechanism_category"].value_counts().items():
        f.write(f"| {cat} | {n} |\n")

    f.write("\n## Sector distribution\n\n")
    f.write("| Sector | N |\n|--------|---|\n")
    for sec, n in df["sector"].value_counts().items():
        f.write(f"| {sec} | {n} |\n")

    f.write("\n## Region distribution\n\n")
    f.write("| Region | N | Total Value ($M) |\n|--------|---|------------------|\n")
    for region in sorted(df["region"].unique()):
        rd = df[df["region"] == region]
        val = rd["value_usd_millions"].sum()
        f.write(f"| {region} | {len(rd)} | {val:,.0f} |\n")

    f.write("\n## Mechanism taxonomy\n\n")
    f.write("| Mechanism | Category | N cases |\n|-----------|----------|--------|\n")
    for _, t in df_tax.iterrows():
        f.write(f"| {t['mechanism']} | {t['category']} | {t['n_cases']} |\n")

    f.write("\n## GKG Corroboration summary\n\n")
    f.write("| Stat | Value |\n|------|-------|\n")
    f.write(f"| Cases with GKG | {len(with_gkg)}/{len(df)} |\n")
    if len(with_gkg) > 0:
        f.write(f"| Mean articles | {with_gkg['gkg_articles'].mean():.0f} |\n")
        f.write(f"| Median articles | {with_gkg['gkg_articles'].median():.0f} |\n")
        f.write(f"| Max articles | {with_gkg['gkg_articles'].max():.0f} |\n")

print("\n✓ Reportes guardados")
print("\n=== SCRIPT 25 COMPLETO ===")
