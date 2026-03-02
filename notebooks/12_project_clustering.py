"""
Script 12 v2 — Clustering de proyectos candidatos (actor-aware)
Input: data/samples/geo/bri_events_geo.csv

v2 mejoras vs v1:
  - Clustering por (país + actor_norm) — ya no mezcla CRRC con COSCO en el mismo cluster
  - Ventana de 180 días (antes 90) con gap-reopen: si silencio > 180 días, nuevo cluster
  - Fórmula de relevancia ponderada: n_eventos × log(menciones) × |tono| (antes: n×menciones)
  - Umbral mínimo: 2 eventos para SOEs específicas, 3 para actores genéricos
  - Columna 'mechanism' por cluster (la más frecuente de las filas)
  - Output: project_candidates_events_v2.csv (mantiene v1 para comparación)
"""

import os
import re
import numpy as np
import pandas as pd
from collections import Counter

df = pd.read_csv("data/samples/geo/bri_events_geo.csv")
df["year"] = df["SQLDATE"] // 10000
print(f"Input: {len(df):,} eventos BRI geo")

# ── Paso 1: Filtro URL estricto ─────────────────────────────────────────────
INVEST_KEYWORDS = [
    "invest", "project", "infrastructure", "port", "railway", "dam", "pipeline",
    "power.plant", "power-plant", "powerplant", "energy", "telecom", "fiber",
    "bridge", "road", "highway", "airport", "stadium", "hospital",
    "belt.road", "belt-road", "bri", "silk.road", "silk-road",
    "obor", "cpec", "loan", "debt", "cancel", "halt", "suspend", "withdraw",
    "block", "reject", "ban", "scrap", "abandon", "terminate", "freeze",
    "chinese.firm", "chinese-firm", "chinese.company", "state-owned",
    "soe", "exim", "cdb", "china.develop", "silk", "corridor",
    "concession", "contract", "construction", "mining", "refinery", "terminal",
]


def has_invest_keyword(url: str) -> bool:
    url = str(url).lower()
    return any(re.search(kw, url) for kw in INVEST_KEYWORDS)


df["url_relevant"] = df["SOURCEURL"].apply(has_invest_keyword)
df_filtered = df[df["url_relevant"] & ~df["ActionGeo_CountryCode"].isin(["CH", "US", "HK"])].copy()
print(f"\nPost-filtro URL + excl. China/EEUU/HK: {len(df_filtered):,} eventos")

# ── Paso 2: Normalizar actores chinos ────────────────────────────────────────
SOE_GROUPS = {
    "RAILWAY":   ["CHINA RAILWAY", "CRRC", "CR GROUP"],
    "MARITIME":  ["COSCO", "CHINA OCEAN SHIPPING"],
    "HARBOUR":   ["CHINA HARBOUR", "CHINA COMMUNICATIONS", "CCCC"],
    "ENERGY":    ["SINOHYDRO", "POWERCHINA", "THREE GORGES", "GEZHOUBA", "CHINA ENERGY"],
    "OIL":       ["CNPC", "PETROCHINA", "SINOPEC", "CNOOC", "CHINA NATIONAL PETROLEUM"],
    "TELECOM":   ["HUAWEI", "ZTE", "CHINA TELECOM", "CHINA MOBILE"],
    "FINANCE":   ["CHINA DEVELOPMENT BANK", "EXIM BANK", "CDB", "EXIMBANK", "SILK ROAD FUND"],
    "CONSTRUCT": ["CHINA STATE CONSTRUCTION", "CHINA ROAD AND BRIDGE", "CHINA OVERSEAS"],
    "MINING":    ["CHINALCO", "CHINA MINMETALS", "CITIC"],
}


def normalize_actor(name: str) -> str:
    name = str(name or "").upper()
    for group, keywords in SOE_GROUPS.items():
        if any(kw in name for kw in keywords):
            return f"SOE_{group}"
    if "CHINA" in name or "CHINESE" in name or "SINO" in name:
        return "SOE_GENERIC"
    return name[:25] if name.strip() else "UNKNOWN"


df_filtered["actor_norm"] = df_filtered["Actor1Name"].apply(normalize_actor)
# Si actor1 es genérico, intentar con actor2
mask_generic = df_filtered["actor_norm"].isin(["SOE_GENERIC", "UNKNOWN"])
df_filtered.loc[mask_generic, "actor_norm"] = \
    df_filtered.loc[mask_generic, "Actor2Name"].apply(normalize_actor)

print("\n=== Distribución de actor_norm ===")
print(df_filtered["actor_norm"].value_counts().head(15).to_string())

# ── Paso 3: Distribución post-filtro ────────────────────────────────────────
print("\n=== Top 20 países post-filtro estricto ===")
top = df_filtered.groupby("pais").agg(
    n=("SOURCEURL", "count"),
    tono=("AvgTone", "mean"),
    menciones=("NumMentions", "sum")
).sort_values("n", ascending=False).head(20)
top["tono"] = top["tono"].round(2)
print(top.to_string())

