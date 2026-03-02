# GDELT China Cancellations Pipeline

Pipeline de descubrimiento automatizado de proyectos con capital chino cancelados o interrumpidos globalmente (2015–2024), construido sobre datos GDELT y Google BigQuery.

Desarrollado como soporte empírico para la tesis de Magíster en Economía de **Ariel Villalobos** (Universidad de Chile) sobre los determinantes de cancelación de proyectos BRI/inversión china.

---

## Contexto

La tesis parte de una muestra manual de 18 casos documentados y busca expandirla mediante minería de texto a escala. El pipeline procesa ~450,000 eventos GDELT y ~200M artículos del Global Knowledge Graph para identificar señales de fricción entre China y países receptores de inversión.

**Hallazgo principal:** Las sanciones secundarias de EEUU (empresas chinas que se retiran de terceros países bajo presión estadounidense) constituyen un mecanismo de cancelación no sistematizado en la literatura BRI existente.

**Dataset final estimado:** ~60 casos validados (expansión 3× desde los 18 manuales).

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

- **801** proyectos candidatos identificados automáticamente
- **309** candidatos cross-validados (Events + GKG)
- **88%** de recall vs. señales manuales conocidas (7/8 casos recuperados)
- **~60** casos estimados en el dataset final validado
- **5** mecanismos de cancelación identificados: sanciones EEUU, oposición ambiental, rechazo político, falla de proyecto, renegociación de deuda

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
