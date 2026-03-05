# Identifying BRI Project Disruptions Through GDELT Text Mining

Pipeline automatizado para descubrir y verificar proyectos con inversión china cancelados, suspendidos o interrumpidos a nivel global (2013–2024), mediante minería de texto sobre GDELT Events y Global Knowledge Graph (GKG) vía Google BigQuery.

Soporte empírico para la tesis de Magíster en Economía de **Ariel Villalobos** (Universidad de Chile) sobre los determinantes de cancelación de proyectos BRI e inversión china.

---

## Motivación

La literatura sobre la Belt and Road Initiative (BRI) documenta casos individuales de cancelación de proyectos, pero no existe un dataset sistemático. Los trabajos existentes (Baumgartner & Zeitz, 2022; AidData/Dreher et al., 2022) identifican ~120 casos manualmente. Esta tesis parte de una muestra manual de 18 casos y busca expandirla con minería de texto a escala.

**Pregunta de investigación:** ¿Qué factores determinan la cancelación de proyectos de inversión china en el marco de la BRI?

---

## Resultados principales

### Dataset

| Métrica | Valor |
|---------|-------|
| Casos verificados | **70** |
| Países | **30+** |
| Regiones | **9** |
| Valor total afectado | **US$123,353M** |
| Cobertura temporal | 2011–2024 |
| Tasa de detección del pipeline | 54/70 (77%) |

### Distribución por región

| Región | Casos | Valor (US$M) | Mecanismos principales |
|--------|-------|-------------|------------------------|
| Africa | 16 | 64,318 | economic, political |
| LATAM | 14 | 16,800 | security, economic |
| South Asia | 13 | 6,516 | security, social |
| Europe | 8 | 1,244 | security, economic |
| Middle East | 7 | — | security, political |
| Central Asia | 4 | 275 | social, security |
| SE Asia | 4 | 34,200 | political, economic |
| Oceania | 3 | — | political, security |
| Eurasia | 1 | — | — |

### Taxonomía de mecanismos de cancelación

| Mecanismo | Casos | Ejemplos |
|-----------|-------|----------|
| Security | 23 | Bans de Huawei 5G, ataques a trabajadores CPEC, sanciones secundarias EEUU |
| Economic | 15 | Debt distress (Zambia, Sri Lanka), financing failure |
| Political | 12 | Cambio de gobierno (Malasia ECRL), oposición política (Ghana) |
| Social | 9 | Protestas locales (Gwadar, Bolivia litio), oposición indígena |
| Legal | 5 | Arbitraje inversor-estado, disputas contractuales |
| Quality | 1 | Defectos de construcción (Ecuador Coca Codo) |
| Climate | 1 | Política climática (Zimbabwe Sengwa coal) |

### Hallazgo original

Las **sanciones secundarias de EEUU** constituyen un mecanismo de cancelación no sistematizado en la literatura BRI: empresas chinas se retiran de terceros países no por decisión del país receptor, sino por presión regulatoria estadounidense. Venezuela (2018–2020) es el caso paradigmático, con Unipec/CNPC, ZTE y otros actores suspendiendo operaciones para evitar sanciones.

### Casos de mayor valor

| País | Proyecto | US$M | Mecanismo | Año |
|------|----------|------|-----------|-----|
| Malasia | ECRL + Two Pipelines | 22,000 | Cambio de gobierno | 2018 |
| Ghana | China Loan Package | 19,000 | Oposición política | 2017 |
| Nigeria | Railway Financing | 14,400 | Debt concerns | 2021 |
| Tanzania | Bagamoyo Mega-Port | 10,000 | Términos predatorios | 2019 |
| Indonesia | Jakarta-Bandung HSR | 7,300 | Debt distress | 2020 |
| Zambia | Chinese Loans Default | 6,000 | Debt distress | 2020 |
| Philippines | Three Railway Projects | 4,900 | Tensión geopolítica | 2023 |
| Chile | SQM Lithium Acquisition | 4,000 | Rechazo político | 2018 |

---

## Metodología

El pipeline procesa datos GDELT en 4 etapas y 27 scripts:

```
663,825 eventos GDELT  →  52,439 BRI-related  →  801 candidatos  →  70 casos verificados
626,775 artículos GKG  →  63,377 señales SOE  →  3,803 clusters
```

