"""
Script 27 — Final Consolidated Dataset v2
==========================================
Merge de todas las fuentes en un dataset thesis-ready:
  1. 52 casos originales (Script 22)
  2. 16 nuevos CONFIRMED del Tier 2 (Script 24/25)
  3. Casos regionales genuinos (Script 26) — curación manual
  4. Corroboración GKG (Script 23a)

Produce:
  - Dataset final CSV con metadata completa
  - Tablas estadísticas para la tesis
  - Reporte narrativo con análisis de mecanismos
  - Actualización de CHANGELOG y README

Output:
  data/samples/final/bri_cancellations_FINAL_v2.csv
  data/samples/final/bri_cancellations_FINAL_v2.md
  data/samples/final/thesis_tables/
"""

import os
import re
import pandas as pd
import numpy as np
from collections import Counter

os.makedirs("data/samples/final/thesis_tables", exist_ok=True)

# ── Region standardization ────────────────────────────────────────────────────
REGION_STD = {
    "LATAM": "LATAM",
    "Asia Sur": "South_Asia", "South_Asia": "South_Asia",
    "Asia SE": "SE_Asia", "SE_Asia": "SE_Asia",
    "Asia Central": "Central_Asia", "Central_Asia": "Central_Asia",
    "Medio Oriente": "Middle_East", "Middle_East": "Middle_East",
    "Africa": "Africa",
    "Europa W": "Europe", "Europa E": "Europe", "Europe": "Europe",
    "Oceania": "Oceania",
    "Eurasia": "Eurasia",
    "North_America": "North_America", "NorteAmerica": "North_America",
    "East_Asia": "East_Asia", "Asia_E": "East_Asia",
    "Other": "Other",
}

# ── Mechanism standardization ─────────────────────────────────────────────────
MECHANISM_TO_CATEGORY = {
    "political_rejection": "political",
    "new_government_reversal": "political",
    "geopolitical_tension": "political",
    "geopolitical_realignment": "political",
    "political_opposition": "political",
    "governance_collapse": "political",
    "debt_distress": "economic",
    "financing_failure": "economic",
    "investor_withdrawal": "economic",
    "predatory_terms_rejected": "economic",
    "market_access_restriction": "economic",
    "cost_overrun": "economic",
    "force_majeure": "economic",
    "terrorism": "security",
    "security_concern": "security",
    "us_secondary_sanctions": "security",
    "us_geopolitical_pressure": "security",
    "us_sanctions": "security",
    "community_opposition": "social",
    "environmental_opposition": "social",
    "indigenous_opposition": "social",
    "labor_dispute": "social",
    "corruption_scandal": "legal",
    "investor_state_arbitration": "legal",
    "human_rights_sanctions": "legal",
    "quality_defects": "quality",
    "construction_failure": "quality",
    "climate_policy": "climate",
    "unknown": "unknown",
    "confirmed_presence": "other",
}

# ── Sector classification ─────────────────────────────────────────────────────
def classify_sector(project, description, actors):
    text = f"{project} {description} {actors}".lower()
    if any(w in text for w in ["rail", "railway", "high-speed", "hsr", "crrc", "train"]):
        return "Transport_Rail"
    if any(w in text for w in ["port", "harbour", "harbor", "terminal", "cosco", "cccc", "gwadar", "hambantota"]):
        return "Transport_Port"
    if any(w in text for w in ["highway", "road", "bridge", "expressway"]):
        return "Transport_Road"
    if any(w in text for w in ["airport", "aviation"]):
        return "Transport_Air"
    if any(w in text for w in ["coal power", "thermal plant", "coal plant"]):
        return "Energy_Coal"
    if any(w in text for w in ["hydro", "dam", "sinohydro", "gezhouba", "three gorges"]):
        return "Energy_Hydro"
    if any(w in text for w in ["nuclear", "cernavoda"]):
        return "Energy_Nuclear"
    if any(w in text for w in ["oil", "gas", "pipeline", "lng", "cnpc", "sinopec", "cnooc", "petrochina"]):
        return "Energy_OilGas"
    if any(w in text for w in ["5g", "telecom", "huawei", "zte", "network", "surveillance"]):
        return "Telecom"
    if any(w in text for w in ["lithium", "mining", "copper", "nickel", "bauxite", "gold"]):
        return "Mining"
    if any(w in text for w in ["industrial park", "factory", "manufacturing", "zone"]):
        return "Manufacturing"
    if any(w in text for w in ["loan", "debt", "default", "financing", "bank"]):
        return "Finance"
    if any(w in text for w in ["shrimp", "fish", "agricultural", "pork", "commodity"]):
        return "Agriculture"
    return "Other"


