"""
Script 18 — Dataset final curado para la tesis
Combina señales de Events + GKG para producir el dataset limpio de
proyectos chinos disrumpidos/cancelados en LATAM (2017-2024).

Criterios de inclusión:
  A. Eventos con mecanismo identificado + URL relevante a inversión china
  B. Clusters GKG con ≥5 artículos + SOE_OIL / SOE_MARITIME / SOE_MINING / SOE_HARBOUR
     (excluye SOE_TELECOM masivo de sanciones Huawei que no son proyectos BRI)

Output:
  - data/samples/final/latam_bri_signals_final.csv    (señales LATAM curadas)
  - data/samples/final/latam_bri_signals_final.md     (narrativa para tesis)
  - data/samples/final/global_bri_signals_final.csv  (global top señales)
"""

import os
import re
import pandas as pd
import numpy as np

os.makedirs("data/samples/final", exist_ok=True)

FIPS = {
    "CI":"Chile","AR":"Argentina","BR":"Brasil","MX":"México","PE":"Perú",
    "CO":"Colombia","VE":"Venezuela","BL":"Bolivia","EC":"Ecuador","UY":"Uruguay",
    "PA":"Paraguay","PM":"Panamá","CU":"Cuba","GT":"Guatemala","NU":"Nicaragua",
    "ES":"El Salvador","HO":"Honduras","BH":"Belice","DR":"Dom.Rep.",
    "GY":"Guyana","NS":"Suriname","CS":"Costa Rica","JM":"Jamaica","HA":"Haití",
    "PK":"Pakistán","AF":"Afganistán","KE":"Kenia","TZ":"Tanzania",
    "ET":"Etiopía","GH":"Ghana","ZA":"Zambia","ZI":"Zimbabwe",
    "MY":"Malasia","ID":"Indonesia","VM":"Vietnam","CB":"Camboya",
    "LA":"Laos","BM":"Myanmar","RP":"Filipinas","TH":"Tailandia",
    "SI":"Serbia","HU":"Hungría","BK":"Bosnia",
}
LATAM = set(list(FIPS.keys())[:24])  # primeras 24 = LATAM

# ── A. Señales confirmadas de Events con mecanismo ───────────────────────────
print("=== A. Señales Events con mecanismo identificado ===")
df = pd.read_csv("data/samples/bri_investment_events_all.csv")
df["year"] = df["SQLDATE"] // 10000
df["pais"] = df["ActionGeo_CountryCode"].map(FIPS).fillna(df["ActionGeo_CountryCode"])
df["region"] = df["ActionGeo_CountryCode"].apply(
    lambda c: "LATAM" if c in LATAM else "Global"
)

# Filtrar: mecanismo identificado + excluyendo urls claramente irrelevantes
df_identified = df[df["mechanism"] != "unknown"].copy()

# Score de relevancia: penalizar URLs que hablan de otro país (ruido geográfico)
NOISE_PATTERNS = [
    r"iran\b", r"korea\b", r"north.korea", r"nkorea", r"syria\b",
    r"russia\b", r"ukraine\b", r"pakistan\b", r"afghanistan\b",
    r"crime", r"drug.cartel", r"fentanyl", r"trafficking", r"arrest",
    r"murder", r"robbery", r"gang\b", r"prison\b",
]
SIGNAL_PATTERNS = [
    r"invest", r"project", r"infrastructure", r"port", r"oil",
    r"pipeline", r"railway", r"dam", r"loan", r"debt", r"bri\b",
    r"silk.road", r"cpec", r"concession", r"mining", r"telecom",
    r"huawei", r"zte", r"cosco", r"sinopec", r"petrochina", r"cnpc",
    r"unipec", r"sanctions.venezuela", r"venezuela.sanction",
    r"china.sanction", r"chinese.sanction", r"cancel", r"suspend",
    r"halt", r"renegotiat", r"arbitrat",
]

def score_url(url: str) -> int:
    url = str(url).lower()
    noise = sum(1 for p in NOISE_PATTERNS if re.search(p, url))
    signal = sum(1 for p in SIGNAL_PATTERNS if re.search(p, url))
    return signal - noise

df_identified["url_score"] = df_identified["SOURCEURL"].apply(score_url)
df_good = df_identified[df_identified["url_score"] >= 0].copy()

print(f"Eventos con mecanismo: {len(df_identified):,}")
print(f"Eventos relevantes (url_score ≥ 0): {len(df_good):,}")
print(f"  LATAM: {df_good[df_good['ActionGeo_CountryCode'].isin(LATAM)].shape[0]}")

