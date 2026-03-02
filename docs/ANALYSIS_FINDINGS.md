# Hallazgos del análisis de datos GDELT Events

## Script 08 — Auditoría y deduplicación

### Dataset Conflicto
- Original: 374,108 filas
- Post-dedup (URLs únicas): 248,745 artículos reales
- Reducción: 125,363 filas duplicadas

### Dataset Económico
- Original: 76,771 filas
- Post-dedup (URLs únicas): 45,531 artículos reales
- Reducción: 31,240 filas duplicadas

### Overlap entre datasets
- 9,218 URLs aparecen en ambos datasets

### FIPS críticos
- `CH` = China (NO Chile). Chile = `CI`
- Bug presente en scripts anteriores que usaban 'CH' para Chile

### Próximo paso
- Script 09: taxonomía de contextos (separar guerra comercial de BRI/inversión)

## Script 09 — Taxonomía de contextos

### Conflicto (248k post-dedup)
- `other`: 167,370 (67.3%)
- `bri_investment`: 46,155 (18.6%)
- `trade_war`: 19,055 (7.7%)
- `military`: 14,804 (6.0%)
- `financial`: 1,361 (0.5%)

### Económico (45k post-dedup)
- `other`: 25,197 (55.3%)
- `bri_investment`: 7,677 (16.9%)
- `trade_war`: 7,285 (16.0%)
- `military`: 4,623 (10.2%)
- `financial`: 749 (1.6%)

### BRI/Investment combinado
- Total eventos BRI únicos: 52,439
- Guardado en: `data/samples/bri_investment_events_all.csv`

### Próximo paso
- Script 10: análisis geográfico profundo sobre bri_investment_events_all.csv

## Script 10 — Análisis geográfico

### Eventos BRI por región
- **Other**: 28,275 eventos, 115 países, tono -6.52
- **Asia_SE**: 5,792 eventos, 8 países, tono -7.04
- **MedioO**: 4,668 eventos, 11 países, tono -6.13
- **Asia_C**: 4,199 eventos, 7 países, tono -7.16
- **Europa_E**: 3,634 eventos, 12 países, tono -6.97
- **Africa**: 3,116 eventos, 20 países, tono -7.01
- **LATAM**: 2,679 eventos, 17 países, tono -6.36
- **Oceania**: 76 eventos, 3 países, tono -6.15

### LATAM total: 2,679 eventos
- México: 502 eventos, tono -6.49
- Brasil: 429 eventos, tono -6.03
- Venezuela: 360 eventos, tono -5.58
- Colombia: 261 eventos, tono -7.12
- Ecuador: 248 eventos, tono -6.53
- Cuba: 194 eventos, tono -6.75
- Argentina: 179 eventos, tono -5.91
- Perú: 120 eventos, tono -6.84
- Chile: 112 eventos, tono -5.98
- Bolivia: 97 eventos, tono -6.99
- Panamá: 68 eventos, tono -6.89
- Guatemala: 39 eventos, tono -6.97
- Nicaragua: 33 eventos, tono -6.36
- Paraguay: 25 eventos, tono -6.01
- Uruguay: 7 eventos, tono -4.85
- Honduras: 3 eventos, tono -1.87
- El Salvador: 2 eventos, tono -7.74

### Próximo paso
- Script 11: evolución temporal y picos por año/región

## Script 11 — Evolución temporal

### Volumen BRI por año
- 2017: 6,596 eventos, tono -6.77
- 2018: 6,569 eventos, tono -6.64
- 2019: 8,208 eventos, tono -6.83
- 2020: 9,904 eventos, tono -6.50
- 2021: 5,098 eventos, tono -6.51
- 2022: 4,548 eventos, tono -6.54
- 2023: 5,517 eventos, tono -6.47
- 2024: 5,999 eventos, tono -6.86

