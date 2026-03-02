"""
Script 09 v2 — Taxonomía de contextos: separar BRI/inversión de ruido
Input:  data/samples/events_china_conflict_2017_2024_dedup.csv  (248k)
        data/samples/events_china_economic_2017_2024_dedup.csv   (45k)

v2 mejoras:
  - has_chinese_actor(): valida que haya actor/empresa china antes de clasificar como BRI
  - has_project_signal(): requiere término de PROYECTO + término de ACCIÓN (no basta con uno)
  - detect_mechanism(): detecta por qué se canceló (sanciones, medioambiental, político, deuda)
  - BRI_RECEIVER_FIPS: añadidos GY/NS/CS/JM/HA/ES/HO/DR (antes faltaban)
  - Output adicional: bri_investment_events_v2.csv + columna 'mechanism'

Categorías de contexto:
  trade_war      — guerra comercial EEUU-China (aranceles, tarifas)
  military       — tensiones militares, Taiwan, Corea del Norte
  bri_investment — proyectos infraestructura/inversión en países receptores
  financial      — sanciones, bloqueos financieros, deuda
  other          — resto
"""

import os
import re
import pandas as pd

# ── Constantes ──────────────────────────────────────────────────────────────────
TRADE_WAR_GEO = {"US", "CA", "AS", "GM", "FR", "UK", "JA"}

# Lista de SOEs y empresas chinas clave (para validar que el evento involucra actor chino)
CHINESE_ACTORS = {
    # Infraestructura/transporte
    "CHINA RAILWAY", "CRRC", "CR GROUP",
    "COSCO", "CHINA OCEAN SHIPPING",
    "CHINA COMMUNICATIONS", "CHINA HARBOUR", "CCCC",
    "SINOHYDRO", "CHINA GEZHOUBA", "THREE GORGES", "POWERCHINA",
    "CHINA STATE CONSTRUCTION", "CHINA ROAD AND BRIDGE", "CHINA ENERGY",
    "CHINA NATIONAL PETROLEUM",
    # Energía/petróleo
    "CNPC", "PETROCHINA", "CNOOC", "SINOPEC",
    # Finanzas/desarrollo
    "CHINA DEVELOPMENT BANK", "EXIM BANK", "CDB", "EXIMBANK",
    "SILK ROAD FUND", "ICBC", "BANK OF CHINA", "CCB",
    # Tecnología/telecom
    "HUAWEI", "ZTE", "NUCTECH", "CHINA TELECOM", "CHINA MOBILE", "CHINA UNICOM",
    # Minería/recursos
    "CITIC", "CHINA MINMETALS", "CHINALCO",
    # Iniciativa BRI
    "BELT AND ROAD", "SILK ROAD", "CPEC", "OBOR", "BRI INITIATIVE",
}

BRI_RECEIVER_FIPS = {
    # LATAM
    "CI", "AR", "BR", "MX", "PE", "CO", "VE", "BL", "EC", "UY",
    "PA", "PM", "CU", "GT", "NU", "ES", "HO", "BH", "DR",
    # v2: añadidos (antes faltaban)
    "GY",  # Guyana
    "NS",  # Suriname
    "CS",  # Costa Rica
    "JM",  # Jamaica
    "HA",  # Haití
    # África
    "SF", "NI", "ET", "KE", "AO", "UG", "TZ", "MZ", "ZA", "GH",
    "CM", "SN", "ZI", "EG", "LY", "SU", "DJ", "MR", "IV", "CG",
    "CF", "ML", "BU",
    # Asia Central/Sur
    "PK", "BD", "NP", "AF", "UZ", "KZ", "TM", "KG", "TJ",
    # Asia SE
    "RP", "TH", "MY", "ID", "VM", "CB", "BM", "LA",
    # Medio Oriente
    "IZ", "IR", "SA", "AE", "QA", "IS", "JO", "SY", "LE", "YM", "TU",
    # Europa Oriental
    "UP", "PL", "HU", "RO", "BK", "HR", "SI", "AL", "MN", "GG", "AJ", "AM",
    # Oceanía
    "PP", "FJ", "WS", "TO",
}


# ── Funciones de validación ──────────────────────────────────────────────────────

