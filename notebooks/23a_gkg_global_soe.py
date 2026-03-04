"""
Script 23a — GKG Global SOE Mining
===================================
Extiende Script 17 (LATAM-only) a escala global:
  1. Carga GKG año por año para manejar memoria (no el 2.3GB combinado)
  2. Mapea SOE chinas expandidas (filtro Huawei para reducir ruido)
  3. Extrae señales por país-SOE-año en TODAS las regiones
  4. Señales especializadas: deuda, oposición ambiental, sanciones
  5. Cross-referencia con los 52 casos conocidos del consolidado

Output:
  data/samples/gkg_global/gkg_global_soe_timelines.csv    — timeline país×SOE×año
  data/samples/gkg_global/gkg_debt_signals.csv             — señales de deuda
  data/samples/gkg_global/gkg_env_opposition_signals.csv   — señales ambientales
  data/samples/gkg_global/gkg_underrep_urls.csv            — URLs de regiones sub-representadas
  data/samples/gkg_global/gkg_case_corroboration.csv       — corroboración de 52 casos
  data/samples/gkg_global/gkg_global_mining_report.md      — reporte narrativo
"""

import os
import re
import pandas as pd
import numpy as np
from collections import Counter, defaultdict

os.makedirs("data/samples/gkg_global", exist_ok=True)

# ── FIPS global → país → región ──────────────────────────────────────────────
FIPS_MAP = {
    # LATAM
    "CI":"Chile","AR":"Argentina","BR":"Brasil","MX":"México","PE":"Perú",
    "CO":"Colombia","VE":"Venezuela","BL":"Bolivia","EC":"Ecuador","UY":"Uruguay",
    "PA":"Paraguay","PM":"Panamá","CU":"Cuba","GT":"Guatemala","NU":"Nicaragua",
    "ES":"El Salvador","HO":"Honduras","BH":"Belice","DR":"Dom.Rep.",
    "GY":"Guyana","NS":"Suriname","CS":"Costa Rica","JM":"Jamaica","HA":"Haití",
    "TD":"Trinidad and Tobago",
    # South Asia
    "PK":"Pakistan","IN":"India","CE":"Sri Lanka","NP":"Nepal","BG":"Bangladesh",
    "MV":"Maldives","BT":"Bhutan",
    # SE Asia
    "MY":"Malaysia","TH":"Thailand","ID":"Indonesia","VM":"Vietnam","CB":"Cambodia",
    "LA":"Laos","BM":"Myanmar","RP":"Philippines","SN":"Singapore","TI":"Tajikistan",
    # Central Asia
    "KZ":"Kazakhstan","UZ":"Uzbekistan","KG":"Kyrgyzstan","TX":"Turkmenistan",
    # East Asia (excluir China/HK/TW/JP/KS para foco BRI receptor)
    "MG":"Mongolia",
    # Middle East
    "IR":"Iran","IS":"Israel","SA":"Saudi Arabia","AE":"UAE","QA":"Qatar",
    "BA":"Bahrain","KU":"Kuwait","MU":"Oman","IZ":"Iraq","JO":"Jordan",
    "LE":"Lebanon","SY":"Syria","YM":"Yemen","TU":"Turkey",
    # Africa
    "NI":"Nigeria","KE":"Kenya","SF":"South Africa","ET":"Ethiopia","TZ":"Tanzania",
    "UG":"Uganda","GH":"Ghana","SU":"Sudan","AO":"Angola","ZA":"Zambia",
    "ZI":"Zimbabwe","CG":"Congo (DRC)","CF":"Congo (Brazzaville)",
    "CM":"Cameroon","SG":"Senegal","IV":"Côte d'Ivoire","GA":"Gabon",
    "ML":"Mali","BC":"Botswana","MZ":"Mozambique","MI":"Malawi","RW":"Rwanda",
    "DJ":"Djibouti","ER":"Eritrea","SO":"Somalia","LY":"Libya","EG":"Egypt",
    "MR":"Mauritania","TS":"Tunisia","AG":"Algeria","MA":"Morocco",
    "WA":"Namibia","LT":"Lesotho","SL":"Sierra Leone","GB":"Gabon",
    # Europe
    "UK":"United Kingdom","GM":"Germany","FR":"France","IT":"Italy","SP":"Spain",
    "PL":"Poland","GR":"Greece","HU":"Hungary","RO":"Romania","BU":"Bulgaria",
    "AU":"Austria","BE":"Belgium","NL":"Netherlands","SW":"Sweden","NO":"Norway",
    "DA":"Denmark","FI":"Finland","EI":"Ireland","PO":"Portugal",
    "LO":"Slovakia","SI":"Slovenia","HR":"Croatia","EN":"Estonia",
    "LG":"Latvia","LH":"Lithuania","LU":"Luxembourg","MT":"Malta","CY":"Cyprus",
    "BO":"Belarus","UP":"Ukraine","RS":"Russia","AL":"Albania","MK":"North Macedonia",
    "MN":"Montenegro","BK":"Bosnia-Herzegovina","SR":"Serbia",
    # Oceania
    "AS":"Australia","NZ":"New Zealand","PP":"Papua New Guinea","FJ":"Fiji",
    "TN":"Tonga","WS":"Samoa","NR":"Nauru","TV":"Tuvalu",
    # North America (referencia, no BRI receptor)
    "US":"United States","CA":"Canada",
}

