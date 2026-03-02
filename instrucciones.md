
# GDELT Project — Exploración y Extracción desde Python

> **Objetivo:** Conectarse a GDELT (Global Database of Events, Language and Tone) desde Python, explorar sus capacidades, documentar hallazgos, y construir pipelines de extracción útiles para análisis de noticias, actores económicos y sentimiento.

---

## Contexto Técnico

GDELT monitorea medios de comunicación del mundo entero (prensa, TV, web) en más de 100 idiomas, actualizándose cada 15 minutos. Existen tres formas principales de acceso desde Python:

| Método | Librería | Ventajas | Limitaciones |
|--------|----------|----------|--------------|
| **gdeltPyR** | `pip install gdeltPyR` | Rápido para explorar, API simple | Solo GDELT 2.0, algunos endpoints inestables |
| **BigQuery** | `google-cloud-bigquery` | Dataset completo, SQL nativo, escala masiva | Costo por query (pero tier gratuito generoso) |
| **API REST directa** | `requests` | Sin dependencias, acceso a DOC/GEO/TV APIs | Parsing manual, rate limits |

### Datasets principales en GDELT

1. **Events (GKG Events):** Quién hizo qué a quién, dónde, cuándo. Codificado en CAMEO.
2. **Global Knowledge Graph (GKG):** Entidades, temas, tonos, fuentes extraídas de cada artículo.
3. **Mentions:** Cada mención individual de un evento en un artículo.
4. **DOC API:** Búsqueda full-text en artículos recientes.
5. **GEO API:** Geolocalización de noticias.
6. **TV API:** Monitoreo de televisión (solo US, transcripciones closed-caption).

---

## FASE 0 — Setup del Entorno

### Instrucciones

```bash
# Crear entorno virtual
python -m venv gdelt_env
source gdelt_env/bin/activate

# Instalar dependencias
pip install gdeltPyR google-cloud-bigquery pandas requests pyarrow db-dtypes

# Verificar autenticación GCP (si se usará BigQuery)
gcloud auth application-default login
```

### Estructura del proyecto

```
gdelt-exploration/
├── README.md
├── CHANGELOG.md
├── requirements.txt
├── notebooks/
│   ├── 01_gdeltpyr_exploration.py
│   ├── 02_bigquery_exploration.py
│   ├── 03_rest_api_exploration.py
│   └── 04_extraction_pipeline.py
├── src/
│   ├── __init__.py
│   ├── gdelt_bq.py          # Funciones BigQuery
│   ├── gdelt_api.py          # Funciones API REST
│   └── gdelt_pyr.py          # Wrapper gdeltPyR
├── docs/
│   ├── FINDINGS.md            # Documentación de hallazgos
│   ├── SCHEMA_REFERENCE.md    # Esquemas documentados
│   └── QUERY_CATALOG.md       # Queries útiles probadas
├── data/
│   └── samples/               # Datos de muestra descargados
└── tests/
    └── test_connections.py
```

Crear esta estructura completa antes de comenzar.

---

## FASE 1 — Pruebas de Conexión y Documentación (OBLIGATORIA)

> ⚠️ **No avanzar a Fase 2 sin completar toda la Fase 1.** Cada paso debe documentarse en `docs/FINDINGS.md`.

### 1.1 — Probar gdeltPyR

**Archivo:** `notebooks/01_gdeltpyr_exploration.py`

Tareas:

- Importar `gdelt` y crear instancia: `gd = gdelt.gdelt(version=2)`
- Hacer una búsqueda simple de events para una fecha reciente (últimas 48h)
- Hacer una búsqueda de GKG para la misma fecha
- Documentar en FINDINGS.md:
  - Columnas retornadas (nombre, tipo, descripción inferida)
  - Tiempo de respuesta
  - Volumen de datos retornado
  - Errores encontrados (gdeltPyR tiene bugs conocidos, documentarlos)
  - Formatos de fecha aceptados

### 1.2 — Probar BigQuery

**Archivo:** `notebooks/02_bigquery_exploration.py`

Tablas públicas a explorar (proyecto `gdelt-bq`):

