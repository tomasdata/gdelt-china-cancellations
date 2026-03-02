# GDELT — Hallazgos de Exploración

> Actualizado progresivamente durante la Fase 1.

---

## 1. Métodos de Acceso: Estado Real

| Método | Estado | Notas |
|--------|--------|-------|
| `api.gdeltproject.org` (REST API) | ❌ No accesible | Timeout completo (connect + read). Bloqueado en este entorno. |
| `data.gdeltproject.org` (CSV v2) | ✅ Funciona | HTTP, 467ms avg. Datos crudos cada 15 min. |
| BigQuery (`gdelt-bq`) | ⚠️ Pendiente | Cuenta `tomas@orsan.ai` activa, pero falta `gcloud auth application-default login` |

**Decisión**: La ruta principal es **archivos CSV públicos** vía `data.gdeltproject.org`. Para búsquedas históricas 2017-2024, se usa el master file list.

---

## 2. Estructura del CSV de Events (61 columnas)

Cada archivo `.export.CSV.zip` tiene ~1500-2500 filas por actualización de 15 min. Sin headers — se cargan con los nombres del codebook.

**Columnas más útiles para la tesis:**

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `GlobalEventID` | int | ID único del evento |
| `Day` | int | Fecha YYYYMMDD |
| `Actor1Name` / `Actor2Name` | str | Nombre actor (ej: "CHINA", "HUAWEI") |
| `Actor1CountryCode` / `Actor2CountryCode` | str | Código FIPS (CHN, USA, CHL...) |
| `EventCode` | int | Código CAMEO del evento |
| `EventRootCode` | int | Categoría raíz CAMEO (1=verbal coop, 14=protest, 19=force...) |
| `GoldsteinScale` | float | Intensidad conflicto: -10 (más conflictivo) a +10 (más cooperativo) |
| `AvgTone` | float | Tono promedio de artículos: negativo = hostilidad |
| `NumMentions` | int | Nº total de menciones en medios |
| `NumSources` | int | Nº fuentes distintas |
| `ActionGeo_FullName` | str | Lugar del evento (ej: "Santiago, Metropolitana, Chile") |
| `Actor1Geo_CountryCode` | str | Código FIPS del país Actor1 |
| `Actor2Geo_CountryCode` | str | Código FIPS del país Actor2 |
| `SOURCEURL` | str | URL del artículo fuente |

**Observaciones del slice actual (15 min):**
- GoldsteinScale: min=-10, max=10, mean=0.15
- AvgTone: min=-15.38, max=13.54, mean=-2.25 (tendencia negativa general)
- China (CHN) aparece en 59 de 1901 eventos (3.1%) en un slice típico
- Top países Actor1: USA, IRN, GBR, RUS, ISR, NGA, **CHN** (7mo)

---

## 3. Estructura del CSV de GKG (27 columnas)

Cada archivo `.gkg.csv.zip` tiene ~1900 filas por update (un artículo = una fila).

**Columnas clave:**

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `GKGRECORDID` | str | ID único del registro |
| `DATE` | str | Timestamp YYYYMMDDHHMMSS |
| `SourceCommonName` | str | Dominio del medio (ej: "reuters.com") |
| `DocumentIdentifier` | str | URL completa del artículo |
| `V2Themes` | str | Temas GDELT con offsets (`THEME,offset;THEME,offset`) |
| `V2Locations` | str | Lugares extraídos con coords |
| `V2Persons` | str | Personas mencionadas con offsets |
| `V2Organizations` | str | Organizaciones mencionadas con offsets |
| `V2Tone` | str | 7 valores CSV: Tone, Positive, Negative, Polarity, ActivityRef, SelfRef, WordCount |
| `AllNames` | str | Todas las entidades nombradas con offset |
| `GCAM` | str | Métricas GCAM (sentiment counts por diccionario) |

**V2Tone — cómo leer los 7 valores:**
```
Tone        = score neto compuesto (-100 a +100)
Positive    = % de referencias positivas
Negative    = % de referencias negativas
Polarity    = Positive + Negative (volatilidad emocional)
ActivityRef = % de referencias a acciones/movimiento
SelfRef     = % de referencias a quién habla
WordCount   = nº total de palabras del artículo
```

**Ejemplo de V2Tone de artículo negativo:**
```
Tone=-3.83, Positive=2.44%, Negative=6.26%, Polarity=8.70
```

**Observaciones:**
- 539 de 1908 artículos (28.3%) mencionan China en themes u organizaciones — muy alta cobertura
- `V2Themes` contiene códigos como `TAX_ETHNICITY_CHINESE`, `ECON_FOREIGNINVESTMENT`, `EPU_CATS_NATIONAL_SECURITY`
- Para la tesis, el campo más útil es la combinación: `V2Organizations` (contiene empresas chinas) + `V2Tone` (sentimiento) + `DocumentIdentifier` (URL para verificar)

---

## 4. Resultados Scripts 05-06: Events Table (76,771 eventos económicos)

Scripts ejecutados y resultados guardados en `data/samples/`.

