"""
Script 01 — Exploración de archivos CSV públicos de GDELT v2
Objetivo: entender qué hay en lastupdate.txt, descargar un slice pequeño
de events, y documentar el schema real.

Hallazgo previo: api.gdeltproject.org no accesible desde este entorno.
Alternativa: data.gdeltproject.org/gdeltv2/ (HTTP, funciona perfectamente).
"""

import requests
import zipfile
import io
import pandas as pd

LASTUPDATE_URL = "http://data.gdeltproject.org/gdeltv2/lastupdate.txt"

def fetch_lastupdate() -> dict[str, str]:
    """Retorna los URLs de los 3 archivos de la última actualización."""
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


def download_csv(url: str) -> pd.DataFrame:
    """Descarga un ZIP de GDELT y lo retorna como DataFrame."""
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    z = zipfile.ZipFile(io.BytesIO(resp.content))
    csv_name = z.namelist()[0]
    with z.open(csv_name) as f:
        # GDELT events no tiene header — se carga sin él
        df = pd.read_csv(f, sep="\t", header=None, low_memory=False)
    return df


if __name__ == "__main__":
    print("=== Paso 1: lastupdate.txt ===")
    files = fetch_lastupdate()
    for k, v in files.items():
        print(f"  {k}: {v}")

    print("\n=== Paso 2: Descargar events (export) ===")
    df_events = download_csv(files["events"])
    print(f"  Filas: {len(df_events)}")
    print(f"  Columnas: {df_events.shape[1]}")
    print(f"  Primeras 5 filas (primeras 10 columnas):")
    print(df_events.iloc[:5, :10].to_string())
    print(f"\n  Tipos de datos:")
    print(df_events.dtypes.head(20))

    # Guardar muestra
    df_events.head(100).to_csv("data/samples/events_sample_100rows.csv",
                               index=False, header=False)
    print("\n  ✓ Muestra guardada en data/samples/events_sample_100rows.csv")

    print("\n=== Paso 3: Descargar GKG ===")
    df_gkg = download_csv(files["gkg"])
    print(f"  Filas: {len(df_gkg)}")
    print(f"  Columnas: {df_gkg.shape[1]}")
    print(f"  Primeras 3 filas (primeras 8 columnas):")
    print(df_gkg.iloc[:3, :8].to_string())

    df_gkg.head(50).to_csv("data/samples/gkg_sample_50rows.csv",
                            index=False, header=False)
    print("\n  ✓ Muestra guardada en data/samples/gkg_sample_50rows.csv")