```
gdelt-bq.gdeltv2.events          -- Eventos
gdelt-bq.gdeltv2.eventmentions   -- Menciones
gdelt-bq.gdeltv2.gkg             -- Global Knowledge Graph
gdelt-bq.gdeltv2.gkg_partitioned -- GKG particionado (más eficiente)
gdelt-bq.full.events             -- Eventos históricos completos
```

Tareas:

- Conectar con `google.cloud.bigquery.Client()`
- Ejecutar `SELECT * FROM gdelt-bq.gdeltv2.events LIMIT 10` y documentar schema completo
- Ejecutar `SELECT * FROM gdelt-bq.gdeltv2.gkg_partitioned LIMIT 10` y documentar schema
- Probar una query con filtro de fecha y de país (Chile = `CI` en FIPS, `CL` en ISO)
- Estimar costos: ejecutar con `QueryJobConfig(dry_run=True)`
- Documentar en FINDINGS.md:
  - Schema completo de cada tabla con tipos
  - Campos más útiles identificados
  - Costos estimados por query tipo
  - Diferencias entre tablas particionadas y no particionadas

### 1.3 — Probar API REST

**Archivo:** `notebooks/03_rest_api_exploration.py`

Endpoints a probar:

```
# DOC API (búsqueda de artículos)
https://api.gdeltproject.org/api/v2/doc/doc?query=KEYWORD&mode=artlist&format=json

# GEO API (noticias geolocalizadas)
https://api.gdeltproject.org/api/v2/geo/geo?query=KEYWORD&format=geojson

# TV API (transcripciones TV)
https://api.gdeltproject.org/api/v2/tv/tv?query=KEYWORD&mode=artlist
```

Tareas:

- Probar DOC API con un keyword simple (ej: "Chile economía")
- Probar distintos `mode`: `artlist`, `timelinevol`, `timelinetone`, `wordcloud`
- Probar GEO API y verificar formato GeoJSON
- Documentar en FINDINGS.md:
  - Parámetros aceptados por cada endpoint
  - Formatos de respuesta
  - Rate limits observados
  - Campos retornados y su utilidad

### 1.4 — Documentar Schemas

**Archivo:** `docs/SCHEMA_REFERENCE.md`

Con los hallazgos de 1.1–1.3, crear un documento de referencia que incluya:

- Schema de `events` con descripción de cada campo
- Schema de `gkg` con descripción de cada campo
- Códigos CAMEO más relevantes (categorías de eventos)
- Códigos de país FIPS vs ISO
- Campos de tono/sentimiento y cómo interpretarlos

---

## FASE 2 — Queries Útiles y Catálogo

### 2.1 — Desarrollar y probar estas queries

Cada query debe probarse, validarse, y guardarse en `docs/QUERY_CATALOG.md` con:

- Descripción de qué busca
- Query SQL (BigQuery) o llamada Python
- Resultado de ejemplo (primeras 5 filas)
- Costo estimado (BigQuery)
- Tiempo de ejecución

#### Queries a desarrollar:

**A) Monitoreo de noticias por país y tema:**
- Todas las noticias sobre Chile en las últimas 24h
- Filtrar por tono positivo/negativo
- Top fuentes que cubren Chile

**B) Análisis de actores:**
- Eventos donde un actor específico (empresa, persona, institución) aparece
- Red de actores: quién interactúa con quién
- Evolución temporal de menciones de un actor

**C) Sentimiento y tono:**
- Tono promedio de noticias sobre un tema por día (timeline)
- Artículos con tono extremo (muy positivo o muy negativo)
- Comparación de tono entre fuentes para el mismo evento

**D) Geolocalización:**
- Mapa de eventos en una región específica
- Concentración de noticias negativas por zona geográfica
- Eventos en Chile por región

**E) Temas y entidades:**
- Extracción de organizaciones mencionadas (campo GKG `V2Organizations`)
- Temas más frecuentes (`V2Themes`)
- Personas mencionadas (`V2Persons`)

**F) Alertas y monitoreo:**
- Query para detectar picos de cobertura sobre un tema
- Detección de cambios bruscos de tono
- Monitoreo de keywords específicos en tiempo casi-real

