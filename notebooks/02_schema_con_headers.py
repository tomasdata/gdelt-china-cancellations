"""
Script 02 — Añadir headers documentados y entender el schema real
Objetivo: Cargar events y GKG con nombres de columnas reales (GDELT codebook)
y ver qué campos son útiles para buscar proyectos chinos cancelados.
"""

import requests
import zipfile
import io
import pandas as pd

LASTUPDATE_URL = "http://data.gdeltproject.org/gdeltv2/lastupdate.txt"

# Columnas del GDELT 2.0 Events (codebook oficial, 61 columnas)
EVENTS_COLS = [
    "GlobalEventID", "Day", "MonthYear", "Year", "FractionDate",
    "Actor1Code", "Actor1Name", "Actor1CountryCode", "Actor1KnownGroupCode",
    "Actor1EthnicCode", "Actor1Religion1Code", "Actor1Religion2Code",
    "Actor1Type1Code", "Actor1Type2Code", "Actor1Type3Code",
    "Actor2Code", "Actor2Name", "Actor2CountryCode", "Actor2KnownGroupCode",
    "Actor2EthnicCode", "Actor2Religion1Code", "Actor2Religion2Code",
    "Actor2Type1Code", "Actor2Type2Code", "Actor2Type3Code",
    "IsRootEvent", "EventCode", "EventBaseCode", "EventRootCode",
    "QuadClass", "GoldsteinScale", "NumMentions", "NumSources",
    "NumArticles", "AvgTone",
    "Actor1Geo_Type", "Actor1Geo_FullName", "Actor1Geo_CountryCode",
    "Actor1Geo_ADM1Code", "Actor1Geo_ADM2Code", "Actor1Geo_Lat",
    "Actor1Geo_Long", "Actor1Geo_FeatureID",
    "Actor2Geo_Type", "Actor2Geo_FullName", "Actor2Geo_CountryCode",
    "Actor2Geo_ADM1Code", "Actor2Geo_ADM2Code", "Actor2Geo_Lat",
    "Actor2Geo_Long", "Actor2Geo_FeatureID",
    "ActionGeo_Type", "ActionGeo_FullName", "ActionGeo_CountryCode",
    "ActionGeo_ADM1Code", "ActionGeo_ADM2Code", "ActionGeo_Lat",
    "ActionGeo_Long", "ActionGeo_FeatureID",
    "DATEADDED", "SOURCEURL",
]

# Columnas del GKG v2 (27 columnas)
GKG_COLS = [
    "GKGRECORDID", "DATE", "SourceCollectionIdentifier", "SourceCommonName",
    "DocumentIdentifier", "Counts", "V2Counts", "Themes", "V2Themes",
    "Locations", "V2Locations", "Persons", "V2Persons", "Organizations",
    "V2Organizations", "V2Tone", "Dates", "GCAM", "SharingImage",
    "RelatedImages", "SocialImageEmbeds", "SocialVideoEmbeds", "Quotations",
    "AllNames", "Amounts", "TranslationInfo", "Extras",
]


def fetch_lastupdate() -> dict[str, str]:
    resp = requests.get(LASTUPDATE_URL, timeout=15)
    resp.raise_for_status()
    files = {}
    for line in resp.text.strip().splitlines():
        parts = line.split()
        url = parts[2]
        if "export" in url:
            files["events"] = url
        elif "mentions" in url:
            files["mentions"] = url
        elif ".gkg." in url:
            files["gkg"] = url
    return files


def download_csv(url: str, col_names: list[str] | None = None) -> pd.DataFrame:
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    z = zipfile.ZipFile(io.BytesIO(resp.content))
    with z.open(z.namelist()[0]) as f:
        df = pd.read_csv(
            f, sep="\t",
            header=None if col_names else 0,
            names=col_names,
            low_memory=False
        )
    return df


if __name__ == "__main__":
    files = fetch_lastupdate()

    # --- Events con nombres ---
    print("=== EVENTS con headers ===")
    df_ev = download_csv(files["events"], EVENTS_COLS)
    print(f"Shape: {df_ev.shape}")
    print("\nColumnas clave con ejemplos:")
    key_cols = ["GlobalEventID", "Day", "Actor1Name", "Actor1CountryCode",
                "Actor2Name", "Actor2CountryCode", "EventCode", "EventRootCode",
                "GoldsteinScale", "AvgTone", "NumMentions", "ActionGeo_FullName",
                "SOURCEURL"]
    print(df_ev[key_cols].head(5).to_string())

    print("\nRango de GoldsteinScale:")
    print(f"  min={df_ev['GoldsteinScale'].min():.2f}  max={df_ev['GoldsteinScale'].max():.2f}  "
          f"mean={df_ev['GoldsteinScale'].mean():.2f}")

    print("\nRango de AvgTone:")
    print(f"  min={df_ev['AvgTone'].min():.2f}  max={df_ev['AvgTone'].max():.2f}  "
          f"mean={df_ev['AvgTone'].mean():.2f}")

    print("\nEventRootCode más frecuentes (top 10):")
    print(df_ev["EventRootCode"].value_counts().head(10).to_string())

    print("\nPaíses Actor1 más frecuentes (top 10):")
    print(df_ev["Actor1CountryCode"].value_counts().head(10).to_string())

    # Filtrar eventos donde China es actor
    china_ev = df_ev[
        (df_ev["Actor1CountryCode"] == "CHN") | (df_ev["Actor2CountryCode"] == "CHN")
    ]
    print(f"\nEventos con China como actor (en este slice): {len(china_ev)}")
    if len(china_ev) > 0:
        print(china_ev[key_cols].head(5).to_string())

    # --- GKG con nombres ---
    print("\n\n=== GKG con headers ===")
    df_gkg = download_csv(files["gkg"], GKG_COLS)
    print(f"Shape: {df_gkg.shape}")
    print("\nCampos disponibles:")
    for col in GKG_COLS:
        sample = str(df_gkg[col].dropna().iloc[0])[:120] if df_gkg[col].dropna().shape[0] > 0 else "N/A"
        print(f"  {col}: {sample}")

    print("\nV2Tone (6 valores separados por coma):")
    tone_sample = df_gkg["V2Tone"].dropna().head(3)
    for t in tone_sample:
        vals = t.split(",")
        labels = ["Tone", "Positive", "Negative", "Polarity", "ActivityRef", "SelfRef"]
        print(f"  {dict(zip(labels, vals))}")

    # Artículos que mencionan China en Themes o Organizations
    china_gkg = df_gkg[
        df_gkg["V2Themes"].str.contains("CHINA|CHN", na=False) |
        df_gkg["V2Organizations"].str.contains("China|chinese", case=False, na=False)
    ]
    print(f"\nArtículos GKG con China en themes/orgs (este slice): {len(china_gkg)}")
    if len(china_gkg) > 0:
        print(china_gkg[["SourceCommonName", "DocumentIdentifier", "V2Tone"]].head(5).to_string())