# ── 1. Cargar base: casos enriquecidos (Script 25) ───────────────────────────
print("=== Cargando datos ===")
df_enriched = pd.read_csv("data/samples/final/bri_cases_enriched.csv")
print(f"Casos enriquecidos (Script 25): {len(df_enriched)}")

# ── 2. Cargar casos regionales genuinos (Script 26) ──────────────────────────
# Curación manual: excluir duplicados y false positives del Script 26
regional_path = "data/samples/gkg_global/regional_new_cases.csv"
regional_genuine = []

if os.path.exists(regional_path):
    df_regional = pd.read_csv(regional_path)
    print(f"Casos regionales brutos: {len(df_regional)}")

    # Dedup por título (muchos artículos duplicados en francés)
    seen_titles = set()
    for _, r in df_regional.iterrows():
        title = str(r.get("title", ""))[:50].lower()
        country = str(r.get("country", ""))

        # Skip duplicados
        key = f"{country}|{title}"
        if key in seen_titles:
            continue
        seen_titles.add(key)

        # Skip false positives conocidos:
        # - "Canadien condamné" = artículos sobre muerte en China (no BRI)
        # - "Ex-Hong Kong minister" = bribery trial (no project disruption)
        # - "Political Unrest Creates Shipping Crisis" = generic shipping (check)
        skip_patterns = [
            "canadien condamn",
            "patrick ho",          # Bribery trial, not a project
            "key issues that drive us-china",  # Generic geopolitics
        ]
        if any(p in title for p in skip_patterns):
            continue

        # Solo incluir si no es un duplicado del enriched
        existing_countries = set(df_enriched["country"].dropna().str.lower())
        if country.lower() in ["australia"]:
            # Australia ya bien representada, skip duplicados Huawei
            if "huawei" in str(r.get("companies", "")).lower() and "sanction" in str(r.get("disruptions", "")):
                continue

        regional_genuine.append(r.to_dict())

    print(f"Casos regionales genuinos (post-curación): {len(regional_genuine)}")

# ── 3. Cargar GKG corroboración ──────────────────────────────────────────────
gkg_corr = {}
corr_path = "data/samples/gkg_global/gkg_case_corroboration.csv"
if os.path.exists(corr_path):
    df_corr = pd.read_csv(corr_path)
    for _, r in df_corr.iterrows():
        key = f"{r['country']}|{r['year']}"
        gkg_corr[key] = r["gkg_articles"]

# ── 4. Build final dataset ────────────────────────────────────────────────────
final_rows = []

# 4a. Casos enriquecidos
for _, row in df_enriched.iterrows():
    region = REGION_STD.get(str(row.get("region", "")), "Other")
    mechanism = str(row.get("mechanism", "unknown"))

    final_rows.append({
        "country": row["country"],
        "region": region,
        "year": row["year"],
        "project": row["project"],
        "status": row.get("status", ""),
        "mechanism": mechanism,
        "mechanism_category": MECHANISM_TO_CATEGORY.get(mechanism, "unknown"),
        "sector": row.get("sector", classify_sector(
            str(row.get("project", "")), str(row.get("description", "")),
            str(row.get("chinese_actors", "")))),
        "value_usd_millions": row.get("value_usd_millions", 0),
        "chinese_actors": row.get("chinese_actors", ""),
        "source": row.get("source", ""),
        "pipeline_detected": row.get("pipeline_detected", ""),
        "description": row.get("description", ""),
        "gkg_articles": row.get("gkg_articles", 0),
        "data_source": row.get("source_type", "existing"),
    })

