"""
Script 06 — Refinar eventos: foco en cancelaciones económicas
Hallazgos script 05: 374k eventos muy ruidosos (militar, político, COVID, etc.)
Este script filtra por EventCode específicos de rechazo económico/cooperación.

CAMEO codes relevantes para cancelaciones de inversión:
  1224 = Reject proposal for economic cooperation
  1225 = Reject request for economic aid
  163  = Impose embargo / sanctions / expel
  164  = Halt negotiations
  165  = Expel or withdraw economic actors
  1624 = Reduce or cut off economic aid and cooperation
  1625 = Break economic relations
  1641 = Impose restrictions on political freedoms
"""

import pandas as pd
from google.cloud import bigquery

PROJECT = "tomasdata-gdelt-research"
client = bigquery.Client(project=PROJECT)

# FIPS codes correctos para LATAM
LATAM_FIPS = {
    "CI": "Chile", "AR": "Argentina", "BR": "Brazil",
    "MX": "Mexico", "PE": "Peru", "CO": "Colombia",
    "VE": "Venezuela", "BL": "Bolivia", "EC": "Ecuador",
    "UY": "Uruguay", "PA": "Paraguay", "GY": "Guyana",
    "NS": "Suriname", "BH": "Belize", "CU": "Cuba",
}

QUERY_ECONOMIC = """
SELECT
  SQLDATE,
  Actor1Name, Actor1CountryCode, Actor1Type1Code,
  Actor2Name, Actor2CountryCode, Actor2Type1Code,
  EventCode, EventBaseCode, EventRootCode,
  GoldsteinScale, AvgTone, NumMentions,
  ActionGeo_FullName, ActionGeo_CountryCode,
  SOURCEURL
FROM `gdelt-bq.gdeltv2.events`
WHERE SQLDATE BETWEEN 20170101 AND 20241231
AND (Actor1CountryCode = 'CHN' OR Actor2CountryCode = 'CHN')
AND (
    -- Rechazar cooperación económica (1224, 1225)
    EventBaseCode IN ('1224','1225')
    -- Reducir relaciones económicas (163, 164, 165, 1624, 1625)
    OR EventCode IN ('163','164','165','1624','1625')
    -- Imponer sanciones / embargo
    OR EventBaseCode = '163'
    -- Rechazo de propuestas de cooperación en general
    OR EventCode IN ('1252','1253','1254')
)
AND NumMentions >= 2
ORDER BY NumMentions DESC
"""

print("Ejecutando query económica refinada...")
df = client.query(QUERY_ECONOMIC).to_dataframe()
print(f"Filas: {len(df):,}")

print("\n=== Distribución por EventCode ===")
print(df["EventCode"].value_counts().head(20).to_string())

print("\n=== Distribución temporal ===")
df["year"] = df["SQLDATE"] // 10000
print(df.groupby("year").size().rename("n").to_string())

print("\n=== Top países contraparte ===")
df["counterpart_code"] = df.apply(
    lambda r: r["Actor2CountryCode"] if r["Actor1CountryCode"] == "CHN" else r["Actor1CountryCode"],
    axis=1,
)
df["counterpart_geo"] = df.apply(
    lambda r: r["Actor2CountryCode"] if r["Actor1CountryCode"] == "CHN" else r["Actor1CountryCode"],
    axis=1,
)
print(df["counterpart_code"].value_counts().head(25).to_string())

print("\n=== América Latina (FIPS correcto) ===")
latam_codes = list(LATAM_FIPS.keys())
df_latam = df[
    df["ActionGeo_CountryCode"].isin(latam_codes) |
    df["counterpart_code"].isin(latam_codes)
]
print(f"Eventos LATAM: {len(df_latam):,}")
if len(df_latam) > 0:
    df_latam["country_name"] = df_latam["ActionGeo_CountryCode"].map(LATAM_FIPS).fillna(
        df_latam["counterpart_code"].map(LATAM_FIPS)
    )
    print(df_latam.groupby(["country_name","year"]).size().unstack(fill_value=0).to_string())
    print("\nTop eventos LATAM por menciones:")
    cols = ["SQLDATE","Actor1Name","Actor1CountryCode","Actor2Name","Actor2CountryCode",
            "EventCode","AvgTone","NumMentions","ActionGeo_FullName","SOURCEURL"]
    print(df_latam.nlargest(15, "NumMentions")[cols].to_string(index=False))

print("\n=== Top 30 eventos con más cobertura (global) ===")
cols_top = ["SQLDATE","Actor1Name","Actor1CountryCode","Actor2Name","Actor2CountryCode",
            "EventCode","GoldsteinScale","AvgTone","NumMentions","ActionGeo_FullName","SOURCEURL"]
print(df.nlargest(30, "NumMentions")[cols_top].to_string(index=False))

# Guardar
df.to_csv("data/samples/events_china_economic_2017_2024.csv", index=False)
print(f"\n✓ Guardado: data/samples/events_china_economic_2017_2024.csv ({len(df):,} filas)")