### Patrones clave
- Pico 2020 en todas las regiones (COVID impacta proyectos)
- Filipinas 2024: 579 eventos (pico récord — proyectos cancelados Mar Céleste/BRI)
- Bosnia tono más negativo (-9.36): plantas carbón chinas rechazadas
- Ecuador 2023-2024: tendencia al alza (Coca Codo Sinclair y otros)

### Próximo paso
- Script 12: clustering de proyectos candidatos

## Script 12 — Clustering de proyectos candidatos

### Filtro URL estricto
- Post-filtro (URL contiene keywords inversión + excl. China/EEUU/HK): 8,912 eventos
- Reducción desde 52k: 43,527 eventos de ruido eliminados

### Proyectos candidatos (clusters ≥3 eventos)
- Total candidatos: 801
- Other: 364 proyectos
- Asia_SE: 117 proyectos
- MedioO: 86 proyectos
- Africa: 82 proyectos
- Asia_C: 56 proyectos
- LATAM: 53 proyectos
- Europa_E: 42 proyectos
- Oceania: 1 proyectos

### LATAM: 53 proyectos candidatos
- Brasil (2017): 20 eventos, tono -5.92
- Venezuela (2019): 12 eventos, tono -3.12
- México (2019): 9 eventos, tono -4.91
- Brasil (2021): 8 eventos, tono -8.81
- Chile (2018): 7 eventos, tono -2.53
- Brasil (2020): 7 eventos, tono -6.32
- Ecuador (2024): 7 eventos, tono -6.72
- Venezuela (2018): 3 eventos, tono -4.96
- México (2023): 7 eventos, tono -5.55
- Argentina (2019): 3 eventos, tono -7.51
- Brasil (2017): 7 eventos, tono -5.83
- Ecuador (2020): 6 eventos, tono -1.76
- Venezuela (2024): 7 eventos, tono -2.05
- Venezuela (2020): 9 eventos, tono -3.87
- Brasil (2023): 6 eventos, tono -5.86
- Venezuela (2019): 5 eventos, tono -4.40
- Venezuela (2024): 5 eventos, tono -4.89
- México (2024): 5 eventos, tono -5.39
- Perú (2021): 5 eventos, tono -6.46
- México (2020): 4 eventos, tono -5.85
- Brasil (2020): 4 eventos, tono -5.49
- Chile (2017): 4 eventos, tono -4.64
- Cuba (2018): 3 eventos, tono -7.53
- Colombia (2024): 4 eventos, tono -6.54
- Brasil (2019): 4 eventos, tono -3.35
- México (2019): 4 eventos, tono -6.85
- Brasil (2020): 4 eventos, tono -6.10
- México (2018): 4 eventos, tono -5.97
- Cuba (2023): 4 eventos, tono -5.85
- México (2024): 3 eventos, tono -9.29
- Brasil (2024): 5 eventos, tono -3.24
- México (2021): 4 eventos, tono -3.57
- Argentina (2018): 3 eventos, tono -2.22
- Brasil (2022): 3 eventos, tono -6.98
- Ecuador (2019): 3 eventos, tono -2.70
- Venezuela (2017): 4 eventos, tono -4.57
- Ecuador (2024): 3 eventos, tono -6.73
- Ecuador (2023): 3 eventos, tono -6.23
- Brasil (2018): 4 eventos, tono -6.92
- Venezuela (2021): 3 eventos, tono -5.01
- Brasil (2019): 3 eventos, tono -6.32
- Ecuador (2017): 3 eventos, tono -5.79
- Argentina (2017): 3 eventos, tono -8.17
- Cuba (2020): 3 eventos, tono -5.79
- México (2018): 3 eventos, tono -7.31
- Bolivia (2017): 3 eventos, tono -7.75
- Perú (2023): 3 eventos, tono -9.23
- Panamá (2020): 3 eventos, tono -6.92
- México (2020): 3 eventos, tono -6.89
- Argentina (2018): 3 eventos, tono -2.74
- México (2019): 3 eventos, tono -6.21
- Venezuela (2018): 3 eventos, tono -5.79
- Brasil (2021): 3 eventos, tono -4.60