# ── Paso 4: Clustering por (país + actor_norm + ventana 180 días con gap) ───
print("\n=== Clustering actor-aware (ventana 180 días, gap-reopen) ===")
df_filtered = df_filtered.sort_values("SQLDATE")
df_filtered["fecha"] = pd.to_datetime(
    df_filtered["SQLDATE"].astype(str), format="%Y%m%d", errors="coerce"
)

clusters = []
for (pais, actor_norm), group in df_filtered.groupby(["ActionGeo_CountryCode", "actor_norm"]):
    group = group.sort_values("fecha").reset_index(drop=True)
    cluster_id = 0
    cluster_start = None
    cluster_last = None

    for _, row in group.iterrows():
        gap_days = (row["fecha"] - cluster_last).days if cluster_last is not None else 9999
        # Nueva cluster si: primera vez o gap > 180 días
        if cluster_start is None or gap_days > 180:
            cluster_id += 1
            cluster_start = row["fecha"]
        cluster_last = row["fecha"]

        clusters.append({
            "cluster_id": f"{pais}_{actor_norm[:8]}_{cluster_id:03d}",
            "pais": pais,
            "pais_nombre": row["pais"],
            "region": row["region"],
            "actor_norm": actor_norm,
            "fecha": row["fecha"],
            "SQLDATE": row["SQLDATE"],
            "year": row["year"],
            "Actor1Name": row.get("Actor1Name", ""),
            "Actor2Name": row.get("Actor2Name", ""),
            "AvgTone": row["AvgTone"],
            "NumMentions": row.get("NumMentions", 1),
            "mechanism": row.get("mechanism", "unknown"),
            "SOURCEURL": row["SOURCEURL"],
            "ActionGeo_FullName": row.get("ActionGeo_FullName", ""),
        })

df_clusters = pd.DataFrame(clusters)

# ── Paso 5: Agregar por cluster ─────────────────────────────────────────────
cluster_agg = df_clusters.groupby("cluster_id").agg(
    pais=("pais", "first"),
    pais_nombre=("pais_nombre", "first"),
    region=("region", "first"),
    actor_norm=("actor_norm", "first"),
    year=("year", "first"),
    fecha_inicio=("fecha", "min"),
    fecha_fin=("fecha", "max"),
    n_eventos=("SQLDATE", "count"),
    tono_medio=("AvgTone", "mean"),
    menciones_total=("NumMentions", "sum"),
    url_representativa=("SOURCEURL", "first"),
    actor1_mas_frecuente=("Actor1Name",
                          lambda x: x.dropna().value_counts().index[0]
                          if len(x.dropna()) > 0 else ""),
    geo_fullname=("ActionGeo_FullName", "first"),
    mechanism_dominante=("mechanism",
                         lambda x: x.value_counts().index[0]
                         if len(x) > 0 else "unknown"),
).reset_index()

cluster_agg["tono_medio"] = cluster_agg["tono_medio"].round(2)
cluster_agg["duracion_dias"] = (cluster_agg["fecha_fin"] - cluster_agg["fecha_inicio"]).dt.days

# ── Paso 6: Fórmula de relevancia mejorada (ponderada por tono) ─────────────
# v1: n_eventos × menciones_total  →  sesgada hacia eventos con muchas menciones
# v2: n_eventos × log(menciones+1) × |tono|  →  tono negativo importa más
cluster_agg["tono_abs"] = cluster_agg["tono_medio"].clip(upper=-1).abs()
cluster_agg["relevancia"] = (
    cluster_agg["n_eventos"]
    * np.log1p(cluster_agg["menciones_total"])
    * cluster_agg["tono_abs"]
).round(2)

# ── Paso 7: Candidatos con umbral diferenciado ──────────────────────────────
# SOEs específicas: umbral 2 eventos (señal más precisa)
# Actores genéricos: umbral 3 eventos (más ruido esperado)
specific_soes = cluster_agg["actor_norm"].str.startswith("SOE_") & \
                (cluster_agg["actor_norm"] != "SOE_GENERIC")

candidatos = cluster_agg[
    (cluster_agg["n_eventos"] >= 3) |  # 3+ para cualquier actor
    (specific_soes & (cluster_agg["n_eventos"] >= 2))  # 2+ para SOE específica
].sort_values("relevancia", ascending=False)

print(f"\nClusters con umbral cumplido: {len(candidatos):,} proyectos candidatos")
print(f"  SOEs específicas (≥2 eventos): {specific_soes.sum():,} clusters totales")
print(f"Distribución por n_eventos:")
print(candidatos["n_eventos"].value_counts().sort_index().head(10).to_string())

print("\n=== Top 40 proyectos candidatos (por relevancia v2) ===")
top_cand = candidatos.head(40)[[
    "cluster_id", "pais_nombre", "region", "actor_norm", "year", "n_eventos",
    "tono_medio", "menciones_total", "duracion_dias", "mechanism_dominante",
    "geo_fullname", "url_representativa"
]]
pd.set_option("display.max_colwidth", 80)
print(top_cand.to_string(index=False))