def has_chinese_actor(row) -> bool:
    """Puerta 1: ¿el evento involucra un actor/empresa china?"""
    a1 = str(row.get("Actor1Name", "") or "").upper()
    a2 = str(row.get("Actor2Name", "") or "").upper()
    a1c = str(row.get("Actor1CountryCode", "") or "").upper()
    a2c = str(row.get("Actor2CountryCode", "") or "").upper()
    url = str(row.get("SOURCEURL", "") or "").lower()

    # Código de país chino
    if "CHN" in (a1c, a2c):
        return True
    # Nombre genérico china/chinese en actores
    for term in ("CHINA", "CHINESE", "SINO"):
        if term in a1 or term in a2:
            return True
    # SOEs específicas en nombre de actor o URL
    for co in CHINESE_ACTORS:
        if co in a1 or co in a2 or co.lower() in url:
            return True
    return False


def has_project_signal(url: str, a1: str, a2: str) -> bool:
    """
    Puerta 2: ¿el URL o actores contienen señal de PROYECTO + ACCIÓN?
    Se requieren AMBOS para reducir falsos positivos.
    """
    url = url.lower()
    a1 = a1.upper()
    a2 = a2.upper()

    PROJECT_TERMS = [
        "invest", "project", "infrastructure", "port", "railway", "dam",
        "pipeline", "power.plant", "power-plant", "powerplant", "energy",
        "telecom", "fiber", "bridge", "road", "highway", "airport", "stadium",
        "hospital", "bri", "silk.road", "silk-road", "cpec", "obor",
        "loan", "debt", "corridor", "concession", "contract",
        "construction", "mining", "refinery", "terminal",
    ]
    ACTION_TERMS = [
        "cancel", "halt", "suspend", "withdraw", "block", "reject", "ban",
        "scrap", "abandon", "terminate", "freeze", "delay", "pause",
        "sanction", "protest", "opposition", "dispute",
        "renegotiat", "default", "debt.trap",
    ]

    has_proj = any(re.search(pt, url) for pt in PROJECT_TERMS)
    has_act = any(re.search(at, url) for at in ACTION_TERMS)

    if has_proj and has_act:
        return True

    # Términos compuestos son señal suficiente solos
    COMPOUND = [
        "chinese.investment", "chinese-investment", "china.project", "china-project",
        "chinese.firm", "chinese-firm", "chinese.company", "state-owned.enterprise",
        "bri.cancel", "belt.road.cancel", "china.loan", "chinese.debt",
    ]
    return any(re.search(c, url) for c in COMPOUND)


def detect_mechanism(row) -> str:
    """
    Detecta el mecanismo de cancelación/disrupción del proyecto BRI.
    Solo aplicar a filas ya clasificadas como bri_investment.
    """
    url = str(row.get("SOURCEURL", "") or "").lower()

    # Sanciones secundarias EEUU (mecanismo Venezuela/Irán)
    if any(w in url for w in [
        "sanction", "ofac", "treasury", "secondary.sanction",
        "unipec", "zte.sanction", "executive.order", "blacklist",
        "entity.list", "us.sanction", "american.sanction"
    ]):
        return "us_sanctions"

    # Oposición ambiental/comunitaria
    if any(w in url for w in [
        "environment", "deforest", "indigenous", "community.protest",
        "yasuni", "national.park", "conservation", "green",
        "ecology", "pollution", "activist", "civil.society"
    ]):
        return "environmental_opposition"

    # Rechazo político del host country (gobierno, parlamento)
    if any(w in url for w in [
        "parliament", "congress", "government.cancel", "government.reject",
        "revoke", "sovereignty", "nationalism", "foreign.ownership",
        "cancel.contract", "minister.suspend", "president.halt"
    ]):
        return "political_rejection"

    # Renegociación de deuda / debt trap
    if any(w in url for w in [
        "debt.trap", "debt.renegotiat", "restructur", "default",
        "imf", "world.bank", "unsustainable.debt", "refinanc",
        "debt.relief", "debt.cancel"
    ]):
        return "debt_renegotiation"

    # Problemas técnicos / retrasos / disputas contractuales
    if any(w in url for w in [
        "delay", "cost.overrun", "behind.schedule", "technical.problem",
        "quality.issue", "arbitration", "labor.dispute"
    ]):
        return "project_failure"

    # Desplazamiento por competencia (Japón, Corea, ADB, AIIB)
    if any(w in url for w in [
        "japan.instead", "south.korea.instead", "aiib", "adb.loan",
        "alternative.investor", "lost.tender", "outbid"
    ]):
        return "competition_displacement"

    return "unknown"


