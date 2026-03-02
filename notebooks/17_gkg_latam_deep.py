"""
Script 17 — GKG-LATAM deep analysis
Objetivo: extraer señales reales de proyectos chinos disrumpidos en LATAM
usando los 92,990 artículos GKG, filtrando por:
  1. Ubicación en país LATAM (V2Locations)
  2. SOE china en V2Organizations
  3. Tono negativo (tono < -3)
  4. Temas relevantes en V2Themes (inversión, cancelación, protesta, etc.)

Output:
  - data/samples/gkg_latam/gkg_latam_soe_signals.csv   (artículos filtrados)
  - data/samples/gkg_latam/gkg_latam_clusters.csv      (clusters por país+SOE+año)
  - data/samples/gkg_latam/gkg_latam_top_signals.md    (narrativa de señales)
"""

import os
import re
import pandas as pd
import numpy as np
from collections import Counter

os.makedirs("data/samples/gkg_latam", exist_ok=True)

# ── Cargar GKG ───────────────────────────────────────────────────────────────
print("Cargando GKG...")
gkg = pd.read_parquet("data/samples/gkg_por_año/raw/gkg_china_2017_2024.parquet")
gkg["year"] = gkg["DATE"].astype(str).str[:4].astype(int, errors="ignore")
gkg["tone"] = gkg["V2Tone"].str.split(",").str[0].astype(float, errors="ignore")
print(f"GKG: {len(gkg):,} artículos")

# ── FIPS y regiones ──────────────────────────────────────────────────────────
LATAM_FIPS = {
    "CI":"Chile","AR":"Argentina","BR":"Brasil","MX":"México","PE":"Perú",
    "CO":"Colombia","VE":"Venezuela","BL":"Bolivia","EC":"Ecuador","UY":"Uruguay",
    "PA":"Paraguay","PM":"Panamá","CU":"Cuba","GT":"Guatemala","NU":"Nicaragua",
    "ES":"El Salvador","HO":"Honduras","BH":"Belice","DR":"Dom.Rep.",
    "GY":"Guyana","NS":"Suriname","CS":"Costa Rica","JM":"Jamaica","HA":"Haití",
}

# ── Mapeo SOE → grupo ────────────────────────────────────────────────────────
SOE_MAP = {
    "CHINA RAILWAY": "SOE_RAILWAY",    "CRRC": "SOE_RAILWAY",
    "COSCO": "SOE_MARITIME",           "CHINA OCEAN SHIPPING": "SOE_MARITIME",
    "CHINA HARBOUR": "SOE_HARBOUR",    "CHINA COMMUNICATIONS CONSTRUCTION": "SOE_HARBOUR",
    "CCCC": "SOE_HARBOUR",             "CHEC": "SOE_HARBOUR",
    "SINOHYDRO": "SOE_ENERGY",         "POWERCHINA": "SOE_ENERGY",
    "THREE GORGES": "SOE_ENERGY",      "CHINA THREE GORGES": "SOE_ENERGY",
    "GEZHOUBA": "SOE_ENERGY",
    "CNPC": "SOE_OIL",                 "PETROCHINA": "SOE_OIL",
    "SINOPEC": "SOE_OIL",              "CNOOC": "SOE_OIL",
    "CHINA NATIONAL PETROLEUM": "SOE_OIL",  "UNIPEC": "SOE_OIL",
    "HUAWEI": "SOE_TELECOM",           "ZTE": "SOE_TELECOM",
    "CHINA TELECOM": "SOE_TELECOM",    "CHINA MOBILE": "SOE_TELECOM",
    "NUCTECH": "SOE_TELECOM",
    "CHINA DEVELOPMENT BANK": "SOE_FINANCE",  "EXIM BANK": "SOE_FINANCE",
    "CDB": "SOE_FINANCE",              "EXIMBANK": "SOE_FINANCE",
    "SILK ROAD FUND": "SOE_FINANCE",   "CHINESE EXIM": "SOE_FINANCE",
    "CHINA EXIM": "SOE_FINANCE",
    "CHINA STATE CONSTRUCTION": "SOE_CONSTRUCT",
    "CHINA ROAD AND BRIDGE": "SOE_CONSTRUCT",
    "CHINALCO": "SOE_MINING",          "CHINA MINMETALS": "SOE_MINING",
    "CITIC": "SOE_MINING",             "TIANQI": "SOE_MINING",
    "BAIC": "SOE_AUTO",                "SAIC": "SOE_AUTO",
    "GEELY": "SOE_AUTO",
    # Genéricos BRI
    "BELT AND ROAD": "SOE_BRI_GENERIC",
    "SILK ROAD": "SOE_BRI_GENERIC",
    "BRI INITIATIVE": "SOE_BRI_GENERIC",
    "CPEC": "SOE_BRI_GENERIC",
    "OBOR": "SOE_BRI_GENERIC",
}

