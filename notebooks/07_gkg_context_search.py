"""
Script 07 — Descubrimiento GKG por contexto temático (Fase 1: 2017-2024, ~$12 una vez)

Hallazgo técnico importante: los filtros LIKE en columnas string (V2Themes, V2Organizations,
AllNames) fuerzan un scan del tamaño total de la tabla (~3,464 GB) independientemente del
rango de fechas. Dividir por año costaría 8x$12 = ~$96. Por eso: UNA sola query para
2017-2024, y luego se divide por año localmente (gratis).

Estructura de output:
  data/samples/gkg_por_año/2017/gkg_china_2017.parquet
  data/samples/gkg_por_año/2018/gkg_china_2018.parquet
  ...
  data/samples/gkg_por_año/raw/gkg_china_2017_2024.parquet  (raw completo)

Fase 2 futura: pre-2017 con GDELT v1 (schema diferente).
"""

import os
import pandas as pd
from google.cloud import bigquery
from collections import Counter

PROJECT = os.environ.get("GDELT_PROJECT", "tomasdata-gdelt-research")
GDELT = "gdelt-bq.gdeltv2"

client = bigquery.Client(project=PROJECT)

QUERY = f"""
SELECT
  DATE,
  SourceCommonName,
  DocumentIdentifier,
  V2Tone,
  V2Organizations,
  V2Themes,
  V2Locations,
  AllNames,
  Quotations
FROM `{GDELT}.gkg_partitioned`
WHERE _PARTITIONTIME BETWEEN TIMESTAMP('2017-01-01') AND TIMESTAMP('2024-12-31')
AND (
    -- Temas de inversión/infraestructura BRI
    UPPER(V2Themes) LIKE '%ECON_FOREIGNINVESTMENT%'
    OR UPPER(V2Themes) LIKE '%WB_1803_TRANSPORT_INFRASTRUCTURE%'
    OR UPPER(V2Themes) LIKE '%ECON_ELECTRICPOWER%'
    OR UPPER(V2Themes) LIKE '%WB_2773_MINING%'
    OR UPPER(V2Themes) LIKE '%CRISISLEX_C04_LOGISTICS_TRANSPORT%'
    -- Temas de protesta/oposición ambiental (mecanismo de cancelación)
    OR UPPER(V2Themes) LIKE '%CRISISLEX_C04_PROTESTS%'
    OR UPPER(V2Themes) LIKE '%ENV_DEFORESTATION%'
    OR UPPER(V2Themes) LIKE '%UNGP_ENVIRONMENT_POLICY%'
    -- Referencias directas a BRI/Ruta de la Seda
    OR UPPER(AllNames) LIKE '%BELT AND ROAD%'
    OR UPPER(AllNames) LIKE '%SILK ROAD%'
    OR UPPER(AllNames) LIKE '%CPEC%'
    OR UPPER(AllNames) LIKE '%OBOR%'
)
AND (
    -- SOEs chinas específicas (más preciso que buscar "CHINA" genérico)
    UPPER(V2Organizations) LIKE '%HUAWEI%'
    OR UPPER(V2Organizations) LIKE '%SINOPEC%'
    OR UPPER(V2Organizations) LIKE '%CRRC%'
    OR UPPER(V2Organizations) LIKE '%COSCO%'
    OR UPPER(V2Organizations) LIKE '%CHINA RAILWAY%'
    OR UPPER(V2Organizations) LIKE '%CHINA COMMUNICATIONS%'
    OR UPPER(V2Organizations) LIKE '%CHINA HARBOUR%'
    OR UPPER(V2Organizations) LIKE '%SINOHYDRO%'
    OR UPPER(V2Organizations) LIKE '%CHINA GEZHOUBA%'
    OR UPPER(V2Organizations) LIKE '%THREE GORGES%'
    OR UPPER(V2Organizations) LIKE '%CHINA DEVELOPMENT BANK%'
    OR UPPER(V2Organizations) LIKE '%EXIM BANK%'
    OR UPPER(V2Organizations) LIKE '%SILK ROAD FUND%'
    OR UPPER(V2Organizations) LIKE '%CHINA STATE CONSTRUCTION%'
    OR UPPER(V2Organizations) LIKE '%ZTE%'
    OR UPPER(V2Organizations) LIKE '%CHINA TELECOM%'
    OR UPPER(V2Organizations) LIKE '%NUCTECH%'
    OR UPPER(V2Organizations) LIKE '%CITIC%'
    OR UPPER(V2Organizations) LIKE '%CNPC%'
    OR UPPER(V2Organizations) LIKE '%PETROCHINA%'
    OR UPPER(V2Organizations) LIKE '%CNOOC%'
    OR UPPER(V2Organizations) LIKE '%POWERCHINA%'
    OR UPPER(V2Organizations) LIKE '%CHINA ROAD AND BRIDGE%'
    -- Fallback para artículos BRI que mencionan "China" en org + tema específico
    OR (UPPER(V2Organizations) LIKE '%CHINA%' AND (
        UPPER(AllNames) LIKE '%BELT AND ROAD%'
        OR UPPER(AllNames) LIKE '%SILK ROAD%'
        OR UPPER(AllNames) LIKE '%CPEC%'
    ))
)
-- Tono: -3 captura sanciones (~-4), protestas ambientales (~-3.5), renegociaciones (~-3.8)
-- antes era -5, demasiado restrictivo para estos mecanismos de cancelación
AND SAFE_CAST(SPLIT(V2Tone, ',')[SAFE_OFFSET(0)] AS FLOAT64) < -3
ORDER BY DATE DESC
"""