### Etapa 1 — Extracción y filtrado (Scripts 01–12)

Descarga de eventos GDELT v2 (2015–2024) vía BigQuery, deduplicación (~35% duplicados eliminados), clasificación por contexto (BRI vs. trade war vs. military), filtrado geográfico (exclusión de China/EEUU/HK como ActionGeo), clustering temporal-geográfico.

### Etapa 2 — Minería de texto GKG (Scripts 07, 17, 23a/b)

Procesamiento de 4.7 GB de artículos del Knowledge Graph: extracción de menciones de SOEs chinas, señales de deuda, oposición ambiental, nombres de proyecto, citas directas de cancelación. Filtro de Huawei (83% de menciones de SOEs) preservando solo artículos con temas de cancelación/ban.

### Etapa 3 — Verificación web (Scripts 19–20, 24, 26)

Web scraping de ~400 URLs para verificar contenido real. Clasificación en CONFIRMED / LIKELY / WEAK / NOISE / DEAD. Auditoría de robustez: 269 señales iniciales → 12 de alta confianza solo en LATAM (96% era ruido). Verificación global de 202 señales Tier 2 (54% signal rate).

### Etapa 4 — Consolidación (Scripts 22, 25, 27)

Curación manual desde la literatura, enriquecimiento con taxonomía de mecanismos (8 macro-categorías) y sectores (12 tipos), cross-referencia con GKG para profundidad de evidencia, deduplicación final, generación de tablas para tesis.

### Limitaciones

- **Sesgo idiomático:** GDELT/GKG en inglés — África francófona, Asia Central (ruso), Islas del Pacífico sub-representadas
- **Cobertura temporal:** GDELT v2 desde 2015-02-19; casos pre-2015 provienen solo de la literatura
- **URL rot:** 32% de URLs muertas al momento de verificación
- **Huawei/5G:** Domina sector telecom; puede inflar conteo de mecanismo "security"
- **Recall:** 77% de detección implica que ~23% de los casos provienen exclusivamente de la literatura

---

## Estructura del repositorio

```
├── notebooks/              # 29 scripts Python (ejecutar en orden)
│   ├── 01–06              # Exploración, schema, BigQuery, extracción
│   ├── 07–12              # GKG context, auditoría, filtros, clustering
│   ├── 13–16              # Histórico, SOEs, causal, cross-validation
│   ├── 17–20              # GKG LATAM, curación, web scraping, robustez
│   ├── 21–22              # Señales globales, consolidación manual
│   └── 23a–27             # GKG global mining, verificación, dataset final
│
├── data/samples/           # Datos procesados (Git LFS, ~2.9 GB)
│   ├── final/             # Dataset final + thesis tables
│   │   ├── bri_cancellations_FINAL_v2.csv    # ← DATASET PRINCIPAL (70 casos)
│   │   ├── bri_cancellations_FINAL_v2.md     # Reporte narrativo
│   │   ├── thesis_tables/                     # 6 tablas para la tesis
│   │   ├── bri_cases_enriched.csv            # 68 casos con metadata extendida
│   │   ├── tier2_verified.csv                # 202 señales Tier 2 verificadas
│   │   └── mechanism_taxonomy.csv            # Taxonomía de mecanismos
│   ├── clusters/          # 801 proyectos candidatos
│   ├── gkg_global/        # GKG mining global (SOE, deuda, ambiental)
│   ├── gkg_latam/         # GKG mining LATAM
│   ├── gkg_por_año/       # GKG Knowledge Graph 2017–2024 (parquets)
│   ├── validation/        # Cross-validación Events × GKG
│   ├── geo/               # Análisis geográfico
│   ├── temporal/          # Serie temporal 2017–2024
│   ├── companies/         # Ranking de SOEs chinas
│   ├── causal/            # Mecanismos de cancelación
│   └── historical/        # Eventos 2015–2016
│
├── docs/                  # Documentación técnica
│   ├── ANALYSIS_FINDINGS.md
│   └── SETUP_NUEVA_CUENTA_GCP.md
│
├── CHANGELOG.md           # Log detallado de cada script
└── requirements.txt
```