### Limitaciones identificadas
- Filipinas 2024: dominado por disputas Mar Sur China (no BRI)
- Bosnia: eventos de conflicto interno (no plantas carbón chinas)
- La validación manual de los top candidatos es necesaria
- Cruzar con dataset GKG (script 07) cuando esté listo para validación

## Análisis profundo LATAM — 53 candidatos (post script 12)

### Metodología de análisis
- Revisión URL por URL de cada cluster, identificando señal real vs. ruido
- Categorización por mecanismo de cancelación/suspensión
- Total revisado: 53 clusters LATAM → **8 señales reales identificadas** (~15% signal rate)

### Señales reales BRI/inversión China en LATAM

#### Chile (CI_003 — 2018, 7 eventos, tono -2.53)
- **Evento**: Chile bloquea venta de acciones SQM a empresas chinas (Tianqi Lithium)
- **URL clave**: seekingalpha.com — "Chile files complaint to block sale of SQM shares to Chinese firms"
- **Mecanismo**: Gobierno del país receptor bloquea adquisición (nacionalismo del litio)
- **Relevancia tesis**: ALTO — caso paradigmático de rechazo de inversión china por host country

#### Ecuador — Camarón (EC_005 — 2019, 3 eventos)
- **Evento**: China suspende aprobación de exportación de camarón a Santa Priscila y Omarsa (Ecuador)
- **URL clave**: undercurrentnews.com — "China appears to have suspended shrimp export approval"
- **Mecanismo**: Bans de mercado chino como presión política (nuevo vertical)
- **Relevancia tesis**: MEDIO — no es "proyecto de inversión" sino restricción de acceso a mercado

#### Ecuador — Yasuni (EC_011 — 2024, 3 eventos)
- **Evento**: Contexto sobre Yasuni oil y resistencia ambiental en Ecuador
- **URL clave**: globalproject.info — "sullorlo del baratro lamerica latina"
- **Mecanismo**: Moratoria ambiental (bloqueo político interno)
- **Relevancia tesis**: MEDIO — contexto, requiere validación manual adicional

#### Venezuela — Unipec/CNPC retiro de tanqueros (Oct 2018)
- **Evento**: Unipec (brazo comercial de CNPC) prohíbe uso de tanqueros vinculados a Venezuela
- **URL clave**: reuters.com — "chinas-unipec-bans-use-of-oil-tankers-linked-to-venezuela"
- **Mecanismo**: Auto-censura de empresa china para evitar sanciones secundarias de EEUU
- **Relevancia tesis**: ALTO — mecanismo nuevo (empresa china se retira por presión EEUU, no por host country)

#### Venezuela — ZTE vigilancia (Dic 2018)
- **Evento**: EEUU sanciona a ZTE por proveer tecnología de vigilancia a Venezuela
- **URL clave**: telecomstechnews.com — "zte us sanctions venezuelan surveillance"
- **Mecanismo**: Sanciones secundarias EEUU fuerzan retiro de empresa china
- **Relevancia tesis**: ALTO — caso emblemático (carnet de la patria)

#### Venezuela — CNPC suspende operaciones (Sep 2019)
- **Evento**: Petrolera china suspende operaciones en Venezuela para evitar sanciones
- **URL clave**: es.panampost.com — "petrolera china suspende operaciones en venezuela para evitar sanciones"
- **Mecanismo**: CNPC/PetroChina se retira voluntariamente por sanciones EEUU
- **Relevancia tesis**: ALTO — caso documentable con monto de inversión afectada

#### Venezuela — EEUU sanciona empresa china (Nov-Dic 2020)
- **Evento**: EEUU impone sanciones a empresa china por rol en censura de internet en Venezuela
- **URL clave**: reuters.com — "us-imposes-venezuela-related-sanctions-targeting-chinese-firm"
- **Mecanismo**: Sanciones secundarias directas a empresa china
- **Relevancia tesis**: ALTO — sanciones EEUU como mecanismo de expulsión de inversión china