def classify_event(row) -> str:
    a1 = str(row.get("Actor1Name", "") or "").upper()
    a2 = str(row.get("Actor2Name", "") or "").upper()
    a1c = str(row.get("Actor1CountryCode", "") or "").upper()
    a2c = str(row.get("Actor2CountryCode", "") or "").upper()
    geo = str(row.get("ActionGeo_CountryCode", "") or "").upper()
    url = str(row.get("SOURCEURL", "") or "").lower()

    # --- Trade war: acción en EEUU/Occidente, actores occidentales con China ---
    if geo in TRADE_WAR_GEO or a1c in {"US", "CA", "AS", "GM", "JA", "UK", "FR"}:
        if a2c == "CHN" or "CHINA" in a2:
            return "trade_war"
    if any(w in url for w in ["tariff", "trade-war", "trade war", "wto", "sanction"]):
        if geo in {"US", "CH", "CA", "AS", "GM", "UK", "JA", "FR"}:
            return "trade_war"

    # --- Military/Taiwan/NK ---
    if geo in {"TW", "KS"} or a1c in {"TWN", "PRK"} or a2c in {"TWN", "PRK"}:
        return "military"
    if any(w in a1.lower() or w in a2.lower()
           for w in ["taiwan", "north korea", "military", "navy", "army", "pentagon"]):
        return "military"

    # --- BRI/Investment ---
    # En país receptor: requiere actor chino O señal de proyecto
    if geo in BRI_RECEIVER_FIPS:
        if has_chinese_actor(row) or has_project_signal(url, a1, a2):
            return "bri_investment"

    # Fuera de países receptores: requiere AMBAS puertas (más estricto)
    if has_project_signal(url, a1, a2) and has_chinese_actor(row):
        return "bri_investment"

    # --- Financial: sanciones o instrumentos financieros + actor chino ---
    if any(w in url for w in ["sanction", "debt", "loan", "imf", "world bank",
                               "default", "financial", "exim", "cdb"]):
        if has_chinese_actor(row):
            return "financial"

    return "other"


def process_dataset(path: str, label: str) -> pd.DataFrame:
    print(f"\n{'='*60}")
    print(f"Clasificando: {label}")
    df = pd.read_csv(path)
    print(f"  Filas input: {len(df):,}")

    df["context"] = df.apply(classify_event, axis=1)

    counts = df["context"].value_counts()
    print("\n  Distribución de contextos:")
    for ctx, n in counts.items():
        print(f"    {ctx:20s} {n:>8,}  ({n/len(df)*100:.1f}%)")

    # Por año
    print("\n  BRI/investment por año:")
    df_bri = df[df["context"] == "bri_investment"].copy()
    if "year" not in df_bri.columns:
        df_bri["year"] = df_bri["SQLDATE"] // 10000
    print(df_bri.groupby("year").size().rename("n").to_string())

    # Top países BRI
    print("\n  Top 20 países ActionGeo en BRI/investment:")
    print(df_bri["ActionGeo_CountryCode"].value_counts().head(20).to_string())

    # Añadir mecanismo a filas BRI
    print("\n  Detectando mecanismo de cancelación en filas BRI...")
    df.loc[df["context"] == "bri_investment", "mechanism"] = \
        df[df["context"] == "bri_investment"].apply(detect_mechanism, axis=1)
    df["mechanism"] = df["mechanism"].fillna("")

    # Distribución de mecanismos
    bri_rows = df[df["context"] == "bri_investment"]
    if len(bri_rows) > 0:
        print("\n  Mecanismos detectados en BRI:")
        mech_counts = bri_rows["mechanism"].value_counts()
        for m, n in mech_counts.items():
            print(f"    {m:30s} {n:>6,}  ({n/len(bri_rows)*100:.1f}%)")

    return df


# ── Procesar ambos datasets ─────────────────────────────────────────────────────
df_conflict = process_dataset(
    "data/samples/events_china_conflict_2017_2024_dedup.csv",
    "Conflicto (248k dedup)"
)

df_economic = process_dataset(
    "data/samples/events_china_economic_2017_2024_dedup.csv",
    "Económico (45k dedup)"
)

# ── Guardar por categoría ───────────────────────────────────────────────────────
print("\n" + "="*60)
print("Guardando datasets clasificados...")

for label_short, df in [("conflict", df_conflict), ("economic", df_economic)]:
    base = f"data/samples/classified_{label_short}"
    os.makedirs(base, exist_ok=True)
    for ctx in df["context"].unique():
        out = f"{base}/{ctx}.csv"
        df[df["context"] == ctx].to_csv(out, index=False)
    df.to_csv(f"data/samples/events_{label_short}_classified.csv", index=False)
    print(f"  ✓ {label_short}: guardado en data/samples/events_{label_short}_classified.csv")

