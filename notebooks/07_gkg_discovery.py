"""
Script 07 — Descubrimiento comprehensivo via GKG (costo ~$10-12, ejecutar una vez)
Prerequisito: cuenta GCP personal con créditos ($300 gratis en cuenta nueva)
Ver: docs/SETUP_NUEVA_CUENTA_GCP.md

Objetivo: encontrar TODOS los artículos de noticias (2017-2024) donde aparecen
empresas chinas involucradas en proyectos de inversión/infraestructura con
cobertura negativa. De ahí extraer candidatos a proyectos cancelados.
"""

import os
import pandas as pd
from google.cloud import bigquery

# Cambiar si usas otro proyecto
PROJECT = os.environ.get("GDELT_PROJECT", "tomasdata-gdelt-research")
GDELT = "gdelt-bq.gdeltv2"

client = bigquery.Client(project=PROJECT)

# Empresas chinas a buscar (estado + privadas relevantes para BRI/infraestructura)
CHINESE_ORGS = [
    "HUAWEI", "SINOPEC", "CNNC", "CNPC", "CRRC", "COSCO",
    "CHINA RAILWAY", "CHINA COMMUNICATIONS", "CHINA HARBOUR",
    "CHINA POWER", "SINOHYDRO", "CHINA GEZHOUBA", "CITIC",
    "THREE GORGES", "CHINA DEVELOPMENT BANK", "EXIM BANK",
    "CHINA NATIONAL PETROLEUM", "CHINA STATE CONSTRUCTION",
    "CHINA ENERGY", "CHINA OVERSEAS", "ZTE", "NUCTECH",
    "CHINA TELECOM", "CHINA MOBILE", "CHINA UNICOM",
    "BELT AND ROAD", "BRI PROJECT", "SILK ROAD FUND",
]

# Construir condición OR para organizaciones
org_conditions = "\n    OR ".join(
    [f"UPPER(V2Organizations) LIKE '%{org}%'" for org in CHINESE_ORGS]
)

QUERY = f"""
SELECT
  DATE,
  SourceCommonName,
  DocumentIdentifier,
  V2Tone,
  V2Organizations,
  V2Themes,
  V2Locations,
  V2Persons,
  AllNames,
  Quotations
FROM `{GDELT}.gkg_partitioned`
WHERE DATE BETWEEN 20170101 AND 20241231
AND (
    {org_conditions}
)
AND SAFE_CAST(SPLIT(V2Tone, ',')[SAFE_OFFSET(0)] AS FLOAT64) < -3
AND (
    UPPER(V2Themes) LIKE '%ECON_FOREIGNINVESTMENT%'
    OR UPPER(V2Themes) LIKE '%EPU_CATS_NATIONAL_SECURITY%'
    OR UPPER(V2Themes) LIKE '%WB_1803_TRANSPORT_INFRASTRUCTURE%'
    OR UPPER(V2Themes) LIKE '%ENV_OIL%'
    OR UPPER(V2Themes) LIKE '%CRISISLEX_C04_LOGISTICS_TRANSPORT%'
    OR UPPER(V2Themes) LIKE '%ECON_ELECTRICPOWER%'
    OR UPPER(V2Organizations) LIKE '%BELT AND ROAD%'
    OR UPPER(V2Organizations) LIKE '%BRI PROJECT%'
)
ORDER BY DATE DESC
"""

print(f"Proyecto: {PROJECT}")
print("Verificando costo antes de ejecutar...")

# Dry run primero
job_dry = client.query(QUERY, job_config=bigquery.QueryJobConfig(dry_run=True))
gb = job_dry.total_bytes_processed / 1e9
print(f"  Bytes a procesar: {gb:.1f} GB")
print(f"  Costo estimado: {'GRATIS (free tier)' if gb < 1000 else f'~${(gb-1000)/1000*5:.2f} USD'}")

confirm = input("\n¿Ejecutar query? (s/n): ").strip().lower()
if confirm != "s":
    print("Cancelado.")
    exit()

print("\nEjecutando... (puede tomar 2-5 minutos)")
df = client.query(QUERY).to_dataframe()
print(f"Artículos encontrados: {len(df):,}")

# --- Parsear V2Tone ---
def parse_tone(tone_str):
    try:
        return float(str(tone_str).split(",")[0])
    except Exception:
        return None

df["tone"] = df["V2Tone"].apply(parse_tone)
df["year"] = df["DATE"].astype(str).str[:4].astype(int)

# --- Análisis de distribución ---
print("\n=== Artículos por año ===")
print(df.groupby("year").size().rename("n_articulos").to_string())

print("\n=== Tono promedio por año ===")
print(df.groupby("year")["tone"].mean().round(2).to_string())

print("\n=== Top 20 fuentes ===")
print(df["SourceCommonName"].value_counts().head(20).to_string())

print("\n=== Top organizaciones chinas mencionadas ===")
# Extraer qué org china aparece más en los artículos
from collections import Counter
org_counter = Counter()
for orgs in df["V2Organizations"].dropna():
    for org in CHINESE_ORGS:
        if org.lower() in orgs.lower():
            org_counter[org] += 1
print(pd.Series(org_counter).sort_values(ascending=False).head(20).to_string())

print("\n=== Top países en V2Locations ===")
# Parsear locaciones: campo formato "type#name#country_code#..."
loc_counter = Counter()
for locs in df["V2Locations"].dropna():
    for entry in locs.split(";"):
        parts = entry.split("#")
        if len(parts) >= 3 and parts[2]:
            loc_counter[parts[2]] += 1
print(pd.Series(loc_counter).sort_values(ascending=False).head(25).to_string())

# --- Guardar resultado completo ---
os.makedirs("data/samples", exist_ok=True)
df.to_parquet("data/samples/gkg_china_investment_negative_2017_2024.parquet", index=False)
df.to_csv("data/samples/gkg_china_investment_negative_2017_2024.csv", index=False)
print(f"\n✓ Guardado en data/samples/gkg_china_investment_negative_2017_2024.parquet")
print(f"  Shape: {df.shape}")
print(f"  Columnas: {list(df.columns)}")

print("\n=== Muestra de artículos más negativos (tono < -8) ===")
muy_neg = df[df["tone"] < -8].nsmallest(20, "tone")
for _, row in muy_neg.iterrows():
    orgs = str(row["V2Organizations"])[:80]
    print(f"  [{row['DATE']}] tone={row['tone']:.1f} | {row['SourceCommonName']}")
    print(f"    URL: {str(row['DocumentIdentifier'])[:100]}")
    print(f"    Orgs: {orgs}")
    print()