# ── B. Señales GKG LATAM (excluir Telecom noise) ─────────────────────────────
print("\n=== B. Señales GKG LATAM (SOE no-Telecom, ≥5 artículos) ===")
try:
    gkg_clusters = pd.read_csv("data/samples/gkg_latam/gkg_latam_clusters.csv")
    # Excluir SOE_TELECOM (noise Huawei/ZTE sanciones), mantener sectores reales
    INFRA_SOES = ["SOE_OIL","SOE_MARITIME","SOE_MINING","SOE_HARBOUR","SOE_ENERGY",
                  "SOE_RAILWAY","SOE_CONSTRUCT","SOE_FINANCE"]
    gkg_infra = gkg_clusters[
        (gkg_clusters["soe"].isin(INFRA_SOES)) &
        (gkg_clusters["n_articulos"] >= 5)
    ].copy()
    print(f"Clusters GKG infraestructura (≥5 art): {len(gkg_infra)}")
    gkg_infra["pais"] = gkg_infra["pais"]
    print(gkg_infra[["cluster_id","pais","soe","year","n_articulos","avg_tone","min_tone"]].to_string(index=False))
except FileNotFoundError:
    print("⚠️  No se encontró gkg_latam_clusters.csv — ejecutar script 17 primero")
    gkg_infra = pd.DataFrame()

# ── C. Dataset curado LATAM ──────────────────────────────────────────────────
print("\n=== C. Dataset curado — señales LATAM ===")

latam_events = df_good[df_good["ActionGeo_CountryCode"].isin(LATAM)].copy()

# Construir filas de señales curadas
signals = []

# Fuente: Events (mecanismo identificado + URL relevante)
for _, row in latam_events.iterrows():
    signals.append({
        "source": "Events",
        "pais": row["pais"],
        "cc": row["ActionGeo_CountryCode"],
        "year": row["year"],
        "date": str(row["SQLDATE"]),
        "mechanism": row["mechanism"],
        "actor1": str(row.get("Actor1Name","") or ""),
        "actor2": str(row.get("Actor2Name","") or ""),
        "tone": round(row["AvgTone"],2),
        "mentions": row.get("NumMentions",1),
        "soe": "unknown",
        "url": row["SOURCEURL"],
        "url_score": row["url_score"],
        "n_articles": 1,
    })

# Fuente: GKG (clusters infraestructura LATAM)
for _, row in gkg_infra.iterrows():
    signals.append({
        "source": "GKG",
        "pais": row["pais"],
        "cc": row["cc"],
        "year": row["year"],
        "date": str(row["year"]),
        "mechanism": "confirmed_presence",
        "actor1": row["soe"],
        "actor2": "",
        "tone": row["avg_tone"],
        "mentions": row["n_articulos"] * 10,  # proxy
        "soe": row["soe"],
        "url": row["url_representativa"],
        "url_score": 1,
        "n_articles": row["n_articulos"],
    })

df_final = pd.DataFrame(signals)

# Deduplicar por (pais, year, mechanism) tomando el más negativo
df_final_dedup = df_final.sort_values("tone").groupby(
    ["pais","year","mechanism","soe"]
).first().reset_index()

print(f"Total señales curadas: {len(df_final_dedup)}")
print(f"Fuente Events: {(df_final_dedup['source']=='Events').sum()}")
print(f"Fuente GKG: {(df_final_dedup['source']=='GKG').sum()}")

# ── Ranking por relevancia ───────────────────────────────────────────────────
df_final_dedup["relevancia"] = (
    -df_final_dedup["tone"] *
    np.log1p(df_final_dedup["n_articles"]) *
    df_final_dedup["url_score"].clip(lower=0.1)
).round(2)

df_ranked = df_final_dedup.sort_values("relevancia", ascending=False)

pd.set_option("display.max_colwidth", 110)
print("\n=== Top señales LATAM curadas (por relevancia) ===")
print(df_ranked[[
    "pais","year","mechanism","soe","tone","n_articles","url_score","source","url"
]].head(40).to_string(index=False))

# ── Resumen por país ─────────────────────────────────────────────────────────
print("\n=== Señales por país ===")
by_pais = df_ranked.groupby("pais").agg(
    n_señales=("relevancia","count"),
    tono_min=("tone","min"),
    tono_medio=("tone","mean"),
    mecanismos=("mechanism", lambda x: ",".join(sorted(set(x))))
).sort_values("n_señales", ascending=False)
by_pais["tono_medio"] = by_pais["tono_medio"].round(2)
print(by_pais.to_string())

# ── Resumen por mecanismo ────────────────────────────────────────────────────
print("\n=== Señales por mecanismo ===")
by_mech = df_ranked.groupby("mechanism").agg(
    n=("relevancia","count"),
    n_paises=("pais","nunique"),
    tono_medio=("tone","mean"),
).sort_values("n", ascending=False)
by_mech["tono_medio"] = by_mech["tono_medio"].round(2)
print(by_mech.to_string())

