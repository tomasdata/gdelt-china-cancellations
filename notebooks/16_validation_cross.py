"""
Script 16 — Validación cruzada Events × GKG
Input:
  - data/samples/clusters/project_candidates_events_v2.csv  (309 candidatos)
  - data/samples/gkg_por_año/raw/gkg_china_2017_2024.parquet  (92,990 artículos)

Lógica:
  Para cada cluster de Events:
    1. Buscar artículos GKG con mismo país (V2Locations) + mismo año ± 1
    2. Verificar si V2Organizations del artículo GKG contiene el tipo SOE del cluster
    3. Asignar confidence: "events_only" | "geo_match" | "soe_match" | "high" (geo+soe)

Recall vs casos conocidos:
  - 8 señales reales LATAM identificadas manualmente en sesiones anteriores
  - Cuántas captura el pipeline cruzado?

Output:
  - data/samples/validation/cross_validated_candidates.csv   (309 candidatos con score)
  - data/samples/validation/high_confidence_candidates.csv   (geo+soe match)
  - data/samples/validation/recall_analysis.md
"""

import os
import re
import pandas as pd
import numpy as np

os.makedirs("data/samples/validation", exist_ok=True)

# ── Cargar datos ─────────────────────────────────────────────────────────────
print("Cargando datos...")
cand = pd.read_csv("data/samples/clusters/project_candidates_events_v2.csv")
gkg = pd.read_parquet("data/samples/gkg_por_año/raw/gkg_china_2017_2024.parquet")

print(f"Candidatos Events v2: {len(cand):,}")
print(f"Artículos GKG: {len(gkg):,}")

gkg["year"] = gkg["DATE"].astype(str).str[:4].astype(int, errors="ignore")
gkg["tone"] = gkg["V2Tone"].str.split(",").str[0].astype(float, errors="ignore")

# ── Mapeo SOE para GKG ───────────────────────────────────────────────────────
GKG_SOE_KEYWORDS = {
    "SOE_RAILWAY":   ["CHINA RAILWAY","CRRC","CR GROUP","RAILWAY CONSTRUCTION"],
    "SOE_MARITIME":  ["COSCO","CHINA OCEAN SHIPPING","CHINA COSCO"],
    "SOE_HARBOUR":   ["CHINA HARBOUR","CHINA COMMUNICATIONS CONSTRUCTION","CCCC","CHEC"],
    "SOE_ENERGY":    ["SINOHYDRO","POWERCHINA","THREE GORGES","GEZHOUBA","CHINA ENERGY"],
    "SOE_OIL":       ["CNPC","PETROCHINA","SINOPEC","CNOOC","CHINA NATIONAL PETROLEUM",
                      "UNIPEC","CHINA OIL"],
    "SOE_TELECOM":   ["HUAWEI","ZTE","CHINA TELECOM","CHINA MOBILE","NUCTECH"],
    "SOE_FINANCE":   ["CHINA DEVELOPMENT BANK","EXIM BANK","CDB","EXIMBANK",
                      "SILK ROAD FUND","CHINESE EXIM","CHINA EXIM"],
    "SOE_CONSTRUCT": ["CHINA STATE CONSTRUCTION","CHINA ROAD AND BRIDGE","CHINA OVERSEAS"],
    "SOE_MINING":    ["CHINALCO","CHINA MINMETALS","CITIC"],
    "SOE_GENERIC":   ["BELT AND ROAD","SILK ROAD","BRI INITIATIVE","CPEC","OBOR"],
}


def has_soe_in_gkg(v2orgs_str: str, soe_type: str) -> bool:
    """Check if V2Organizations contains a keyword matching the SOE type."""
    if not v2orgs_str or pd.isna(v2orgs_str):
        return False
    orgs_upper = str(v2orgs_str).upper()
    keywords = GKG_SOE_KEYWORDS.get(soe_type, [])
    return any(kw in orgs_upper for kw in keywords)


# ── Parsear V2Locations para extraer country codes ───────────────────────────
def extract_country_codes(v2locs_str: str) -> set:
    """Extract 2-char FIPS country codes from V2Locations field."""
    if not v2locs_str or pd.isna(v2locs_str):
        return set()
    codes = set()
    for part in str(v2locs_str).split(";"):
        fields = part.split("#")
        if len(fields) >= 4:
            cc = fields[3].strip()
            if len(cc) == 2 and cc.isalpha():
                codes.add(cc.upper())
    return codes


# Pre-computar country codes de GKG (costoso pero necesario)
print("\nPre-computando country codes en GKG...")
gkg["countries"] = gkg["V2Locations"].apply(extract_country_codes)
print("OK")

