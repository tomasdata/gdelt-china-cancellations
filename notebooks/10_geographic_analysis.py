"""
Script 10 v2 — Análisis geográfico profundo
Input: data/samples/bri_investment_events_all.csv (31k eventos BRI v2)

v2 mejoras:
  - Añadidos GY/NS/CS/JM/HA/BH/DR a FIPS y REGIONS["LATAM"]
  - Fix colisión SN: Senegal=SN (Africa), Singapore removido de Asia_SE (es hub financiero, no BRI)
  - Análisis de mecanismo por región (columna 'mechanism' de script 09 v2)
  - Deep-dive para Guyana (petróleo offshore, interés chino) y Costa Rica (Huawei 5G)
"""

import os
import pandas as pd
from collections import defaultdict

df = pd.read_csv("data/samples/bri_investment_events_all.csv")
df["year"] = df["SQLDATE"] // 10000
print(f"Input: {len(df):,} eventos BRI")

# ── Mapas FIPS completos ────────────────────────────────────────────────────
FIPS = {
    # LATAM
    "CI":"Chile","AR":"Argentina","BR":"Brasil","MX":"México","PE":"Perú",
    "CO":"Colombia","VE":"Venezuela","BL":"Bolivia","EC":"Ecuador","UY":"Uruguay",
    "PA":"Paraguay","PM":"Panamá","CU":"Cuba","GT":"Guatemala","NU":"Nicaragua",
    "ES":"El Salvador","HO":"Honduras","BH":"Belice","DR":"Dom.Rep.",
    # LATAM v2 (añadidos)
    "GY":"Guyana","NS":"Suriname","CS":"Costa Rica","JM":"Jamaica","HA":"Haití",
    # África
    "SF":"Sudáfrica","NI":"Nigeria","ET":"Etiopía","KE":"Kenia","AO":"Angola",
    "UG":"Uganda","TZ":"Tanzania","MZ":"Mozambique","ZA":"Zambia","GH":"Ghana",
    "CM":"Camerún","SN":"Senegal","ZI":"Zimbabwe","EG":"Egipto","LY":"Libia",
    "AL":"Albania","SU":"Sudán","DJ":"Djibouti","MR":"Mauritania","IV":"Costa Marfil",
    "CG":"Congo","CF":"R.C.Africana","ML":"Mali","BU":"Burkina Faso",
    # Asia Central
    "PK":"Pakistán","BD":"Bangladesh","NP":"Nepal","AF":"Afganistán",
    "UZ":"Uzbekistán","KZ":"Kazajistán","TM":"Turkmenistán","KG":"Kirguistán","TJ":"Tayikistán",
    # Asia SE — NOTE: SN removido (colisión con Senegal; Singapore es hub financiero no receptor BRI)
    "RP":"Filipinas","TH":"Tailandia","MY":"Malasia","ID":"Indonesia",
    "VM":"Vietnam","CB":"Camboya","BM":"Myanmar","LA":"Laos",
    # Europa Oriental / Balcanes
    "UP":"Ucrania","PL":"Polonia","HU":"Hungría","RO":"Rumanía",
    "BK":"Bosnia","HR":"Croacia","SI":"Serbia","AL":"Albania","MK":"Macedonia",
    "MN":"Montenegro","GG":"Georgia","AJ":"Azerbaiyán","AM":"Armenia",
    # Medio Oriente
    "IZ":"Irak","IR":"Irán","SA":"Arabia Saudita","AE":"Emiratos","QA":"Qatar",
    "IS":"Israel","JO":"Jordania","SY":"Siria","LE":"Líbano","YM":"Yemen",
    "TU":"Turquía",
    # Oceanía
    "PP":"Papua N.Guinea","FJ":"Fiji","WS":"Samoa","TO":"Tonga",
    # Principales no-BRI (para referencia)
    "CH":"China","US":"EEUU","RS":"Rusia","UK":"R.Unido","AS":"Australia",
    "CA":"Canadá","GM":"Alemania","FR":"Francia","JA":"Japón","IN":"India",
    "KS":"Corea del Sur","TW":"Taiwan","HK":"Hong Kong",
}