REGION_MAP = {}
_LATAM = {"CI","AR","BR","MX","PE","CO","VE","BL","EC","UY","PA","PM","CU","GT",
           "NU","ES","HO","BH","DR","GY","NS","CS","JM","HA","TD"}
_SOUTH_ASIA = {"PK","IN","CE","NP","BG","MV","BT"}
_SE_ASIA = {"MY","TH","ID","VM","CB","LA","BM","RP","SN"}
_CENTRAL_ASIA = {"KZ","UZ","KG","TX","TI"}
_MIDDLE_EAST = {"IR","IS","SA","AE","QA","BA","KU","MU","IZ","JO","LE","SY","YM","TU"}
_AFRICA = {"NI","KE","SF","ET","TZ","UG","GH","SU","AO","ZA","ZI","CG","CF",
           "CM","SG","IV","GA","ML","BC","MZ","MI","RW","DJ","ER","SO","LY","EG",
           "MR","TS","AG","MA","WA","LT","SL","GB"}
_EUROPE = {"UK","GM","FR","IT","SP","PL","GR","HU","RO","BU","AU","BE","NL","SW",
           "NO","DA","FI","EI","PO","LO","SI","HR","EN","LG","LH","LU","MT","CY",
           "BO","UP","RS","AL","MK","MN","BK","SR"}
_OCEANIA = {"AS","NZ","PP","FJ","TN","WS","NR","TV"}
_EURASIA = {"RS","MG"}
_EXCLUDE = {"US","CA","CH","TW","HK","JA","KS","KN"}  # excluir China, EEUU, etc.

for cc in _LATAM: REGION_MAP[cc] = "LATAM"
for cc in _SOUTH_ASIA: REGION_MAP[cc] = "South_Asia"
for cc in _SE_ASIA: REGION_MAP[cc] = "SE_Asia"
for cc in _CENTRAL_ASIA: REGION_MAP[cc] = "Central_Asia"
for cc in _MIDDLE_EAST: REGION_MAP[cc] = "Middle_East"
for cc in _AFRICA: REGION_MAP[cc] = "Africa"
for cc in _EUROPE: REGION_MAP[cc] = "Europe"
for cc in _OCEANIA: REGION_MAP[cc] = "Oceania"
for cc in _EURASIA: REGION_MAP[cc] = "Eurasia"