#### Brasil — Autopista Tamoios (Sep 2017)
- **Evento**: Inversores chinos "pueden no seguir" con la concesión de la autopista Tamoios (São Paulo)
- **URL clave**: bnamericas.com — "chinese-investors-may-not-pursue-sao-paulos-tamoios-highway-concession"
- **Mecanismo**: Inversores chinos se retiran de licitación (razones desconocidas, requiere verificación)
- **Relevancia tesis**: MEDIO — puede ser retiro voluntario o rechazo de licitación

### Ruido dominante (92 de 53 clusters clasificados como noise)
- **Brasil (15 clusters)**: Bans de carne por escándalo sanitario + vacas locas + COVID + vacuna Coronavac (todo food safety, no BRI)
- **México (10 clusters)**: Fentanilo y política de drogas EEUU-China (ningún proyecto de inversión)
- **Argentina (3 clusters)**: G20 diplomacia genérica, crimen local
- **Cuba (3 clusters)**: Política interna EEUU (TikTok, Flynn), ninguna inversión china
- **Colombia (1 cluster)**: FARC, violencia interna
- **Perú (2 clusters)**: Crimen organizado, persecución Falun Gong
- **Bolivia (1 cluster)**: Sanciones ONU a Siria (geo erróneo)
- **Panamá (1 cluster)**: Corrupción penitenciaria local

### Hallazgo crítico — Nuevo mecanismo identificado
**"Sanciones secundarias EEUU como mecanismo de cancelación de proyectos BRI"**
- Venezuela muestra un mecanismo NO documentado en la literatura: empresas chinas se retiran de un país anfitrión NO por decisión del host country, sino porque EEUU aplica sanciones secundarias que hacen imposible operar sin consecuencias para la empresa china
- Este mecanismo (externo al host country) puede ser una contribución genuina de la tesis al debate académico
- Casos: Unipec (tanqueros), ZTE (vigilancia), CNPC (petróleo), empresa no identificada (internet 2020)

### Conclusión del análisis LATAM
- **Rate de señal real**: ~8/53 = 15% (muy bajo — el pipeline Events sigue siendo ruidoso para LATAM)
- **GKG pipeline (script 07)** esperado para mejorar dramáticamente la calidad (filtra por organizaciones y temas, no por geografía)
- **Proyectos reales identificados**: Chile SQM/litio, Venezuela PetroChina/CNPC/ZTE (sanciones), Ecuador camarón/Yasuni, Brasil Tamoios highway
- **Próximo paso**: Cruzar estos 8 casos con los 18 del paper de Villalobos para ver overlap


## Script 09 v2 — Clasificador BRI mejorado

### Mejoras implementadas
- **Puerta-1**: `has_chinese_actor()` — valida que haya actor/empresa china antes de clasificar
- **Puerta-2**: `has_project_signal()` — requiere término de proyecto + término de acción (no solo uno)
- **`detect_mechanism()`**: detecta por qué se canceló (sanciones, medioambiental, político, deuda)
- **FIPS expandido**: añadidos GY/NS/CS/JM/HA/ES/HO/DR a BRI_RECEIVER_FIPS

### Resultados v2
- BRI combinado v2: 31,090 eventos únicos
  - Conflicto BRI: 27,553
  - Económico BRI: 4,408
- Comparativa: v1=52,439 → v2=31,090 (cambio: -21,349)

### Distribución de mecanismos (v2)
- `unknown`: 29,766 (95.7%)
- `us_sanctions`: 898 (2.9%)
- `environmental_opposition`: 203 (0.7%)
- `political_rejection`: 108 (0.3%)
- `project_failure`: 67 (0.2%)
- `debt_renegotiation`: 48 (0.2%)

### Próximo paso
- Script 10 v2: análisis geográfico con países LATAM corregidos

## Script 10 — Análisis geográfico

