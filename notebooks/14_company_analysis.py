"""
Script 14 — Análisis por empresa china (SOE)
Input:
  - data/samples/clusters/project_candidates_events_v2.csv
  - data/samples/gkg_por_año/raw/gkg_china_2017_2024.parquet

Pregunta: ¿Qué empresas chinas tienen más proyectos disrumpidos/cancelados?
¿Qué sectores tienen más riesgo? ¿En qué regiones?

Output:
  - data/samples/companies/soe_risk_profile.csv   (perfil de riesgo por SOE)
  - data/samples/companies/soe_by_region.csv      (SOE × región)
  - data/samples/companies/soe_by_year.csv        (SOE × año)
  - data/samples/companies/gkg_org_ranking.csv    (ranking de orgs en GKG)
"""

import os
import re
import pandas as pd
import numpy as np

os.makedirs("data/samples/companies", exist_ok=True)

# ── Parte A: Análisis desde Events (project_candidates_v2) ──────────────────
print("=" * 60)
print("PARTE A: SOE desde Events (project_candidates_v2)")
print("=" * 60)

cand = pd.read_csv("data/samples/clusters/project_candidates_events_v2.csv")
print(f"Input clusters: {len(cand):,} proyectos candidatos")

# Grupos SOE detectados (del script 12 v2)
SOE_GROUPS = {
    "SOE_RAILWAY":   ["CHINA RAILWAY", "CRRC", "CR GROUP"],
    "SOE_MARITIME":  ["COSCO", "CHINA OCEAN SHIPPING"],
    "SOE_HARBOUR":   ["CHINA HARBOUR", "CHINA COMMUNICATIONS", "CCCC"],
    "SOE_ENERGY":    ["SINOHYDRO", "POWERCHINA", "THREE GORGES", "GEZHOUBA", "CHINA ENERGY"],
    "SOE_OIL":       ["CNPC", "PETROCHINA", "SINOPEC", "CNOOC", "CHINA NATIONAL PETROLEUM"],
    "SOE_TELECOM":   ["HUAWEI", "ZTE", "CHINA TELECOM", "CHINA MOBILE"],
    "SOE_FINANCE":   ["CHINA DEVELOPMENT BANK", "EXIM BANK", "CDB", "EXIMBANK", "SILK ROAD FUND"],
    "SOE_CONSTRUCT": ["CHINA STATE CONSTRUCTION", "CHINA ROAD AND BRIDGE", "CHINA OVERSEAS"],
    "SOE_MINING":    ["CHINALCO", "CHINA MINMETALS", "CITIC"],
}

soe_cand = cand[cand["actor_norm"].str.startswith("SOE_", na=False)]
print(f"Clusters con SOE identificada: {len(soe_cand)} / {len(cand)}")

if len(soe_cand) > 0:
    soe_events_profile = soe_cand.groupby("actor_norm").agg(
        n_clusters=("cluster_id", "count"),
        n_paises=("pais", "nunique"),
        avg_tone=("tono_medio", "mean"),
        total_relevancia=("relevancia", "sum"),
        menciones_total=("menciones_total", "sum"),
        top_mechanism=("mechanism_dominante", lambda x: x.value_counts().index[0]),
    ).sort_values("n_clusters", ascending=False)
    soe_events_profile["avg_tone"] = soe_events_profile["avg_tone"].round(2)
    print("\n=== SOEs identificadas en Events ===")
    print(soe_events_profile.to_string())

# ── Parte B: Análisis desde GKG (organizaciones en artículos) ───────────────
print("\n" + "=" * 60)
print("PARTE B: Organizaciones chinas en GKG")
print("=" * 60)

gkg = pd.read_parquet("data/samples/gkg_por_año/raw/gkg_china_2017_2024.parquet")
print(f"GKG artículos: {len(gkg):,}")
print(f"Columnas GKG: {list(gkg.columns)}")