# Temas de inversión/cancelación en V2Themes
INVEST_THEMES = [
    "INVEST", "INFRASTRUCTURE", "LOAN", "DEBT", "CONTRACT", "CONCESSION",
    "CONSTRUCTION", "PORT", "RAILWAY", "PIPELINE", "ENERGY", "MINING",
    "CANCEL", "SUSPEND", "HALT", "REJECT", "SANCTION", "PROTEST",
    "CRISISLEX", "ECON_BANKRUPTCY", "UNGP_FORCED_LABOUR",
]

# ── Función: extraer SOEs de V2Organizations ─────────────────────────────────
def get_soes(orgs_str: str) -> list:
    if not orgs_str or pd.isna(orgs_str):
        return []
    orgs_upper = str(orgs_str).upper()
    found = set()
    for keyword, group in SOE_MAP.items():
        if keyword in orgs_upper:
            found.add(group)
    return sorted(found)


# ── Función: extraer FIPS de LATAM en V2Locations ───────────────────────────
def get_latam_countries(locs_str: str) -> list:
    if not locs_str or pd.isna(locs_str):
        return []
    found = set()
    for part in str(locs_str).split(";"):
        fields = part.split("#")
        if len(fields) >= 4:
            cc = fields[3].strip().upper()
            if cc in LATAM_FIPS:
                found.add(cc)
    return sorted(found)


# ── Función: detectar si hay tema de inversión/cancelación ──────────────────
def has_invest_theme(themes_str: str) -> bool:
    if not themes_str or pd.isna(themes_str):
        return False
    themes_upper = str(themes_str).upper()
    return any(t in themes_upper for t in INVEST_THEMES)


# ── Filtro: SOE + LATAM + tono < -2 ─────────────────────────────────────────
print("\nFiltrando artículos GKG con SOE china + LATAM + tono negativo...")
records = []
for idx, row in gkg.iterrows():
    tone = row.get("tone", 0)
    if tone > -2:
        continue  # solo artículos negativos

    soes = get_soes(row.get("V2Organizations", ""))
    if not soes:
        continue

    countries = get_latam_countries(row.get("V2Locations", ""))
    if not countries:
        continue

    url = str(row.get("DocumentIdentifier", ""))
    year = row.get("year", 0)
    themes = str(row.get("V2Themes", "") or "")

    records.append({
        "year": year,
        "tone": tone,
        "soes": ",".join(soes),
        "countries": ",".join(countries),
        "has_invest_theme": has_invest_theme(themes),
        "source": str(row.get("SourceCommonName", "")),
        "url": url,
        "themes_sample": themes[:200],
        "orgs_sample": str(row.get("V2Organizations", ""))[:200],
    })

df_signals = pd.DataFrame(records)
print(f"Artículos filtrados (SOE + LATAM + tono < -2): {len(df_signals):,}")

# ── Estadísticas básicas ─────────────────────────────────────────────────────
print("\n=== Distribución por SOE ===")
soe_counts = {}
for soes in df_signals["soes"]:
    for s in soes.split(","):
        soe_counts[s] = soe_counts.get(s, 0) + 1
for soe, n in sorted(soe_counts.items(), key=lambda x: -x[1]):
    print(f"  {n:5d}  {soe}")

print("\n=== Distribución por país LATAM ===")
country_counts = {}
for countries in df_signals["countries"]:
    for c in countries.split(","):
        country_counts[c] = country_counts.get(c, 0) + 1
for cc, n in sorted(country_counts.items(), key=lambda x: -x[1]):
    print(f"  {n:5d}  {cc} ({LATAM_FIPS.get(cc, '?')})")

print(f"\n=== Con tema de inversión/cancelación: {df_signals['has_invest_theme'].sum():,} ===")

# ── Deep dive por combinación (país × SOE) ───────────────────────────────────
print("\n=== Top combinaciones País × SOE (artículos más negativos) ===")
combos = []
for _, row in df_signals.iterrows():
    for cc in row["countries"].split(","):
        for soe in row["soes"].split(","):
            combos.append({"cc": cc, "pais": LATAM_FIPS.get(cc, cc),
                           "soe": soe, "year": row["year"],
                           "tone": row["tone"], "url": row["url"]})