### Eventos BRI por región
- **MedioO**: 6,455 eventos, 11 países, tono -6.37
- **Asia_SE**: 5,792 eventos, 8 países, tono -7.04
- **Asia_C**: 4,199 eventos, 7 países, tono -7.16
- **Africa**: 3,926 eventos, 20 países, tono -7.09
- **Europa_E**: 3,837 eventos, 12 países, tono -6.97
- **Other**: 3,819 eventos, 54 países, tono -6.45
- **LATAM**: 2,966 eventos, 24 países, tono -6.43
- **Oceania**: 96 eventos, 4 países, tono -6.19

### LATAM total: 2,966 eventos
- México: 502 eventos, tono -6.49
- Brasil: 429 eventos, tono -6.03
- Venezuela: 360 eventos, tono -5.58
- Colombia: 261 eventos, tono -7.12
- Ecuador: 248 eventos, tono -6.53
- Cuba: 194 eventos, tono -6.75
- Argentina: 179 eventos, tono -5.91
- Perú: 120 eventos, tono -6.84
- Chile: 112 eventos, tono -5.98
- Bolivia: 97 eventos, tono -6.99
- El Salvador: 73 eventos, tono -7.40
- Panamá: 68 eventos, tono -6.89
- Guatemala: 39 eventos, tono -6.97
- Haití: 39 eventos, tono -6.38
- Jamaica: 38 eventos, tono -6.99
- Honduras: 34 eventos, tono -6.40
- Nicaragua: 33 eventos, tono -6.36
- Guyana: 29 eventos, tono -7.89
- Costa Rica: 27 eventos, tono -6.61
- Belice: 26 eventos, tono -7.27
- Paraguay: 25 eventos, tono -6.01
- Dom.Rep.: 13 eventos, tono -7.81
- Suriname: 13 eventos, tono -7.45
- Uruguay: 7 eventos, tono -4.85

### Mejoras v2
- Añadidos GY/NS/CS/JM/HA/BH/DR al mapa LATAM
- Fix colisión SN: Senegal=SN (Africa), Singapore removido de Asia_SE
- Análisis de mecanismo por región (columna 'mechanism' de script 09 v2)

### Próximo paso
- Script 12 v2: clustering actor-aware con ventana 180 días

## Script 12 v2 — Clustering actor-aware

### Mejoras implementadas
- Clustering por (país + actor_norm): CRRC ya no se mezcla con COSCO en mismo cluster
- Ventana 180 días (antes 90) con gap-reopen
- Relevancia = n_eventos × log(menciones) × |tono| (antes: n×menciones lineal)
- Umbral mínimo: 2 eventos para SOEs específicas, 3 para actores genéricos

### Resultados v2
- Total proyectos candidatos: 309
- Asia_SE: 61 proyectos
- Africa: 58 proyectos
- MedioO: 50 proyectos
- Asia_C: 44 proyectos
- Other: 38 proyectos
- LATAM: 28 proyectos
- Europa_E: 27 proyectos
- Oceania: 3 proyectos

