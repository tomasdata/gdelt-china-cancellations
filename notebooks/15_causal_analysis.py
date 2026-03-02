"""
Script 15 — Análisis causal de mecanismos de cancelación
Input:
  - data/samples/events_conflict_classified.csv (mecanismo en filas BRI)
  - data/samples/events_economic_classified.csv
  - data/samples/clusters/project_candidates_events_v2.csv

Preguntas:
  1. ¿Crecen las sanciones EEUU después de 2018/2019?
  2. ¿Crecen protestas ambientales post-2019 (ESG)?
  3. ¿Dominan restructuraciones de deuda en 2020-2022 (COVID)?
  4. ¿Qué mecanismo domina en LATAM vs África vs Asia?

Output:
  - data/samples/causal/mechanism_by_region_year.csv
  - data/samples/causal/mechanism_by_sector.csv  (usando SOE de GKG)
  - data/samples/causal/us_sanctions_timeline.csv (sanciones por año)
"""

import os
import re
import pandas as pd
import numpy as np

os.makedirs("data/samples/causal", exist_ok=True)

# ── Cargar datos ─────────────────────────────────────────────────────────────
conf = pd.read_csv("data/samples/events_conflict_classified.csv")
econ = pd.read_csv("data/samples/events_economic_classified.csv")

# Usar solo eventos BRI
bri_conf = conf[conf["context"] == "bri_investment"].copy()
bri_econ = econ[econ["context"] == "bri_investment"].copy()
bri_all = pd.concat([bri_conf, bri_econ], ignore_index=True)
bri_all = bri_all.drop_duplicates(subset=["SOURCEURL"])

print(f"Eventos BRI analizados: {len(bri_all):,}")
print(f"  Conflicto: {len(bri_conf):,} | Económico: {len(bri_econ):,}")
print(f"  Overlap eliminado: {len(bri_conf)+len(bri_econ)-len(bri_all)}")

# Map geo
FIPS = {
    "CI":"Chile","AR":"Argentina","BR":"Brasil","MX":"México","PE":"Perú",
    "CO":"Colombia","VE":"Venezuela","BL":"Bolivia","EC":"Ecuador","UY":"Uruguay",
    "PA":"Paraguay","PM":"Panamá","CU":"Cuba","GT":"Guatemala","NU":"Nicaragua",
    "ES":"El Salvador","HO":"Honduras","BH":"Belice","DR":"Dom.Rep.",
    "GY":"Guyana","NS":"Suriname","CS":"Costa Rica","JM":"Jamaica","HA":"Haití",
    "SF":"Sudáfrica","NI":"Nigeria","ET":"Etiopía","KE":"Kenia","AO":"Angola",
    "UG":"Uganda","TZ":"Tanzania","MZ":"Mozambique","ZA":"Zambia","GH":"Ghana",
    "CM":"Camerún","SN":"Senegal","ZI":"Zimbabwe","EG":"Egipto","DJ":"Djibouti",
    "PK":"Pakistán","BD":"Bangladesh","NP":"Nepal","AF":"Afganistán",
    "UZ":"Uzbekistán","KZ":"Kazajistán","TM":"Turkmenistán","KG":"Kirguistán",
    "RP":"Filipinas","TH":"Tailandia","MY":"Malasia","ID":"Indonesia",
    "VM":"Vietnam","CB":"Camboya","BM":"Myanmar","LA":"Laos",
    "UP":"Ucrania","PL":"Polonia","HU":"Hungría","RO":"Rumanía",
    "BK":"Bosnia","HR":"Croacia","SI":"Serbia","MK":"Macedonia","MN":"Montenegro",
    "IZ":"Irak","IR":"Irán","SA":"Arabia Saudita","AE":"Emiratos","QA":"Qatar",
    "IS":"Israel","JO":"Jordania","SY":"Siria","TU":"Turquía",
    "PP":"Papua N.Guinea","FJ":"Fiji","WS":"Samoa","TO":"Tonga",
}
REGIONS = {
    "LATAM":    {"CI","AR","BR","MX","PE","CO","VE","BL","EC","UY","PA","PM","CU","GT",
                 "NU","ES","HO","BH","DR","GY","NS","CS","JM","HA"},
    "Africa":   {"SF","NI","ET","KE","AO","UG","TZ","MZ","ZA","GH","CM","SN","ZI","EG",
                 "DJ","IV","CG","ML","CF"},
    "Asia_C":   {"PK","BD","NP","AF","UZ","KZ","TM","KG","TJ"},
    "Asia_SE":  {"RP","TH","MY","ID","VM","CB","BM","LA"},
    "Europa_E": {"UP","PL","HU","RO","BK","HR","SI","AL","MN","GG","AJ","AM"},
    "MedioO":   {"IZ","IR","SA","AE","QA","IS","JO","SY","LE","YM","TU"},
    "Oceania":  {"PP","FJ","WS","TO"},
}