df_combos = pd.DataFrame(combos)
combo_stats = df_combos.groupby(["pais", "soe"]).agg(
    n=("url", "count"),
    min_tone=("tone", "min"),
    avg_tone=("tone", "mean"),
    years=("year", lambda x: f"{x.min()}-{x.max()}"),
).sort_values("n", ascending=False)
combo_stats["avg_tone"] = combo_stats["avg_tone"].round(2)
combo_stats["min_tone"] = combo_stats["min_tone"].round(2)
print(combo_stats.head(30).to_string())

# ── Casos clave: Venezuela × SOE_OIL ─────────────────────────────────────────
print("\n=== Venezuela × SOE_OIL — artículos más negativos ===")
ve_oil = df_combos[(df_combos["cc"] == "VE") & (df_combos["soe"] == "SOE_OIL")].drop_duplicates("url")
ve_oil_top = ve_oil.nsmallest(15, "tone")
pd.set_option("display.max_colwidth", 100)
print(ve_oil_top[["year","tone","url"]].to_string(index=False))

print("\n=== Venezuela × SOE_TELECOM — artículos más negativos ===")
ve_tel = df_combos[(df_combos["cc"] == "VE") & (df_combos["soe"] == "SOE_TELECOM")].drop_duplicates("url")
ve_tel_top = ve_tel.nsmallest(10, "tone")
print(ve_tel_top[["year","tone","url"]].to_string(index=False))

print("\n=== Chile × SOE_MINING — artículos más negativos ===")
ci_min = df_combos[(df_combos["cc"] == "CI") & (df_combos["soe"] == "SOE_MINING")].drop_duplicates("url")
ci_min_top = ci_min.nsmallest(10, "tone")
print(ci_min_top[["year","tone","url"]].to_string(index=False))

print("\n=== México × SOE_TELECOM — artículos más negativos ===")
mx_tel = df_combos[(df_combos["cc"] == "MX") & (df_combos["soe"] == "SOE_TELECOM")].drop_duplicates("url")
mx_tel_top = mx_tel.nsmallest(10, "tone")
print(mx_tel_top[["year","tone","url"]].to_string(index=False))

print("\n=== Ecuador × SOE_OIL ===")
ec_oil = df_combos[(df_combos["cc"] == "EC") & (df_combos["soe"] == "SOE_OIL")].drop_duplicates("url")
print(f"  {len(ec_oil)} artículos")
print(ec_oil.nsmallest(10, "tone")[["year","tone","url"]].to_string(index=False))

print("\n=== Perú — todos los SOE ===")
pe_all = df_combos[df_combos["cc"] == "PE"].drop_duplicates("url")
print(f"  {len(pe_all)} artículos, SOEs: {pe_all['soe'].value_counts().to_string()}")
print(pe_all.nsmallest(10, "tone")[["year","soe","tone","url"]].to_string(index=False))

# ── Clustering GKG-LATAM: país + SOE + ventana 1 año ────────────────────────
print("\n=== Clustering GKG LATAM (país × SOE × año) ===")
cluster_rows = []
for _, row in df_combos.iterrows():
    cluster_rows.append({
        "cluster_id": f"{row['cc']}_{row['soe'].replace('SOE_','')[:5]}_{row['year']}",
        "pais": row["pais"],
        "cc": row["cc"],
        "soe": row["soe"],
        "year": row["year"],
        "tone": row["tone"],
        "url": row["url"],
    })

df_clust = pd.DataFrame(cluster_rows)
gkg_clusters = df_clust.groupby("cluster_id").agg(
    pais=("pais", "first"),
    cc=("cc", "first"),
    soe=("soe", "first"),
    year=("year", "first"),
    n_articulos=("url", "nunique"),
    avg_tone=("tone", "mean"),
    min_tone=("tone", "min"),
    url_representativa=("url", lambda x: x.iloc[
        x.reset_index(drop=True).index[
            df_clust.loc[x.index, "tone"].values.argmin()
        ]
    ] if len(x) > 0 else ""),
).sort_values("n_articulos", ascending=False).reset_index()

gkg_clusters["avg_tone"] = gkg_clusters["avg_tone"].round(2)
gkg_clusters["min_tone"] = gkg_clusters["min_tone"].round(2)

# Umbral: al menos 3 artículos
candidatos_gkg = gkg_clusters[gkg_clusters["n_articulos"] >= 3]
print(f"\nTotal clusters GKG-LATAM: {len(gkg_clusters)}")
print(f"Con ≥ 3 artículos: {len(candidatos_gkg)}")

