"""
Script 24 — Tier 2 Global Signal Verification
===============================================
Verifica los 202 señales Tier 2 (score 3.0-4.9) del Script 21:
  1. Prioriza regiones sub-representadas (Middle East, Central Asia, Africa, Oceania)
  2. Web scrape de URLs para extraer contenido real
  3. Clasifica: CONFIRMED / LIKELY / WEAK / NOISE
  4. Extrae nuevos casos no presentes en el consolidado de 52

Output:
  data/samples/final/tier2_verified.csv             — todas las señales verificadas
  data/samples/final/tier2_new_cases.csv            — nuevos casos descubiertos
  data/samples/final/tier2_verification_report.md   — reporte narrativo
"""

import os
import re
import time
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

os.makedirs("data/samples/final", exist_ok=True)

# ── Configuración ────────────────────────────────────────────────────────────
FETCH_TIMEOUT = 8
SLEEP_BETWEEN = 1.2
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    )
}

# ── Patrones de extracción ───────────────────────────────────────────────────
CHINESE_COMPANIES_RE = re.compile(
    r"\b(COSCO|Huawei|ZTE|CNPC|PetroChina|Sinopec|CNOOC|Sinohydro|PowerChina|"
    r"Three Gorges|CRRC|China Railway|CCCC|China Harbour|China Communications|"
    r"Chinalco|China Minmetals|CITIC|China Development Bank|Exim Bank|"
    r"China State Construction|China Road and Bridge|China Energy|"
    r"China Merchants|China General Nuclear|CGN|CRBC|SEPCO|ICBC|"
    r"China Mobile|China Telecom|Bank of China|AIIB|Tianqi|MMG|"
    r"China Molybdenum|Gezhouba|China National Nuclear|Nuctech)\b",
    re.IGNORECASE
)

DISRUPTION_KEYWORDS = [
    "cancel", "suspend", "halt", "withdraw", "block", "reject", "scrap",
    "abandon", "terminate", "freeze", "delay", "sanction", "protest",
    "opposition", "renegotiat", "default", "dispute", "arbitrat",
    "overrun", "behind schedule", "pull out", "pull back", "stall",
    "debt trap", "controversy", "backlash", "concern", "criticiz",
    "threat", "ban", "restrict", "revoke", "indefinitely postpone",
]

BRI_KEYWORDS = [
    "chinese investment", "china investment", "bri", "belt and road",
    "silk road", "cpec", "chinese company", "chinese firm", "state-owned",
    "chinese-funded", "chinese-built", "financed by china",
    "chinese loan", "chinese debt", "china loan", "china debt",
    "chinese infrastructure", "china infrastructure",
]

# Mapeo región prioridad
REGION_PRIORITY = {
    "MedioOriente": 1, "Asia_C": 2, "Africa": 3, "Oceania": 4,
    "Asia_Sur": 5, "Asia_SE": 6, "Europa_E": 7, "Europa_W": 8,
    "Eurasia": 9, "Asia_E": 10, "NorteAmerica": 11, "Other": 12,
}

# ── Función de descarga ──────────────────────────────────────────────────────
def fetch_article(url):
    result = {"fetched": False, "status_code": None, "title": "", "text": "", "error": ""}
    try:
        r = requests.get(url, timeout=FETCH_TIMEOUT, headers=HEADERS, allow_redirects=True)
        result["status_code"] = r.status_code
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
    except requests.exceptions.Timeout:
        result["error"] = "timeout"
    except Exception as e:
        result["error"] = str(e)[:100]
    return result