# 4b. Casos regionales genuinos
for r in regional_genuine:
    country = str(r.get("country", ""))
    region = REGION_STD.get(str(r.get("region", "")), "Other")
    companies = str(r.get("companies", ""))
    disruptions = str(r.get("disruptions", ""))
    title = str(r.get("title", ""))

    # Infer mechanism from disruptions
    if "sanction" in disruptions:
        mechanism = "us_secondary_sanctions"
    elif "ban" in disruptions:
        mechanism = "us_secondary_sanctions"
    elif "protest" in disruptions or "opposition" in disruptions:
        mechanism = "community_opposition"
    elif "default" in disruptions or "debt" in disruptions:
        mechanism = "debt_distress"
    elif "cancel" in disruptions or "reject" in disruptions:
        mechanism = "political_rejection"
    elif "halt" in disruptions or "delay" in disruptions or "suspend" in disruptions:
        mechanism = "cost_overrun"
    elif "withdraw" in disruptions:
        mechanism = "investor_withdrawal"
    else:
        mechanism = "unknown"

    sector = classify_sector(title, disruptions, companies)

    final_rows.append({
        "country": country,
        "region": region,
        "year": r.get("year", 0),
        "project": title[:80],
        "status": "disrupted",
        "mechanism": mechanism,
        "mechanism_category": MECHANISM_TO_CATEGORY.get(mechanism, "unknown"),
        "sector": sector,
        "value_usd_millions": 0,
        "chinese_actors": companies,
        "source": str(r.get("url", "")),
        "pipeline_detected": "yes",
        "description": title[:200],
        "gkg_articles": 0,
        "data_source": "regional_deep_dive",
    })

# ── 5. Dedup by (country, project) ───────────────────────────────────────────
df_final = pd.DataFrame(final_rows)
print(f"\nPre-dedup: {len(df_final)} rows")

# Simple dedup: same country + similar project name
df_final["_dedup_key"] = df_final["country"].str.lower() + "|" + df_final["project"].str[:30].str.lower()
df_final = df_final.drop_duplicates("_dedup_key", keep="first").drop(columns=["_dedup_key"])
print(f"Post-dedup: {len(df_final)} rows")

# ── 6. Quality control ───────────────────────────────────────────────────────
print("\n=== Quality Control ===")
missing_country = df_final["country"].isna().sum()
missing_year = df_final["year"].isna().sum()
missing_mechanism = (df_final["mechanism"] == "unknown").sum()
print(f"Missing country: {missing_country}")
print(f"Missing year: {missing_year}")
print(f"Unknown mechanism: {missing_mechanism}")

# ── 7. Statistics ─────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"=== FINAL DATASET: {len(df_final)} cases ===")

print("\n--- By region ---")
region_stats = df_final.groupby("region").agg(
    n_cases=("country", "count"),
    total_value=("value_usd_millions", "sum"),
    with_value=("value_usd_millions", lambda x: (x > 0).sum()),
).sort_values("n_cases", ascending=False)
region_stats["total_value"] = region_stats["total_value"].astype(int)
print(region_stats.to_string())

print("\n--- By mechanism category ---")
mech_stats = df_final["mechanism_category"].value_counts()
print(mech_stats.to_string())

print("\n--- By sector ---")
sector_stats = df_final["sector"].value_counts()
print(sector_stats.to_string())

# Normalize year to int (some have "2017-2024" ranges)
df_final["year"] = df_final["year"].apply(lambda x: int(str(x).split("-")[0]) if pd.notna(x) else 0)

print("\n--- By year ---")
year_stats = df_final.groupby("year").size().sort_index()
print(year_stats.to_string())

print("\n--- Value summary ---")
with_value = df_final[df_final["value_usd_millions"] > 0]
print(f"Cases with value: {len(with_value)}/{len(df_final)}")
print(f"Total value: ${with_value['value_usd_millions'].sum():,.0f}M")
print(f"Median value: ${with_value['value_usd_millions'].median():,.0f}M")

print("\n--- Pipeline detection ---")
print(df_final["pipeline_detected"].value_counts().to_string())

print("\n--- Data source ---")
print(df_final["data_source"].value_counts().to_string())

# ── 8. Thesis tables ──────────────────────────────────────────────────────────
print("\n=== Generating thesis tables ===")

# Table 1: Region × Mechanism cross-tab
tab1 = pd.crosstab(df_final["region"], df_final["mechanism_category"], margins=True)
tab1.to_csv("data/samples/final/thesis_tables/table1_region_mechanism.csv")
print("  Table 1: region × mechanism")