Cada subcarpeta de `data/samples/` contiene un archivo `ANALYSIS.md` con análisis de los datos.

---

## Pipeline completo

| # | Script | Input | Output |
|---|--------|-------|--------|
| 01 | `01_gdelt_csv_exploration.py` | CSVs públicos GDELT | Exploración inicial |
| 02 | `02_schema_con_headers.py` | — | Schema con headers nombrados |
| 03 | `03_bigquery_conexion.py` | — | Verificación conexión BigQuery |
| 04 | `04_discovery_cost_estimate.py` | — | Estimación costos queries |
| 05 | `05_events_china_discovery.py` | BigQuery Events | 374k eventos China+conflicto |
| 06 | `06_events_refine_economic.py` | BigQuery Events | 76k eventos económicos |
| 07 | `07_gkg_context_search.py` | BigQuery GKG | Búsqueda por contexto temático |
| 08 | `08_data_audit.py` | Events CSVs | Deduplicación (374k→248k) |
| 09 | `09_false_positive_filter.py` | Events dedup | Taxonomía BRI vs. trade war |
| 10 | `10_geographic_analysis.py` | Events BRI | Análisis por región y país |
| 11 | `11_temporal_evolution.py` | Events BRI | Evolución 2017–2024 |
| 12 | `12_project_clustering.py` | Events filtrados | 801 proyectos candidatos |
| 13 | `13_historical_download.py` | BigQuery Events | 289k eventos 2015–2016 |
| 14 | `14_company_analysis.py` | Events + GKG | Ranking SOEs chinas |
| 15 | `15_causal_analysis.py` | Candidatos | Mecanismos de cancelación |
| 16 | `16_validation_cross.py` | Events × GKG | Cross-validación (88% recall) |
| 17 | `17_gkg_latam_deep.py` | GKG parquets | Mining GKG LATAM |
| 18 | `18_final_dataset.py` | Todas las fuentes | 269 señales curadas |
| 19 | `19_deep_candidate_review.py` | 269 señales | Web scraping 60 candidatos |
| 20 | `20_robust_synthesis.py` | 269 señales | Auditoría robustez → 12 alta confianza |
| 21 | `21_global_signals.py` | Events globales | 1,214 señales en 98 países |
| 22 | `22_consolidated_dataset.py` | Literatura + pipeline | 52 casos consolidados |
| 23a | `23a_gkg_global_soe.py` | GKG parquets (4.7 GB) | 63,377 señales SOE globales |
| 23b | `23b_gkg_theme_discovery.py` | GKG parquets | Nombres de proyecto + citas |
| 24 | `24_tier2_verification.py` | 202 señales Tier 2 | 16 CONFIRMED + 93 LIKELY |
| 25 | `25_case_enrichment.py` | 68 casos | Taxonomía mecanismos + sectores |
| 26 | `26_regional_deep_dives.py` | GKG URLs | 27 señales regiones sub-representadas |
| 27 | `27_final_dataset_v2.py` | Todo lo anterior | **70 casos verificados** |

---

## Reproducibilidad

### Setup

```bash
python3 -m venv gdelt_env
source gdelt_env/bin/activate
pip install -r requirements.txt
```

### BigQuery (requerido para scripts 03+)

```bash
gcloud auth application-default login
gcloud auth application-default set-quota-project <tu-proyecto-gcp>
python notebooks/03_bigquery_conexion.py  # verificar conexión
```

### Datos pre-procesados (Git LFS)

Los datos procesados (~2.9 GB) están disponibles vía Git LFS — no es necesario re-ejecutar las queries de BigQuery para trabajar con el dataset final.

```bash
git lfs pull
```

**Nota:** `gkg_china_2017_2024.parquet` (2.3 GB) excede el límite de GitHub LFS. Los parquets anuales individuales en `gkg_por_año/` cubren los mismos datos.

---

## Referencias

- Baumgartner & Zeitz (2022) — 120 casos manuales BRI 2013–2021
- Dreher et al. / AidData (2022) — *Banking on the Belt and Road*
- Gallagher & Myers (2021) — China-Latin America Finance Database
- Farrell & Newman (2019) — *Weaponized Interdependence*
- GDELT Project — https://www.gdeltproject.org/