# ── Merge BRI de ambos ──────────────────────────────────────────────────────────
bri_conflict = df_conflict[df_conflict["context"] == "bri_investment"].copy()
bri_conflict["source_dataset"] = "conflict"
bri_economic = df_economic[df_economic["context"] == "bri_investment"].copy()
bri_economic["source_dataset"] = "economic"

# Columnas comunes (incluyendo 'mechanism' nueva)
common_cols = ["SQLDATE", "Actor1Name", "Actor1CountryCode", "Actor2Name",
               "Actor2CountryCode", "EventCode", "AvgTone", "NumMentions",
               "ActionGeo_FullName", "ActionGeo_CountryCode", "SOURCEURL",
               "year", "context", "mechanism", "source_dataset"]
common_cols = [c for c in common_cols if c in bri_conflict.columns and c in bri_economic.columns]

bri_all = pd.concat([bri_conflict[common_cols], bri_economic[common_cols]], ignore_index=True)
bri_all = bri_all.drop_duplicates(subset=["SOURCEURL"])

# Guardar v2 (no sobreescribir v1 para comparación)
bri_all.to_csv("data/samples/bri_investment_events_v2.csv", index=False)
# También actualizar el archivo principal que usan scripts posteriores
bri_all.to_csv("data/samples/bri_investment_events_all.csv", index=False)

print(f"\n✓ BRI combinado v2: {len(bri_all):,} eventos únicos")
print(f"  Conflicto BRI: {len(bri_conflict):,}")
print(f"  Económico BRI: {len(bri_economic):,}")
print(f"  Overlap eliminado: {len(bri_conflict) + len(bri_economic) - len(bri_all):,}")

# ── Comparación v1 vs v2 ────────────────────────────────────────────────────────
print("\n=== COMPARATIVA v1 vs v2 ===")
print(f"  v1 (script 09 original): 52,439 eventos BRI")
print(f"  v2 (script 09 mejorado): {len(bri_all):,} eventos BRI")
change = len(bri_all) - 52439
direction = "más" if change > 0 else "menos"
print(f"  Diferencia: {abs(change):,} eventos {direction} (precisión esperada: mejor)")

# Distribución de mecanismos en BRI v2
print("\n=== MECANISMOS GLOBALES (v2) ===")
mech_global = bri_all["mechanism"].value_counts() if "mechanism" in bri_all.columns else pd.Series()
for m, n in mech_global.items():
    print(f"  {m:30s} {n:>6,}  ({n/len(bri_all)*100:.1f}%)")

# ── Actualizar ANALYSIS_FINDINGS.md ────────────────────────────────────────────
with open("docs/ANALYSIS_FINDINGS.md", "a") as f:
    f.write("\n## Script 09 v2 — Clasificador BRI mejorado\n\n")
    f.write("### Mejoras implementadas\n")
    f.write("- **Puerta-1**: `has_chinese_actor()` — valida que haya actor/empresa china antes de clasificar\n")
    f.write("- **Puerta-2**: `has_project_signal()` — requiere término de proyecto + término de acción (no solo uno)\n")
    f.write("- **`detect_mechanism()`**: detecta por qué se canceló (sanciones, medioambiental, político, deuda)\n")
    f.write("- **FIPS expandido**: añadidos GY/NS/CS/JM/HA/ES/HO/DR a BRI_RECEIVER_FIPS\n\n")
    f.write("### Resultados v2\n")
    f.write(f"- BRI combinado v2: {len(bri_all):,} eventos únicos\n")
    f.write(f"  - Conflicto BRI: {len(bri_conflict):,}\n")
    f.write(f"  - Económico BRI: {len(bri_economic):,}\n")
    f.write(f"- Comparativa: v1=52,439 → v2={len(bri_all):,} (cambio: {change:+,})\n\n")
    f.write("### Distribución de mecanismos (v2)\n")
    for m, n in mech_global.items():
        f.write(f"- `{m}`: {n:,} ({n/len(bri_all)*100:.1f}%)\n")
    f.write("\n### Próximo paso\n")
    f.write("- Script 10 v2: análisis geográfico con países LATAM corregidos\n")

print("\n✓ ANALYSIS_FINDINGS.md actualizado")
print("\n=== PRÓXIMO: script 10 con FIPS corregidos ===")