# ── Función de validación cruzada para un cluster ───────────────────────────
def cross_validate_cluster(cluster: dict, gkg_df: pd.DataFrame) -> dict:
    """
    Buscar en GKG artículos que confirmen el cluster.
    Returns dict con confidence, n_gkg_geo, n_gkg_soe, best_url_gkg.
    """
    pais_code = cluster["pais"]
    year = int(cluster["year"])
    actor_norm = str(cluster.get("actor_norm", ""))
    years_window = {year - 1, year, year + 1}

    # Filtrar GKG por año ± 1
    gkg_year = gkg_df[gkg_df["year"].isin(years_window)]

    # Paso 1: geo match (mismo país en V2Locations)
    geo_mask = gkg_year["countries"].apply(lambda c: pais_code in c)
    gkg_geo = gkg_year[geo_mask]
    n_geo = len(gkg_geo)

    # Paso 2: SOE match (V2Organizations contiene el tipo de SOE)
    if actor_norm.startswith("SOE_") and n_geo > 0:
        soe_mask = gkg_geo["V2Organizations"].apply(
            lambda o: has_soe_in_gkg(o, actor_norm)
        )
        gkg_soe = gkg_geo[soe_mask]
    else:
        gkg_soe = pd.DataFrame()

    n_soe = len(gkg_soe)

    # Determinar confidence
    if n_soe > 0:
        confidence = "high"
        best_url = gkg_soe.nsmallest(1, "tone")["DocumentIdentifier"].values[0] if len(gkg_soe) > 0 else ""
        best_tone_gkg = gkg_soe["tone"].min()
    elif n_geo > 0:
        confidence = "geo_match"
        best_url = gkg_geo.nsmallest(1, "tone")["DocumentIdentifier"].values[0] if len(gkg_geo) > 0 else ""
        best_tone_gkg = gkg_geo["tone"].min()
    else:
        confidence = "events_only"
        best_url = ""
        best_tone_gkg = np.nan

    return {
        "n_gkg_geo": n_geo,
        "n_gkg_soe": n_soe,
        "confidence": confidence,
        "best_url_gkg": best_url,
        "best_tone_gkg": round(float(best_tone_gkg), 2) if not np.isnan(best_tone_gkg) else np.nan,
    }


# ── Validación cruzada de todos los candidatos ───────────────────────────────
print(f"\nValidando cruzado {len(cand)} clusters...")
results = []
for i, (_, row) in enumerate(cand.iterrows()):
    if i % 50 == 0:
        print(f"  Procesando {i}/{len(cand)}...")
    cv = cross_validate_cluster(row.to_dict(), gkg)
    results.append(cv)

df_cv = pd.DataFrame(results)
cand_val = pd.concat([cand.reset_index(drop=True), df_cv], axis=1)

# ── Resumen de validación ────────────────────────────────────────────────────
print("\n=== Resumen de validación cruzada ===")
conf_dist = cand_val["confidence"].value_counts()
print(conf_dist.to_string())
print(f"\n  Total candidatos: {len(cand_val)}")
print(f"  Confirmados (high confidence = geo+SOE): {(cand_val['confidence']=='high').sum()}")
print(f"  Geo match solamente: {(cand_val['confidence']=='geo_match').sum()}")
print(f"  Events only (sin GKG): {(cand_val['confidence']=='events_only').sum()}")

# ── High confidence candidatos ───────────────────────────────────────────────
high_conf = cand_val[cand_val["confidence"] == "high"].sort_values("relevancia", ascending=False)
print(f"\n=== {len(high_conf)} candidatos de alta confianza (Events + GKG SOE match) ===")
pd.set_option("display.max_colwidth", 90)
print(high_conf[[
    "cluster_id", "pais_nombre", "region", "actor_norm", "year",
    "n_eventos", "tono_medio", "n_gkg_soe", "mechanism_dominante",
    "geo_fullname", "best_url_gkg"
]].head(30).to_string(index=False))

# ── LATAM validados ─────────────────────────────────────────────────────────
print("\n=== LATAM — candidatos validados ===")
latam_val = cand_val[cand_val["region"] == "LATAM"].sort_values("confidence")
print(latam_val[[
    "cluster_id", "pais_nombre", "actor_norm", "year", "n_eventos",
    "tono_medio", "confidence", "n_gkg_geo", "n_gkg_soe",
    "mechanism_dominante", "best_url_gkg"
]].to_string(index=False))

# ── Recall vs casos conocidos ────────────────────────────────────────────────
print("\n=== Recall vs señales reales conocidas ===")