# Regiones sub-representadas (prioridad para nuevos descubrimientos)
UNDERREP_REGIONS = {"Middle_East", "Central_Asia", "Oceania", "Africa"}

# ── SOE MAP expandido ─────────────────────────────────────────────────────────
SOE_MAP = {
    # Railway
    "CHINA RAILWAY": "SOE_RAILWAY", "CRRC": "SOE_RAILWAY",
    "CHINA RAIL": "SOE_RAILWAY",
    # Maritime
    "COSCO": "SOE_MARITIME", "CHINA OCEAN SHIPPING": "SOE_MARITIME",
    "CHINA MERCHANTS": "SOE_MARITIME",
    # Harbour/Construction
    "CHINA HARBOUR": "SOE_HARBOUR", "CHINA COMMUNICATIONS CONSTRUCTION": "SOE_HARBOUR",
    "CCCC": "SOE_HARBOUR", "CHEC": "SOE_HARBOUR",
    "CHINA ROAD AND BRIDGE": "SOE_CONSTRUCT", "CRBC": "SOE_CONSTRUCT",
    "CHINA STATE CONSTRUCTION": "SOE_CONSTRUCT", "CSCEC": "SOE_CONSTRUCT",
    "CHINA ENERGY ENGINEERING": "SOE_CONSTRUCT", "SEPCO": "SOE_CONSTRUCT",
    # Energy
    "SINOHYDRO": "SOE_ENERGY", "POWERCHINA": "SOE_ENERGY",
    "THREE GORGES": "SOE_ENERGY", "CHINA THREE GORGES": "SOE_ENERGY",
    "GEZHOUBA": "SOE_ENERGY", "CHINA GENERAL NUCLEAR": "SOE_ENERGY",
    "CGN": "SOE_ENERGY", "CHINA NATIONAL NUCLEAR": "SOE_ENERGY",
    "STATE POWER INVESTMENT": "SOE_ENERGY", "SPIC": "SOE_ENERGY",
    "CHINA ENERGY": "SOE_ENERGY",
    # Oil & Gas
    "CNPC": "SOE_OIL", "PETROCHINA": "SOE_OIL",
    "SINOPEC": "SOE_OIL", "CNOOC": "SOE_OIL",
    "CHINA NATIONAL PETROLEUM": "SOE_OIL", "UNIPEC": "SOE_OIL",
    # Telecom (procesado aparte — filtro Huawei)
    "HUAWEI": "SOE_TELECOM", "ZTE": "SOE_TELECOM",
    "CHINA TELECOM": "SOE_TELECOM", "CHINA MOBILE": "SOE_TELECOM",
    "NUCTECH": "SOE_TELECOM",
    # Finance
    "CHINA DEVELOPMENT BANK": "SOE_FINANCE", "EXIM BANK": "SOE_FINANCE",
    "CDB": "SOE_FINANCE", "EXIMBANK": "SOE_FINANCE",
    "SILK ROAD FUND": "SOE_FINANCE", "CHINESE EXIM": "SOE_FINANCE",
    "CHINA EXIM": "SOE_FINANCE", "ICBC": "SOE_FINANCE",
    "BANK OF CHINA": "SOE_FINANCE", "AIIB": "SOE_FINANCE",
    # Mining
    "CHINALCO": "SOE_MINING", "CHINA MINMETALS": "SOE_MINING",
    "CITIC": "SOE_MINING", "TIANQI": "SOE_MINING",
    "MMG": "SOE_MINING", "CHINA MOLYBDENUM": "SOE_MINING",
    # Auto
    "BAIC": "SOE_AUTO", "SAIC": "SOE_AUTO", "GEELY": "SOE_AUTO",
    # BRI genéricos
    "BELT AND ROAD": "SOE_BRI_GENERIC", "SILK ROAD": "SOE_BRI_GENERIC",
    "BRI INITIATIVE": "SOE_BRI_GENERIC", "CPEC": "SOE_BRI_GENERIC",
    "OBOR": "SOE_BRI_GENERIC",
}

