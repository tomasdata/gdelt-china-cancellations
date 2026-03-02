"""
Script 04 — Estimar costo de la query de descubrimiento de proyectos cancelados
Antes de ejecutar, verificamos cuánto data scannea para mantenernos en el free tier.
"""

from google.cloud import bigquery

PROJECT = "tomasdata-gdelt-research"
GDELT = "gdelt-bq.gdeltv2"

client = bigquery.Client(project=PROJECT)


def dry_run(label: str, query: str) -> float:
    job = client.query(query, job_config=bigquery.QueryJobConfig(dry_run=True))
    gb = job.total_bytes_processed / 1e9
    cost = max(0, (gb - 1000) / 1000 * 5)  # free tier 1TB, luego $5/TB
    print(f"  [{label}] {gb:.1f} GB  →  {'GRATIS' if gb < 1000 else f'~${cost:.2f} USD'}")
    return gb


# --- Query A: GKG con empresas chinas conocidas + tono negativo ---
query_a = f"""
SELECT
  DATE, SourceCommonName, DocumentIdentifier,
  V2Tone, V2Organizations, V2Themes, V2Locations, AllNames
FROM `{GDELT}.gkg_partitioned`
WHERE DATE BETWEEN 20170101 AND 20241231
AND (
    UPPER(V2Organizations) LIKE '%HUAWEI%'
    OR UPPER(V2Organizations) LIKE '%SINOPEC%'
    OR UPPER(V2Organizations) LIKE '%CNNC%'
    OR UPPER(V2Organizations) LIKE '%CNPC%'
    OR UPPER(V2Organizations) LIKE '%CRRC%'
    OR UPPER(V2Organizations) LIKE '%CHINA RAILWAY%'
    OR UPPER(V2Organizations) LIKE '%CHINA COMMUNICATIONS%'
    OR UPPER(V2Organizations) LIKE '%EXIM BANK%'
    OR UPPER(V2Organizations) LIKE '%CHINA DEVELOPMENT BANK%'
    OR UPPER(V2Organizations) LIKE '%POWER CONSTRUCTION%'
    OR UPPER(V2Organizations) LIKE '%CHINA HARBOUR%'
    OR UPPER(V2Organizations) LIKE '%SINOHYDRO%'
    OR UPPER(V2Organizations) LIKE '%CHINA GEZHOUBA%'
    OR UPPER(V2Organizations) LIKE '%CITIC%'
    OR UPPER(V2Organizations) LIKE '%COSCO%'
    OR UPPER(V2Organizations) LIKE '%THREE GORGES%'
)
AND SAFE_CAST(SPLIT(V2Tone, ',')[SAFE_OFFSET(0)] AS FLOAT64) < -3
"""

# --- Query B: GKG con temas BRI/inversión china + tono muy negativo ---
query_b = f"""
SELECT
  DATE, SourceCommonName, DocumentIdentifier,
  V2Tone, V2Organizations, V2Themes, V2Locations, AllNames
FROM `{GDELT}.gkg_partitioned`
WHERE DATE BETWEEN 20170101 AND 20241231
AND (
    UPPER(V2Themes) LIKE '%ECON_FOREIGNINVESTMENT%'
    OR UPPER(V2Themes) LIKE '%EPU_CATS_NATIONAL_SECURITY%'
)
AND (
    UPPER(V2Organizations) LIKE '%CHINESE%'
    OR UPPER(V2Organizations) LIKE '%CHINA%'
    OR UPPER(AllNames) LIKE '%BELT AND ROAD%'
    OR UPPER(AllNames) LIKE '%BRI%'
)
AND SAFE_CAST(SPLIT(V2Tone, ',')[SAFE_OFFSET(0)] AS FLOAT64) < -5
"""

# --- Query C: Events table, China como actor + eventos de conflicto/rechazo ---
query_c = f"""
SELECT
  Day, Actor1Name, Actor1CountryCode, Actor2Name, Actor2CountryCode,
  EventCode, EventBaseCode, GoldsteinScale, AvgTone,
  NumMentions, NumSources, ActionGeo_FullName, SOURCEURL
FROM `{GDELT}.events`
WHERE Day BETWEEN 20170101 AND 20241231
AND (Actor1CountryCode = 'CHN' OR Actor2CountryCode = 'CHN')
AND EventRootCode IN ('12', '13', '14', '15', '16', '17')
AND AvgTone < -5
AND NumMentions >= 3
"""

print("=== Estimación de costos (dry run) ===")
print()
gb_a = dry_run("GKG empresas chinas + tono negativo", query_a)
gb_b = dry_run("GKG temas BRI/inversión + tono muy negativo", query_b)
gb_c = dry_run("Events China + conflicto/rechazo", query_c)

total = gb_a + gb_b + gb_c
print(f"\n  Total combinado: {total:.1f} GB")
print(f"  Free tier mensual: 1000 GB")
print(f"  Costo estimado: {'GRATIS (dentro del free tier)' if total < 1000 else f'~${(total-1000)/1000*5:.2f} USD'}")
