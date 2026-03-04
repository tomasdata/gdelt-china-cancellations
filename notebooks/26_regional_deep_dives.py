"""
Script 26 — Regional Deep Dives
================================
Búsqueda dirigida de casos BRI en regiones sub-representadas:
  1. Middle East: UAE, Saudi Arabia, Iran, Turkey
  2. Central Asia: Kazakhstan, Kyrgyzstan, Tajikistan
  3. Pacific Islands: PNG, Fiji, Tonga
  4. Francophone Africa: Cameroon, Senegal, Congo

Combina:
  - URLs prometedoras del GKG Script 23a (regiones sub-representadas)
  - Web search para casos conocidos de la literatura
  - Medición de tasa de detección GKG por región

Output:
  data/samples/gkg_global/regional_new_cases.csv          — nuevos casos
  data/samples/gkg_global/gkg_detection_rate_by_region.csv — tasa de detección
  data/samples/gkg_global/regional_deep_dive_report.md    — reporte
"""

import os
import re
import time
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

os.makedirs("data/samples/gkg_global", exist_ok=True)

FETCH_TIMEOUT = 8
SLEEP_BETWEEN = 1.2
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    )
}

CHINESE_COMPANIES_RE = re.compile(
    r"\b(COSCO|Huawei|ZTE|CNPC|PetroChina|Sinopec|CNOOC|Sinohydro|PowerChina|"
    r"Three Gorges|CRRC|China Railway|CCCC|China Harbour|China Communications|"
    r"Chinalco|China Minmetals|CITIC|China Development Bank|Exim Bank|"
    r"China State Construction|China Road and Bridge|China Energy|"
    r"China Merchants|CGN|CRBC|SEPCO|ICBC|"
    r"China Mobile|China Telecom|Bank of China|AIIB|Tianqi|MMG|"
    r"Gezhouba|Nuctech)\b",
    re.IGNORECASE
)

DISRUPTION_KEYWORDS = [
    "cancel", "suspend", "halt", "withdraw", "block", "reject", "scrap",
    "abandon", "terminate", "freeze", "delay", "sanction", "protest",
    "opposition", "renegotiat", "default", "dispute", "debt trap",
    "controversy", "backlash", "concern", "ban", "restrict",
]

BRI_KEYWORDS = [
    "chinese investment", "china investment", "bri", "belt and road",
    "silk road", "cpec", "chinese company", "chinese firm",
    "chinese-funded", "chinese-built", "chinese loan", "chinese debt",
]


def fetch_article(url):
    result = {"fetched": False, "title": "", "text": "", "error": ""}
    try:
        r = requests.get(url, timeout=FETCH_TIMEOUT, headers=HEADERS, allow_redirects=True)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "lxml")
            title_tag = soup.find("title")
            result["title"] = title_tag.get_text(strip=True)[:200] if title_tag else ""
            paragraphs = soup.find_all(["p", "article", "section"])
            text = " ".join(p.get_text(separator=" ", strip=True) for p in paragraphs)
            result["text"] = text[:10000]
            result["fetched"] = True
        else:
            result["error"] = f"HTTP {r.status_code}"
    except Exception as e:
        result["error"] = str(e)[:100]
    return result


def evaluate_article(text, title):
    full = (title + " " + text).lower()
    companies = CHINESE_COMPANIES_RE.findall(title + " " + text)
    disruptions = [kw for kw in DISRUPTION_KEYWORDS if kw in full]
    bri = [kw for kw in BRI_KEYWORDS if kw in full]
    return {
        "companies": list(set(c for c in companies)),
        "n_disruptions": len(disruptions),
        "n_bri": len(bri),
        "disruptions": disruptions[:5],
        "bri_kw": bri[:3],
    }


# ── Cargar GKG URLs de regiones sub-representadas ────────────────────────────
print("=== Cargando GKG URLs sub-representadas ===")
underrep_path = "data/samples/gkg_global/gkg_underrep_urls.csv"
if os.path.exists(underrep_path):
    gkg_urls = pd.read_csv(underrep_path)
    print(f"URLs disponibles: {len(gkg_urls)}")
    print(f"Por región:")
    print(gkg_urls["region"].value_counts().to_string())