### LATAM v2: 28 proyectos candidatos
- Brasil / BRAZIL (2021): 6 eventos, tono -9.97, mec=unknown
- Brasil / BRAZIL (2020): 8 eventos, tono -6.44, mec=unknown
- Brasil / BRAZIL (2017): 7 eventos, tono -6.85, mec=unknown
- Brasil / BRAZILIAN (2017): 9 eventos, tono -4.77, mec=unknown
- Haití / HAITI (2022): 5 eventos, tono -9.48, mec=unknown
- Brasil / BRAZIL (2018): 5 eventos, tono -9.25, mec=unknown
- Brasil / NAN (2017): 6 eventos, tono -6.09, mec=unknown
- Argentina / PROTESTER (2019): 3 eventos, tono -7.51, mec=unknown
- Guyana / GUYANA (2018): 3 eventos, tono -8.98, mec=unknown
- México / NAN (2024): 5 eventos, tono -5.75, mec=unknown
- México / NAN (2018): 5 eventos, tono -5.39, mec=unknown
- Brasil / NAN (2018): 5 eventos, tono -4.72, mec=unknown
- Ecuador / CANTON (2017): 4 eventos, tono -5.38, mec=unknown
- Ecuador / CANTON (2024): 3 eventos, tono -7.83, mec=unknown
- Venezuela / NAN (2020): 3 eventos, tono -8.31, mec=unknown
- Argentina / ARGENTINA (2018): 3 eventos, tono -6.79, mec=unknown
- México / NAN (2023): 4 eventos, tono -5.53, mec=us_sanctions
- Brasil / BRAZIL (2023): 3 eventos, tono -8.79, mec=unknown
- Brasil / BRAZILIAN (2018): 3 eventos, tono -6.08, mec=unknown
- Venezuela / VENEZUELA (2023): 9 eventos, tono -1.75, mec=unknown
- México / PROSECUTOR (2023): 3 eventos, tono -5.57, mec=unknown
- México / MEXICO (2020): 3 eventos, tono -5.96, mec=unknown
- Venezuela / VENEZUELA (2018): 5 eventos, tono -3.27, mec=unknown
- México / NAN (2019): 4 eventos, tono -3.64, mec=unknown
- Venezuela / NAN (2019): 4 eventos, tono -3.56, mec=unknown
- Chile / CHILE (2018): 6 eventos, tono -1.56, mec=unknown
- Ecuador / ECUADOR (2020): 3 eventos, tono -2.95, mec=unknown
- Venezuela / UNITED STATES (2020): 4 eventos, tono -3.29, mec=unknown

### Mecanismos (candidatos globales)
- `unknown`: 293 proyectos (94.8%)
- `us_sanctions`: 16 proyectos (5.2%)

### Próximo paso
- Script 14: análisis por empresa SOE china
- Script 15: análisis causal de mecanismos
- Script 16: validación cruzada Events × GKG

## Script 14 — Análisis por empresa SOE china

### Fuentes analizadas
- Events clusters v2: 309 candidatos
- GKG artículos: 92,990 artículos 2017-2024

### SOEs en Events
- **SOE_GENERIC**: 3 clusters, 3 países, tono -6.05
- **SOE_TELECOM**: 1 clusters, 1 países, tono -3.08

### SOEs en GKG (artículos con tono negativo)
- **SOE_TELECOM**: 64779 artículos únicos, tono medio -5.23, mín -27.59
- **SOE_OIL**: 9124 artículos únicos, tono medio -4.54, mín -17.42
- **SOE_MINING**: 5722 artículos únicos, tono medio -4.29, mín -17.89
- **SOE_RAILWAY**: 4028 artículos únicos, tono medio -4.81, mín -17.19
- **SOE_MARITIME**: 2856 artículos únicos, tono medio -4.62, mín -17.18
- **SOE_FINANCE**: 2414 artículos únicos, tono medio -4.53, mín -11.49
- **SOE_HARBOUR**: 1384 artículos únicos, tono medio -4.38, mín -14.06
- **SOE_ENERGY**: 342 artículos únicos, tono medio -4.59, mín -9.23
- **SOE_CONSTRUCT**: 284 artículos únicos, tono medio -4.30, mín -10.93

### Top orgs chinas mencionadas en GKG
- `HUAWEI`: 279589 artículos
- `SINOPEC`: 15322 artículos
- `COSCO`: 7119 artículos
- `CHINESE COMMUNIST PARTY`: 2467 artículos
- `CHINA TELECOMMUNICATIONS`: 2305 artículos
- `PETROCHINA`: 2131 artículos
- `HUAWEI TECHNOLOGIES LTD`: 2038 artículos
- `CHINA RAILWAY`: 2006 artículos
- `CHINA FOREIGN MINISTRY`: 1996 artículos
- `HUAWEI TECHNOLOGIES CO LTD`: 1961 artículos
- `CHINESE FOREIGN MINISTRY`: 1931 artículos
- `CNOOC`: 1815 artículos
- `HUAWEI TECHNOLOGIES CO`: 1747 artículos
- `CHINESE EMBASSY`: 1643 artículos
- `B CHINA RAILWAY`: 1374 artículos