# SOEs que son telecom (para filtro Huawei)
TELECOM_KEYWORDS = {"HUAWEI", "ZTE"}

# ── Temas especializados ──────────────────────────────────────────────────────
DEBT_THEMES = [
    "ECON_DEBT", "ECON_BANKRUPTCY", "ECON_DEBTCRISIS",
    "WB_2024_DEBT_MANAGEMENT", "WB_696_DEBT_MANAGEMENT",
    "ECON_COST_OF_LIVING_CRISIS", "WB_2791_DEBT_RESOLUTION",
]

ENV_THEMES = [
    "ENV_DEFORESTATION", "ENV_POLLUTION", "ENV_FISHERIES",
    "UNGP_ENVIRONMENT_POLICY", "PROTEST", "CRISISLEX_C04_PROTESTS",
    "ENV_GREEN", "ENV_COAL", "UNGP_CLIMATE_CHANGE",
]

CANCEL_THEMES = [
    "CANCEL", "SUSPEND", "HALT", "REJECT", "SANCTION",
    "BAN", "BLOCK", "WITHDRAW", "TERMINATE",
]

INVEST_THEMES = [
    "INVEST", "INFRASTRUCTURE", "LOAN", "DEBT", "CONTRACT", "CONCESSION",
    "CONSTRUCTION", "PORT", "RAILWAY", "PIPELINE", "ENERGY", "MINING",
]


# ── Funciones de parsing ──────────────────────────────────────────────────────
def get_soes(orgs_str):
    """Extrae SOE groups de V2Organizations."""
    if not orgs_str or pd.isna(orgs_str):
        return []
    orgs_upper = str(orgs_str).upper()
    found = set()
    for keyword, group in SOE_MAP.items():
        if keyword in orgs_upper:
            found.add(group)
    return sorted(found)


def get_soe_names(orgs_str):
    """Extrae nombres específicos de SOE (no solo grupos)."""
    if not orgs_str or pd.isna(orgs_str):
        return []
    orgs_upper = str(orgs_str).upper()
    found = []
    for keyword in SOE_MAP:
        if keyword in orgs_upper:
            found.append(keyword)
    return found


def is_huawei_only(orgs_str):
    """True si las únicas SOE son Huawei/ZTE (para filtrado de ruido telecom)."""
    if not orgs_str or pd.isna(orgs_str):
        return False
    orgs_upper = str(orgs_str).upper()
    has_telecom = any(kw in orgs_upper for kw in TELECOM_KEYWORDS)
    has_other = any(kw in orgs_upper for kw, g in SOE_MAP.items()
                    if g != "SOE_TELECOM" and g != "SOE_BRI_GENERIC" and kw in orgs_upper)
    return has_telecom and not has_other


def get_countries(locs_str):
    """Extrae FIPS codes de V2Locations (global, no solo LATAM)."""
    if not locs_str or pd.isna(locs_str):
        return []
    found = set()
    for part in str(locs_str).split(";"):
        fields = part.split("#")
        if len(fields) >= 4:
            cc = fields[3].strip().upper()
            if cc in REGION_MAP:
                found.add(cc)
    return sorted(found)


def has_themes(themes_str, theme_list):
    """Verifica si el string de temas contiene alguno de la lista."""
    if not themes_str or pd.isna(themes_str):
        return False
    themes_upper = str(themes_str).upper()
    return any(t in themes_upper for t in theme_list)


def has_cancel_theme(themes_str):
    """Verifica si hay temas de cancelación/suspensión."""
    return has_themes(themes_str, CANCEL_THEMES)


# ── Cargar casos conocidos ────────────────────────────────────────────────────
known_cases = pd.read_csv("data/samples/final/bri_cancellations_consolidated.csv")
print(f"Casos conocidos: {len(known_cases)}")

