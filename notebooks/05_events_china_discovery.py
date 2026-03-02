"""
Script 05 — Descubrimiento vía Events table (GRATIS, 144 GB)
Busca eventos donde China es actor + tipo conflicto/rechazo + tono negativo (2017-2024)
Objetivo: identificar candidatos a proyectos cancelados por país, sector, año
"""

import pandas as pd
from google.cloud import bigquery

PROJECT = "tomasdata-gdelt-research"
client = bigquery.Client(project=PROJECT)

QUERY = """
SELECT
  SQLDATE,
  Actor1Name, Actor1CountryCode,
  Actor2Name, Actor2CountryCode,
  EventCode, EventBaseCode, EventRootCode,
  GoldsteinScale, AvgTone,
  NumMentions, NumSources, NumArticles,
  ActionGeo_FullName, ActionGeo_CountryCode,
  Actor1Geo_CountryCode, Actor2Geo_CountryCode,
  SOURCEURL
FROM `gdelt-bq.gdeltv2.events`
WHERE SQLDATE BETWEEN 20170101 AND 20241231
AND (Actor1CountryCode = 'CHN' OR Actor2CountryCode = 'CHN')
AND EventRootCode IN ('12','13','14','15','16','17','18','19')
AND AvgTone < -5
AND NumMentions >= 3
ORDER BY NumMentions DESC
"""

# Codigos CAMEO relevantes para contexto
CAMEO_ROOT = {
    "12": "Reject / Demand",
    "13": "Threaten",
    "14": "Protest",
    "15": "Exhibit Force Posture",
    "16": "Reduce Relations",
    "17": "Coerce",
    "18": "Assault",
    "19": "Fight / Use Force",
}

print("Ejecutando query Events (144 GB, ~30-60s)...")
df = client.query(QUERY).to_dataframe()
print(f"Filas obtenidas: {len(df):,}")

# --- Análisis general ---
print("\n=== Distribución temporal (cancelaciones por año) ===")
df["year"] = df["SQLDATE"] // 10000
print(df.groupby("year").size().rename("n_eventos").to_string())

print("\n=== Top 20 países contraparte de China (más eventos negativos) ===")
# País que se enfrenta a China (el que NO es CHN)
df["counterpart"] = df.apply(
    lambda r: r["Actor2CountryCode"] if r["Actor1CountryCode"] == "CHN" else r["Actor1CountryCode"],
    axis=1,
)
print(df["counterpart"].value_counts().head(20).to_string())

print("\n=== Tipo de evento (EventRootCode) ===")
df["event_label"] = df["EventRootCode"].map(CAMEO_ROOT)
print(df["event_label"].value_counts().to_string())

print("\n=== Top 20 zonas de acción (ActionGeo_FullName) ===")
print(df["ActionGeo_FullName"].value_counts().head(20).to_string())

print("\n=== Eventos con más cobertura mediática (top 30) ===")
top = df.nlargest(30, "NumMentions")[
    ["SQLDATE", "Actor1Name", "Actor1CountryCode", "Actor2Name", "Actor2CountryCode",
     "EventRootCode", "GoldsteinScale", "AvgTone", "NumMentions", "ActionGeo_FullName", "SOURCEURL"]
]
pd.set_option("display.max_colwidth", 80)
print(top.to_string(index=False))

# --- América Latina específicamente ---
latam = ["CH", "AR", "BR", "MX", "PE", "CO", "VE", "BO", "EC", "UY", "PY", "CL"]
df_latam = df[df["counterpart"].isin(latam)]
print(f"\n=== América Latina (filtro FIPS): {len(df_latam):,} eventos ===")
print(df_latam.groupby(["counterpart", "year"]).size().unstack(fill_value=0).to_string())

# Guardar
df.to_csv("data/samples/events_china_conflict_2017_2024.csv", index=False)
print("\n✓ Guardado en data/samples/events_china_conflict_2017_2024.csv")
print(f"  Columnas: {list(df.columns)}")
print(f"  Países únicos contraparte: {df['counterpart'].nunique()}")
print(f"  Rango de fechas: {df['SQLDATE'].min()} - {df['SQLDATE'].max()}")
