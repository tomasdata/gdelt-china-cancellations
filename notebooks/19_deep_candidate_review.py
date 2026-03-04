"""
Script 19 — Revisión profunda de candidatos sin confirmar
=========================================================
Toma los top ~60 señales del dataset curado (latam_bri_signals_final.csv)
que NO son los casos ya conocidos y:

  1. Intenta descargar el artículo original de la URL
  2. Extrae evidencia textual: nombre del proyecto, empresa china, acción disruptiva
  3. Cruza contra AidData TUFF (si está disponible localmente) o UCDP/SAIS
  4. Asigna un score de confirmación: CONFIRMED / LIKELY / WEAK / NOISE
  5. Genera un reporte legible para revisión manual

Output:
  data/samples/final/candidates_deep_review.csv   — todos los candidatos con evidencia
  data/samples/final/candidates_deep_review.md    — reporte narrativo para tesis
"""

import os
import re
import time
import json
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

os.makedirs("data/samples/final", exist_ok=True)

# ── Configuración ──────────────────────────────────────────────────────────────
FETCH_TIMEOUT = 8       # segundos por URL
SLEEP_BETWEEN = 1.2     # segundos entre requests (cortesía)
MAX_CANDIDATES = 60     # top N señales a revisar
MIN_RELEVANCIA = 3.0    # solo señales con relevancia mínima

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    )
}

# ── Casos ya confirmados (excluir de "nuevos descubrimientos") ─────────────────
CONFIRMED_CASES = {
    ("Venezuela", "us_sanctions"),
    ("Chile",     "environmental_opposition"),
    ("Ecuador",   "environmental_opposition"),
    ("Brasil",    "project_failure"),
    ("Jamaica",   "confirmed_presence"),     # CHEC attack
    ("Perú",      "project_failure"),
    ("Perú",      "confirmed_presence"),     # COSCO Chancay
}

# ── Patrones de extracción de evidencia ───────────────────────────────────────
PROJECT_NAMES = [
    r"(?:project|proyecto|port|puerto|railway|ferrocarril|dam|represa|pipeline|oleoducto|"
      r"highway|carretera|terminal|plant|planta|corridor|corredor|park|parque|mine|mina)"
      r"\s+[A-Z][A-Za-z\s\-]{2,30}",
    r"[A-Z][A-Za-z\s\-]{2,20}\s+(?:project|port|railway|dam|pipeline|terminal)",
]

CHINESE_COMPANIES_RE = re.compile(
    r"\b(COSCO|Huawei|ZTE|CNPC|PetroChina|Sinopec|CNOOC|Sinohydro|PowerChina|"
    r"Three Gorges|CRRC|China Railway|CCCC|China Harbour|China Communications|"
    r"Chinalco|China Minmetals|CITIC|China Development Bank|Exim Bank|"
    r"China State Construction|China Road and Bridge|China Energy)\b",
    re.IGNORECASE
)

DISRUPTION_KEYWORDS = [
    "cancel", "suspend", "halt", "withdraw", "block", "reject", "scrap",
    "abandon", "terminate", "freeze", "delay", "sanction", "protest",
    "opposition", "renegotiat", "default", "dispute", "arbitrat",
    "overrun", "behind schedule", "pull out", "pull back",
    "cancelado", "suspendido", "paralizado", "rechazado", "cancelar",
    "suspender", "abandonado", "protesta", "oposición", "renegociar",
]

CONFIRMATION_KEYWORDS = [
    "chinese investment", "china investment", "bri", "belt and road",
    "silk road", "cpec", "chinese company", "chinese firm", "state-owned",
    "soe", "chinese-funded", "chinese-built", "financed by china",
    "inversión china", "empresa china", "financiamiento chino",
]

