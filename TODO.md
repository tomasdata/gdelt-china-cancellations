# TODO — GDELT BRI Pipeline

**Última actualización**: 2026-03-05
**Estado actual**: 70 casos verificados (Scripts 01–29), AidData descargado y cruzado

---

## Próximo paso: Script 30 — Búsqueda GDELT de proyectos AidData

### Contexto
Script 29 cruzó nuestros 70 casos con AidData GCDF 3.0 (20,985 proyectos chinos). Resultado:
- **627 proyectos problemáticos** en AidData (92 cancelled, 45 suspended, 493 financial distress)
- 42/70 de nuestros casos tienen match fuerte con AidData
- 5 casos confirmados como problemáticos en ambos datasets

### Objetivo
Buscar **TODOS** los 627 proyectos AidData problemáticos en GDELT (BigQuery Events + GKG local) para:
1. Entender qué % de cancelaciones AidData captura GDELT
2. Descubrir nuevos casos que no tenemos en nuestros 70
3. Analizar la dinámica global completa (no solo los de alto valor)

### Implementación (`notebooks/30_aiddata_gdelt_search.py`)

**Paso 1: Preparar queries**
- Extraer país (FIPS code), año ± 2, keywords del título de cada proyecto
- Agrupar por país para queries batch
- Reutilizar FIPS_MAP de `notebooks/23a_gkg_global_soe.py`

**Paso 2: GDELT Events search** (BigQuery ~$3-5)
- Para cada país con proyectos AidData problemáticos:
  - Query: eventos China+conflicto+económico en ese país, 2015-2024
  - Extraer URLs con keywords del proyecto
- Proyecto GCP: `tomasdata-gdelt-research` (salareuniones113@gmail.com)
- SIEMPRE dry_run primero

**Paso 3: GKG search** (parquets locales, $0)
- Usar parquets en `data/samples/gkg_por_año/raw/` (4.7 GB, 2017-2024)
- Buscar por nombre de empresa china (Funding Agencies de AidData)
- Buscar por nombre de proyecto en AllNames/DocumentIdentifier

**Paso 4: Clasificar**
- COVERED (≥3 artículos), PARTIAL (1-2), NOT_FOUND (0)
- Análisis por país, sector, status, región

**Paso 5: Narrativa**
- Estadística clave: "De 627 proyectos problemáticos AidData, GDELT detecta X (Y%)"

**Output:**
- `data/samples/validation/aiddata_gdelt_coverage.csv` (627 filas)
- `data/samples/validation/aiddata_gdelt_new_cases.csv`
- `data/samples/validation/aiddata_gdelt_report.md`

---

## Pendientes adicionales

### Dataset AidData — Hallazgos clave del Script 29
- **20,985 proyectos chinos** en 165 países (2000-2021), US$1.34T
- Solo **0.6% formalmente cancelados/suspendidos** (137 de 20,985)
- **2.3% en financial distress** (493 proyectos)
- **96 proyectos de infraestructura** cancelados/suspendidos
- Top candidatos no en nuestro dataset:
  - Ghana: $14.5B transport (Suspended)
  - Argentina: $7.4B nuclear (Suspended) + $2.5B hydro (Suspended)
  - Thailand: $5.9B rail (Cancelled)
  - Ukraine: $4.3B energy transition (Cancelled)
  - Kazakhstan: $1.8B petrochemical (Suspended) + $1.7B rail (Cancelled)
  - Bolivia: $1.2B Rositas hydro (Suspended)
  - Zimbabwe: $1B water (Suspended)
  - Belarus: $836M airport (Cancelled)
  - Sudan: $775M rail (Cancelled × 2)
  - Niger: $1.1B master facility (Cancelled)

### Script 31: Dataset Final v3 (después de Script 30)
- Merge: 70 casos actuales + nuevos descubiertos via AidData+GDELT
- Enriquecer con: `aiddata_project_id`, `aiddata_status`, `aiddata_amount`
- Tablas thesis actualizadas

### Otros pendientes
- **GDELT v1** para pre-2015 (muchos proyectos AidData son 2000-2014)
- **93 señales LIKELY** del Tier 2 (Script 24) sin verificar manualmente
- **42/70 casos** sin value_usd — enriquecer con datos AidData
- **IISS China Connects** database (https://chinaconnects.iiss.org/) — otra fuente de proyectos BRI con filtro halted/cancelled

---

## Datos disponibles

### Dataset principal
- `data/samples/final/bri_cancellations_FINAL_v2.csv` — **70 casos verificados**

### AidData (descargado)
- `data/external/aiddata_gcdf_v3/` — GCDF 3.0 Excel (20,985 proyectos)
- `data/samples/validation/aiddata_new_candidates.csv` — 627 candidatos problemáticos
- `data/samples/validation/aiddata_match_results.csv` — matching 70 casos
- `data/samples/validation/aiddata_coverage_analysis.csv` — gaps por país
- `data/samples/validation/aiddata_validation_report.md` — reporte

### GKG local
- `data/samples/gkg_por_año/raw/` — parquets 2017-2024 (4.7 GB)

### BigQuery
- Proyecto: `tomasdata-gdelt-research`
- Cuenta: `salareuniones113@gmail.com`
- Créditos: $300 disponibles
- Events table: `gdelt-bq.gdeltv2.events` (~7 GB scan)
- GKG table: `gdelt-bq.gdeltv2.gkg` (~$6-12/query)