bri_all["year"] = bri_all["SQLDATE"] // 10000
bri_all["region"] = bri_all["ActionGeo_CountryCode"].apply(
    lambda c: next((r for r, s in REGIONS.items() if c in s), "Other")
)
bri_all["pais"] = bri_all["ActionGeo_CountryCode"].map(FIPS).fillna(bri_all["ActionGeo_CountryCode"])

# ── 1. Distribución global de mecanismos ────────────────────────────────────
print("\n=== 1. Distribución global de mecanismos BRI ===")
mech_global = bri_all.groupby("mechanism").agg(
    n=("SOURCEURL", "count"),
    pct=("SOURCEURL", lambda x: len(x)/len(bri_all)*100),
    avg_tone=("AvgTone", "mean"),
    n_paises=("ActionGeo_CountryCode", "nunique"),
).sort_values("n", ascending=False)
mech_global["pct"] = mech_global["pct"].round(1)
mech_global["avg_tone"] = mech_global["avg_tone"].round(2)
print(mech_global.to_string())

# ── 2. Mecanismos por año (¿crecen sanciones post-2018?) ───────────────────
print("\n=== 2. Mecanismos por año (normalizado) ===")
mech_year = bri_all.groupby(["year", "mechanism"])["SOURCEURL"].count().unstack(fill_value=0)
# Normalizar por total del año
mech_year_pct = mech_year.div(mech_year.sum(axis=1), axis=0).mul(100).round(1)
print("\nAbsoluto:")
print(mech_year.to_string())
print("\nPorcentaje por año:")
print(mech_year_pct.to_string())
mech_year.to_csv("data/samples/causal/mechanism_by_year.csv")

# ── 3. Sanciones EEUU: ¿pre vs post-2018? ──────────────────────────────────
print("\n=== 3. US Sanctions — evolución temporal ===")
sanctions = bri_all[bri_all["mechanism"] == "us_sanctions"].copy()
sanctions_year = sanctions.groupby("year").agg(
    n=("SOURCEURL", "count"),
    n_paises=("ActionGeo_CountryCode", "nunique"),
    avg_tone=("AvgTone", "mean"),
).sort_index()
sanctions_year["avg_tone"] = sanctions_year["avg_tone"].round(2)
print(sanctions_year.to_string())

# Pre/post 2018 comparison
pre_2018 = bri_all[bri_all["year"] < 2018]
post_2018 = bri_all[bri_all["year"] >= 2018]
sanc_pct_pre = (pre_2018["mechanism"] == "us_sanctions").sum() / len(pre_2018) * 100
sanc_pct_post = (post_2018["mechanism"] == "us_sanctions").sum() / len(post_2018) * 100
print(f"\n  % Sanciones pre-2018:  {sanc_pct_pre:.2f}%")
print(f"  % Sanciones post-2018: {sanc_pct_post:.2f}%")
print(f"  Ratio post/pre: {sanc_pct_post/sanc_pct_pre:.1f}x" if sanc_pct_pre > 0 else "  (pre-2018 = 0)")

# ── 4. Mecanismos por región ─────────────────────────────────────────────────
print("\n=== 4. Mecanismos por región ===")
mech_region = bri_all.groupby(["region", "mechanism"]).size().unstack(fill_value=0)
mech_region_pct = mech_region.div(mech_region.sum(axis=1), axis=0).mul(100).round(1)
print("\nAbsoluto:")
print(mech_region.to_string())
print("\nPorcentaje por región:")
print(mech_region_pct.to_string())
mech_region.to_csv("data/samples/causal/mechanism_by_region.csv")

# ── 5. Mecanismos × región × año (pivot 3D) ─────────────────────────────────
print("\n=== 5. Mecanismos significativos × región × año ===")
MECH_FOCUS = ["us_sanctions", "environmental_opposition", "political_rejection",
               "debt_renegotiation", "project_failure"]
for mech in MECH_FOCUS:
    sub = bri_all[bri_all["mechanism"] == mech]
    if len(sub) == 0:
        continue
    pivot = sub.groupby(["region", "year"]).size().unstack(fill_value=0)
    print(f"\n--- {mech} ({len(sub)} eventos) ---")
    print(pivot.to_string())

# ── 6. LATAM deep dive ───────────────────────────────────────────────────────
print("\n=== 6. LATAM — mecanismos por país ===")
latam = bri_all[bri_all["region"] == "LATAM"]
latam_mech = latam.groupby(["pais", "mechanism"]).size().unstack(fill_value=0)
print(latam_mech.to_string())

print("\n--- Top LATAM eventos con mecanismo identificado ---")
latam_nontrivial = latam[latam["mechanism"] != "unknown"].sort_values("AvgTone")
pd.set_option("display.max_colwidth", 90)
print(latam_nontrivial[["SQLDATE", "pais", "Actor1Name", "Actor2Name",
                          "AvgTone", "mechanism", "SOURCEURL"]].head(30).to_string(index=False))