else:
    gkg_urls = pd.DataFrame()
    print("No hay URLs GKG sub-representadas")

# ── Cargar casos existentes para evitar duplicados ───────────────────────────
existing = pd.read_csv("data/samples/final/bri_cases_enriched.csv")
existing_countries = set(existing["country"].str.lower().dropna())
print(f"\nCasos existentes: {len(existing)}")

# ── Seleccionar top URLs por región para verificación ─────────────────────────
# Estrategia: para cada región, tomar las URLs con tono más negativo
# y que NO sean de países ya bien representados
PRIORITY_COUNTRIES = {
    "Middle_East": ["Iran", "Saudi Arabia", "UAE", "Turkey", "Iraq", "Qatar", "Jordan"],
    "Central_Asia": ["Kazakhstan", "Kyrgyzstan", "Tajikistan", "Turkmenistan", "Uzbekistan"],
    "Oceania": ["Papua New Guinea", "Fiji", "Tonga", "Samoa"],
    "Africa": ["Cameroon", "Senegal", "Côte d'Ivoire", "Gabon", "Mozambique",
               "Angola", "Ethiopia", "Egypt", "Djibouti", "Algeria", "Morocco"],
}

MAX_PER_REGION = 25
selected_urls = []

if len(gkg_urls) > 0:
    for region, countries in PRIORITY_COUNTRIES.items():
        reg_df = gkg_urls[gkg_urls["region"] == region].copy()
        # Priorizar países de la lista de prioridad
        for country in countries:
            c_df = reg_df[reg_df["country"] == country].nsmallest(5, "tone")
            selected_urls.extend(c_df.to_dict("records"))
        # Completar con los más negativos de la región
        remaining = MAX_PER_REGION - len([u for u in selected_urls if u.get("region") == region])
        if remaining > 0:
            extra = reg_df.nsmallest(remaining + 10, "tone").head(remaining)
            selected_urls.extend(extra.to_dict("records"))

print(f"\nURLs seleccionadas para verificación: {len(selected_urls)}")

# ── Verificar URLs ───────────────────────────────────────────────────────────
print(f"\n=== Verificando {len(selected_urls)} URLs ===\n")
new_cases = []
results = []

for i, u in enumerate(selected_urls):
    url = str(u.get("url", ""))
    country = str(u.get("country", ""))
    region = str(u.get("region", ""))
    year = u.get("year", 0)
    tone = u.get("tone", 0)

    print(f"[{i+1}/{len(selected_urls)}] {country:20s} {region:15s} tone={tone:.1f}", end=" ")

    article = fetch_article(url)
    is_real = False

    if article["fetched"]:
        ev = evaluate_article(article["text"], article["title"])
        is_real = (len(ev["companies"]) >= 1 and ev["n_disruptions"] >= 1) or \
                  (ev["n_disruptions"] >= 2 and ev["n_bri"] >= 1)

        if is_real:
            classification = "CONFIRMED" if len(ev["companies"]) >= 1 else "LIKELY"
            print(f"→ {classification} [{','.join(ev['companies'][:3])}] [{','.join(ev['disruptions'][:3])}]")

            new_cases.append({
                "country": country,
                "region": region,
                "year": year,
                "tone": tone,
                "classification": classification,
                "companies": ",".join(ev["companies"][:5]),
                "disruptions": ",".join(ev["disruptions"][:5]),
                "bri_kw": ",".join(ev["bri_kw"][:3]),
                "title": article["title"][:200],
                "url": url,
                "source": u.get("source", ""),
            })
        else:
            print(f"→ WEAK/NOISE (co={len(ev['companies'])} dis={ev['n_disruptions']} bri={ev['n_bri']})")
    else:
        print(f"→ DEAD ({article['error'][:30]})")

    results.append({
        "url": url, "country": country, "region": region,
        "fetched": article["fetched"],
        "classification": "REAL" if is_real else ("WEAK" if article["fetched"] else "DEAD"),
    })

    time.sleep(SLEEP_BETWEEN)

