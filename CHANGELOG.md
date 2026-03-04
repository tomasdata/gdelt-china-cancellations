# Changelog

## [Unreleased]

### Added
- Estructura completa del proyecto (directorios, requirements.txt, venv con Python 3.14)
- CLAUDE.md con orientación completa para Claude Code
- Script 01: exploración CSV públicos GDELT v2 (events 61 cols + GKG 27 cols)
- Script 02: schema completo con headers nombrados y ejemplos reales de datos
- Script 03: conexión BigQuery verificada, schema de tablas gdelt-bq
- Script 04: estimación de costos de queries via dry_run
- Script 05: 374,108 eventos China+conflicto 2017-2024 descargados (144 GB, gratis)
- Script 06: 76,771 eventos económicos refinados (EventCode 163/164/165), LATAM 665 eventos
- Script 07: discovery GKG preparado y listo para ejecutar (~$10-12, cubierto por créditos)

### Documented
- docs/FINDINGS.md: schemas Events y GKG, costos reales BigQuery, hallazgos LATAM
- docs/SETUP_NUEVA_CUENTA_GCP.md: instrucciones para cuenta GCP personal
- Hallazgo nuevo: Chile bloqueó venta $5B litio a empresa china (2018) — no está en dataset tesis

### Infrastructure
- Proyecto GCP: `tomasdata-gdelt-research` (cuenta salareuniones113@gmail.com)
- Créditos $300 disponibles — cubre todos los costos del proyecto
- Separado completamente de Orsan
- Todos los scripts apuntan a `tomasdata-gdelt-research`

### Fixed
- FIPS codes LATAM: Chile = CI (no CL)
- BigQuery column: SQLDATE (no Day), DATE es INTEGER
- REST API (api.gdeltproject.org) no accesible — se usa BigQuery como método principal

### Redesign — Pipeline: Contexto → Empresas → Casos
- **Cambio de enfoque aprobado:** el pipeline ya NO parte de una lista pre-definida de 25 empresas chinas. En cambio:
  1. Script 07 busca por **contexto temático** (inversión + infraestructura + China + tono < -5) sin filtrar por empresa
  2. Script 08 extrae el universo de empresas chinas desde los resultados → ranking real
  3. Script 09 hace búsqueda profunda por empresa (caso a caso)
  4. Script 10 estructura el dataset final para la tesis
- Script 07 original (empresa-primero) archivado como referencia
- Nuevo script: `07_gkg_context_search.py`

### Alcance temporal documentado
- **Fase 1 (actual):** 2017–2024
- **Fase 2 (futura):** Extender a 2010–2016 usando GDELT v1 (schema diferente, pre-2015)

### Metodología: ciclo iterativo
- **Premisa fundamental:** un script a la vez. No se planifica el siguiente hasta ver y analizar los resultados del actual.
- Los resultados pueden generar **verticales nuevas** (hallazgos que merecen su propio script de profundización) o **reasignación** (cambiar el enfoque del próximo script según lo que emerge).
- El pipeline 07→08→09→10 es una guía, no un roadmap fijo. Cada resultado manda.

### Pipeline Analysis — Scripts 08-12 (ejecutados sobre Events datasets)

#### Script 08 — Auditoría y deduplicación
- Conflicto 374k → **248,745 URLs únicas** (33% duplicados eliminados)
- Económico 76k → **45,531 URLs únicas** (40% duplicados eliminados)
- Descubrimiento crítico: `CH`=China en FIPS (no Chile). Chile=`CI`. Bug confirmado en scripts previos.
- Overlap entre datasets: 9,218 URLs aparecen en ambos (20% del económico)
- Output: `*_dedup.csv`

#### Script 09 — Taxonomía de contextos (falsos positivos)
- Conflicto: 18.6% BRI/investment (46,155), 67.3% other, 7.7% trade_war, 6.0% military
- Económico: 16.9% BRI/investment (7,677), 55.3% other, 16.0% trade_war, 10.2% military
- **BRI combinado: 52,439 eventos únicos** → `bri_investment_events_all.csv`
- Output: `events_*_classified.csv`, subcarpetas por categoría

#### Script 10 — Análisis geográfico
- Regiones: Asia SE (5,792) > Medio Oriente (4,668) > Asia Central (4,199) > Europa E (3,634) > África (3,116) > LATAM (2,679)
- Top países BRI: Pakistán (2,767), Irán (2,469), Ucrania (2,332), Filipinas (2,028), Israel (1,152)
- LATAM: México (502) > Brasil (429) > Venezuela (360) > Colombia (261) > Ecuador (248) > Chile (112)
- Output: `data/samples/geo/` con subcarpetas por región