REGIONS = {
    # v2: añadidos GY/NS/CS/JM/HA/BH/DR que antes faltaban
    "LATAM":    {"CI","AR","BR","MX","PE","CO","VE","BL","EC","UY","PA","PM","CU","GT","NU",
                 "ES","HO","BH","DR","GY","NS","CS","JM","HA"},
    # v2: SN removido de Asia_SE (colisión con Senegal en Africa, Singapore no es receptor BRI)
    "Africa":   {"SF","NI","ET","KE","AO","UG","TZ","MZ","ZA","GH","CM","SN","ZI","EG","LY","SU","DJ","IV","CG","ML"},
    "Asia_C":   {"PK","BD","NP","AF","UZ","KZ","TM","KG","TJ"},
    "Asia_SE":  {"RP","TH","MY","ID","VM","CB","BM","LA"},
    "Europa_E": {"UP","PL","HU","RO","BK","HR","SI","AL","MN","GG","AJ","AM"},
    "MedioO":   {"IZ","IR","SA","AE","QA","IS","JO","SY","LE","YM","TU"},
    "Oceania":  {"PP","FJ","WS","TO"},
}

df["pais"] = df["ActionGeo_CountryCode"].map(FIPS).fillna(df["ActionGeo_CountryCode"])
df["region"] = df["ActionGeo_CountryCode"].apply(
    lambda c: next((r for r, s in REGIONS.items() if c in s), "Other")
)

# ── 1. Distribución global por región ──────────────────────────────────────
print("\n=== Eventos BRI por región ===")
reg = df.groupby("region").agg(
    n_eventos=("SOURCEURL","count"),
    n_paises=("ActionGeo_CountryCode","nunique"),
    tono_medio=("AvgTone","mean"),
    menciones=("NumMentions","sum")
).sort_values("n_eventos", ascending=False)
reg["tono_medio"] = reg["tono_medio"].round(2)
print(reg.to_string())

# ── 2. Top 40 países ────────────────────────────────────────────────────────
print("\n=== Top 40 países (eventos BRI) ===")
top_paises = df.groupby(["ActionGeo_CountryCode","pais"]).agg(
    n=("SOURCEURL","count"),
    tono=("AvgTone","mean"),
    menciones=("NumMentions","sum")
).sort_values("n", ascending=False).head(40)
top_paises["tono"] = top_paises["tono"].round(2)
print(top_paises.to_string())

# ── 3. Evolución por región × año ──────────────────────────────────────────
print("\n=== Evolución BRI por región y año ===")
reg_year = df.groupby(["region","year"]).size().unstack(fill_value=0)
print(reg_year.to_string())

# ── 4. LATAM deep dive ──────────────────────────────────────────────────────
df_latam = df[df["region"] == "LATAM"].copy()
print(f"\n=== LATAM — {len(df_latam):,} eventos BRI ===")
latam_año = df_latam.groupby(["pais","year"]).size().unstack(fill_value=0)
print(latam_año.to_string())

print("\n--- LATAM tono y menciones ---")
latam_stats = df_latam.groupby("pais").agg(
    n=("SOURCEURL","count"),
    tono=("AvgTone","mean"),
    menciones=("NumMentions","sum"),
    n_urls_unicas=("SOURCEURL","nunique")
).sort_values("n", ascending=False)
latam_stats["tono"] = latam_stats["tono"].round(2)
print(latam_stats.to_string())

print("\n--- Top 20 eventos LATAM por menciones ---")
top_latam = df_latam.nlargest(20, "NumMentions")[
    ["SQLDATE","Actor1Name","Actor2Name","pais","AvgTone","NumMentions","ActionGeo_FullName","SOURCEURL"]
]
pd.set_option("display.max_colwidth", 85)
print(top_latam.to_string(index=False))

# ── 5. Análisis de mecanismo por región (v2) ──────────────────────────────
if "mechanism" in df.columns:
    print("\n=== MECANISMOS de cancelación por región (v2) ===")
    mech_latam = df[df["region"]=="LATAM"].groupby("mechanism")["SOURCEURL"].count()
    mech_global = df.groupby(["region","mechanism"])["SOURCEURL"].count().unstack(fill_value=0)
    cols_order = ["us_sanctions","environmental_opposition","political_rejection",
                  "debt_renegotiation","project_failure","unknown"]
    cols_avail = [c for c in cols_order if c in mech_global.columns]
    print(mech_global[cols_avail].sort_values("us_sanctions", ascending=False).to_string())
    print(f"\n--- LATAM mecanismos ---")
    print(mech_latam.to_string())