# ── Procesar GKG año por año ──────────────────────────────────────────────────
YEARS = range(2017, 2025)
all_signals = []
debt_signals = []
env_signals = []
underrep_urls = []
case_corr = defaultdict(int)  # (country, year) → count of corroborating articles

total_articles = 0
total_with_soe = 0
total_huawei_filtered = 0
total_huawei_cancel = 0

for year in YEARS:
    path = f"data/samples/gkg_por_año/{year}/gkg_china_{year}.parquet"
    if not os.path.exists(path):
        print(f"  ⚠ No existe: {path}")
        continue

    print(f"\n{'='*60}")
    print(f"Procesando {year}...")
    df = pd.read_parquet(path)
    df["tone"] = df["V2Tone"].str.split(",").str[0].astype(float, errors="ignore")
    if "year" not in df.columns:
        df["year"] = year
    total_articles += len(df)
    print(f"  Artículos: {len(df):,}")

    year_soe = 0
    year_huawei_skip = 0
    year_huawei_cancel = 0

    for idx, row in df.iterrows():
        orgs = row.get("V2Organizations", "")
        soes = get_soes(orgs)
        if not soes:
            continue
        year_soe += 1

        tone = row.get("tone", 0)
        themes = str(row.get("V2Themes", "") or "")
        locs = row.get("V2Locations", "")
        url = str(row.get("DocumentIdentifier", ""))
        source = str(row.get("SourceCommonName", ""))
        countries = get_countries(locs)

        if not countries:
            continue

        # ── Filtro Huawei: solo pasar si tiene tema de cancel/ban ─────
        if is_huawei_only(orgs):
            year_huawei_skip += 1
            if has_cancel_theme(themes):
                year_huawei_cancel += 1
                # Incluir Huawei solo con cancelación
            else:
                continue  # Skip Huawei sin contexto de cancelación

        soe_names = get_soe_names(orgs)

        for cc in countries:
            region = REGION_MAP.get(cc, "Other")
            country_name = FIPS_MAP.get(cc, cc)

            record = {
                "year": year,
                "cc": cc,
                "country": country_name,
                "region": region,
                "tone": tone,
                "soes": ",".join(soes),
                "soe_names": ",".join(soe_names[:5]),
                "has_invest_theme": has_themes(themes, INVEST_THEMES),
                "has_cancel_theme": has_cancel_theme(themes),
                "has_debt_theme": has_themes(themes, DEBT_THEMES),
                "has_env_theme": has_themes(themes, ENV_THEMES),
                "source": source,
                "url": url,
            }
            all_signals.append(record)

            # ── Señales de deuda ──────────────────────────────────────
            if has_themes(themes, DEBT_THEMES) and tone < -2:
                debt_signals.append({
                    "year": year, "cc": cc, "country": country_name,
                    "region": region, "tone": tone,
                    "soes": ",".join(soes), "source": source, "url": url,
                    "themes_sample": themes[:300],
                })

            # ── Señales ambientales ───────────────────────────────────
            if has_themes(themes, ENV_THEMES) and tone < -2:
                if any(s not in ("SOE_TELECOM", "SOE_BRI_GENERIC") for s in soes):
                    env_signals.append({
                        "year": year, "cc": cc, "country": country_name,
                        "region": region, "tone": tone,
                        "soes": ",".join(soes), "source": source, "url": url,
                        "themes_sample": themes[:300],
                    })

            # ── URLs de regiones sub-representadas ────────────────────
            if region in UNDERREP_REGIONS and tone < -3:
                underrep_urls.append({
                    "year": year, "cc": cc, "country": country_name,
                    "region": region, "tone": tone,
                    "soes": ",".join(soes), "url": url, "source": source,
                })

            # ── Corroboración de casos conocidos ──────────────────────
            for _, kc in known_cases.iterrows():
                kc_country = str(kc["country"])
                try:
                    kc_year = int(str(kc["year"]).split("-")[0])
                except (ValueError, TypeError):
                    kc_year = 0
                if (country_name == kc_country and abs(year - kc_year) <= 1):
                    key = f"{kc_country}|{kc_year}|{kc['project']}"
                    case_corr[key] += 1

    total_with_soe += year_soe
    total_huawei_filtered += year_huawei_skip
    total_huawei_cancel += year_huawei_cancel

    print(f"  Con SOE: {year_soe:,}")
    print(f"  Huawei-only filtrado: {year_huawei_skip:,} (rescue cancel: {year_huawei_cancel:,})")
    print(f"  Señales acumuladas: {len(all_signals):,}")

    del df  # liberar memoria