# Extraer organizaciones del campo V2Organizations (formato: "ORG,offset;ORG2,offset2")
def extract_orgs(v2orgs_str: str) -> list:
    if not v2orgs_str or pd.isna(v2orgs_str):
        return []
    orgs = []
    for part in str(v2orgs_str).split(";"):
        name = part.split(",")[0].strip()
        if name:
            orgs.append(name.upper())
    return orgs


# Mapeo de nombres GKG a grupos SOE
GKG_SOE_MAP = {
    # RAILWAY
    "CHINA RAILWAY": "SOE_RAILWAY",
    "CRRC": "SOE_RAILWAY",
    # MARITIME
    "COSCO": "SOE_MARITIME",
    "CHINA OCEAN SHIPPING": "SOE_MARITIME",
    "CHINA COSCO": "SOE_MARITIME",
    # HARBOUR / CONSTRUCTION
    "CHINA HARBOUR": "SOE_HARBOUR",
    "CHINA COMMUNICATIONS": "SOE_HARBOUR",
    "CCCC": "SOE_HARBOUR",
    "CHINA ROAD AND BRIDGE": "SOE_CONSTRUCT",
    "CHINA STATE CONSTRUCTION": "SOE_CONSTRUCT",
    # ENERGY
    "SINOHYDRO": "SOE_ENERGY",
    "POWERCHINA": "SOE_ENERGY",
    "THREE GORGES": "SOE_ENERGY",
    "CHINA THREE GORGES": "SOE_ENERGY",
    "GEZHOUBA": "SOE_ENERGY",
    "CHINA ENERGY": "SOE_ENERGY",
    # OIL
    "CNPC": "SOE_OIL",
    "PETROCHINA": "SOE_OIL",
    "SINOPEC": "SOE_OIL",
    "CNOOC": "SOE_OIL",
    "CHINA NATIONAL PETROLEUM": "SOE_OIL",
    "UNIPEC": "SOE_OIL",
    # TELECOM
    "HUAWEI": "SOE_TELECOM",
    "ZTE": "SOE_TELECOM",
    "CHINA TELECOM": "SOE_TELECOM",
    "CHINA MOBILE": "SOE_TELECOM",
    "NUCTECH": "SOE_TELECOM",
    # FINANCE
    "CHINA DEVELOPMENT BANK": "SOE_FINANCE",
    "EXIM BANK": "SOE_FINANCE",
    "CDB": "SOE_FINANCE",
    "EXIMBANK": "SOE_FINANCE",
    "SILK ROAD FUND": "SOE_FINANCE",
    "CHINESE EXIM BANK": "SOE_FINANCE",
    "CHINA EXIM BANK": "SOE_FINANCE",
    # MINING
    "CHINALCO": "SOE_MINING",
    "CHINA MINMETALS": "SOE_MINING",
    "CITIC": "SOE_MINING",
    "CITIC BANK": "SOE_MINING",
}

# Extraer año del campo DATE (14-digit YYYYMMDDHHMMSS)
gkg["year"] = gkg["DATE"].astype(str).str[:4].astype(int, errors="ignore")
gkg["tone"] = gkg["V2Tone"].str.split(",").str[0].astype(float, errors="ignore")

# Procesar V2Organizations para detectar SOEs
print("\nProcesando V2Organizations para detectar SOEs...")
org_records = []

for idx, row in gkg.iterrows():
    orgs = extract_orgs(row.get("V2Organizations", ""))
    tone = row.get("tone", 0)
    year = row.get("year", 0)
    url = str(row.get("DocumentIdentifier", ""))

    # Detectar cuáles son SOEs chinas
    soe_in_article = set()
    raw_orgs_in_article = []
    for org in orgs:
        # Match por substring
        for key, group in GKG_SOE_MAP.items():
            if key in org:
                soe_in_article.add(group)
                raw_orgs_in_article.append(f"{org}→{group}")

    for soe_group in soe_in_article:
        org_records.append({
            "soe_group": soe_group,
            "year": year,
            "tone": tone,
            "url": url,
        })

