# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

Pipeline GDELT para descubrimiento exhaustivo de proyectos con capital chino cancelados globalmente. Alimenta la tesis académica de Ariel Villalobos (Magíster Economía, U. Chile) sobre determinantes de cancelación de proyectos BRI/inversión china. El objetivo es expandir la muestra manual de 18 casos hacia un dataset comprehensivo.

## Alcance temporal

**Fase 1 (actual):** 2017–2024 — período principal de auge y tensión del BRI post-2015.
**Fase 2 (futura):** Retroceder a 2010–2016 para capturar ciclos anteriores a la formalización del BRI (2013+). GDELT v2 arranca en 2015; para pre-2015 se necesita `gdelt-bq.gdeltv1` con schema diferente. Los costos escalan proporcionalmente.

## Environment Setup

```bash
python3 -m venv gdelt_env
source gdelt_env/bin/activate
pip install -r requirements.txt
```

### BigQuery — cuenta GCP personal (ver docs/SETUP_NUEVA_CUENTA_GCP.md)
```bash
# Una vez creada cuenta en cloud.google.com/free ($300 créditos gratis)
gcloud auth application-default login
gcloud auth application-default set-quota-project gdelt-china-cancellations
python notebooks/03_bigquery_conexion.py   # verificar
```

**Cuenta activa:** `salareuniones113@gmail.com` → proyecto `tomasdata-gdelt-research`. $300 créditos disponibles. Completamente separado de Orsan.

## Pipeline de scripts (flujo aprobado)

**Enfoque: Contexto → Empresas → Casos** (no empresa pre-definida → artículos)

| Script | Estado | Qué hace |
|--------|--------|---------|
| `01_gdelt_csv_exploration.py` | ✅ Ejecutado | Prueba CSV públicos, documenta schema Events + GKG |
| `02_schema_con_headers.py` | ✅ Ejecutado | Schema con columnas nombradas, ejemplos reales |
| `03_bigquery_conexion.py` | ✅ Ejecutado | Verifica conexión BigQuery, esquemas de tablas |
| `04_discovery_cost_estimate.py` | ✅ Ejecutado | Estimación de costos de queries |
| `05_events_china_discovery.py` | ✅ Ejecutado | 374k eventos China+conflicto 2017-2024 (gratis) |
| `06_events_refine_economic.py` | ✅ Ejecutado | 76k eventos económicos refinados, LATAM 665 |
| `07_gkg_context_search.py` | ⏳ PRÓXIMO | GKG por **contexto temático** (no por empresa), ~$10-12 |
| `08_extract_companies.py` | ⏳ Pendiente | Extrae y rankea empresas chinas del output del 07 |
| `09_deep_dive_by_company.py` | ⏳ Pendiente | Búsqueda profunda caso a caso por empresa top |
| `10_dataset_final.py` | ⏳ Pendiente | Dataset estructurado para tesis (schema Año/Proyecto/País/Sector/Razón) |

**Datos ya en `data/samples/`:**
- `events_china_conflict_2017_2024.csv` — 374k eventos
- `events_china_economic_2017_2024.csv` — 76k eventos económicos

## BigQuery: tablas y costos reales observados

| Tabla | Período | Costo estimado |
|-------|---------|----------------|
| `gdeltv2.events` — Actor1/2CountryCode = CHN + conflicto | 2017-2024 | **144 GB → GRATIS** |
| `gdeltv2.gkg_partitioned` — V2Organizations LIKE '%HUAWEI%' | 2017-2024 | ~3,400 GB → ~$12 |
| `gdeltv2.gkg_partitioned` — 1 solo año | 1 año | ~3,000 GB → ~$10 |

**Regla de costos GKG:** LIKE queries en campos string largos (V2Organizations) escanean toda la columna sin importar los filtros de fecha. El costo es fijo por 8 años ~ $10-12 total como discovery único.

**Columnas clave:**
- Events: `SQLDATE` (no `Day`), `Actor1CountryCode`, `Actor2CountryCode` usan FIPS (CHN, CHL, ARG)
- GKG: `DATE` es INTEGER (20170101, no string), `V2Tone` = "Tone,Pos,Neg,Polarity,Activity,SelfRef,WordCount"

## Hallazgos documentados

Ver `docs/FINDINGS.md` para detalle completo. Resumen:
- API REST (`api.gdeltproject.org`) no accesible — usar CSV directo o BigQuery
- Chile FIPS = `CI` (no `CL`), Argentina = `AR`
- **Hallazgo nuevo:** Chile bloqueó venta de $5B en litio a empresa china (2018) — no está en los 18 del dataset original

## Próximo paso

Ejecutar `notebooks/07_gkg_context_search.py` — búsqueda GKG por contexto temático (inversión china + tono < -5). Siempre hacer dry_run primero, luego confirmar ejecución.

## Key Rules

1. Siempre hacer `dry_run=True` antes de ejecutar queries GKG (pueden costar $10+).
2. Guardar resultados en `data/samples/` inmediatamente después de cada query.
3. Documentar hallazgos en `docs/FINDINGS.md` continuamente, no al final.
4. Actualizar `CHANGELOG.md` después de cada script completado.
5. Scripts numerados secuencialmente (01_, 02_...) — no crear todos a la vez.

## Ciclo iterativo — principio fundamental

**Un script a la vez.** No se crea ni se ejecuta el siguiente hasta analizar los resultados del actual.

Cada resultado puede generar:
- **Verticales nuevas:** un hallazgo inesperado (empresa, país, patrón) que justifica una sub-query propia
- **Reasignación:** el enfoque del siguiente script cambia según lo que muestra el resultado real (ej: si el top de orgs no son chinas, ajustar el filtro; si un sector domina, profundizar ahí)

Flujo correcto por script:
1. Ejecutar
2. Analizar resultados en pantalla
3. Discutir hallazgos — ¿qué verticales emergen? ¿hay que reasignar el enfoque?
4. Solo entonces definir y crear el siguiente script