# ── Crear DataFrames ──────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print("Consolidando resultados...")

df_signals = pd.DataFrame(all_signals)
df_debt = pd.DataFrame(debt_signals)
df_env = pd.DataFrame(env_signals)
df_underrep = pd.DataFrame(underrep_urls)

print(f"\nTotal artículos procesados: {total_articles:,}")
print(f"Con SOE china: {total_with_soe:,}")
print(f"Huawei-only filtrado: {total_huawei_filtered:,} (rescue: {total_huawei_cancel:,})")
print(f"Señales globales (SOE + país receptor): {len(df_signals):,}")
print(f"Señales de deuda: {len(df_debt):,}")
print(f"Señales ambientales: {len(df_env):,}")
print(f"URLs regiones sub-representadas: {len(df_underrep):,}")

# ── Clustering: país × SOE × año ──────────────────────────────────────────────
print("\n=== Clustering global (país × SOE × año) ===")
if len(df_signals) > 0:
    timeline = df_signals.groupby(["country", "region", "soes", "year"]).agg(
        n_articles=("url", "nunique"),
        avg_tone=("tone", "mean"),
        min_tone=("tone", "min"),
        n_cancel=("has_cancel_theme", "sum"),
        n_debt=("has_debt_theme", "sum"),
        n_env=("has_env_theme", "sum"),
        n_invest=("has_invest_theme", "sum"),
        sample_url=("url", "first"),
    ).reset_index()
    timeline["avg_tone"] = timeline["avg_tone"].round(2)
    timeline["min_tone"] = timeline["min_tone"].round(2)
    timeline = timeline.sort_values("n_articles", ascending=False)

    print(f"Total clusters: {len(timeline):,}")
    strong = timeline[timeline["n_articles"] >= 5]
    print(f"Con ≥5 artículos: {len(strong):,}")

    # ── Top señales por región ────────────────────────────────────────────
    print("\n=== Top señales por región (≥5 artículos) ===")
    for region in sorted(strong["region"].unique()):
        reg_data = strong[strong["region"] == region].head(10)
        print(f"\n--- {region} ({len(strong[strong['region']==region])} clusters ≥5) ---")
        for _, r in reg_data.iterrows():
            cancel_flag = " [CANCEL]" if r["n_cancel"] > 0 else ""
            print(f"  {r['country']:20s} {r['soes']:25s} {r['year']}  "
                  f"n={r['n_articles']:4d}  tone={r['avg_tone']:6.2f}{cancel_flag}")

    # ── Regiones sub-representadas: señales prometedoras ──────────────────
    print("\n=== Señales prometedoras en regiones sub-representadas ===")
    for region in UNDERREP_REGIONS:
        reg_strong = strong[strong["region"] == region]
        if len(reg_strong) == 0:
            reg_any = timeline[(timeline["region"] == region) & (timeline["n_articles"] >= 2)]
            print(f"\n--- {region}: 0 clusters ≥5, {len(reg_any)} con ≥2 ---")
            for _, r in reg_any.head(10).iterrows():
                print(f"  {r['country']:20s} {r['soes']:25s} {r['year']}  "
                      f"n={r['n_articles']:3d}  tone={r['avg_tone']:6.2f}")
        else:
            print(f"\n--- {region}: {len(reg_strong)} clusters ≥5 ---")
            for _, r in reg_strong.head(15).iterrows():
                print(f"  {r['country']:20s} {r['soes']:25s} {r['year']}  "
                      f"n={r['n_articles']:4d}  tone={r['avg_tone']:6.2f}")