# ── 6. Deep-dives nuevos países LATAM (v2) ────────────────────────────────
print("\n--- Guyana (GY) — petróleo offshore, interés chino ---")
df_gy = df[df["ActionGeo_CountryCode"] == "GY"]
if len(df_gy) > 0:
    print(f"  {len(df_gy)} eventos")
    pd.set_option("display.max_colwidth", 100)
    print(df_gy[["SQLDATE","Actor1Name","Actor2Name","AvgTone","NumMentions","SOURCEURL"]].head(10).to_string(index=False))
else:
    print("  Sin eventos (Guyana no aparece en datos v2)")

print("\n--- Costa Rica (CS) — Huawei 5G, inversión digital ---")
df_cs = df[df["ActionGeo_CountryCode"] == "CS"]
if len(df_cs) > 0:
    print(f"  {len(df_cs)} eventos")
    print(df_cs[["SQLDATE","Actor1Name","Actor2Name","AvgTone","NumMentions","SOURCEURL"]].head(10).to_string(index=False))
else:
    print("  Sin eventos (Costa Rica no aparece en datos v2)")

# ── 7. África deep dive ────────────────────────────────────────────────────
df_africa = df[df["region"] == "Africa"].copy()
print(f"\n=== África — {len(df_africa):,} eventos BRI ===")
africa_pais = df_africa.groupby(["pais","year"]).size().unstack(fill_value=0)
print(africa_pais.to_string())

# ── 8. Asia SE ──────────────────────────────────────────────────────────────
df_ase = df[df["region"] == "Asia_SE"].copy()
print(f"\n=== Asia SE — {len(df_ase):,} eventos BRI ===")
ase_pais = df_ase.groupby(["pais","year"]).size().unstack(fill_value=0)
print(ase_pais.to_string())

# ── Guardar outputs ─────────────────────────────────────────────────────────
os.makedirs("data/samples/geo", exist_ok=True)
df.to_csv("data/samples/geo/bri_events_geo.csv", index=False)
df_latam.to_csv("data/samples/geo/bri_latam.csv", index=False)
df_africa.to_csv("data/samples/geo/bri_africa.csv", index=False)
df_ase.to_csv("data/samples/geo/bri_asia_se.csv", index=False)
df[df["region"]=="Asia_C"].to_csv("data/samples/geo/bri_asia_central.csv", index=False)
df[df["region"]=="Europa_E"].to_csv("data/samples/geo/bri_europa_e.csv", index=False)
df[df["region"]=="MedioO"].to_csv("data/samples/geo/bri_medio_oriente.csv", index=False)

print("\n✓ Archivos guardados en data/samples/geo/")

# ── Actualizar findings ─────────────────────────────────────────────────────
with open("docs/ANALYSIS_FINDINGS.md", "a") as f:
    f.write("\n## Script 10 — Análisis geográfico\n\n")
    f.write("### Eventos BRI por región\n")
    for region, row in reg.iterrows():
        f.write(f"- **{region}**: {int(row['n_eventos']):,} eventos, {int(row['n_paises'])} países, tono {row['tono_medio']:.2f}\n")
    f.write(f"\n### LATAM total: {len(df_latam):,} eventos\n")
    for pais, row in latam_stats.iterrows():
        f.write(f"- {pais}: {int(row['n'])} eventos, tono {row['tono']:.2f}\n")
    f.write("\n### Mejoras v2\n")
    f.write("- Añadidos GY/NS/CS/JM/HA/BH/DR al mapa LATAM\n")
    f.write("- Fix colisión SN: Senegal=SN (Africa), Singapore removido de Asia_SE\n")
    if "mechanism" in df.columns:
        f.write("- Análisis de mecanismo por región (columna 'mechanism' de script 09 v2)\n")
    f.write("\n### Próximo paso\n")
    f.write("- Script 12 v2: clustering actor-aware con ventana 180 días\n")

print("✓ ANALYSIS_FINDINGS.md actualizado")
print("\n=== PRÓXIMO: script 12 v2 (clustering actor-aware) ===")