### EventCodes encontrados (China + rechazo económico 2017-2024)
| EventCode | Descripción | N |
|-----------|-------------|---|
| 163 | Impose embargo/sanctions/expel | 61,043 |
| 164 | Halt negotiations | 15,716 |
| 165 | Expel economic actor | 12 |

### Distribución temporal
| Año | N eventos | Observación |
|-----|-----------|-------------|
| 2017 | 12,717 | Línea base |
| 2018 | 9,792 | |
| 2019 | 10,808 | Inicio tensiones USA-China |
| 2020 | 12,239 | Pico COVID + guerra comercial |
| 2021 | 10,959 | Sanciones Xinjiang |
| 2022 | 6,962 | Baja |
| 2023 | 7,227 | |
| 2024 | 6,067 | |

### Top países contraparte de China (eventos negativos)
USA (13,534), PRK (5,007), RUS (4,112), AUS (2,299), IRN, KOR, GBR, JPN, PHL

### LATAM: 665 eventos económicos negativos
| País | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|------|------|------|------|------|------|------|------|------|
| Chile | 8 | 20 | 4 | 3 | 1 | 0 | 0 | 0 |
| Argentina | 5 | 30 | 20 | 2 | 0 | 4 | 4 | 0 |
| Brazil | 19 | 5 | 45 | 13 | 19 | 6 | 10 | 13 |
| Venezuela | 52 | 3 | 73 | 48 | 10 | 7 | 7 | 17 |
| Mexico | 10 | 16 | 27 | 5 | 13 | 5 | 18 | 14 |

### Hallazgo clave LATAM
**Chile 2018** (20 eventos): Evento más mencionado es "China slams Chile for blocking $5 billion sale of shares in lithium mine" — esta es una **cancelación NO incluida en los 18 del dataset original de la tesis**.
URL: https://ipolitics.ca/2018/04/26/the-drilldown-china-slams-chile-for-blocking-5-billion-sale-of-shares-in-lithium-mine/

### Limitación de la Events Table
La tabla captura *eventos diplomáticos* (actor-level) pero NO incluye el nombre del proyecto específico. Para saber "Huawei cable" o "CRRC trenes" se necesita la GKG.

---

## 5. Pendiente: GKG Discovery (~$10, ejecutar con cuenta GCP personal)

Script listo: `notebooks/07_gkg_discovery.py`. Solo falta ejecutar con nueva cuenta GCP.

**Qué busca:** artículos de noticias donde aparecen ~25 empresas chinas
(Huawei, Sinopec, CNNC, CRRC, China Railway, COSCO, etc.) con tono negativo
y temas de inversión/infraestructura/energía. Resultado esperado: miles de
artículos candidatos → filtrar por keywords de cancelación → dataset comprehensivo.

**Costo estimado:** ~$10-12 una sola vez (cubierto por $300 créditos de cuenta nueva).
**Ver instrucciones:** `docs/SETUP_NUEVA_CUENTA_GCP.md`

---

## 6. Contexto de la investigación (latex-base.tex)

El master file list contiene TODOS los archivos desde 2015:

```
http://data.gdeltproject.org/gdeltv2/masterfilelist.txt
```

Formato de cada línea:
```
<size_bytes> <md5> <url>
```

Para el período 2017-2024, son ~350,000 archivos (events + mentions + gkg). La estrategia correcta es:
1. Descargar `masterfilelist.txt` (unos MB, solo texto)
2. Filtrar por rango de fecha (el nombre del archivo contiene el timestamp)
3. Para cada proyecto cancelado, filtrar ±30 días de su fecha de cancelación
4. Descargar solo esos archivos y filtrar por actores/organizaciones relevantes

**BigQuery (pendiente):** La vía más eficiente. Requiere:
```bash
gcloud auth application-default login
```
Proyecto: `gdelt-bq`, tabla: `gdeltv2.gkg_partitioned` (más eficiente).

---

## 5. Temas GDELT Relevantes para la Tesis

Temas que aparecen en artículos sobre inversiones chinas:

| Tema GDELT | Descripción |
|------------|-------------|
| `ECON_FOREIGNINVESTMENT` | Inversión extranjera directa |
| `EPU_CATS_NATIONAL_SECURITY` | Seguridad nacional (factor geopolítico) |
| `TAX_ETHNICITY_CHINESE` | Referencia étnica/cultural china |
| `WB_2473_DIPLOMACY_AND_NEGOTIATIONS` | Diplomacia y negociaciones |
| `CRISISLEX_C04_LOGISTICS_TRANSPORT` | Infraestructura de transporte |
| `ENV_OIL` | Petróleo/energía |
| `ECON_UNIONS` | Sindicatos/laborales |
| `LEGISLATION` | Marco legal/regulatorio |

Para clasificar automáticamente razones de cancelación:
- **Geopolítica**: `EPU_CATS_NATIONAL_SECURITY`, `SOVEREIGNTY`, `TAX_WORLDMAMMALS` (relaciones bilaterales)
- **Económica**: `ECON_FOREIGNINVESTMENT`, `EPU_ECONOMY`, `SHORTAGE`
- **Técnica**: `CRISISLEX_C04_LOGISTICS_TRANSPORT`, `LEGISLATION`, `WB_845_LEGAL_AND_REGULATORY_FRAMEWORK`