# ── Resultados ────────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print("=== RESULTADOS ===")
print(f"URLs verificadas: {len(results)}")
print(f"Nuevos casos descubiertos: {len(new_cases)}")

df_new = pd.DataFrame(new_cases)
if len(df_new) > 0:
    print(f"\nPor región:")
    print(df_new["region"].value_counts().to_string())
    print(f"\nPor país:")
    print(df_new["country"].value_counts().to_string())

    print("\n=== Detalle nuevos casos ===")
    for _, c in df_new.iterrows():
        print(f"\n  [{c['classification']}] {c['country']} ({c['year']}) tone={c['tone']:.1f}")
        print(f"    Companies: {c['companies'][:80]}")
        print(f"    Disruptions: {c['disruptions'][:80]}")
        print(f"    Title: {c['title'][:100]}")

# ── GKG detection rate by region ──────────────────────────────────────────────
print("\n=== GKG Detection Rate ===")
# Para cada región en el dataset enriquecido, qué % de casos tiene cobertura GKG
detection_rows = []
for region in sorted(existing["region"].unique()):
    rd = existing[existing["region"] == region]
    with_gkg = len(rd[rd["gkg_articles"] > 0])
    total = len(rd)
    rate = 100 * with_gkg / total if total > 0 else 0
    detection_rows.append({
        "region": region, "total_cases": total,
        "with_gkg": with_gkg, "detection_rate_pct": round(rate, 1),
    })
    print(f"  {region:20s} {with_gkg}/{total} ({rate:.0f}%)")

df_detection = pd.DataFrame(detection_rows)

# ── Guardar ───────────────────────────────────────────────────────────────────
print("\n=== Guardando ===")

if len(df_new) > 0:
    df_new.to_csv("data/samples/gkg_global/regional_new_cases.csv", index=False)
    print(f"  regional_new_cases.csv: {len(df_new)} rows")

df_detection.to_csv("data/samples/gkg_global/gkg_detection_rate_by_region.csv", index=False)
print(f"  gkg_detection_rate_by_region.csv: {len(df_detection)} rows")

# ── Reporte ───────────────────────────────────────────────────────────────────
with open("data/samples/gkg_global/regional_deep_dive_report.md", "w") as f:
    f.write("# Regional Deep Dive Report (Script 26)\n\n")
    f.write(f"**Fecha**: {pd.Timestamp.now().strftime('%Y-%m-%d')}\n\n")

    f.write("## Resumen\n\n")
    f.write(f"- URLs GKG verificadas: {len(results)}\n")
    f.write(f"- Nuevos casos descubiertos: {len(new_cases)}\n\n")

    f.write("## GKG Detection Rate by Region\n\n")
    f.write("| Region | Cases | With GKG | Rate |\n|--------|-------|----------|------|\n")
    for _, r in df_detection.iterrows():
        f.write(f"| {r['region']} | {r['total_cases']} | {r['with_gkg']} | {r['detection_rate_pct']}% |\n")

    if len(df_new) > 0:
        f.write("\n## Nuevos casos por región\n\n")
        for region in sorted(df_new["region"].unique()):
            rd = df_new[df_new["region"] == region]
            f.write(f"\n### {region} ({len(rd)} new cases)\n\n")
            for _, c in rd.iterrows():
                f.write(f"- **{c['country']} ({c['year']})**: {c['title'][:100]}\n")
                f.write(f"  - Companies: {c['companies'][:80]}\n")
                f.write(f"  - Disruptions: {c['disruptions'][:80]}\n")
                f.write(f"  - Source: {c['url'][:100]}\n\n")

    f.write("\n## Limitaciones metodológicas\n\n")
    f.write("- Pacific Islands y Francophone Africa tienen cobertura GKG mínima en inglés\n")
    f.write("- Central Asia tiene cobertura significativa en ruso, no capturada\n")
    f.write("- Middle East tiene sesgo hacia cobertura de sanciones (Irán) vs proyectos BRI\n")

print("\n✓ Reporte: data/samples/gkg_global/regional_deep_dive_report.md")
print("\n=== SCRIPT 26 COMPLETO ===")
