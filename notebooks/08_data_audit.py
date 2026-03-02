"""
Script 08 — Auditoría y deduplicación de los dos datasets Events
Datasets: events_china_conflict_2017_2024.csv (374k) y events_china_economic_2017_2024.csv (76k)

Objetivos:
  1. Cuántos artículos únicos hay realmente (dedup por SOURCEURL)
  2. Calidad de datos: nulos, FIPS mal asignados, columnas clave
  3. Distribución de duplicados: cuántas filas repiten la misma URL
  4. Output: versiones deduplicadas + reporte de calidad en docs/ANALYSIS_FINDINGS.md
"""

import os
import pandas as pd

os.makedirs("data/samples", exist_ok=True)
os.makedirs("docs", exist_ok=True)

FIPS_PAISES = {
    "CH": "China", "CI": "Chile", "AR": "Argentina", "BR": "Brasil",
    "MX": "México", "PE": "Perú", "CO": "Colombia", "VE": "Venezuela",
    "BL": "Bolivia", "EC": "Ecuador", "UY": "Uruguay", "PA": "Paraguay",
    "PM": "Panamá", "CU": "Cuba", "DO": "República Dominicana",
    "US": "Estados Unidos", "RS": "Rusia", "UK": "Reino Unido",
    "GM": "Alemania", "FR": "Francia", "AU": "Australia", "IN": "India",
    "PK": "Pakistán", "KN": "Kenia", "SF": "Sudáfrica", "NI": "Nigeria",
    "EG": "Egipto", "ET": "Etiopía", "TW": "Taiwan", "KS": "Corea del Sur",
    "KN": "Kenia",
}


def audit_dataset(path: str, label: str) -> pd.DataFrame:
    print(f"\n{'='*60}")
    print(f"=== {label} ===")
    print(f"{'='*60}")

    df = pd.read_csv(path)
    print(f"\nShape original: {df.shape}")
    print(f"Columnas: {list(df.columns)}")

    # --- Nulos por columna clave ---
    key_cols = [c for c in ["SQLDATE", "Actor1CountryCode", "Actor2CountryCode",
                             "ActionGeo_CountryCode", "EventCode", "AvgTone",
                             "NumMentions", "SOURCEURL"] if c in df.columns]
    print("\n--- Nulos en columnas clave ---")
    for col in key_cols:
        n_null = df[col].isna().sum()
        pct = n_null / len(df) * 100
        if n_null > 0:
            print(f"  {col}: {n_null:,} nulos ({pct:.1f}%)")

    # --- Deduplicación por SOURCEURL ---
    n_total = len(df)
    df_dedup = df.dropna(subset=["SOURCEURL"]).drop_duplicates(subset=["SOURCEURL"])
    n_dedup = len(df_dedup)
    print(f"\n--- Deduplicación por SOURCEURL ---")
    print(f"  Total filas:          {n_total:,}")
    print(f"  URLs únicas:          {n_dedup:,}  ({n_dedup/n_total*100:.1f}%)")
    print(f"  Filas duplicadas:     {n_total - n_dedup:,}  ({(n_total-n_dedup)/n_total*100:.1f}%)")

    # Top URLs repetidas
    url_counts = df["SOURCEURL"].value_counts()
    print(f"\n  Distribución de repeticiones:")
    for n_rep, count in url_counts.value_counts().sort_index().head(6).items():
        print(f"    {n_rep} veces: {count:,} URLs")
    print(f"  URL más repetida ({url_counts.iloc[0]} veces): {url_counts.index[0][:80]}")

    # --- Distribución FIPS ActionGeo ---
    print("\n--- Top 20 países ActionGeo_CountryCode (FIPS) ---")
    fips_counts = df["ActionGeo_CountryCode"].value_counts().head(20)
    for fips, n in fips_counts.items():
        nombre = FIPS_PAISES.get(fips, f"?? ({fips})")
        print(f"  {fips:4s} {nombre:25s} {n:>8,}")

    # --- Rango temporal ---
    df["year"] = df["SQLDATE"] // 10000
    print(f"\n--- Rango temporal ---")
    print(f"  {df['year'].min()} → {df['year'].max()}")
    print(df.groupby("year").size().rename("n").to_string())

    # --- Guardar dedup ---
    out_path = path.replace(".csv", "_dedup.csv")
    df_dedup["year"] = df_dedup["SQLDATE"] // 10000
    df_dedup.to_csv(out_path, index=False)
    print(f"\n✓ Dedup guardado: {out_path} — {len(df_dedup):,} filas")

    return df_dedup


# --- Ejecutar auditoría en ambos datasets ---
df_conflict = audit_dataset(
    "data/samples/events_china_conflict_2017_2024.csv",
    "CONFLICTO (374k) — China + EventRootCode 12-19 + AvgTone < -5"
)

df_economic = audit_dataset(
    "data/samples/events_china_economic_2017_2024.csv",
    "ECONÓMICO (76k) — EventCode 163/164/165"
)

# --- Análisis cruzado ---
print("\n" + "="*60)
print("=== ANÁLISIS CRUZADO ===")
print("="*60)

urls_conflict = set(df_conflict["SOURCEURL"].dropna())
urls_economic = set(df_economic["SOURCEURL"].dropna())
overlap = urls_conflict & urls_economic
print(f"\nURLs en conflicto:  {len(urls_conflict):,}")
print(f"URLs en económico:  {len(urls_economic):,}")
print(f"URLs en ambos:      {len(overlap):,}  ({len(overlap)/len(urls_economic)*100:.1f}% del económico)")

# --- Actualizar ANALYSIS_FINDINGS.md ---
findings_path = "docs/ANALYSIS_FINDINGS.md"
with open(findings_path, "w") as f:
    f.write("# Hallazgos del análisis de datos GDELT Events\n\n")
    f.write("## Script 08 — Auditoría y deduplicación\n\n")
    f.write("### Dataset Conflicto\n")
    f.write(f"- Original: 374,108 filas\n")
    f.write(f"- Post-dedup (URLs únicas): {len(df_conflict):,} artículos reales\n")
    f.write(f"- Reducción: {374108 - len(df_conflict):,} filas duplicadas\n\n")
    f.write("### Dataset Económico\n")
    f.write(f"- Original: 76,771 filas\n")
    f.write(f"- Post-dedup (URLs únicas): {len(df_economic):,} artículos reales\n")
    f.write(f"- Reducción: {76771 - len(df_economic):,} filas duplicadas\n\n")
    f.write(f"### Overlap entre datasets\n")
    f.write(f"- {len(overlap):,} URLs aparecen en ambos datasets\n\n")
    f.write("### FIPS críticos\n")
    f.write("- `CH` = China (NO Chile). Chile = `CI`\n")
    f.write("- Bug presente en scripts anteriores que usaban 'CH' para Chile\n\n")
    f.write("### Próximo paso\n")
    f.write("- Script 09: taxonomía de contextos (separar guerra comercial de BRI/inversión)\n")

print(f"\n✓ Hallazgos guardados en {findings_path}")
print("\n=== PRÓXIMO PASO: script 09_false_positive_filter.py ===")
print("Analizar resultados y definir criterios de clasificación antes de ejecutarlo.")