### 2.2 — Encapsular en funciones reutilizables

**Archivos:** `src/gdelt_bq.py`, `src/gdelt_api.py`

Crear funciones limpias para cada tipo de query:

```python
# Ejemplo de interfaz esperada (no copiar literal, diseñar la mejor)
def get_events_by_country(country_code: str, days_back: int = 7) -> pd.DataFrame: ...
def get_tone_timeline(query: str, days_back: int = 30) -> pd.DataFrame: ...
def get_top_actors(country_code: str, days_back: int = 7) -> pd.DataFrame: ...
def search_articles(query: str, max_results: int = 50) -> list[dict]: ...
def get_geo_events(query: str) -> dict:  # GeoJSON ...
```

---

## FASE 3 — Pipeline de Extracción

### 3.1 — Diseñar pipeline configurable

Crear un pipeline que permita:

- Definir queries de monitoreo en un archivo de configuración (YAML o JSON)
- Ejecutar extracciones programadas
- Guardar resultados en formato Parquet (eficiente para análisis posterior)
- Deduplicar registros entre ejecuciones
- Logging de cada ejecución

### 3.2 — Implementar en `src/`

El pipeline debe:

- Leer configuración
- Ejecutar queries contra BigQuery y/o API REST
- Transformar y limpiar datos
- Guardar en `data/` con particionamiento por fecha
- Generar un reporte resumido de cada ejecución

---

## FASE 4 — Tests

**Archivo:** `tests/test_connections.py`

Tests mínimos requeridos:

- Test de conexión a BigQuery (query trivial)
- Test de conexión a API REST (health check)
- Test de gdeltPyR (si se incluye)
- Test de cada función en `src/` con datos de muestra
- Test de pipeline con configuración mínima

Usar `pytest`. Incluir fixtures para datos de muestra.

---

## CHANGELOG

> Mantener actualizado con cada cambio significativo. Formato: [Keep a Changelog](https://keepachangelog.com/).

```markdown
# Changelog

Todos los cambios notables del proyecto se documentan aquí.

## [Unreleased]

### Added
- Estructura inicial del proyecto
- (ir completando a medida que se avanza)

### Changed

### Fixed

### Documented
```

### Reglas del Changelog

1. **Actualizar el CHANGELOG.md después de cada tarea completada**, no al final
2. Cada entrada debe ser clara y concisa
3. Usar las categorías: `Added`, `Changed`, `Fixed`, `Documented`, `Removed`
4. Incluir fecha cuando se cierre una versión
5. La sección `[Unreleased]` siempre está arriba

---

## Reglas Generales para Claude Code

1. **Fase 1 es obligatoria y secuencial.** No escribir código de extracción sin haber probado y documentado cada método de acceso.
2. **Documentar mientras se avanza.** No dejar la documentación para el final. Cada hallazgo va a `docs/FINDINGS.md` inmediatamente.
3. **Actualizar CHANGELOG.md después de cada tarea.**
4. **Preferir BigQuery** para queries analíticas pesadas. Usar API REST para búsquedas puntuales y tiempo real.
5. **Estimar costos antes de ejecutar queries grandes** en BigQuery. Usar `dry_run=True`.
6. **Guardar samples de datos** en `data/samples/` para desarrollo sin consultar APIs repetidamente.
7. **Código limpio:** Type hints, docstrings, manejo de errores. Sin código hardcodeado.
8. **Si algo falla, documentar el fallo** antes de buscar alternativa. Los errores son hallazgos valiosos.
9. **Commits semánticos** si se usa git: `feat:`, `fix:`, `docs:`, `test:`.
10. **No instalar dependencias innecesarias.** Justificar cada `pip install` adicional.

---

## Referencias

- GDELT Project: https://www.gdeltproject.org/
- GDELT 2.0 DOC API: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
- GDELT GEO API: https://blog.gdeltproject.org/gdelt-geo-2-0-api-debuts/
- GDELT BigQuery: https://www.gdeltproject.org/data.html#googlebigquery
- gdeltPyR docs: https://github.com/linwoodc3/gdeltPyR
- Códigos CAMEO: https://www.gdeltproject.org/data