def parse_tone(tone_str):
    try:
        return float(str(tone_str).split(",")[0])
    except Exception:
        return None


print(f"Proyecto: {PROJECT}")
print("Verificando costo (dry run)...")

job_dry = client.query(QUERY, job_config=bigquery.QueryJobConfig(dry_run=True))
gb = job_dry.total_bytes_processed / 1e9
costo = max(0, (gb - 1000) / 1000 * 5)
print(f"  Bytes a procesar: {gb:.1f} GB")
print(f"  Costo estimado: ~${costo:.2f} USD (cubierto por créditos)")

confirm = input("\n¿Ejecutar query completa 2017-2024? (s/n): ").strip().lower()
if confirm != "s":
    print("Cancelado.")
    exit()

print("\nEjecutando query 2017-2024... (puede tomar 5-15 minutos)")
job_config = bigquery.QueryJobConfig(maximum_bytes_billed=5 * 1000**4)  # 5TB max
df = client.query(QUERY, job_config=job_config).to_dataframe()
print(f"Total artículos encontrados: {len(df):,}")

if df.empty:
    print("Sin resultados — verificar query.")
    exit()

df["tone"] = df["V2Tone"].apply(parse_tone)
df["year"] = df["DATE"].astype(str).str[:4].astype(int)

# --- Análisis general ---
print("\n=== Artículos por año ===")
print(df.groupby("year").size().rename("n_articulos").to_string())

print("\n=== Tono promedio por año ===")
print(df.groupby("year")["tone"].mean().round(2).to_string())

print("\n=== Top 20 fuentes ===")
print(df["SourceCommonName"].value_counts().head(20).to_string())

# --- Organizaciones chinas mencionadas ---
print("\n=== Top 50 organizaciones con 'China/Chinese/Sino' ===")
org_counter = Counter()
for orgs_raw in df["V2Organizations"].dropna():
    for org in orgs_raw.split(";"):
        org = org.strip()
        if org and ("china" in org.lower() or "chinese" in org.lower() or "sino" in org.lower()):
            org_counter[org] += 1
china_orgs = pd.Series(org_counter).sort_values(ascending=False).head(50)
print(china_orgs.to_string())

# --- Países ---
print("\n=== Top 25 países en V2Locations ===")
loc_counter = Counter()
for locs in df["V2Locations"].dropna():
    for entry in locs.split(";"):
        parts = entry.split("#")
        if len(parts) >= 3 and parts[2]:
            loc_counter[parts[2]] += 1
print(pd.Series(loc_counter).sort_values(ascending=False).head(25).to_string())

# --- Guardar raw completo ---
raw_dir = "data/samples/gkg_por_año/raw"
os.makedirs(raw_dir, exist_ok=True)
raw_path = f"{raw_dir}/gkg_china_2017_2024.parquet"
df.to_parquet(raw_path, index=False)
print(f"\n✓ Raw guardado: {raw_path} — shape: {df.shape}")

# --- Dividir por año y guardar en subcarpetas ---
print("\nDividiendo por año...")
for year, df_year in df.groupby("year"):
    year_dir = f"data/samples/gkg_por_año/{year}"
    os.makedirs(year_dir, exist_ok=True)
    year_path = f"{year_dir}/gkg_china_{year}.parquet"
    df_year.to_parquet(year_path, index=False)
    print(f"  {year}: {len(df_year):,} artículos → {year_path}")

print("\n=== Muestra — artículos más negativos (tono < -12) ===")
muy_neg = df[df["tone"] < -12].nsmallest(10, "tone")
for _, row in muy_neg.iterrows():
    orgs = str(row["V2Organizations"])[:100]
    print(f"  [{row['DATE']}] tone={row['tone']:.1f} | {row['SourceCommonName']}")
    print(f"    URL: {str(row['DocumentIdentifier'])[:100]}")
    print(f"    Orgs: {orgs}")
    print()