#### Script 11 — Evolución temporal
- Pico global: 2020 (9,904 eventos BRI) — impacto COVID en proyectos
- Crecimiento sostenido: Filipinas (+396), Israel (+232), Ucrania (+125), Pakistán (+69)
- Caída: Venezuela (-50%), Camboya (-40%), India (-113), Indonesia (-101)
- **Alerta falso positivo**: Filipinas 2024 (579 eventos) = disputas Mar Sur China, NO proyectos BRI
- **Alerta falso positivo**: Bosnia = conflictos internos (no plantas carbón chinas)
- Output: `data/samples/temporal/`

#### Script 12 — Clustering de proyectos candidatos
- Filtro URL estricto: 52,439 → **8,912 eventos con keywords de inversión/proyecto**
- Clustering (país + 90 días): **801 proyectos candidatos** con ≥3 eventos
- Por región: Other (364) > Asia SE (117) > Medio Oriente (86) > África (82) > Asia C (56) > LATAM (53) > Europa E (42)
- **LATAM: 53 proyectos candidatos** — mezcla de ruido + señal real
- Señal real LATAM identificada: Chile SQM/litio, Ecuador Yasuni oil, Venezuela petrochina
- Output: `data/samples/clusters/project_candidates_events.csv` (801 proyectos)
         `data/samples/clusters/project_candidates_latam.csv` (53 LATAM)

### GKG Pipeline — Script 07 (en ejecución BigQuery)
- `07_gkg_context_search.py` corriendo — búsqueda por contexto temático ~$6.90
- DATE en GKG = YYYYMMDDHHMMSS (14 dígitos), usar `_PARTITIONTIME` para filtro temporal
- Billing habilitado en cuenta salareuniones113@gmail.com (Cobranzas Orsan SPA, RUN 995417405)

### Findings críticos documentados
- `docs/ANALYSIS_FINDINGS.md` — auditoría + taxonomía + geo + temporal + clustering
- Falso positivo sistemático: ActionGeo en países BRI ≠ evento sobre inversión china
- Solución aplicada: filtro URL keywords + exclusión China/EEUU/HK de ActionGeo

### Análisis profundo LATAM — 53 candidatos revisados manualmente

#### Señales reales identificadas (8/53 = 15% signal rate)
- **Chile CI_003** (2018): Bloqueo compra acciones SQM por Tianqi Lithium — gobierno bloquea adquisición china
- **Ecuador EC_005** (2019): China suspende aprobación exportación camarón Santa Priscila/Omarsa — presión política via acceso mercado
- **Ecuador EC_011** (2024): Contexto Yasuni oil — moratoria ambiental bloquea explotación
- **Venezuela**: 4 señales relacionadas con sanciones EEUU:
  - Oct 2018: Unipec (CNPC) prohíbe tanqueros vinculados a Venezuela (Reuters) — auto-retiro por sanciones secundarias
  - Dic 2018: ZTE sancionada por EEUU por vigilancia Venezuela (telecomstechnews.com)
  - Sep 2019: CNPC suspende operaciones Venezuela para evitar sanciones (panampost.com)
  - Nov 2020: EEUU sanciona empresa china por censura internet Venezuela (Reuters)
- **Brasil** (2017): Inversores chinos no persiguen concesión autopista Tamoios São Paulo (bnamericas.com)

#### Nuevo mecanismo documentado
**"Sanciones secundarias EEUU como mecanismo de expulsión de inversión china"** — Venezuela muestra que proyectos BRI pueden cancelarse NO por decisión del host country sino por sanciones externas (EEUU) que hacen inviable la operación china. Potencial contribución original a la tesis.

#### Ruido dominante (45/53 = 85% noise)
- Brasil: bans de carne por escándalos sanitarios (food safety, no BRI)
- México: fentanilo y política de drogas (no proyectos BRI)
- Argentina: G20 diplomacia genérica
- Cuba/Colombia/Perú/Bolivia/Panamá: crimen local, política EEUU

### Script 13 — Descarga histórica 2015-2016

#### Descarga completada (gratis — dentro del 1TB gratuito mensual)
- Conflicto 2015-2016: **289,717 eventos** (2015: 124,516 + 2016: 165,201)
- Económico 2015-2016: **15,231 eventos** (2015: 5,105 + 2016: 10,126)
- Escaneo total: 208.8 GB x 2 = 417.6 GB — **$0 costo** (dentro de cuota gratuita)
- Guardado: `data/samples/historical/events_china_conflict_2015_2016.csv`
- Guardado: `data/samples/historical/events_china_economic_2015_2016.csv`