print("\n=== Top 40 candidatos GKG-LATAM ===")
print(candidatos_gkg.head(40)[
    ["cluster_id","pais","soe","year","n_articulos","avg_tone","min_tone","url_representativa"]
].to_string(index=False))

# ── Cruzar con Events para confirmación ─────────────────────────────────────
print("\n=== Candidatos GKG-LATAM con ≥5 artículos (señal fuerte) ===")
strong = candidatos_gkg[candidatos_gkg["n_articulos"] >= 5].copy()
print(strong[["cluster_id","pais","soe","year","n_articulos","avg_tone","min_tone"]].to_string(index=False))

# ── Narrativa de los casos más relevantes ───────────────────────────────────
print("\n=== NARRATIVA: Casos de alta relevancia ===")
for _, row in strong.sort_values("min_tone").head(20).iterrows():
    print(f"\n{'─'*60}")
    print(f"  {row['pais']} × {row['soe']} ({row['year']})")
    print(f"  Artículos: {row['n_articulos']} | tono medio: {row['avg_tone']} | mín: {row['min_tone']}")
    print(f"  URL más negativa: {row['url_representativa'][:100]}")

# ── Guardar ──────────────────────────────────────────────────────────────────
df_signals.to_csv("data/samples/gkg_latam/gkg_latam_soe_signals.csv", index=False)
gkg_clusters.to_csv("data/samples/gkg_latam/gkg_latam_clusters.csv", index=False)
candidatos_gkg.to_csv("data/samples/gkg_latam/gkg_latam_candidatos.csv", index=False)

# Guardar narrativa en markdown
with open("data/samples/gkg_latam/gkg_latam_top_signals.md", "w") as f:
    f.write("# GKG LATAM — Señales de proyectos chinos disrumpidos\n\n")
    f.write(f"Total artículos filtrados (SOE + LATAM + tono < -2): {len(df_signals):,}\n\n")
    f.write("## Candidatos con ≥5 artículos (señal fuerte)\n\n")
    f.write("| Cluster | País | SOE | Año | N artículos | Tono medio | Tono mín |\n")
    f.write("|---------|------|-----|-----|------------|------------|----------|\n")
    for _, row in strong.sort_values("n_articulos", ascending=False).iterrows():
        f.write(f"| {row['cluster_id']} | {row['pais']} | {row['soe']} | {row['year']} | "
                f"{row['n_articulos']} | {row['avg_tone']} | {row['min_tone']} |\n")
    f.write("\n## Detalle por caso clave\n\n")
    for _, row in strong.sort_values("min_tone").head(15).iterrows():
        f.write(f"\n### {row['pais']} × {row['soe']} ({row['year']})\n")
        f.write(f"- Artículos GKG: {row['n_articulos']}\n")
        f.write(f"- Tono medio: {row['avg_tone']} | Tono mínimo: {row['min_tone']}\n")
        f.write(f"- URL representativa: {row['url_representativa']}\n")

print("\n✓ Archivos guardados en data/samples/gkg_latam/")

# ── Actualizar ANALYSIS_FINDINGS.md ─────────────────────────────────────────
with open("docs/ANALYSIS_FINDINGS.md", "a") as f:
    f.write("\n## Script 17 — GKG-LATAM Deep Analysis\n\n")
    f.write(f"### Input: {len(gkg):,} artículos GKG → {len(df_signals):,} con SOE+LATAM+tono<-2\n\n")
    f.write("### Distribución por SOE\n")
    for soe, n in sorted(soe_counts.items(), key=lambda x: -x[1]):
        f.write(f"- `{soe}`: {n} artículos\n")
    f.write("\n### Distribución por país\n")
    for cc, n in sorted(country_counts.items(), key=lambda x: -x[1]):
        f.write(f"- **{LATAM_FIPS.get(cc,cc)}** ({cc}): {n} artículos\n")
    f.write(f"\n### Clusters GKG-LATAM\n")
    f.write(f"- Total: {len(gkg_clusters)} clusters (país × SOE × año)\n")
    f.write(f"- Con ≥3 artículos: {len(candidatos_gkg)}\n")
    f.write(f"- Con ≥5 artículos (señal fuerte): {len(strong)}\n")
    f.write("\n### Señales fuertes (≥5 artículos)\n")
    for _, row in strong.sort_values("n_articulos", ascending=False).head(15).iterrows():
        f.write(f"- **{row['pais']} × {row['soe']} ({row['year']})**: "
                f"{row['n_articulos']} artículos, tono {row['avg_tone']}\n")

print("✓ ANALYSIS_FINDINGS.md actualizado")
print("\n=== SCRIPT 17 COMPLETO ===")