# ── Dataset global (los más relevantes de todo el mundo) ────────────────────
print("\n=== Global — señales no-LATAM con mecanismo identificado ===")
global_signals = df_good[~df_good["ActionGeo_CountryCode"].isin(LATAM)].copy()
global_signals = global_signals.nsmallest(30, "AvgTone")[
    ["SQLDATE","pais","Actor1Name","Actor2Name","AvgTone","mechanism","SOURCEURL"]
]
print(global_signals.to_string(index=False))

# ── Guardar ──────────────────────────────────────────────────────────────────
df_ranked.to_csv("data/samples/final/latam_bri_signals_final.csv", index=False)

# Guardar versión global también
global_df = df_good.sort_values("AvgTone").head(200)
global_df.to_csv("data/samples/final/global_bri_signals_final.csv", index=False)

# Narrativa markdown para la tesis
with open("data/samples/final/latam_bri_signals_final.md", "w") as f:
    f.write("# Señales BRI LATAM — Dataset Final Curado (GDELT 2017-2024)\n\n")
    f.write("## Metodología\n")
    f.write("- Fuente Events: eventos con actor CHN + mecanismo identificado (no-unknown) + URL relevante\n")
    f.write("- Fuente GKG: clusters de artículos (SOE sectorial × país × año) con ≥5 artículos, excluyendo SOE_TELECOM (noise Huawei)\n")
    f.write("- Relevancia = |tono| × log(n_artículos) × url_score\n\n")
    f.write("## Resumen por país\n\n")
    f.write("| País | N señales | Tono mín | Mecanismos |\n")
    f.write("|------|-----------|----------|------------|\n")
    for pais, row in by_pais.iterrows():
        f.write(f"| {pais} | {int(row['n_señales'])} | {row['tono_min']:.2f} | {row['mecanismos']} |\n")
    f.write("\n## Señales individuales (top 30 por relevancia)\n\n")
    f.write("| País | Año | Mecanismo | SOE | Tono | Fuente | URL |\n")
    f.write("|------|-----|-----------|-----|------|--------|-----|\n")
    for _, row in df_ranked.head(30).iterrows():
        f.write(f"| {row['pais']} | {row['year']} | {row['mechanism']} | {row['soe']} | "
                f"{row['tone']:.2f} | {row['source']} | [{row['url'][:60]}...]({row['url']}) |\n")
    f.write("\n## Casos conocidos validados\n\n")
    KNOWN = {
        ("Venezuela","us_sanctions"): "Venezuela CNPC/Unipec/ZTE — sanciones secundarias EEUU",
        ("Chile","environmental_opposition"): "Chile — restricción flota pesca china",
        ("Perú","project_failure"): "Perú — reclamo arbitraje puerto COSCO Chancay",
        ("Argentina","environmental_opposition"): "Argentina — demora acuerdo cerdo China por protestas ambientales",
        ("Venezuela","debt_renegotiation"): "Venezuela — reestructuración deuda China/Rusia",
        ("Brasil","political_rejection"): "Brasil — JBS escándalo carne afecta exportaciones China",
    }
    for (pais, mech), desc in KNOWN.items():
        found = df_ranked[(df_ranked["pais"]==pais) & (df_ranked["mechanism"]==mech)]
        status = "✓ ENCONTRADO" if len(found) > 0 else "✗ NO ENCONTRADO"
        f.write(f"- **{desc}**: {status} ({len(found)} señales)\n")

print(f"\n✓ Archivos guardados en data/samples/final/")

# ── Actualizar ANALYSIS_FINDINGS.md ─────────────────────────────────────────
with open("docs/ANALYSIS_FINDINGS.md", "a") as f:
    f.write("\n## Script 18 — Dataset Final Curado LATAM\n\n")
    f.write(f"### Total señales curadas: {len(df_final_dedup)}\n")
    f.write(f"- Events con mecanismo: {(df_final_dedup['source']=='Events').sum()}\n")
    f.write(f"- GKG infraestructura: {(df_final_dedup['source']=='GKG').sum()}\n\n")
    f.write("### Por país\n")
    for pais, row in by_pais.iterrows():
        f.write(f"- **{pais}**: {int(row['n_señales'])} señales, tono mín {row['tono_min']:.2f}\n")
    f.write("\n### Por mecanismo\n")
    for mech, row in by_mech.iterrows():
        f.write(f"- `{mech}`: {int(row['n'])} señales en {int(row['n_paises'])} países\n")
    f.write("\n### Archivos generados\n")
    f.write("- `data/samples/final/latam_bri_signals_final.csv` — dataset curado LATAM\n")
    f.write("- `data/samples/final/latam_bri_signals_final.md` — narrativa para tesis\n")
    f.write("- `data/samples/final/global_bri_signals_final.csv` — señales globales\n")

print("✓ ANALYSIS_FINDINGS.md actualizado")
print("\n=== SCRIPT 18 COMPLETO — PIPELINE FINALIZADO ===")
print("Archivos para la tesis:")
print("  → data/samples/final/latam_bri_signals_final.csv")
print("  → data/samples/final/latam_bri_signals_final.md")