#### Comparativa temporal completa (GDELT v2 2015-2024)
| Período | Conflicto | Económico |
|---------|-----------|-----------|
| 2015-2016 | 289,717 | 15,231 |
| 2017-2024 | 374,108 | 76,771 |
| **Total v2** | **663,825** | **92,002** |

#### Nota: GDELT v2 comienza el 2015-02-19
- Para datos pre-2015 se necesita GDELT v1 (schema diferente, Fase 2 futura)
- El crecimiento de 289k (2 años) → 374k (8 años) sugiere menor volumen por año en 2015-2016 — normal, los eventos BRI aumentaron con el tiempo

### Script 19 — Deep Candidate Review (web scraping + validación manual)
- Input: 269 señales del Script 18
- Web scraping de URLs para verificar contenido real de cada artículo
- **60 candidatos revisados** con clasificación: CONFIRMED / LIKELY / NOISE
- Hallazgo: artículo qz.com sobre asesinato de Villavicencio (Ecuador) clasificado como CONFIRMED en 5 países distintos — falso positivo sistemático
- Output: `data/samples/final/candidates_deep_review.csv` (60 candidatos)
- Output: `data/samples/final/candidates_deep_review.md` (narrativa)

### Script 20 — Auditoría de robustez y síntesis final
- Re-scoring completo de 269 señales con criterios estrictos:
  - `domain_score`: penaliza fuentes chinas inaccesibles (79 señales eliminadas)
  - `url_contaminated`: detecta URLs compartidas por ≥3 países (52 señales eliminadas)
  - `robust_score_final` (escala 0-10): combina mecanismo + dominio + volumen + tono + corroboración
- **269 → 12 señales de alta confianza** (threshold ≥ 6.0) — reducción de 96% del ruido
- Mecanismos alta confianza: 11 us_sanctions + 1 confirmed_presence
- Recall vs. 10 casos manuales conocidos: **4/10 (40%)**
- Señales genuinas confirmadas: Venezuela (ZTE, CNPC, Unipec, censura internet), Cuba, Chile COVID
- Output: `data/samples/final/robust_synthesis.csv` (dataset auditado completo)
- Output: `data/samples/final/robust_synthesis.md` (reporte narrativo para tesis)

### Resultados finales del pipeline completo
- **Pipeline automatizado**: 20 scripts, ~450k eventos procesados, ~93k artículos GKG
- **Señales alta confianza LATAM**: 12 (de 269 curadas, de 801 candidatos, de 52k eventos BRI)
- **Mecanismo original**: Sanciones secundarias EEUU como driver de cancelación BRI (Venezuela 2018-2020)
- **Limitación principal**: Recall 40% — el pipeline captura bien sanciones EEUU pero pierde casos de rechazo político directo (Chile SQM score=4.0, Brasil Tamoios score=3.5)

### Script 21 — Análisis global de señales BRI
- Expande el análisis más allá de LATAM a los 8,492 eventos globales URL-filtered
- Clasificación por: nombre de proyecto conocido, términos BRI explícitos, indicadores de fricción
- **1,214 señales globales** con score ≥ 2 en **98 países** y **12 regiones**
- **51 señales Tier 1** (score ≥ 5), **202 Tier 2** (3-4.9), **961 Tier 3** (2-2.9)
- **10 proyectos BRI nombrados** detectados: CPEC (50), Gwadar (19), Hambantota (3), Tuzla (3), Port Qasim (3), Colombo Port City (2), Pokhara (1), Diamer-Bhasha (1), Mombasa SGR (1), ECRL (1)
- Verificación de 23 URLs Tier 1: **18 señales verdaderas (78%)**, 4 falsos positivos, 1 no verificable

### Señales globales verificadas (web scraping)
- **Pakistán CPEC**: Ataques a trabajadores chinos → pausas en construcción (Dasu Dam, Gwadar). Protestas locales anti-CPEC en Gwadar (2021). Aeropuerto Gwadar demorado 3 veces.
- **Australia**: Cancelación del acuerdo BRI de Victoria (2021) + China retalia suspendiendo diálogo económico. Ban de Huawei/ZTE de 5G (2018).
- **Sri Lanka**: Hambantota — stalled talks (2017), caso canónico de debt-trap.
- **Nepal**: Protestas contra aeropuerto Pokhara (financiado con préstamo chino, elefante blanco).
- **Zambia**: Llamados a renegociar préstamos chinos (2018). Default soberano 2020.
- **Italia**: Salida formal de BRI (2023) — primer país G7 en retirarse.
- **Bangladesh**: Protesta letal contra planta de carbón china en Banshkhali (2017).
- **Bielorrusia**: Protestas 2020 crean incertidumbre para BRI (Great Stone Industrial Park).
- **Alemania/Japón**: Bans de Huawei/ZTE de redes 5G (Digital Silk Road).
- **Nigeria**: Críticas domésticas a préstamos chinos de Buhari.
- **Rusia**: Invasión de Ucrania (2022) disrumpe corredor norte del BRI.