else:
    timeline = pd.DataFrame()
    strong = pd.DataFrame()

# ── Distribución SOE (sin Huawei dominancia) ──────────────────────────────────
print("\n=== Distribución SOE (post-filtro Huawei) ===")
if len(df_signals) > 0:
    soe_dist = Counter()
    for soes_str in df_signals["soes"]:
        for s in soes_str.split(","):
            soe_dist[s] += 1
    for soe, n in soe_dist.most_common(20):
        print(f"  {n:7,}  {soe}")

# ── Debt signals por país ─────────────────────────────────────────────────────
print("\n=== Señales de deuda por país (top 20) ===")
if len(df_debt) > 0:
    debt_by_country = df_debt.groupby("country").agg(
        n=("url", "nunique"), avg_tone=("tone", "mean")
    ).sort_values("n", ascending=False)
    debt_by_country["avg_tone"] = debt_by_country["avg_tone"].round(2)
    print(debt_by_country.head(20).to_string())

# ── Environmental signals por país ────────────────────────────────────────────
print("\n=== Señales ambientales por país (top 20) ===")
if len(df_env) > 0:
    env_by_country = df_env.groupby("country").agg(
        n=("url", "nunique"), avg_tone=("tone", "mean")
    ).sort_values("n", ascending=False)
    env_by_country["avg_tone"] = env_by_country["avg_tone"].round(2)
    print(env_by_country.head(20).to_string())

# ── Corroboración de casos conocidos ──────────────────────────────────────────
print("\n=== Corroboración GKG de casos conocidos ===")
corr_rows = []
for key, count in sorted(case_corr.items(), key=lambda x: -x[1]):
    parts = key.split("|")
    corr_rows.append({"country": parts[0], "year": parts[1], "project": parts[2],
                       "gkg_articles": count})
    print(f"  {count:4d} artículos  {parts[0]:20s} {parts[1]}  {parts[2][:50]}")

df_corr = pd.DataFrame(corr_rows)

# ── Guardar ───────────────────────────────────────────────────────────────────
print("\n=== Guardando archivos ===")

if len(timeline) > 0:
    timeline.to_csv("data/samples/gkg_global/gkg_global_soe_timelines.csv", index=False)
    print(f"  gkg_global_soe_timelines.csv: {len(timeline):,} rows")

if len(df_debt) > 0:
    df_debt.to_csv("data/samples/gkg_global/gkg_debt_signals.csv", index=False)
    print(f"  gkg_debt_signals.csv: {len(df_debt):,} rows")

if len(df_env) > 0:
    df_env.to_csv("data/samples/gkg_global/gkg_env_opposition_signals.csv", index=False)
    print(f"  gkg_env_opposition_signals.csv: {len(df_env):,} rows")

if len(df_underrep) > 0:
    # Dedup by URL
    df_underrep_dedup = df_underrep.drop_duplicates("url").sort_values("tone")
    df_underrep_dedup.to_csv("data/samples/gkg_global/gkg_underrep_urls.csv", index=False)
    print(f"  gkg_underrep_urls.csv: {len(df_underrep_dedup):,} URLs únicas")

if len(df_corr) > 0:
    df_corr.to_csv("data/samples/gkg_global/gkg_case_corroboration.csv", index=False)
    print(f"  gkg_case_corroboration.csv: {len(df_corr):,} rows")

