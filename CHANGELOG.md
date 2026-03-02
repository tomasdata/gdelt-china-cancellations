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

### Pending (actualizado)
- Esperar script 07 GKG → analizar organizaciones que emergen
- Cruzar 801 candidatos Events con candidatos GKG (validación cruzada)
- Pasar pipeline 08→12 sobre datos históricos 2015-2016 (cuando sea oportuno)
- Comparar 8 señales LATAM identificadas con los 18 del paper de Villalobos
- Investigar mecanismo Venezuela más profundamente (monto inversión CNPC afectada)