def classify_signal(text, title, url, country, score):
    """Clasifica señal como CONFIRMED/LIKELY/WEAK/NOISE."""
    full = (title + " " + text).lower()

    # Evidencia
    companies = CHINESE_COMPANIES_RE.findall(title + " " + text)
    disruptions = [kw for kw in DISRUPTION_KEYWORDS if kw in full]
    bri_context = [kw for kw in BRI_KEYWORDS if kw in full]

    n_company = len(set(c.lower() for c in companies))
    n_disrupt = len(disruptions)
    n_bri = len(bri_context)

    # Extraer valor monetario
    value_match = re.search(r'\$\s*([\d,.]+)\s*(billion|million|bn|mn|b|m)', full, re.IGNORECASE)
    value_str = ""
    if value_match:
        value_str = f"${value_match.group(1)} {value_match.group(2)}"

    # Extraer nombre de proyecto
    project_match = re.search(
        r'(?:project|port|railway|dam|highway|plant|airport|bridge|corridor|park|mine|refinery)'
        r'\s+([A-Z][A-Za-z\s\-]{2,30})',
        title + " " + text
    )
    project_name = project_match.group(0)[:60] if project_match else ""

    # Clasificación
    if n_company >= 1 and n_disrupt >= 2 and n_bri >= 1:
        classification = "CONFIRMED"
    elif n_company >= 1 and n_disrupt >= 1:
        classification = "LIKELY"
    elif n_disrupt >= 2 or (n_bri >= 1 and n_disrupt >= 1):
        classification = "LIKELY"
    elif n_disrupt >= 1 or n_bri >= 1:
        classification = "WEAK"
    else:
        classification = "NOISE"

    return {
        "classification": classification,
        "n_companies": n_company,
        "n_disruptions": n_disrupt,
        "n_bri_context": n_bri,
        "companies_found": ", ".join(sorted(set(c for c in companies)))[:100],
        "disruption_kw": ", ".join(disruptions[:5]),
        "bri_kw": ", ".join(bri_context[:3]),
        "value_hint": value_str,
        "project_hint": project_name,
    }


# ── Cargar señales Tier 2 ────────────────────────────────────────────────────
print("=== Cargando señales Tier 2 ===")
signals = pd.read_csv("data/samples/final/global_bri_verified_signals.csv")
tier2 = signals[(signals["score"] >= 3.0) & (signals["score"] < 5.0)].copy()
print(f"Total Tier 2: {len(tier2)}")

# Priorizar por región sub-representada
tier2["region_priority"] = tier2["region"].map(REGION_PRIORITY).fillna(99)
tier2 = tier2.sort_values(["region_priority", "score"], ascending=[True, False])

# Cargar casos conocidos para excluir duplicados
known = pd.read_csv("data/samples/final/bri_cancellations_consolidated.csv")
known_urls = set(known["source"].str.lower().dropna())
print(f"Casos conocidos: {len(known)}")

# Cargar corroboración GKG de Script 23a
gkg_corr_path = "data/samples/gkg_global/gkg_case_corroboration.csv"
gkg_corr = {}
if os.path.exists(gkg_corr_path):
    df_corr = pd.read_csv(gkg_corr_path)
    for _, r in df_corr.iterrows():
        gkg_corr[r["country"]] = r["gkg_articles"]

# ── Verificar URLs ───────────────────────────────────────────────────────────
print(f"\n=== Verificando {len(tier2)} URLs ===\n")
results = []

for i, (idx, row) in enumerate(tier2.iterrows()):
    url = str(row["url"])
    country = str(row["country_name"]) if pd.notna(row["country_name"]) else "Unknown"
    region = str(row["region"]) if pd.notna(row["region"]) else "Other"
    score = row["score"]

    print(f"[{i+1}/{len(tier2)}] {country:20s} {region:15s} score={score:.1f}", end=" ")

    # Fetch
    article = fetch_article(url)

    if article["fetched"]:
        # Classify
        cls = classify_signal(article["text"], article["title"], url, country, score)
        print(f"→ {cls['classification']} (co={cls['n_companies']} dis={cls['n_disruptions']} bri={cls['n_bri_context']})")
    else:
        cls = {
            "classification": "DEAD_URL",
            "n_companies": 0, "n_disruptions": 0, "n_bri_context": 0,
            "companies_found": "", "disruption_kw": "", "bri_kw": "",
            "value_hint": "", "project_hint": "",
        }
        print(f"→ DEAD ({article['error']})")

    results.append({
        "country": country,
        "country_code": row["country_code"],
        "region": region,
        "year": row["year"],
        "score": score,
        "url": url,
        "category": row["category"],
        "project_match": row.get("project_match", ""),
        "title": article["title"][:200],
        "fetched": article["fetched"],
        "http_error": article["error"],
        **cls,
        "gkg_corroboration": gkg_corr.get(country, 0),
    })

    time.sleep(SLEEP_BETWEEN)

# ── Resultados ────────────────────────────────────────────────────────────────
df_results = pd.DataFrame(results)

