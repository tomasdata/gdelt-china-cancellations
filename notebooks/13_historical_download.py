"""
Script 13 — Descarga histórica de eventos pre-2017
Input: BigQuery gdelt-bq.gdeltv2.events
Output: data/samples/historical/

GDELT v2 tiene datos desde 2015-02-19.
Descargamos los mismos dos datasets que en scripts 05 y 06:
  A) Conflicto China + EventCodes 14-19 + AvgTone < -2  (2015-01-01 a 2016-12-31)
  B) Económico China + EventCodes 163/164/165            (2015-01-01 a 2016-12-31)

Estas descargas se realizan en background mientras se analiza la data de 2017-2024.
"""

import os
from google.cloud import bigquery

PROJECT = "tomasdata-gdelt-research"
client = bigquery.Client(project=PROJECT)

os.makedirs("data/samples/historical", exist_ok=True)

# ── Dry-run primero ────────────────────────────────────────────────────────────
def dry_run(sql: str, label: str) -> int:
    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
    job = client.query(sql, job_config=job_config)
    gb = job.total_bytes_processed / 1e9
    cost = (gb / 1000) * 5 if gb > 1000 else 0
    print(f"  [{label}] Escanea: {gb:.1f} GB — costo estimado: ${cost:.2f}")
    return job.total_bytes_processed


CONFLICT_SQL = """
SELECT
  SQLDATE, Actor1Name, Actor1CountryCode, Actor2Name, Actor2CountryCode,
  EventCode, EventBaseCode, EventRootCode, IsRootEvent,
  GoldsteinScale, AvgTone, NumMentions, NumSources, NumArticles,
  ActionGeo_FullName, ActionGeo_CountryCode, ActionGeo_Lat, ActionGeo_Long,
  SOURCEURL
FROM `gdelt-bq.gdeltv2.events`
WHERE SQLDATE BETWEEN 20150101 AND 20161231
  AND (
    Actor1CountryCode = 'CHN'
    OR Actor2CountryCode = 'CHN'
    OR Actor1Name LIKE '%CHINA%'
    OR Actor2Name LIKE '%CHINA%'
  )
  AND (
    EventRootCode IN ('14','15','16','17','18','19')
    OR EventBaseCode IN ('140','141','142','143','144','145',
                         '150','160','170','180','190')
    OR EventCode IN ('141','142','143','144','145',
                     '171','172','173','174','175',
                     '191','192','193','194','195','196')
  )
  AND AvgTone < -2
"""

ECONOMIC_SQL = """
SELECT
  SQLDATE, Actor1Name, Actor1CountryCode, Actor2Name, Actor2CountryCode,
  EventCode, EventBaseCode, EventRootCode, IsRootEvent,
  GoldsteinScale, AvgTone, NumMentions, NumSources, NumArticles,
  ActionGeo_FullName, ActionGeo_CountryCode, ActionGeo_Lat, ActionGeo_Long,
  SOURCEURL
FROM `gdelt-bq.gdeltv2.events`
WHERE SQLDATE BETWEEN 20150101 AND 20161231
  AND (
    Actor1CountryCode = 'CHN'
    OR Actor2CountryCode = 'CHN'
    OR Actor1Name LIKE '%CHINA%'
    OR Actor2Name LIKE '%CHINA%'
  )
  AND EventCode IN ('163', '164', '165')
"""

# ── Dry-run ────────────────────────────────────────────────────────────────────
print("=== DRY RUN — estimación de costos ===")
dry_run(CONFLICT_SQL, "Conflicto 2015-2016")
dry_run(ECONOMIC_SQL, "Económico 2015-2016")
print()

# ── Confirmación ──────────────────────────────────────────────────────────────
print("¿Ejecutar ambas queries? (s/n): ", end="", flush=True)
resp = input().strip().lower()
if resp != "s":
    print("Cancelado.")
    exit(0)

# ── Ejecutar ──────────────────────────────────────────────────────────────────
job_config = bigquery.QueryJobConfig(
    maximum_bytes_billed=2 * 1000**4  # 2 TB máximo
)

# Query A: Conflicto
print("\n[A] Ejecutando query conflicto 2015-2016...")
job_a = client.query(CONFLICT_SQL, job_config=job_config)
df_conflict = job_a.to_dataframe()
print(f"  ✓ {len(df_conflict):,} eventos conflicto descargados")
df_conflict.to_csv("data/samples/historical/events_china_conflict_2015_2016.csv", index=False)
print(f"  ✓ Guardado: data/samples/historical/events_china_conflict_2015_2016.csv")

# Resumen rápido
print(f"\n  Por año:")
df_conflict["year"] = df_conflict["SQLDATE"] // 10000
print(df_conflict.groupby("year").size().to_string())

# Query B: Económico
print("\n[B] Ejecutando query económico 2015-2016...")
job_b = client.query(ECONOMIC_SQL, job_config=job_config)
df_economic = job_b.to_dataframe()
print(f"  ✓ {len(df_economic):,} eventos económicos descargados")
df_economic.to_csv("data/samples/historical/events_china_economic_2015_2016.csv", index=False)
print(f"  ✓ Guardado: data/samples/historical/events_china_economic_2015_2016.csv")

print(f"\n  Por año:")
df_economic["year"] = df_economic["SQLDATE"] // 10000
print(df_economic.groupby("year").size().to_string())

# ── Comparar con 2017-2024 ─────────────────────────────────────────────────────
import pandas as pd
df_2017_2024 = pd.read_csv("data/samples/events_china_conflict_2017_2024.csv", nrows=1)
print(f"\n=== COMPARATIVA DE DATASETS ===")
print(f"  Conflicto 2015-2016: {len(df_conflict):,} eventos")
print(f"  Conflicto 2017-2024: 374,108 eventos (referencia)")
print(f"  Económico 2015-2016: {len(df_economic):,} eventos")
print(f"  Económico 2017-2024: 76,771 eventos (referencia)")
print()
print("✓ Descarga histórica completa")
print("Siguiente: analizar estos datasets con el mismo pipeline 08→09→10→11→12")
print("(Pero primero esperar resultados del GKG script 07)")