# Table 2: Year × Status
tab2 = pd.crosstab(df_final["year"], df_final["status"], margins=True)
tab2.to_csv("data/samples/final/thesis_tables/table2_year_status.csv")
print("  Table 2: year × status")

# Table 3: Value by region
tab3 = df_final.groupby("region").agg(
    n_cases=("country", "count"),
    n_with_value=("value_usd_millions", lambda x: (x > 0).sum()),
    total_value_M=("value_usd_millions", "sum"),
    mean_value_M=("value_usd_millions", lambda x: x[x > 0].mean() if (x > 0).any() else 0),
).sort_values("total_value_M", ascending=False)
tab3["total_value_M"] = tab3["total_value_M"].astype(int)
tab3["mean_value_M"] = tab3["mean_value_M"].round(0).astype(int)
tab3.to_csv("data/samples/final/thesis_tables/table3_value_by_region.csv")
print("  Table 3: value by region")

# Table 4: Detection rate by region
pipeline_yes = df_final[df_final["pipeline_detected"] == "yes"]
pipeline_no = df_final[df_final["pipeline_detected"] == "no"]
det_rows = []
for region in sorted(df_final["region"].unique()):
    rd = df_final[df_final["region"] == region]
    detected = len(rd[rd["pipeline_detected"] == "yes"])
    total = len(rd)
    rate = 100 * detected / total if total > 0 else 0
    det_rows.append({"region": region, "total": total, "detected": detected, "rate_pct": round(rate, 1)})
tab4 = pd.DataFrame(det_rows)
tab4.to_csv("data/samples/final/thesis_tables/table4_detection_rate.csv", index=False)
print("  Table 4: detection rate")

# Table 5: GKG evidence depth
tab5 = df_final[df_final["gkg_articles"] > 0][["country", "year", "project", "gkg_articles"]].sort_values(
    "gkg_articles", ascending=False)
tab5.to_csv("data/samples/final/thesis_tables/table5_gkg_evidence_depth.csv", index=False)
print("  Table 5: GKG evidence depth")

# Table 6: Mechanism detail
tab6 = df_final.groupby(["mechanism", "mechanism_category"]).agg(
    n=("country", "count"),
    total_value_M=("value_usd_millions", "sum"),
    regions=("region", lambda x: ", ".join(sorted(set(x)))),
).sort_values("n", ascending=False)
tab6["total_value_M"] = tab6["total_value_M"].astype(int)
tab6.to_csv("data/samples/final/thesis_tables/table6_mechanism_detail.csv")
print("  Table 6: mechanism detail")

# ── 9. Save final dataset ────────────────────────────────────────────────────
print("\n=== Saving final dataset ===")
df_final.to_csv("data/samples/final/bri_cancellations_FINAL_v2.csv", index=False)
print(f"  bri_cancellations_FINAL_v2.csv: {len(df_final)} rows")