# ── Reporte narrativo ─────────────────────────────────────────────────────────
with open("data/samples/gkg_global/gkg_global_mining_report.md", "w") as f:
    f.write("# GKG Global SOE Mining Report (Script 23a)\n\n")
    f.write(f"**Fecha**: {pd.Timestamp.now().strftime('%Y-%m-%d')}\n\n")
    f.write("## Resumen\n\n")
    f.write(f"- Artículos GKG procesados: {total_articles:,}\n")
    f.write(f"- Con SOE china identificada: {total_with_soe:,}\n")
    f.write(f"- Huawei-only filtrado: {total_huawei_filtered:,} (rescue por cancel: {total_huawei_cancel:,})\n")
    f.write(f"- Señales globales (SOE + país receptor): {len(df_signals):,}\n")
    f.write(f"- Clusters (país×SOE×año): {len(timeline):,}\n")
    f.write(f"- Clusters con ≥5 artículos: {len(strong):,}\n")
    f.write(f"- Señales de deuda: {len(df_debt):,}\n")
    f.write(f"- Señales ambientales: {len(df_env):,}\n")

    if len(df_underrep) > 0:
        f.write(f"- URLs regiones sub-representadas: {len(df_underrep.drop_duplicates('url')):,}\n")

    f.write("\n## Distribución SOE (post-filtro Huawei)\n\n")
    if len(df_signals) > 0:
        for soe, n in soe_dist.most_common(15):
            f.write(f"- `{soe}`: {n:,}\n")

    f.write("\n## Top señales por región\n\n")
    if len(strong) > 0:
        for region in sorted(strong["region"].unique()):
            reg_data = strong[strong["region"] == region].head(8)
            f.write(f"\n### {region}\n\n")
            f.write("| País | SOE | Año | Artículos | Tono medio | Cancel |\n")
            f.write("|------|-----|-----|-----------|------------|--------|\n")
            for _, r in reg_data.iterrows():
                f.write(f"| {r['country']} | {r['soes']} | {r['year']} | "
                        f"{r['n_articles']} | {r['avg_tone']} | {r['n_cancel']} |\n")

    f.write("\n## Señales de deuda por país (top 15)\n\n")
    if len(df_debt) > 0:
        debt_top = debt_by_country.head(15)
        f.write("| País | Artículos | Tono medio |\n")
        f.write("|------|-----------|------------|\n")
        for country, r in debt_top.iterrows():
            f.write(f"| {country} | {r['n']} | {r['avg_tone']} |\n")

    f.write("\n## Señales ambientales por país (top 15)\n\n")
    if len(df_env) > 0:
        env_top = env_by_country.head(15)
        f.write("| País | Artículos | Tono medio |\n")
        f.write("|------|-----------|------------|\n")
        for country, r in env_top.iterrows():
            f.write(f"| {country} | {r['n']} | {r['avg_tone']} |\n")

    f.write("\n## Corroboración de casos conocidos\n\n")
    if len(df_corr) > 0:
        f.write("| País | Año | Proyecto | Artículos GKG |\n")
        f.write("|------|-----|----------|---------------|\n")
        for _, r in df_corr.head(30).iterrows():
            f.write(f"| {r['country']} | {r['year']} | {r['project'][:40]} | {r['gkg_articles']} |\n")

    f.write("\n## Regiones sub-representadas: oportunidades\n\n")
    if len(timeline) > 0:
        for region in UNDERREP_REGIONS:
            reg_t = timeline[timeline["region"] == region]
            f.write(f"\n### {region}\n")
            f.write(f"- Total clusters: {len(reg_t)}\n")
            f.write(f"- Con ≥5 artículos: {len(reg_t[reg_t['n_articles']>=5])}\n")
            f.write(f"- Con tema cancel: {reg_t['n_cancel'].sum():.0f}\n")
            if len(reg_t) > 0:
                f.write(f"- Top países: {reg_t.groupby('country')['n_articles'].sum().sort_values(ascending=False).head(5).to_dict()}\n")

print("\n✓ Reporte guardado: data/samples/gkg_global/gkg_global_mining_report.md")
print("\n=== SCRIPT 23a COMPLETO ===")
