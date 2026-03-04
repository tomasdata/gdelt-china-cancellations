# GDELT China Cancellations Pipeline

Pipeline de descubrimiento automatizado de proyectos con capital chino cancelados o interrumpidos globalmente (2015–2024), construido sobre datos GDELT y Google BigQuery.

Desarrollado como soporte empírico para la tesis de Magíster en Economía de **Ariel Villalobos** (Universidad de Chile) sobre los determinantes de cancelación de proyectos BRI/inversión china.

---

## Contexto

La tesis parte de una muestra manual de 18 casos documentados y busca expandirla mediante minería de texto a escala. El pipeline procesa ~450,000 eventos GDELT y ~200M artículos del Global Knowledge Graph para identificar señales de fricción entre China y países receptores de inversión.

**Hallazgo principal:** Las sanciones secundarias de EEUU (empresas chinas que se retiran de terceros países bajo presión estadounidense) constituyen un mecanismo de cancelación no sistematizado en la literatura BRI existente.

**Dataset final:** 12 señales de alta confianza tras auditoría de robustez (de 269 candidatas curadas, de 801 clusters iniciales). El mecanismo de sanciones secundarias EEUU domina las señales validadas.

---

## Estructura del repositorio

```
├── notebooks/          # Pipeline de scripts (ejecutar en orden)
├── data/samples/       # Datos procesados (via Git LFS)
│   ├── causal/         # Mecanismos de cancelación por año y región
│   ├── classified_conflict/  # Eventos clasificados por categoría
│   ├── classified_economic/
│   ├── clusters/       # 801 proyectos candidatos identificados
│   ├── companies/      # Ranking y perfil de riesgo de SOEs chinas
│   ├── geo/            # Eventos por región geográfica
│   ├── gkg_por_año/    # GKG Knowledge Graph 2017–2024 (parquets)
│   ├── historical/     # Eventos 2015–2016
│   ├── temporal/       # Serie temporal 2017–2024
│   └── validation/     # 309 candidatos cross-validados (recall 88%)
├── docs/               # Hallazgos técnicos y setup GCP
├── src/
└── requirements.txt
```

Cada subcarpeta de `data/samples/` contiene un archivo `ANALYSIS.md` con análisis económico detallado de los datos que contiene.

---

## Pipeline (scripts en orden)

| Script | Descripción |
|--------|-------------|
| `01_gdelt_csv_exploration.py` | Exploración inicial de CSVs públicos GDELT |
| `02_schema_con_headers.py` | Schema con columnas nombradas |
| `03_bigquery_conexion.py` | Conexión y verificación BigQuery |
| `04_discovery_cost_estimate.py` | Estimación de costos de queries |
| `05_events_china_discovery.py` | 374k eventos China+conflicto 2017–2024 |
| `06_events_refine_economic.py` | 76k eventos económicos refinados |
| `07_gkg_context_search.py` | Búsqueda GKG por contexto temático |
| `08_data_audit.py` | Deduplicación y auditoría de datos |
| `09_false_positive_filter.py` | Filtro de falsos positivos por URL keywords |
| `10_geographic_analysis.py` | Análisis geográfico por región |
| `11_temporal_evolution.py` | Evolución temporal 2017–2024 |
| `12_project_clustering.py` | Clustering → 801 proyectos candidatos |
| `13_historical_download.py` | Descarga datos históricos 2015–2016 |
| `14_company_analysis.py` | Análisis de empresas chinas (SOEs) |
| `15_causal_analysis.py` | Identificación de mecanismos de cancelación |
| `16_validation_cross.py` | Cross-validación Events × GKG |
| `17_gkg_latam_deep.py` | Análisis profundo GKG en LATAM |
| `18_final_dataset.py` | Dataset estructurado final |
| `19_deep_candidate_review.py` | Web scraping y validación de 60 candidatos |
| `20_robust_synthesis.py` | Auditoría de robustez → 12 señales alta confianza |
| `21_global_signals.py` | Señales globales BRI → 1,214 en 98 países |
| `22_consolidated_dataset.py` | Dataset consolidado manual → 52 casos base |
| `23a_gkg_global_soe.py` | GKG mining global SOE → 63,377 señales |
| `23b_gkg_theme_discovery.py` | GKG temas + nombres de proyecto + citas |
| `24_tier2_verification.py` | Verificación web 202 señales Tier 2 |
| `25_case_enrichment.py` | Enriquecimiento + taxonomía mecanismos |
| `26_regional_deep_dives.py` | Deep dives regionales sub-representadas |
| `27_final_dataset_v2.py` | Dataset final v2 → 70 casos verificados |

---

## Setup

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

Los datos ya procesados están disponibles en `data/samples/` via Git LFS — no es necesario re-ejecutar las queries de BigQuery (que tienen costo) para trabajar con los datos.

---

## Datos (Git LFS)

Los archivos de datos (~2.9 GB) se almacenan via Git LFS. Para descargarlos:

```bash
git lfs pull
```

**Nota:** El archivo consolidado `gkg_china_2017_2024.parquet` (2.3 GB) excede el límite de GitHub LFS y no está disponible en el repo. Los parquets anuales individuales en `gkg_por_año/` cubren los mismos datos.

---

## Resultados clave

### Dataset Final v2 (Scripts 01–27)
- **70 casos verificados** de disrupciones BRI en **30+ países** y **9 regiones**
- **$123,353M** en valor total afectado
- **8 macro-mecanismos** de cancelación: security (23 casos), economic (15), political (12), social (9), legal (5)
- **77% de detección** — 54/70 casos encontrados por el pipeline automatizado GDELT

### LATAM (14 casos)
- Chile SQM ($4B), Venezuela sanciones EEUU (×4), Ecuador camarón + Coca Codo, Brasil Tamoios, Argentina pork deal, Perú Chancay ($3.6B), Bolivia Uyuni ($2B), México HSR ($3.75B), Costa Rica SORESCO ($1.2B)

### Global (56 casos)
- **1,214** señales identificadas en **98 países** (Scripts 21-24)
- **GKG mining**: 626,775 artículos procesados, 63,377 señales SOE, 3,803 clusters (Scripts 23a/b)
- Casos emblemáticos: Australia cancela BRI (2021), Italia sale de BRI (2023), Pakistán CPEC+Dasu+Gwadar, Sri Lanka Hambantota+Colombo, Malaysia ECRL ($22B), Indonesia HSR ($7.3B), Tanzania Bagamoyo ($10B), Ghana loans ($19B)

---

## Cobertura temporal

- **GDELT v2:** desde 2015-02-19
- **Datos procesados:** 2015–2024 (Events) · 2017–2024 (GKG)
- **Fase 2 (futura):** 2010–2014 con GDELT v1

---

## Literatura relacionada

- Baumgartner & Zeitz (2022) — 120 casos manuales BRI 2013–2021
- Dreher et al. / AidData (2022) — *Banking on the Belt and Road*
- Gallagher & Myers (2021) — China-Latin America Finance Database
- Farrell & Newman (2019) — *Weaponized Interdependence*