# ── 10. Narrative report ──────────────────────────────────────────────────────
with open("data/samples/final/bri_cancellations_FINAL_v2.md", "w") as f:
    f.write("# BRI Cancellations & Disruptions Dataset v2\n\n")
    f.write(f"**Generated**: {pd.Timestamp.now().strftime('%Y-%m-%d')}\n")
    f.write(f"**Pipeline**: Scripts 01-27 (GDELT v2 + GKG + web verification)\n\n")

    f.write("## Summary\n\n")
    f.write(f"- **{len(df_final)} verified cases** of BRI project disruptions across ")
    f.write(f"**{df_final['country'].nunique()} countries** and ")
    f.write(f"**{df_final['region'].nunique()} regions**\n")
    f.write(f"- Total value affected: **${with_value['value_usd_millions'].sum():,.0f}M**\n")
    f.write(f"- Cases with known value: {len(with_value)}/{len(df_final)}\n")
    f.write(f"- Pipeline detection rate: {len(df_final[df_final['pipeline_detected']=='yes'])}/{len(df_final)} "
            f"({100*len(df_final[df_final['pipeline_detected']=='yes'])/len(df_final):.0f}%)\n\n")

    f.write("## Dataset by Region\n\n")
    f.write("| Region | Cases | Value ($M) | Top mechanisms |\n")
    f.write("|--------|-------|-----------|----------------|\n")
    for region, row in region_stats.iterrows():
        rd = df_final[df_final["region"] == region]
        top_mechs = rd["mechanism_category"].value_counts().head(2).index.tolist()
        f.write(f"| {region} | {row['n_cases']} | {row['total_value']:,} | {', '.join(top_mechs)} |\n")

    f.write("\n## Mechanism Analysis\n\n")
    f.write("| Category | N | % | Regions |\n")
    f.write("|----------|---|---|--------|\n")
    for cat, n in mech_stats.items():
        pct = 100 * n / len(df_final)
        regions = df_final[df_final["mechanism_category"] == cat]["region"].unique()
        f.write(f"| {cat} | {n} | {pct:.0f}% | {', '.join(sorted(regions)[:4])} |\n")

    f.write("\n## Sector Distribution\n\n")
    f.write("| Sector | N | Value ($M) |\n")
    f.write("|--------|---|------------|\n")
    for sector, n in sector_stats.items():
        val = df_final[df_final["sector"] == sector]["value_usd_millions"].sum()
        f.write(f"| {sector} | {n} | {val:,.0f} |\n")

    f.write("\n## Temporal Evolution\n\n")
    f.write("| Year | Cases |\n|------|-------|\n")
    for year, n in year_stats.items():
        f.write(f"| {year} | {n} |\n")

    f.write("\n## Top 20 Cases by Value\n\n")
    f.write("| Country | Project | Value ($M) | Mechanism | Year |\n")
    f.write("|---------|---------|-----------|-----------|------|\n")
    for _, c in df_final.nlargest(20, "value_usd_millions").iterrows():
        f.write(f"| {c['country']} | {str(c['project'])[:40]} | "
                f"{c['value_usd_millions']:,.0f} | {c['mechanism']} | {c['year']} |\n")

    f.write("\n## Data Sources\n\n")
    f.write("| Source | N cases |\n|--------|--------|\n")
    for src, n in df_final["data_source"].value_counts().items():
        f.write(f"| {src} | {n} |\n")

    f.write("\n## Methodology\n\n")
    f.write("This dataset was constructed through a 27-script pipeline:\n\n")
    f.write("1. **GDELT Events** (Scripts 01-12): 663,825 events → 52,439 BRI-related → 801 candidates\n")
    f.write("2. **GKG Text Mining** (Scripts 07, 17, 23a/b): 626,775 articles → SOE timelines, ")
    f.write("debt/environmental signals, project name extraction\n")
    f.write("3. **Web Verification** (Scripts 19-20, 24, 26): URL scraping + evidence extraction\n")
    f.write("4. **Manual Curation** (Script 22): Literature cross-reference, 52 base cases\n")
    f.write("5. **Enrichment** (Script 25): Mechanism taxonomy, sector classification, value estimation\n")
    f.write("6. **Consolidation** (Script 27): Merge, dedup, quality control, thesis tables\n\n")

    f.write("### Limitations\n\n")
    f.write("- GDELT v2 begins 2015-02-19; pre-2015 cases from literature only\n")
    f.write("- English-language bias: francophone Africa, Central Asia (Russian), Pacific Islands underrepresented\n")
    f.write("- Huawei/5G bans dominate telecom sector; may inflate security mechanism counts\n")
    f.write("- Value estimates from news sources; may not match final project costs\n")
    f.write("- Some cases classified as 'disrupted' may have been subsequently resumed\n")

print(f"\n✓ bri_cancellations_FINAL_v2.md")

# ── 11. Print complete dataset ────────────────────────────────────────────────
print(f"\n{'='*60}")
print("=== COMPLETE DATASET ===\n")
for region in sorted(df_final["region"].unique()):
    rd = df_final[df_final["region"] == region].sort_values("year")
    print(f"\n--- {region} ({len(rd)} cases) ---")
    for _, c in rd.iterrows():
        val_str = f"${c['value_usd_millions']:,.0f}M" if c['value_usd_millions'] > 0 else ""
        print(f"  {c['country']:20s} {c['year']}  {str(c['project'])[:40]:40s} "
              f"{c['mechanism'][:25]:25s} {val_str}")

print(f"\n=== SCRIPT 27 COMPLETO ===")
print(f"=== TOTAL: {len(df_final)} CASOS VERIFICADOS ===")
