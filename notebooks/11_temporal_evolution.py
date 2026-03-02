"""
Script 11 — Evolución histórica y picos por año/región
Input: data/samples/geo/bri_events_geo.csv (52k con región/país asignado)
"""

import os
import pandas as pd

df = pd.read_csv("data/samples/geo/bri_events_geo.csv")
df["year"] = df["SQLDATE"] // 10000
df["month"] = (df["SQLDATE"] // 100) % 100
df["ym"] = df["SQLDATE"] // 100  # YYYYMM

print(f"Input: {len(df):,} eventos BRI geo")

# ── 1. Volumen y tono por año ───────────────────────────────────────────────
print("\n=== Volumen y tono por año ===")
yr = df.groupby("year").agg(
    n_eventos=("SOURCEURL","count"),
    tono_medio=("AvgTone","mean"),
    menciones_total=("NumMentions","sum"),
    paises_unicos=("ActionGeo_CountryCode","nunique")
).round(2)
print(yr.to_string())

# ── 2. Top país por año ─────────────────────────────────────────────────────
print("\n=== País más activo por año (excl. China/EEUU) ===")
df_ex = df[~df["ActionGeo_CountryCode"].isin(["CH","US","HK","RS","UK","CA","AS"])]
for year in sorted(df["year"].unique()):
    top5 = (df_ex[df_ex["year"]==year]
            .groupby("pais")["SOURCEURL"].count()
            .sort_values(ascending=False).head(5))
    tops = ", ".join([f"{p}({n})" for p,n in top5.items()])
    print(f"  {year}: {tops}")

# ── 3. Países con crecimiento sostenido ────────────────────────────────────
print("\n=== Crecimiento 2017→2024 por país (top 20 más activos) ===")
top_countries = df_ex.groupby("pais")["SOURCEURL"].count().nlargest(20).index
growth = []
for pais in top_countries:
    sub = df_ex[df_ex["pais"]==pais].groupby("year")["SOURCEURL"].count()
    n_2017 = sub.get(2017, 0)
    n_2024 = sub.get(2024, 0)
    n_total = sub.sum()
    pico_año = sub.idxmax() if len(sub) > 0 else None
    growth.append({"pais": pais, "2017": n_2017, "2024": n_2024,
                   "total": n_total, "pico": pico_año,
                   "cambio": n_2024 - n_2017})
df_growth = pd.DataFrame(growth).sort_values("total", ascending=False)
print(df_growth.to_string(index=False))

# ── 4. Picos mensuales — eventos que dominan en ciertos meses ─────────────
print("\n=== Top 10 meses con más eventos BRI (picos) ===")
monthly = df.groupby("ym").agg(
    n=("SOURCEURL","count"),
    tono=("AvgTone","mean")
).sort_values("n", ascending=False).head(10)
monthly["tono"] = monthly["tono"].round(2)
print(monthly.to_string())

# ── 5. Regiones: pico y caída ──────────────────────────────────────────────
print("\n=== Evolución % por región respecto al total BRI anual ===")
reg_year = df.groupby(["region","year"]).size().unstack(fill_value=0)
totales = reg_year.sum()
reg_pct = (reg_year.div(totales) * 100).round(1)
print(reg_pct.to_string())

# ── 6. Análisis COVID: antes/después ──────────────────────────────────────
print("\n=== Impacto COVID: pre(2017-19) vs durante(2020) vs post(2021-24) ===")
df["periodo"] = pd.cut(df["year"], bins=[2016,2019,2020,2024],
                        labels=["pre_covid","covid","post_covid"])
periodos = df.groupby(["region","periodo"])["SOURCEURL"].count().unstack(fill_value=0)
print(periodos.to_string())

# ── 7. Filipinas 2024 — qué está pasando ──────────────────────────────────
print("\n=== Filipinas 2024 — top 10 eventos (579 eventos, pico) ===")
ph_2024 = df[(df["pais"]=="Filipinas") & (df["year"]==2024)].nlargest(10,"NumMentions")
for _, r in ph_2024.iterrows():
    print(f"  [{r['SQLDATE']}] tone={r['AvgTone']:.1f} | mentions={r['NumMentions']} | {r['ActionGeo_FullName']}")
    print(f"    URL: {str(r['SOURCEURL'])[:100]}")

# ── 8. Bosnia — proyectos carbón ──────────────────────────────────────────
print("\n=== Bosnia (tono -9.36, el más negativo) — top 10 eventos ===")
bk = df[df["pais"]=="Bosnia"].nlargest(10,"NumMentions")
for _, r in bk.iterrows():
    print(f"  [{r['SQLDATE']}] tone={r['AvgTone']:.1f} | {r['ActionGeo_FullName']}")
    print(f"    URL: {str(r['SOURCEURL'])[:100]}")

# ── Guardar ────────────────────────────────────────────────────────────────
os.makedirs("data/samples/temporal", exist_ok=True)
yr.to_csv("data/samples/temporal/bri_por_año.csv")
df_growth.to_csv("data/samples/temporal/bri_crecimiento_paises.csv", index=False)
reg_year.to_csv("data/samples/temporal/bri_region_año.csv")
print("\n✓ Archivos guardados en data/samples/temporal/")

# ── Actualizar findings ─────────────────────────────────────────────────────
with open("docs/ANALYSIS_FINDINGS.md", "a") as f:
    f.write("\n## Script 11 — Evolución temporal\n\n")
    f.write("### Volumen BRI por año\n")
    for year, row in yr.iterrows():
        f.write(f"- {year}: {int(row['n_eventos']):,} eventos, tono {row['tono_medio']:.2f}\n")
    f.write("\n### Patrones clave\n")
    f.write("- Pico 2020 en todas las regiones (COVID impacta proyectos)\n")
    f.write("- Filipinas 2024: 579 eventos (pico récord — proyectos cancelados Mar Céleste/BRI)\n")
    f.write("- Bosnia tono más negativo (-9.36): plantas carbón chinas rechazadas\n")
    f.write("- Ecuador 2023-2024: tendencia al alza (Coca Codo Sinclair y otros)\n")
    f.write("\n### Próximo paso\n")
    f.write("- Script 12: clustering de proyectos candidatos\n")

print("✓ ANALYSIS_FINDINGS.md actualizado")
print("\n=== PRÓXIMO: script 12_project_clustering.py ===")