# ── Paso 8: Por región ──────────────────────────────────────────────────────
print("\n=== Candidatos por región ===")
print(candidatos.groupby("region").agg(
    n_proyectos=("cluster_id", "count"),
    menciones_total=("menciones_total", "sum"),
    tono_medio=("tono_medio", "mean")
).sort_values("n_proyectos", ascending=False).round(2).to_string())

# ── Paso 9: Por empresa SOE ─────────────────────────────────────────────────
print("\n=== Candidatos por empresa SOE ===")
print(candidatos.groupby("actor_norm").agg(
    n_proyectos=("cluster_id", "count"),
    n_paises=("pais", "nunique"),
    tono_medio=("tono_medio", "mean"),
    relevancia_total=("relevancia", "sum")
).sort_values("n_proyectos", ascending=False).round(2).to_string())

# ── Paso 10: LATAM candidatos ───────────────────────────────────────────────
latam_cand = candidatos[candidatos["region"] == "LATAM"]
print(f"\n=== LATAM — {len(latam_cand)} proyectos candidatos v2 ===")
print(latam_cand[[
    "cluster_id", "pais_nombre", "actor_norm", "year", "n_eventos",
    "tono_medio", "menciones_total", "mechanism_dominante",
    "geo_fullname", "url_representativa"
]].to_string(index=False))

# ── Paso 11: Mecanismos globales ────────────────────────────────────────────
print("\n=== Mecanismos de cancelación (candidatos globales) ===")
print(candidatos.groupby("mechanism_dominante").agg(
    n=("cluster_id", "count"),
    tono=("tono_medio", "mean"),
    relevancia=("relevancia", "sum")
).sort_values("n", ascending=False).round(2).to_string())

# ── Guardar ─────────────────────────────────────────────────────────────────
os.makedirs("data/samples/clusters", exist_ok=True)
candidatos.to_csv("data/samples/clusters/project_candidates_events_v2.csv", index=False)
# También actualizar el archivo principal
candidatos.to_csv("data/samples/clusters/project_candidates_events.csv", index=False)
latam_cand.to_csv("data/samples/clusters/project_candidates_latam_v2.csv", index=False)
df_filtered.to_csv("data/samples/clusters/events_url_filtered_v2.csv", index=False)

print(f"\n✓ Candidatos v2: data/samples/clusters/project_candidates_events_v2.csv — {len(candidatos):,} proyectos")
print(f"✓ LATAM v2: data/samples/clusters/project_candidates_latam_v2.csv — {len(latam_cand)} proyectos")

# ── Actualizar changelog + findings ────────────────────────────────────────
with open("docs/ANALYSIS_FINDINGS.md", "a") as f:
    f.write("\n## Script 12 v2 — Clustering actor-aware\n\n")
    f.write("### Mejoras implementadas\n")
    f.write("- Clustering por (país + actor_norm): CRRC ya no se mezcla con COSCO en mismo cluster\n")
    f.write("- Ventana 180 días (antes 90) con gap-reopen\n")
    f.write("- Relevancia = n_eventos × log(menciones) × |tono| (antes: n×menciones lineal)\n")
    f.write("- Umbral mínimo: 2 eventos para SOEs específicas, 3 para actores genéricos\n\n")
    f.write("### Resultados v2\n")
    f.write(f"- Total proyectos candidatos: {len(candidatos):,}\n")
    by_region = candidatos.groupby("region")["cluster_id"].count()
    for reg, n in by_region.sort_values(ascending=False).items():
        f.write(f"- {reg}: {n} proyectos\n")
    f.write(f"\n### LATAM v2: {len(latam_cand)} proyectos candidatos\n")
    for _, r in latam_cand.iterrows():
        f.write(f"- {r['pais_nombre']} / {r['actor_norm']} ({r['year']}): "
                f"{r['n_eventos']} eventos, tono {r['tono_medio']:.2f}, mec={r['mechanism_dominante']}\n")
    f.write("\n### Mecanismos (candidatos globales)\n")
    mech_dist = candidatos.groupby("mechanism_dominante")["cluster_id"].count()
    for m, n in mech_dist.sort_values(ascending=False).items():
        f.write(f"- `{m}`: {n} proyectos ({n/len(candidatos)*100:.1f}%)\n")
    f.write("\n### Próximo paso\n")
    f.write("- Script 14: análisis por empresa SOE china\n")
    f.write("- Script 15: análisis causal de mecanismos\n")
    f.write("- Script 16: validación cruzada Events × GKG\n")

print("✓ ANALYSIS_FINDINGS.md actualizado")
print("\n=== PIPELINE EVENTS v2 COMPLETO ===")
print("Próximos: scripts 14 (empresa SOE), 15 (causal), 16 (validación cruzada GKG)")