df_orgs = pd.DataFrame(org_records)
print(f"Registros SOE detectados: {len(df_orgs):,} (en {df_orgs['url'].nunique():,} artículos únicos)")

if len(df_orgs) == 0:
    print("⚠️  Sin SOEs detectadas en GKG — revisar formato de V2Organizations")
    # Muestra del campo
    sample_orgs = gkg["V2Organizations"].dropna().head(5)
    print("Sample V2Organizations:")
    for s in sample_orgs:
        print(f"  {str(s)[:200]}")
else:
    # ── Ranking global de SOEs en GKG ──────────────────────────────────────
    gkg_ranking = df_orgs.groupby("soe_group").agg(
        n_articulos=("url", "count"),
        n_articulos_unicos=("url", "nunique"),
        avg_tone=("tone", "mean"),
        min_tone=("tone", "min"),
    ).sort_values("n_articulos", ascending=False)
    gkg_ranking["avg_tone"] = gkg_ranking["avg_tone"].round(2)
    gkg_ranking["min_tone"] = gkg_ranking["min_tone"].round(2)

    print("\n=== Ranking SOE en GKG (artículos con tono negativo) ===")
    print(gkg_ranking.to_string())

    # ── SOE × año ──────────────────────────────────────────────────────────
    soe_year = df_orgs.groupby(["soe_group", "year"]).size().unstack(fill_value=0)
    print("\n=== SOE × año (conteo artículos) ===")
    print(soe_year.to_string())

    # ── Artículos más negativos por SOE ────────────────────────────────────
    print("\n=== Artículos más negativos por SOE (top 3 cada una) ===")
    for soe in gkg_ranking.head(8).index:
        top_neg = df_orgs[df_orgs["soe_group"] == soe].nsmallest(3, "tone")
        print(f"\n  {soe}:")
        for _, r in top_neg.iterrows():
            print(f"    year={r['year']} tone={r['tone']:.1f} → {r['url'][:120]}")

    # ── Artículos GKG con V2Locations LATAM ────────────────────────────────
    LATAM_FIPS = {"CI","AR","BR","MX","PE","CO","VE","BL","EC","UY","PA","PM",
                  "CU","GT","NU","ES","HO","BH","DR","GY","NS","CS","JM","HA"}

    gkg_latam_rows = []
    for idx, row in gkg.iterrows():
        locs = str(row.get("V2Locations", "") or "")
        countries_in_locs = set(re.findall(r'(?<=#)(\w{2})(?=#)', locs))
        # V2Locations format: type#fullname#...#countrycode#...
        # Simpler: extract 2-char codes appearing after # separator
        fips_found = set()
        for part in locs.split(";"):
            fields = part.split("#")
            if len(fields) >= 4:
                cc = fields[3].strip()
                if cc in LATAM_FIPS:
                    fips_found.add(cc)
        if fips_found:
            orgs_in_row = extract_orgs(row.get("V2Organizations", ""))
            soes = set()
            for org in orgs_in_row:
                for key, group in GKG_SOE_MAP.items():
                    if key in org:
                        soes.add(group)
            if soes:
                gkg_latam_rows.append({
                    "year": row.get("year", 0),
                    "tone": row.get("tone", 0),
                    "soes": ",".join(sorted(soes)),
                    "fips": ",".join(sorted(fips_found)),
                    "url": str(row.get("DocumentIdentifier", "")),
                })

    df_gkg_latam = pd.DataFrame(gkg_latam_rows)
    print(f"\n=== GKG artículos con SOE china + ubicación LATAM: {len(df_gkg_latam)} ===")
    if len(df_gkg_latam) > 0:
        print(df_gkg_latam.groupby(["fips", "soes"]).size().sort_values(ascending=False).head(20).to_string())
        print("\n--- Artículos más negativos LATAM × SOE ---")
        print(df_gkg_latam.nsmallest(15, "tone")[
            ["year", "tone", "soes", "fips", "url"]
        ].to_string(index=False))

    # ── Guardar ────────────────────────────────────────────────────────────
    gkg_ranking.to_csv("data/samples/companies/soe_risk_profile.csv")
    soe_year.to_csv("data/samples/companies/soe_by_year.csv")
    if len(df_gkg_latam) > 0:
        df_gkg_latam.to_csv("data/samples/companies/gkg_latam_soe.csv", index=False)
    print("\n✓ Archivos guardados en data/samples/companies/")