### Falsos positivos globales identificados
- Malasia ECRL: artículo sobre *revival* del proyecto (no cancelación)
- Kenia Mombasa: narrativa desmentida de "seizure" del puerto (forum post)
- Indonesia: artículo pro-BRI ("not a debt trap")
- Pakistán Gwadar/SSBN: disputa militar, no infraestructura BRI

### Script 23a — GKG Global SOE Mining
- Input: 626,775 artículos GKG (2017-2024), procesados año por año
- **63,377 señales globales** (SOE + país receptor) en 3,803 clusters (país×SOE×año)
- **1,279 clusters con ≥5 artículos** — señales fuertes
- **Filtro Huawei**: 15,946 artículos Huawei-only filtrados, 9,154 rescatados por tema cancel/ban
- **6,910 señales de deuda** (top: Sri Lanka, Zambia, Kenya, Pakistan)
- **9,103 señales ambientales** (top: Russia, UK, Australia, Poland)
- **10,513 URLs** de regiones sub-representadas para exploración
- **29/52 casos conocidos corroborados** en GKG (top: Australia BRI 1,575 artículos)
- Output: `data/samples/gkg_global/` (6 archivos CSV + reporte MD)

### Script 23b — GKG Theme-Based Case Discovery
- **132,925 artículos** con nombres de proyecto BRI (CPEC: 10,396 menciones, Gwadar: 2,360, Hambantota: 1,477)
- **1,185 citas** con evidencia de cancelación + China
- Gap analysis: 9/16 casos no-detectados encontrados en GKG (Ecuador Coca Codo, Philippines, Kazakhstan, etc.)
- Output: `data/samples/gkg_global/` (3 archivos CSV + reporte MD)

### Script 24 — Tier 2 Global Signal Verification
- Verificación web de 202 señales Tier 2 (score 3.0-4.9)
- **16 CONFIRMED + 93 LIKELY** (54% signal rate, mejor que LATAM)
- **64 URLs muertas** (32% URL rot)
- Nuevas señales por región: South Asia (31), SE Asia (18), Africa (11), Oceania (11), Middle East (10)
- Hallazgos notables: Italia BRI exit (VOA), Pakistan Dasu dam + Neelum-Jhelum (Gezhouba abandona), Sri Lanka sanciones EEUU a CCCC
- Output: `data/samples/final/tier2_verified.csv` (202 rows) + `tier2_new_cases.csv`

### Script 25 — Case Enrichment + Mechanism Classification
- **68 casos** con metadata enriquecida (52 existentes + 16 nuevos CONFIRMED)
- Taxonomía de 8 macro-mecanismos: security (24), economic (15), political (12), social (9), legal (5)
- 12 sectores clasificados: Transport_Port (17), Transport_Rail (11), Telecom (7), Energy (13)
- 31/68 casos con valor conocido, total $170,553M
- 29/68 con corroboración GKG (media 214 artículos)
- Output: `data/samples/final/bri_cases_enriched.csv` + case studies top 20

### Script 26 — Regional Deep Dives
- 130 URLs GKG verificadas en regiones sub-representadas
- **27 nuevas señales**: Oceania (11), Africa (10), Middle East (4), Central Asia (2)
- Hallazgos genuinos: Djibouti (China Merchants port dispute), Turkmenistan (CNPC gas contamination), Fiji (China Railway court fine), Mozambique (CNPC political unrest)
- GKG detection rate: LATAM 86%, SE Asia 75%, Oceania 67%, Africa 60%, South Asia 45%
- Limitación confirmada: Central Asia (ruso) y Pacific Islands (cobertura mínima)

### Script 27 — Final Consolidated Dataset v2
- **70 casos verificados** en **9 regiones** y **30+ países**
- Valor total afectado: **$123,353M**
- Mecanismos: security (23), economic (15), political (12), social (9), legal (5)
- Sectores: Transport (33), Energy (14), Telecom (7), Mining (3), Manufacturing (2)
- Pipeline detection rate: 54/70 (77%)
- 6 thesis tables generadas en `data/samples/final/thesis_tables/`
- Output: `data/samples/final/bri_cancellations_FINAL_v2.csv` (70 rows)

### Pending
- Fase 2 futura: GDELT v1 para pre-2015
- Cruce con AidData TUFF 3.0 / Baumgartner & Zeitz (2022) para validación
- Verificación manual de señales LIKELY del Tier 2 (93 candidatos adicionales)
- Completar valores faltantes para 42/70 casos sin value_usd