### Próximo paso
- Script 15: análisis causal de mecanismos
- Script 16: validación cruzada Events × GKG

## Script 15 — Análisis causal de mecanismos

### Input: 31,090 eventos BRI clasificados

### Distribución global de mecanismos
- `unknown`: 29,766 eventos (95.7%), tono -6.82
- `us_sanctions`: 898 eventos (2.9%), tono -5.58
- `environmental_opposition`: 203 eventos (0.7%), tono -6.67
- `political_rejection`: 108 eventos (0.3%), tono -6.38
- `project_failure`: 67 eventos (0.2%), tono -6.57
- `debt_renegotiation`: 48 eventos (0.2%), tono -6.37

### Dinámica temporal de sanciones EEUU
- Pre-2018: 2.11% de eventos BRI son sanciones US
- Post-2018: 3.03% de eventos BRI son sanciones US
- Ratio: 1.4x mayor post-2018

### Mecanismos por región (top no-unknown)
- **Africa**: us_sanctions=1.0%, environmental_opposition=0.8%
- **Asia_C**: us_sanctions=2.0%, environmental_opposition=0.5%
- **Asia_SE**: us_sanctions=0.9%, environmental_opposition=0.7%
- **Europa_E**: us_sanctions=1.6%, environmental_opposition=0.3%
- **LATAM**: us_sanctions=2.2%, environmental_opposition=0.5%
- **MedioO**: us_sanctions=6.2%, environmental_opposition=0.5%
- **Other**: us_sanctions=4.8%, environmental_opposition=1.4%

### Próximo paso
- Script 16: validación cruzada Events × GKG

## Script 16 — Validación cruzada Events × GKG

### Confidence distribution
- `geo_match`: 308 candidatos (99.7%)
- `high`: 1 candidatos (0.3%)

### Recall vs señales conocidas: 7/8 (88%)

### High confidence candidatos globales: 1
- Irán / SOE_TELECOM (2017): 2 eventos, 6145 artículos GKG

### Conclusión pipeline
- Pipeline Events → clustering → GKG cross-validation operativo
- De 309 candidatos Events, 309 tienen confirmación GKG
- 1 casos con confirmación SOE específica en GKG

## Script 17 — GKG-LATAM Deep Analysis

### Input: 92,990 artículos GKG → 11,058 con SOE+LATAM+tono<-2

### Distribución por SOE
- `SOE_TELECOM`: 7850 artículos
- `SOE_OIL`: 1557 artículos
- `SOE_MINING`: 720 artículos
- `SOE_MARITIME`: 434 artículos
- `SOE_FINANCE`: 360 artículos
- `SOE_RAILWAY`: 223 artículos
- `SOE_HARBOUR`: 187 artículos
- `SOE_ENERGY`: 53 artículos
- `SOE_CONSTRUCT`: 12 artículos
- `SOE_AUTO`: 3 artículos
- `SOE_BRI_GENERIC`: 1 artículos

### Distribución por país
- **México** (MX): 4432 artículos
- **Brasil** (BR): 2302 artículos
- **Argentina** (AR): 2184 artículos
- **Venezuela** (VE): 2027 artículos
- **Chile** (CI): 1070 artículos
- **Ecuador** (EC): 864 artículos
- **Cuba** (CU): 727 artículos
- **Perú** (PE): 616 artículos
- **Colombia** (CO): 575 artículos
- **Uruguay** (UY): 292 artículos
- **Nicaragua** (NU): 290 artículos
- **Panamá** (PM): 266 artículos
- **Bolivia** (BL): 233 artículos
- **Guatemala** (GT): 223 artículos
- **Honduras** (HO): 201 artículos
- **Haití** (HA): 187 artículos
- **El Salvador** (ES): 176 artículos
- **Jamaica** (JM): 122 artículos
- **Guyana** (GY): 110 artículos
- **Costa Rica** (CS): 92 artículos
- **Paraguay** (PA): 56 artículos
- **Dom.Rep.** (DR): 34 artículos
- **Belice** (BH): 18 artículos
- **Suriname** (NS): 16 artículos