print(f"\n{'='*60}")
print("=== RESULTADOS ===")
print(f"\nTotal verificadas: {len(df_results)}")
print(f"\nClasificación:")
print(df_results["classification"].value_counts().to_string())

print(f"\nPor región:")
for region in df_results["region"].unique():
    rd = df_results[df_results["region"] == region]
    confirmed = len(rd[rd["classification"].isin(["CONFIRMED", "LIKELY"])])
    total = len(rd)
    print(f"  {region:20s} {confirmed}/{total} confirmed+likely")

# ── Nuevos casos ──────────────────────────────────────────────────────────────
print("\n=== NUEVOS CASOS DESCUBIERTOS ===")
new_cases = df_results[df_results["classification"].isin(["CONFIRMED", "LIKELY"])].copy()
print(f"Confirmed + Likely: {len(new_cases)}")

# Mostrar detalle
for _, c in new_cases.iterrows():
    already = "KNOWN" if any(c["url"].lower() in ku for ku in known_urls) else "NEW"
    print(f"\n  [{c['classification']}] {already} | {c['country']} ({c['region']}) {c['year']}")
    print(f"    Companies: {c['companies_found'][:80]}")
    print(f"    Disruption: {c['disruption_kw'][:80]}")
    print(f"    BRI: {c['bri_kw'][:60]}")
    print(f"    Project: {c['project_hint'][:60]}")
    print(f"    Value: {c['value_hint']}")
    print(f"    Title: {c['title'][:100]}")
    print(f"    URL: {c['url'][:100]}")

# ── Guardar ───────────────────────────────────────────────────────────────────
print("\n=== Guardando ===")
df_results.to_csv("data/samples/final/tier2_verified.csv", index=False)
print(f"  tier2_verified.csv: {len(df_results)} rows")

if len(new_cases) > 0:
    new_cases.to_csv("data/samples/final/tier2_new_cases.csv", index=False)
    print(f"  tier2_new_cases.csv: {len(new_cases)} rows")

# ── Reporte ───────────────────────────────────────────────────────────────────
with open("data/samples/final/tier2_verification_report.md", "w") as f:
    f.write("# Tier 2 Global Signal Verification Report (Script 24)\n\n")
    f.write(f"**Fecha**: {pd.Timestamp.now().strftime('%Y-%m-%d')}\n\n")

    f.write("## Resumen\n\n")
    f.write(f"- Señales Tier 2 verificadas: {len(df_results)}\n")
    f.write(f"- URLs accesibles: {df_results['fetched'].sum()}\n")
    f.write(f"- URLs muertas: {(~df_results['fetched']).sum()}\n\n")

    f.write("### Clasificación\n\n")
    f.write("| Clase | N |\n|-------|---|\n")
    for cls, n in df_results["classification"].value_counts().items():
        f.write(f"| {cls} | {n} |\n")

    f.write("\n### Por región\n\n")
    f.write("| Región | Confirmed+Likely | Total | Precisión |\n")
    f.write("|--------|-----------------|-------|----------|\n")
    for region in sorted(df_results["region"].unique()):
        rd = df_results[df_results["region"] == region]
        confirmed = len(rd[rd["classification"].isin(["CONFIRMED", "LIKELY"])])
        total = len(rd)
        pct = f"{100*confirmed/total:.0f}%" if total > 0 else "N/A"
        f.write(f"| {region} | {confirmed} | {total} | {pct} |\n")

    f.write("\n## Casos confirmados y probables\n\n")
    for _, c in new_cases.iterrows():
        f.write(f"\n### {c['country']} ({c['year']}) — {c['classification']}\n")
        f.write(f"- **Companies**: {c['companies_found'][:100]}\n")
        f.write(f"- **Disruption**: {c['disruption_kw'][:100]}\n")
        f.write(f"- **BRI context**: {c['bri_kw'][:80]}\n")
        f.write(f"- **Project**: {c['project_hint'][:60]}\n")
        f.write(f"- **Value**: {c['value_hint']}\n")
        f.write(f"- **Title**: {c['title'][:150]}\n")
        f.write(f"- **URL**: {c['url']}\n")

print("\n✓ Reporte: data/samples/final/tier2_verification_report.md")
print("\n=== SCRIPT 24 COMPLETO ===")