# ── Parte C: Raw org frequency en GKG (top orgs mencionadas) ────────────────
print("\n" + "=" * 60)
print("PARTE C: Frecuencia de organizaciones en GKG (raw)")
print("=" * 60)

org_counter = {}
for orgs_str in gkg["V2Organizations"].dropna():
    for part in str(orgs_str).split(";"):
        name = part.split(",")[0].strip().upper()
        if len(name) > 3:  # filtrar códigos cortos
            org_counter[name] = org_counter.get(name, 0) + 1

# Filtrar solo orgs con palabras clave chinas
chinese_orgs = {k: v for k, v in org_counter.items()
                if any(kw in k for kw in ["CHINA", "CHINESE", "SINO", "HUAWEI", "COSCO",
                                           "CRRC", "ZTE", "CNPC", "SINOPEC", "CNOOC",
                                           "POWERCHINA", "SINOHYDRO", "EXIM"])}
top_chinese_orgs = sorted(chinese_orgs.items(), key=lambda x: -x[1])[:50]

print("\n=== Top 50 orgs chinas en GKG (por frecuencia) ===")
for org, cnt in top_chinese_orgs:
    print(f"  {cnt:5d}  {org}")

# Guardar ranking
org_df = pd.DataFrame(top_chinese_orgs, columns=["org_name", "n_articulos"])
org_df.to_csv("data/samples/companies/gkg_org_ranking.csv", index=False)
print("\n✓ gkg_org_ranking.csv guardado")

# ── Actualizar ANALYSIS_FINDINGS.md ────────────────────────────────────────
with open("docs/ANALYSIS_FINDINGS.md", "a") as f:
    f.write("\n## Script 14 — Análisis por empresa SOE china\n\n")
    f.write("### Fuentes analizadas\n")
    f.write(f"- Events clusters v2: {len(cand):,} candidatos\n")
    f.write(f"- GKG artículos: {len(gkg):,} artículos 2017-2024\n\n")
    f.write("### SOEs en Events\n")
    if len(soe_cand) > 0:
        for soe, row in soe_events_profile.iterrows():
            f.write(f"- **{soe}**: {int(row['n_clusters'])} clusters, "
                    f"{int(row['n_paises'])} países, tono {row['avg_tone']:.2f}\n")
    else:
        f.write("- Sin SOEs específicas identificadas en Events data (actors son host-country)\n")
    if len(df_orgs) > 0:
        f.write("\n### SOEs en GKG (artículos con tono negativo)\n")
        for soe, row in gkg_ranking.iterrows():
            f.write(f"- **{soe}**: {int(row['n_articulos_unicos'])} artículos únicos, "
                    f"tono medio {row['avg_tone']:.2f}, mín {row['min_tone']:.2f}\n")
    f.write("\n### Top orgs chinas mencionadas en GKG\n")
    for org, cnt in top_chinese_orgs[:15]:
        f.write(f"- `{org}`: {cnt} artículos\n")
    f.write("\n### Próximo paso\n")
    f.write("- Script 15: análisis causal de mecanismos\n")
    f.write("- Script 16: validación cruzada Events × GKG\n")

print("\n✓ ANALYSIS_FINDINGS.md actualizado")
print("\n=== SCRIPT 14 COMPLETO ===")