# 8 señales reales LATAM identificadas manualmente
KNOWN_SIGNALS = [
    {"pais": "CI", "year_range": [2018, 2019], "caso": "Chile SQM — venta acciones a Tianqi Lithium",
     "actor_hint": "MINING"},
    {"pais": "EC", "year_range": [2017, 2019], "caso": "Ecuador — camarón/pesca suspensión China",
     "actor_hint": None},
    {"pais": "VE", "year_range": [2018, 2020], "caso": "Venezuela ZTE — vigilancia (sanciones EEUU)",
     "actor_hint": "TELECOM"},
    {"pais": "VE", "year_range": [2018, 2019], "caso": "Venezuela Unipec — ban tanqueros petroleros",
     "actor_hint": "OIL"},
    {"pais": "VE", "year_range": [2019, 2020], "caso": "Venezuela CNPC — suspensión operaciones",
     "actor_hint": "OIL"},
    {"pais": "VE", "year_range": [2020, 2021], "caso": "Venezuela empresa china internet ban (US sanctions)",
     "actor_hint": None},
    {"pais": "BR", "year_range": [2017, 2019], "caso": "Brasil Tamoios — autopista concesión China",
     "actor_hint": None},
    {"pais": "JM", "year_range": [2022, 2023], "caso": "Jamaica CHEC — ataque complejo portuario",
     "actor_hint": "HARBOUR"},
]

recall_hits = 0
for signal in KNOWN_SIGNALS:
    # Buscar en candidatos validados
    matches = cand_val[
        (cand_val["pais"] == signal["pais"]) &
        (cand_val["year"].between(signal["year_range"][0], signal["year_range"][1]))
    ]
    hit_conf = "NO_MATCH"
    if len(matches) > 0:
        best = matches.sort_values("confidence").iloc[-1]  # high > geo_match > events_only
        hit_conf = best["confidence"]
        recall_hits += 1

    status = "✓" if len(matches) > 0 else "✗"
    print(f"  {status} [{signal['pais']}/{signal['year_range']}] {signal['caso']}")
    if len(matches) > 0:
        print(f"      → {len(matches)} cluster(s) encontrados, conf={hit_conf}")

recall_pct = recall_hits / len(KNOWN_SIGNALS) * 100
print(f"\nRecall: {recall_hits}/{len(KNOWN_SIGNALS)} casos conocidos ({recall_pct:.0f}%)")

# ── Guardar outputs ──────────────────────────────────────────────────────────
cand_val.to_csv("data/samples/validation/cross_validated_candidates.csv", index=False)
high_conf.to_csv("data/samples/validation/high_confidence_candidates.csv", index=False)

# Guardar análisis de recall
recall_md = f"""# Recall Analysis — Pipeline Events × GKG

## Total candidatos: {len(cand_val)}

## Confidence distribution
{conf_dist.to_string()}

## Recall vs señales conocidas: {recall_hits}/{len(KNOWN_SIGNALS)} ({recall_pct:.0f}%)

### Señales conocidas buscadas:
"""
for signal in KNOWN_SIGNALS:
    matches = cand_val[
        (cand_val["pais"] == signal["pais"]) &
        (cand_val["year"].between(signal["year_range"][0], signal["year_range"][1]))
    ]
    status = "FOUND" if len(matches) > 0 else "MISSING"
    recall_md += f"\n- [{status}] {signal['caso']} ({signal['pais']}, {signal['year_range']})"

with open("data/samples/validation/recall_analysis.md", "w") as f:
    f.write(recall_md)

print("\n✓ Archivos guardados en data/samples/validation/")

# ── Actualizar ANALYSIS_FINDINGS.md ─────────────────────────────────────────
with open("docs/ANALYSIS_FINDINGS.md", "a") as f:
    f.write("\n## Script 16 — Validación cruzada Events × GKG\n\n")
    f.write("### Confidence distribution\n")
    for conf_level, n in conf_dist.items():
        f.write(f"- `{conf_level}`: {n} candidatos ({n/len(cand_val)*100:.1f}%)\n")
    f.write(f"\n### Recall vs señales conocidas: {recall_hits}/{len(KNOWN_SIGNALS)} ({recall_pct:.0f}%)\n")
    f.write(f"\n### High confidence candidatos globales: {len(high_conf)}\n")
    if len(high_conf) > 0:
        top5 = high_conf.head(5)
        for _, r in top5.iterrows():
            f.write(f"- {r['pais_nombre']} / {r['actor_norm']} ({r['year']}): "
                    f"{r['n_eventos']} eventos, {r['n_gkg_soe']} artículos GKG\n")
    f.write("\n### Conclusión pipeline\n")
    f.write("- Pipeline Events → clustering → GKG cross-validation operativo\n")
    f.write(f"- De 309 candidatos Events, {(conf_dist.get('high',0)+conf_dist.get('geo_match',0))} tienen confirmación GKG\n")
    f.write(f"- {len(high_conf)} casos con confirmación SOE específica en GKG\n")

print("✓ ANALYSIS_FINDINGS.md actualizado")
print("\n=== SCRIPT 16 COMPLETO ===")
print("\n=== PIPELINE COMPLETO: Scripts 07→09→10→12→14→15→16 ===")