### Clusters GKG-LATAM
- Total: 791 clusters (país × SOE × año)
- Con ≥3 artículos: 452
- Con ≥5 artículos (señal fuerte): 346

### Señales fuertes (≥5 artículos)
- **México × SOE_TELECOM (2019)**: 1445 artículos, tono -4.99
- **México × SOE_TELECOM (2018)**: 1336 artículos, tono -5.52
- **Argentina × SOE_TELECOM (2018)**: 1017 artículos, tono -5.24
- **Venezuela × SOE_TELECOM (2019)**: 519 artículos, tono -4.63
- **México × SOE_TELECOM (2020)**: 403 artículos, tono -4.79
- **Brasil × SOE_TELECOM (2019)**: 396 artículos, tono -4.07
- **Brasil × SOE_TELECOM (2020)**: 396 artículos, tono -3.95
- **Ecuador × SOE_TELECOM (2018)**: 355 artículos, tono -5.2
- **Argentina × SOE_TELECOM (2020)**: 346 artículos, tono -4.67
- **Argentina × SOE_TELECOM (2019)**: 345 artículos, tono -4.18
- **Brasil × SOE_TELECOM (2018)**: 340 artículos, tono -4.99
- **México × SOE_TELECOM (2021)**: 277 artículos, tono -4.39
- **Venezuela × SOE_OIL (2019)**: 230 artículos, tono -4.04
- **Uruguay × SOE_TELECOM (2018)**: 185 artículos, tono -5.08
- **Colombia × SOE_TELECOM (2018)**: 183 artículos, tono -6.96

## Script 18 — Dataset Final Curado LATAM

### Total señales curadas: 269
- Events con mecanismo: 44
- GKG infraestructura: 225

### Por país
- **Brasil**: 41 señales, tono mín -8.67
- **México**: 37 señales, tono mín -8.87
- **Venezuela**: 33 señales, tono mín -10.81
- **Chile**: 28 señales, tono mín -9.14
- **Argentina**: 25 señales, tono mín -9.49
- **Perú**: 24 señales, tono mín -10.00
- **Cuba**: 16 señales, tono mín -10.08
- **Ecuador**: 14 señales, tono mín -9.74
- **Panamá**: 10 señales, tono mín -9.36
- **Jamaica**: 8 señales, tono mín -5.83
- **Bolivia**: 6 señales, tono mín -10.47
- **Colombia**: 6 señales, tono mín -6.11
- **Haití**: 4 señales, tono mín -10.47
- **Honduras**: 4 señales, tono mín -10.47
- **Guyana**: 4 señales, tono mín -3.95
- **Costa Rica**: 3 señales, tono mín -10.47
- **Uruguay**: 3 señales, tono mín -4.07
- **Guatemala**: 2 señales, tono mín -10.47
- **Nicaragua**: 1 señales, tono mín -10.47

### Por mecanismo
- `confirmed_presence`: 225 señales en 19 países
- `us_sanctions`: 19 señales en 7 países
- `environmental_opposition`: 12 señales en 5 países
- `political_rejection`: 7 señales en 6 países
- `debt_renegotiation`: 3 señales en 2 países
- `project_failure`: 3 señales en 3 países

### Archivos generados
- `data/samples/final/latam_bri_signals_final.csv` — dataset curado LATAM
- `data/samples/final/latam_bri_signals_final.md` — narrativa para tesis
- `data/samples/final/global_bri_signals_final.csv` — señales globales