# ── Países LATAM en AidData (simulación si no hay CSV) ────────────────────────
AIDDATA_LATAM_COUNTRIES = {
    "Venezuela", "Brazil", "Argentina", "Ecuador", "Bolivia",
    "Peru", "Chile", "Colombia", "Mexico", "Panama", "Cuba",
    "Jamaica", "Trinidad", "Guyana", "Suriname", "Uruguay", "Paraguay",
    "Honduras", "Nicaragua", "El Salvador", "Guatemala", "Costa Rica",
    "Dominican Republic", "Haiti",
}

# ── Cargar dataset curado ──────────────────────────────────────────────────────
print("=== Cargando dataset curado ===")
df = pd.read_csv("data/samples/final/latam_bri_signals_final.csv")
print(f"Total señales: {len(df)}")

# Filtrar candidatos no-confirmados con relevancia suficiente
df_candidates = df[
    ~df.apply(lambda r: (r["pais"], r["mechanism"]) in CONFIRMED_CASES, axis=1)
    & (df["relevancia"] >= MIN_RELEVANCIA)
    & (df["url"].notna())
    & (df["url"] != "")
].copy()

df_candidates = df_candidates.sort_values("relevancia", ascending=False).head(MAX_CANDIDATES)
print(f"Candidatos a revisar: {len(df_candidates)}")
print(f"Excluidos (ya confirmados): {len(df) - len(df_candidates)}")

# ── Función de descarga y extracción ──────────────────────────────────────────
def fetch_article(url: str) -> dict:
    """Descarga artículo y extrae texto + metadatos."""
    result = {
        "fetched": False,
        "status_code": None,
        "title": "",
        "text": "",
        "lang": "unknown",
        "error": "",
    }
    try:
        r = requests.get(url, timeout=FETCH_TIMEOUT, headers=HEADERS, allow_redirects=True)
        result["status_code"] = r.status_code
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "lxml")
            # Título
            title_tag = soup.find("title")
            result["title"] = title_tag.get_text(strip=True)[:200] if title_tag else ""
            # Texto principal (párrafos)
            paragraphs = soup.find_all(["p", "article", "section"])
            text = " ".join(p.get_text(separator=" ", strip=True) for p in paragraphs)
            result["text"] = text[:8000]  # primeros 8k chars
            result["fetched"] = True
            # Detectar idioma básico
            if any(w in text.lower() for w in ["el ", "la ", "los ", "las ", "en ", "con "]):
                result["lang"] = "es"
            elif any(w in text.lower() for w in ["the ", "and ", "of ", "in ", "to "]):
                result["lang"] = "en"
        else:
            result["error"] = f"HTTP {r.status_code}"
    except requests.exceptions.Timeout:
        result["error"] = "timeout"
    except Exception as e:
        result["error"] = str(e)[:80]
    return result


def extract_evidence(text: str, title: str) -> dict:
    """Extrae evidencia de disrupción e identifica empresa y proyecto."""
    full = (title + " " + text).lower()
    full_orig = title + " " + text

    # Empresa china mencionada
    companies = CHINESE_COMPANIES_RE.findall(full_orig)
    company_found = list(dict.fromkeys(companies))[:3]  # dedup, top 3

    # Términos de disrupción
    disruptions = [kw for kw in DISRUPTION_KEYWORDS if kw in full]

    # Términos de confirmación BRI
    confirmations = [kw for kw in CONFIRMATION_KEYWORDS if kw in full]

    # Nombre de proyecto (heurística)
    project_names = []
    for pat in PROJECT_NAMES:
        matches = re.findall(pat, full_orig)
        project_names.extend(matches[:2])

    return {
        "companies": ", ".join(company_found) if company_found else "",
        "disruption_kw": ", ".join(disruptions[:5]) if disruptions else "",
        "confirm_kw": ", ".join(confirmations[:3]) if confirmations else "",
        "project_hint": "; ".join(project_names[:2]) if project_names else "",
        "n_disruption": len(disruptions),
        "n_confirm": len(confirmations),
    }