# ── 7. África sanciones y deuda ──────────────────────────────────────────────
print("\n=== 7. África — mecanismos ===")
africa = bri_all[bri_all["region"] == "Africa"]
print(f"Total eventos BRI África: {len(africa):,}")
print(africa.groupby(["pais", "mechanism"]).size().unstack(fill_value=0).to_string())

# ── 8. Tono por mecanismo vs desconocido ────────────────────────────────────
print("\n=== 8. Tono medio por mecanismo ===")
tone_mech = bri_all.groupby("mechanism")["AvgTone"].describe()[["mean","min","50%","count"]]
tone_mech["mean"] = tone_mech["mean"].round(2)
tone_mech["min"] = tone_mech["min"].round(2)
tone_mech["50%"] = tone_mech["50%"].round(2)
print(tone_mech.sort_values("mean").to_string())

# ── 9. Análisis de URL keywords para mecanismos desconocidos ────────────────
# ¿Qué temas aparecen en eventos 'unknown' con tono muy negativo?
print("\n=== 9. Keywords en eventos 'unknown' con tono < -8 ===")
unknown_neg = bri_all[(bri_all["mechanism"] == "unknown") & (bri_all["AvgTone"] < -8)]
print(f"Eventos unknown con tono < -8: {len(unknown_neg):,}")

# Extraer keywords de URL
from collections import Counter
url_words = Counter()
for url in unknown_neg["SOURCEURL"].dropna():
    words = re.findall(r"[a-z]{4,}", str(url).lower())
    url_words.update(words)

# Filtrar palabras triviales
STOP = {"https","http","html","news","com","www","article","post","story",
        "2017","2018","2019","2020","2021","2022","2023","2024","page","read",
        "home","site","view","index","media","blog","world","time","from",
        "content","category","topics","title","politics","sport","local"}
signal_words = [(w, c) for w, c in url_words.most_common(100) if w not in STOP]
print("Top 30 keywords en URLs de unknown-negativo:")
for w, c in signal_words[:30]:
    print(f"  {c:5d}  {w}")

# ── 10. Candidatos de clusters con mecanismo específico ─────────────────────
print("\n=== 10. Candidatos clusters × mecanismo ===")
cand = pd.read_csv("data/samples/clusters/project_candidates_events_v2.csv")
print(cand.groupby("mechanism_dominante").agg(
    n=("cluster_id", "count"),
    avg_tone=("tono_medio", "mean"),
    avg_menciones=("menciones_total", "mean"),
    avg_eventos=("n_eventos", "mean"),
).round(2).sort_values("n", ascending=False).to_string())

# ── Guardar ──────────────────────────────────────────────────────────────────
mech_region.to_csv("data/samples/causal/mechanism_by_region.csv")
sanctions_year.to_csv("data/samples/causal/us_sanctions_timeline.csv")
mech_year.to_csv("data/samples/causal/mechanism_by_year.csv")
print("\n✓ Archivos guardados en data/samples/causal/")

# ── Actualizar ANALYSIS_FINDINGS.md ─────────────────────────────────────────
with open("docs/ANALYSIS_FINDINGS.md", "a") as f:
    f.write("\n## Script 15 — Análisis causal de mecanismos\n\n")
    f.write(f"### Input: {len(bri_all):,} eventos BRI clasificados\n\n")
    f.write("### Distribución global de mecanismos\n")
    for mech, row in mech_global.iterrows():
        f.write(f"- `{mech}`: {int(row['n']):,} eventos ({row['pct']:.1f}%), tono {row['avg_tone']:.2f}\n")
    f.write("\n### Dinámica temporal de sanciones EEUU\n")
    f.write(f"- Pre-2018: {sanc_pct_pre:.2f}% de eventos BRI son sanciones US\n")
    f.write(f"- Post-2018: {sanc_pct_post:.2f}% de eventos BRI son sanciones US\n")
    if sanc_pct_pre > 0:
        f.write(f"- Ratio: {sanc_pct_post/sanc_pct_pre:.1f}x mayor post-2018\n")
    f.write("\n### Mecanismos por región (top no-unknown)\n")
    for region in mech_region.index:
        row = mech_region_pct.loc[region]
        top_mech = row[row.index != "unknown"].sort_values(ascending=False).head(2)
        parts = [f"{m}={v:.1f}%" for m, v in top_mech.items() if v > 0]
        if parts:
            f.write(f"- **{region}**: {', '.join(parts)}\n")
    f.write("\n### Próximo paso\n")
    f.write("- Script 16: validación cruzada Events × GKG\n")

print("✓ ANALYSIS_FINDINGS.md actualizado")
print("\n=== SCRIPT 15 COMPLETO ===")