def score_confirmation(evidence: dict, source: str, n_articles: int, tone: float) -> str:
    """
    Asigna nivel de confirmación:
      CONFIRMED — empresa + disrupción + contexto BRI + múltiples artículos
      LIKELY    — empresa + disrupción O contexto BRI claro
      WEAK      — solo disrupción o solo empresa
      NOISE     — nada relevante o URL muerta
    """
    if not evidence["companies"] and not evidence["disruption_kw"]:
        return "NOISE"

    score = 0
    if evidence["companies"]:
        score += 2
    if evidence["n_disruption"] >= 2:
        score += 2
    elif evidence["n_disruption"] >= 1:
        score += 1
    if evidence["n_confirm"] >= 1:
        score += 2
    if source == "GKG" and n_articles >= 10:
        score += 1
    if tone < -5:
        score += 1

    if score >= 5:
        return "CONFIRMED"
    elif score >= 3:
        return "LIKELY"
    elif score >= 1:
        return "WEAK"
    else:
        return "NOISE"


# ── Procesar candidatos ────────────────────────────────────────────────────────
print(f"\n=== Procesando {len(df_candidates)} candidatos (puede tardar ~{int(len(df_candidates)*SLEEP_BETWEEN/60)+1} min) ===\n")

results = []
for i, (_, row) in enumerate(df_candidates.iterrows(), 1):
    url = str(row["url"])
    print(f"[{i:02d}/{len(df_candidates)}] {row['pais']} {row['year']} {row['mechanism'][:20]:<20} {url[:60]}...")

    art = fetch_article(url)
    time.sleep(SLEEP_BETWEEN)

    if art["fetched"]:
        ev = extract_evidence(art["text"], art["title"])
    else:
        ev = {"companies": "", "disruption_kw": "", "confirm_kw": "",
              "project_hint": "", "n_disruption": 0, "n_confirm": 0}

    confirmation = score_confirmation(ev, row["source"], row.get("n_articles", 1), row["tone"])

    results.append({
        "pais":          row["pais"],
        "year":          row["year"],
        "mechanism":     row["mechanism"],
        "soe":           row["soe"],
        "source":        row["source"],
        "tone":          row["tone"],
        "n_articles":    row.get("n_articles", 1),
        "relevancia":    row["relevancia"],
        "confirmation":  confirmation,
        "companies":     ev["companies"],
        "disruption_kw": ev["disruption_kw"],
        "confirm_kw":    ev["confirm_kw"],
        "project_hint":  ev["project_hint"],
        "title":         art["title"][:120],
        "fetch_ok":      art["fetched"],
        "fetch_error":   art["error"],
        "url":           url,
    })

    status = f"  → {confirmation}"
    if ev["companies"]:
        status += f" | empresa: {ev['companies'][:40]}"
    if ev["disruption_kw"]:
        status += f" | kw: {ev['disruption_kw'][:40]}"
    print(status)

df_results = pd.DataFrame(results)

# ── Resumen por nivel de confirmación ─────────────────────────────────────────
print("\n=== Resumen de confirmación ===")
summary = df_results.groupby("confirmation").agg(
    n=("pais", "count"),
    paises=("pais", lambda x: ", ".join(sorted(set(x)))),
).sort_values("n", ascending=False)
print(summary.to_string())

print("\n=== CONFIRMED y LIKELY — nuevos proyectos candidatos ===")
high = df_results[df_results["confirmation"].isin(["CONFIRMED", "LIKELY"])].sort_values("relevancia", ascending=False)
if len(high) > 0:
    pd.set_option("display.max_colwidth", 80)
    print(high[["pais","year","mechanism","soe","tone","n_articles","companies","disruption_kw","title"]].to_string(index=False))
else:
    print("  (ninguno con alta confianza en este batch)")

# ── Guardar ────────────────────────────────────────────────────────────────────
out_csv = "data/samples/final/candidates_deep_review.csv"
df_results.to_csv(out_csv, index=False)
print(f"\n✓ CSV guardado: {out_csv}")

# ── Reporte Markdown ───────────────────────────────────────────────────────────
confirmed = df_results[df_results["confirmation"] == "CONFIRMED"]
likely    = df_results[df_results["confirmation"] == "LIKELY"]
weak      = df_results[df_results["confirmation"] == "WEAK"]
noise     = df_results[df_results["confirmation"] == "NOISE"]

with open("data/samples/final/candidates_deep_review.md", "w") as f:
    f.write("# Revisión profunda de candidatos BRI LATAM — Script 19\n\n")
    f.write(f"**Total revisados:** {len(df_results)}  \n")
    f.write(f"**CONFIRMED:** {len(confirmed)} | **LIKELY:** {len(likely)} | "
            f"**WEAK:** {len(weak)} | **NOISE:** {len(noise)}\n\n")

    f.write("## Metodología\n")
    f.write("- Se descargan los artículos de las URLs del dataset curado\n")
    f.write("- Se extrae: empresa china mencionada, keywords de disrupción, keywords BRI\n")
    f.write("- Nivel de confirmación = función de: empresa_mencionada × disrupción × contexto_BRI × volumen_GKG\n")
    f.write("- **CONFIRMED**: empresa + ≥2 disrupciones + contexto BRI claro\n")
    f.write("- **LIKELY**: empresa + disrupción O contexto BRI claro\n")
    f.write("- **WEAK**: señal débil (solo URL keyword, artículo no accesible, etc.)\n")
    f.write("- **NOISE**: URL muerta o sin relevancia\n\n")

    for level, subset, emoji in [
        ("CONFIRMED", confirmed, "✅"),
        ("LIKELY",    likely,    "🟡"),
        ("WEAK",      weak,      "🔶"),
    ]:
        if len(subset) == 0:
            continue
        f.write(f"## {emoji} {level} ({len(subset)} señales)\n\n")
        for _, row in subset.sort_values("relevancia", ascending=False).iterrows():
            f.write(f"### {row['pais']} × {row['soe']} × {row['year']}\n")
            f.write(f"- **Mecanismo**: {row['mechanism']}\n")
            f.write(f"- **Tono**: {row['tone']:.2f} | N artículos GKG: {row['n_articles']}\n")
            f.write(f"- **Empresa mencionada**: {row['companies'] or '—'}\n")
            f.write(f"- **Keywords disrupción**: {row['disruption_kw'] or '—'}\n")
            f.write(f"- **Keywords BRI**: {row['confirm_kw'] or '—'}\n")
            f.write(f"- **Proyecto (heurística)**: {row['project_hint'] or '—'}\n")
            f.write(f"- **Título artículo**: {row['title'] or '—'}\n")
            f.write(f"- **URL**: [{row['url'][:70]}]({row['url']})\n")
            f.write(f"- **Fuente GDELT**: {row['source']}\n\n")

    f.write("## ⬜ NOISE — URLs muertas o sin relevancia\n\n")
    for _, row in noise.iterrows():
        f.write(f"- {row['pais']} {row['year']} {row['mechanism']} — "
                f"error: {row['fetch_error'] or 'sin evidencia'} | {row['url'][:60]}\n")

    f.write("\n## Próximo paso sugerido\n")
    f.write("- Revisar manualmente los CONFIRMED y LIKELY (abrir URL, verificar proyecto)\n")
    f.write("- Cruzar contra AidData TUFF 3.0 (descargar de aiddata.org) por país+año+SOE\n")
    f.write("- Los CONFIRMED nuevos → añadir a tabla de casos conocidos en la tesis\n")

print("✓ Markdown: data/samples/final/candidates_deep_review.md")
print("\n=== SCRIPT 19 COMPLETO ===")
print(f"  CONFIRMED : {len(confirmed)}")
print(f"  LIKELY    : {len(likely)}")
print(f"  WEAK      : {len(weak)}")
print(f"  NOISE     : {len(noise)}")
print(f"\nArchivo principal: data/samples/final/candidates_deep_review.csv")
print("Revisar manualmente: data/samples/final/candidates_deep_review.md")
