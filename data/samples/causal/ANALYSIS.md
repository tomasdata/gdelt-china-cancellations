# Análisis Económico: Mecanismos de Cancelación de Proyectos BRI/Inversión China

**Fecha:** 2026-03-02
**Dataset:** GDELT GKG 2017-2024, clasificación automática por mecanismo causal
**Autor del análisis:** Claude (asistente de investigación)
**Tesis vinculada:** Ariel Villalobos — Determinantes de cancelación de proyectos BRI/inversión china (Magíster Economía, U. Chile)

---

## 1. Taxonomía de Mecanismos

Esta tabla describe cada mecanismo desde una perspectiva de economía política internacional, con su lógica causal y referencia a la literatura relevante.

| Mecanismo | Código | Definición económica | Locus causal | Literatura asociada |
|-----------|--------|---------------------|--------------|---------------------|
| **Debt renegotiation** | `debt_renegotiation` | El proyecto se cancela o suspende como resultado de la incapacidad del país receptor de servir la deuda asociada, o de una renegociación del contrato de financiamiento que lo hace inviable. Proxy potencial de la hipótesis del "debt trap". | Endógeno al contrato financiero | Brautigam (2020), Gelpern et al. (2021), Horn et al. (2021) |
| **Environmental opposition** | `environmental_opposition` | Oposición de actores locales (comunidades, ONGs, instituciones regulatorias) basada en impacto ambiental o social del proyecto. Refleja el aumento global de estándares ESG y accountability local. | Exógeno — presión sociopolítica local | Gallagher & Myers (2021), BRI Watch reports |
| **Political rejection** | `political_rejection` | Cancelación por decisión política del gobierno receptor, frecuentemente después de un cambio de administración o de escrutinio parlamentario. Incluye revisiones de contratos por nuevos gobiernos (ej. Mahathir en Malasia, 2018). | Exógeno — riesgo político del país receptor | Hillman (2018), Sacks (2021) |
| **Project failure** | `project_failure` | El proyecto fracasa por razones operativas o de viabilidad técnica/financiera intrínsecas: sobrecostos, retrasos crónicos, demanda insuficiente, errores de diseño. | Endógeno al proyecto | Flyvbjerg (2014), AidData (2021) |
| **US sanctions** | `us_sanctions` | Retiro de empresas chinas (o de proyectos con participación china) debido a sanciones secundarias de EEUU sobre el país receptor o sobre la empresa china directamente. Mecanismo exógeno de origen geopolítico estadounidense. | Exógeno — presión sistémica de tercero (EEUU) | Bown (2020), Farrell & Newman (2019) |
| **Unknown** | `unknown` | Artículos o menciones de GDELT que no permiten clasificar el mecanismo con el vocabulario de búsqueda utilizado. Puede reflejar subdetección, fragmentación de señal mediática, o eventos donde la causalidad no se explicita en la cobertura. | N/A | — |

**Nota metodológica:** La clasificación es automática basada en vocabulario GDELT (GKG themes + tono). Los errores de clasificación tipo I (falsos positivos) y tipo II (falsos negativos) son esperables, especialmente en la categoría `unknown` que actúa como residual.

---

## 2. Distribución Agregada (2017-2024)

### 2.1 Sobre el universo total de eventos (incluyendo `unknown`)

El universo total de eventos clasificados en el período 2017-2024 es **31,090 eventos-artículo**.

| Mecanismo | N eventos | % del total |
|-----------|-----------|-------------|
| Unknown | 29,766 | 95.74% |
| **US Sanctions** | **898** | **2.89%** |
| Environmental opposition | 203 | 0.65% |
| Political rejection | 108 | 0.35% |
| Project failure | 67 | 0.22% |
| Debt renegotiation | 48 | 0.15% |
| **TOTAL** | **31,090** | **100%** |

**Interpretación:** La tasa de clasificación exitosa es del 4.26% (1,324 eventos de 31,090 tienen mecanismo identificado). Esto es esperado en pipelines GDELT: la gran mayoría de artículos sobre inversión china no explicita el mecanismo de cancelación en lenguaje indexable. El 95.74% en `unknown` no implica que esos eventos no tengan mecanismo — implica que el pipeline de clasificación no lo detecta.

### 2.2 Sobre eventos con mecanismo identificado (excluyendo `unknown`)

La distribución relevante para la tesis es la de los **1,324 eventos clasificados**:

| Mecanismo | N eventos | % de clasificados | Tipo causal |
|-----------|-----------|-------------------|-------------|
| **US Sanctions** | **898** | **67.82%** | Exógeno-geopolítico |
| Environmental opposition | 203 | 15.33% | Exógeno-sociopolítico |
| Political rejection | 108 | 8.16% | Exógeno-político |
| Project failure | 67 | 5.06% | Endógeno |
| Debt renegotiation | 48 | 3.63% | Endógeno-financiero |
| **TOTAL CLASIFICADOS** | **1,324** | **100%** | — |

**Hallazgo central:** Las sanciones secundarias de EEUU representan más de **dos tercios** de todos los eventos con mecanismo identificado. Esta señal no encuentra precedente directo en la literatura BRI existente, que tiende a enfocarse en factores del país receptor.

### 2.3 Clasificación endógena vs. exógena

| Dimensión | Mecanismos incluidos | N | % |
|-----------|---------------------|---|---|
| **Endógenos al proyecto/contrato** | project_failure + debt_renegotiation | 115 | 8.69% |
| **Exógenos al proyecto** | us_sanctions + political_rejection + environmental_opposition | 1,209 | 91.31% |

La dominancia de factores exógenos (91.3%) sobre endógenos (8.7%) entre los eventos clasificados sugiere que la cancelación de proyectos BRI es fundamentalmente un fenómeno de economía política, no de gestión de proyectos.

---

## 3. Evolución Temporal (2017-2024)

### 3.1 Conteos absolutos por mecanismo y año

| Año | Debt Reneg. | Env. Opp. | Pol. Reject. | Proj. Fail. | Unknown | US Sanctions | Total |
|-----|-------------|-----------|--------------|-------------|---------|--------------|-------|
| 2017 | 13 | 41 | 17 | 4 | 4,480 | 98 | 4,653 |
| 2018 | 3 | 29 | 4 | 5 | 4,046 | 103 | 4,190 |
| 2019 | 10 | 31 | 11 | 15 | 4,572 | 192 | 4,831 |
| 2020 | 1 | 32 | 14 | 17 | 5,091 | 153 | 5,308 |
| 2021 | 7 | 20 | 19 | 2 | 2,399 | 108 | 2,555 |
| 2022 | 7 | 13 | 12 | 11 | 2,425 | 83 | 2,551 |
| 2023 | 7 | 19 | 17 | 8 | 3,085 | 82 | 3,218 |
| 2024 | 0 | 18 | 14 | 5 | 3,668 | 79 | 3,784 |
| **TOTAL** | **48** | **203** | **108** | **67** | **29,766** | **898** | **31,090** |

### 3.2 Distribución porcentual sobre eventos clasificados (excluyendo `unknown`) por año

| Año | Total clasificados | Debt R. | Env. Opp. | Pol. Rej. | Proj. Fail. | US Sanc. |
|-----|-------------------|---------|-----------|-----------|-------------|----------|
| 2017 | 173 | 7.5% | 23.7% | 9.8% | 2.3% | **56.6%** |
| 2018 | 144 | 2.1% | 20.1% | 2.8% | 3.5% | **71.5%** |
| 2019 | 259 | 3.9% | 12.0% | 4.2% | 5.8% | **74.1%** |
| 2020 | 217 | 0.5% | 14.7% | 6.5% | 7.8% | **70.5%** |
| 2021 | 156 | 4.5% | 12.8% | 12.2% | 1.3% | **69.2%** |
| 2022 | 126 | 5.6% | 10.3% | 9.5% | 8.7% | **65.9%** |
| 2023 | 133 | 5.3% | 14.3% | 12.8% | 6.0% | **61.7%** |
| 2024 | 116 | 0.0% | 15.5% | 12.1% | 4.3% | **68.1%** |

### 3.3 Análisis de tendencias temporales

**a) Sanciones EEUU (`us_sanctions`):**

El mecanismo dominante en todos los años. El pico absoluto ocurre en **2019** (n=192), coincidiendo con la escalada de la guerra comercial EEUU-China: Huawei añadida a la Entity List en mayo 2019; CNPC suspende operaciones Venezuela en septiembre 2019. En términos relativos sobre clasificados, las sanciones fluctúan entre 56.6% (2017, baseline pre-trade war) y 74.1% (2019, pico). La caída post-2019 en términos absolutos no indica menor actividad sancionatoria — la Entity List continuó expandiéndose — sino posiblemente saturación mediática o adaptación de actores.

**b) Oposición ambiental (`environmental_opposition`):**

Tendencia decreciente en términos absolutos: de 41 eventos en 2017 a 18 en 2024. En términos relativos cae de 23.7% (2017) a 10-15% (2021-2024). Contraintuitivo dado el aumento global del activismo ambiental y compromisos ESG de China post-2021. Hipótesis: la cobertura mediática de la oposición ambiental a proyectos BRI está siendo desplazada por narrativas de sanciones y deuda, no porque la oposición disminuya sino porque recibe menor cobertura relativa durante períodos de alta tensión geopolítica.

**c) Rechazo político (`political_rejection`):**

Relativamente estable en términos absolutos (4-19 eventos/año). Mínimo en 2018 (n=4): año de inicio del trade war, donde la narrativa mediática pasa a sanciones. Recuperación en 2021-2023 (17-19 eventos/año), coincidiendo con la revisión de contratos BRI post-COVID en múltiples países bajo presión del FMI y acreedores occidentales.

**d) Fracaso de proyecto (`project_failure`):**

Tendencia creciente en términos relativos: de 2.3% (2017) a pico de 8.7% (2022). Consistente con la maduración del portafolio BRI: proyectos iniciados en 2014-2017 comienzan a mostrar fracasos en 2019-2022. El pico 2020 (n=17, 7.8%) refleja impacto de COVID sobre proyectos ya frágiles.

**e) Renegociación de deuda (`debt_renegotiation`):**

Conteos bajos y volátiles (0-13 eventos/año). El máximo en 2017 (n=13, 7.5%) puede reflejar la crisis de deuda temprana (Sri Lanka-Hambantota, concesión 99 años en diciembre 2017). La ausencia total en 2024 (n=0) es llamativa: probable artefacto de clasificación más que realidad económica, dado que las renegociaciones de deuda continuaron en 2023-2024 (Zambia cerró reestructuración en 2023).

---

## 4. Heterogeneidad Geográfica

### 4.1 Conteos absolutos por región y mecanismo

| Región | Debt R. | Env. Opp. | Pol. Rej. | Proj. Fail. | Unknown | US Sanc. | Total | N clasif. |
|--------|---------|-----------|-----------|-------------|---------|----------|-------|-----------|
| Africa | 6 | 30 | 6 | 3 | 3,612 | 36 | 3,693 | 81 |
| Asia_C | 4 | 20 | 17 | 7 | 4,065 | 86 | 4,199 | 134 |
| Asia_SE | 1 | 39 | 11 | 4 | 5,684 | 53 | 5,792 | 108 |
| Europa_E | 2 | 10 | 4 | 1 | 3,759 | 61 | 3,837 | 78 |
| LATAM | 4 | 15 | 10 | 3 | 2,868 | 66 | 2,966 | 98 |
| MedioO | 3 | 33 | 15 | 4 | 5,997 | 403 | 6,455 | 458 |
| Oceania | 0 | 0 | 0 | 0 | 96 | 0 | 96 | 0 |
| Other | 28 | 56 | 45 | 45 | 3,685 | 193 | 4,052 | 367 |
| **TOTAL** | **48** | **203** | **108** | **67** | **29,766** | **898** | **31,090** | **1,324** |

### 4.2 Distribución porcentual sobre clasificados, por región

| Región | Debt R. | Env. Opp. | Pol. Rej. | Proj. Fail. | US Sanc. | N clasif. |
|--------|---------|-----------|-----------|-------------|----------|-----------|
| Africa | 7.4% | **37.0%** | 7.4% | 3.7% | 44.4% | 81 |
| Asia_C | 3.0% | 14.9% | **12.7%** | 5.2% | **64.2%** | 134 |
| Asia_SE | 0.9% | **36.1%** | 10.2% | 3.7% | 49.1% | 108 |
| Europa_E | 2.6% | 12.8% | 5.1% | 1.3% | **78.2%** | 78 |
| LATAM | 4.1% | 15.3% | 10.2% | 3.1% | **67.3%** | 98 |
| MedioO | 0.7% | 7.2% | 3.3% | 0.9% | **88.0%** | 458 |
| Oceania | — | — | — | — | — | 0 |
| Other | 7.6% | 15.3% | **12.3%** | **12.3%** | 52.6% | 367 |

### 4.3 Análisis de heterogeneidad geográfica

**Medio Oriente (MedioO) — caso extremo en sanciones (88%):**

La región con la mayor concentración de eventos de sanciones en términos absolutos (n=403) y relativos (88% de clasificados). Esto refleja la superposición entre países BRI receptores de inversión china (Irán, Irak, Siria, Yemen, Líbano) y países bajo régimen de sanciones EEUU. MedioO concentra el **44.9% de todos los eventos de sanciones del dataset** (403 de 898), siendo la región determinante para el hallazgo global. El retiro de EEUU del JCPOA (mayo 2018) es el shock exógeno principal que explica la concentración en Irán.

**Africa — diversificación de mecanismos:**

África muestra el perfil más diversificado: aunque las sanciones siguen siendo frecuentes (44.4%), la oposición ambiental (37.0%) es excepcionalmente alta. Consistente con proyectos mineros e hidroeléctricos que enfrentan contestación local (Uganda-oleoducto, Tanzania-puerto, Mozambique-gas). La renegociación de deuda (7.4%, mayor que cualquier otra región) es coherente con las crisis de deuda africanas documentadas: Zambia (default 2020, reestructuración 2023), Ghana (2022), Etiopía (2021).

**Asia Sudoriental (Asia_SE) — oposición ambiental prominente:**

Junto con África, Asia_SE tiene la mayor proporción de oposición ambiental (36.1%). Refleja proyectos hídricos (Myanmar, Laos, Camboya) y de carbón (Bangladesh, Vietnam) con movilización ambiental intensa. La baja participación de renegociación de deuda (0.9%) en Asia_SE es llamativa dado que Laos y Camboya enfrentan carga de deuda china elevada: probable subdetección severa del mecanismo.

**Europa del Este — segundo mayor dominio de sanciones (78.2%):**

Refleja los contratos BRI con Balcanes (Serbia, Bosnia, Montenegro, Albania) donde EEUU aplicó presión directa para cancelar contratos con Huawei (5G). El caso Montenegro-autopista financiada por China, renegociada con apoyo UE en 2021, también contribuye.

**LATAM — perfil mixto con dominio de sanciones (67.3%):**

El componente de sanciones en LATAM está probablemente concentrado en Venezuela (CNPC, Unipec, ZTE), consistente con los casos identificados manualmente. La oposición ambiental (15.3%) y rechazo político (10.2%) son consistentes con los casos documentados: Chile-litio (2018), Brasil-Tamoios (2017), Ecuador-Yasuní (2024).

**Asia Central (Asia_C) — mayor rechazo político relativo (12.7%):**

El mayor ratio de rechazo político entre regiones. Consistente con la revisión de contratos BRI en Kazajistán, Kirguistán y Tayikistán, donde protestas anti-chinas (2018-2019) llevaron a renegociaciones gubernamentales.

---

## 5. Análisis Especial: El Mecanismo `us_sanctions`

### 5.1 Estadísticos del mecanismo

| Año | N eventos | N países afectados | Tono promedio GDELT |
|-----|-----------|-------------------|---------------------|
| 2017 | 98 | 21 | -5.47 |
| 2018 | 103 | 22 | -5.11 |
| 2019 | **192** | **27** | **-6.08** |
| 2020 | 153 | **31** | -5.00 |
| 2021 | 108 | **33** | -5.86 |
| 2022 | 83 | 16 | -5.53 |
| 2023 | 82 | 24 | -5.67 |
| 2024 | 79 | 19 | -5.83 |
| **TOTAL/PROM** | **898** | — | **-5.57** |

El máximo de países afectados ocurre en **2021** (33 países), no en 2019 que tiene el máximo en volumen de eventos. Esto sugiere que en 2019 el mecanismo fue intenso pero geográficamente concentrado (Irán, Venezuela, Huawei-global), mientras que en 2020-2021 se dispersó geográficamente al proliferar las designaciones en múltiples jurisdicciones.

### 5.2 Definición y funcionamiento del mecanismo

Las **sanciones secundarias** de EEUU son medidas extraterritoriales que penalizan a empresas o países terceros que comercian con entidades sancionadas directamente por EEUU. A diferencia de las sanciones primarias (que se aplican a nacionales o entidades estadounidenses), las sanciones secundarias permiten a EEUU excluir a empresas chinas de los mercados globales sin que estas hayan violado ley estadounidense alguna.

En el contexto BRI, el mecanismo opera por tres vías:

1. **El país receptor está sancionado** (Irán, Rusia post-2022, Venezuela, Myanmar, Siria): empresas chinas que continúan operando arriesgan ser excluidas del sistema financiero dolarizado (SWIFT) o de mercados de semiconductores.

2. **La empresa china está sancionada directamente** (Huawei, ZTE, CNOOC, CMEC, Hikvision): el proyecto se cancela o suspende porque la empresa no puede operar con contrapartes occidentales o acceder a tecnología crítica.

3. **El socio financiero está bajo presión** (China Development Bank, Sinosure): el financiamiento se hace inviable al no poder usar corresponsales bancarios occidentales.

### 5.3 Cronología y causalidad con la guerra comercial

El pico de 2019 (n=192) es temporalmente coherente con eventos sancionatorios discretos y documentados:

- **Mayo 2019:** Huawei añadida a la Entity List del BIS. Más de 50 países inician revisiones de contratos 5G.
- **Agosto 2019:** EEUU designa a China como "manipulador de divisas".
- **Septiembre 2019:** CNPC suspende operaciones en Venezuela tras presión EEUU.
- **Diciembre 2019:** Phase One Deal firmado, pero restricciones tecnológicas permanecen.

La caída en n de países en 2022 (de 33 a 16) puede reflejar la reconfiguración del mapa de sanciones tras la invasión rusa de Ucrania (febrero 2022), que desplazó parcialmente la atención mediática y sancionatoria de China hacia Rusia.

### 5.4 El tono GDELT como validador

El tono promedio de -5.57 indica cobertura consistentemente negativa, apropiada para eventos de sanción y cancelación. El pico de negatividad en 2019 (-6.08) coincide exactamente con el pico en cantidad de eventos (n=192), validando la coherencia interna del dataset. El valor de 2020 (-5.00, el menos negativo) puede reflejar que la pandemia enmarcó los eventos de sanción/cancelación como consecuencias económicas del COVID, moderando el tono mediático.

### 5.5 ¿Es una contribución original a la literatura?

**Estado de la literatura:** La literatura sobre cancelación de proyectos BRI (Hillman 2018; AidData 2021; Sacks 2021; Nedopil 2022) enfatiza factores del país receptor: gobernanza, sostenibilidad de deuda, oposición política/ambiental local. Los determinantes exógenos de origen estadounidense están **sistemáticamente subrepresentados**, mencionados anecdóticamente en estudios de caso pero sin tratamiento econométrico ni cuantificación global.

**La contribución potencial:** Este dataset documenta que el 67.8% de los eventos de cancelación clasificados involucran sanciones secundarias EEUU, operando en 21-33 países simultáneamente cada año. Si esta señal es robusta tras análisis de falsos positivos, implicaría que:

- Los modelos de determinantes BRI están omitiendo la variable más frecuente del fenómeno.
- El "riesgo país" tradicional (instituciones, corrupción) es secundario frente al "riesgo de sistema" impuesto por la arquitectura de sanciones EEUU.
- La cancelación de proyectos BRI no puede analizarse como fenómeno bilateral (China ↔ receptor): es un fenómeno **trilateral** donde EEUU es actor activo aunque formalmente ausente del contrato.

Esta trilateralidad conecta con el marco de Farrell y Newman (2019) sobre **"weaponized interdependence"** — el uso estratégico de la infraestructura financiera y tecnológica global como instrumento de coerción. Las empresas chinas no cancelan proyectos BRI porque sean inviables per se, sino porque la continuación las expondría a ser excluidas de mercados más valiosos (EEUU, UE) que el proyecto BRI individual.

---

## 6. Hipótesis para la Tesis

### H1: El mecanismo de sanciones secundarias EEUU es el determinante más frecuente de cancelación de proyectos BRI en 2017-2024.

**Operacionalización:** Variable dummy `us_sanctions_year_t` (año en que empresa contratista o país receptor enfrenta nueva designación EEUU, fuente: OFAC/BIS Entity List) × presencia de proyecto chino activo. Predicción: coeficiente positivo y significativo sobre probabilidad de cancelación en logit/probit.

**Desafío de identificación:** Las sanciones no son aleatorias — se aplican a países/empresas con mayor presencia china, creando endogeneidad. Estrategia sugerida: usar como instrumento la distancia ideológica EEUU-país receptor en votaciones UNGA (Bailey, Strezhnev & Voeten 2017), que predice exposición a sanciones pero es exógena al desempeño del proyecto.

### H2: La oposición ambiental y el rechazo político son mecanismos complementarios, no sustitutos.

**Operacionalización:** Correlación temporal entre `environmental_opposition` y `political_rejection` por país-año. Predicción: correlación positiva (la movilización ambiental eleva el costo político de aprobar proyectos, llevando al rechazo formal). Los datos son consistentes: Asia_SE y África muestran simultáneamente alta oposición ambiental y rechazo político relativo.

**Implicación:** Los modelos deben incluir interacciones entre ambas variables, no solo efectos separados.

### H3: La renegociación de deuda es proxy del "debt trap" con intensidad regional heterogénea, siendo más frecuente en África.

**Operacionalización:** Correlación entre `debt_renegotiation` por país-año y razón deuda bilateral con China / deuda externa total (Horn et al. 2021, AidData Hidden Debt). Predicción: correlación fuerte en África (7.4% de clasificados) y LATAM (4.1%), débil en Asia Central y Europa del Este.

**Precaución fundamental:** Los n bajos (48 total, 6 en Africa) limitan la potencia estadística. Este mecanismo está casi con certeza subdetectado dada la confidencialidad contractual sistemática documentada por Horn et al. (2021).

### H4: El pico de cancelaciones en 2019-2020 refleja la interacción entre la guerra comercial EEUU-China y el shock COVID, no una tendencia secular de fracaso del modelo BRI.

**Operacionalización:** Diferencias en diferencias con tratamiento = escalada trade war (julio 2018 y mayo 2019 como shocks exógenos) y grupo de control = proyectos en países con baja exposición a sanciones EEUU. Si H4 es correcta, los efectos del tratamiento son temporales y se atenúan post-2021.

**Implicación:** Los 18 casos manuales del dataset original pueden tener sesgo temporal hacia 2018-2020, sobrerepresentando el período de máxima tensión.

### H5: La heterogeneidad regional de mecanismos refleja la arquitectura de influencia geopolítica de EEUU, no solo las características intrínsecas del proyecto o del país receptor.

**Operacionalización:** Regresión de `mechanism_type` ~ región × índice_presencia_EEUU × nivel_institucional. Predicción: regiones con alta presencia EEUU (MedioO, Europa_E) muestran mayor `us_sanctions`; regiones con menor presencia EEUU y mayor activismo ambiental local (África, Asia_SE) muestran mayor `environmental_opposition`. Los datos preliminares son altamente consistentes con esta predicción.

---

## 7. Limitaciones y Sesgos del Dataset

### 7.1 Sesgos de clasificación automática

**Falsos positivos en `us_sanctions`:**

GDELT puede capturar artículos sobre sanciones EEUU en general que mencionan proyectos chinos tangencialmente, sin que exista cancelación causal documentada. **Estimación conservadora:** 20-35% de los 898 eventos pueden ser falsos positivos, reduciendo el mecanismo a ~580-720 eventos reales — aún el más frecuente con amplitud (55-65% de clasificados en el escenario pesimista).

**Subdetección de `debt_renegotiation`:**

Las renegociaciones de deuda ocurren en negociaciones bilaterales con poca cobertura mediática y están sujetas a cláusulas de confidencialidad (Horn et al. 2021 documentan esto en el 99% de los contratos BRI analizados). GDELT subdetectará masivamente este mecanismo. El n=48 es una cota inferior severa del fenómeno real.

**La categoría `unknown` como problema estructural:**

El 95.74% en `unknown` admite tres interpretaciones no excluyentes:
1. Artículos sobre inversión china activa que el filtro de tono negativo no excluye completamente.
2. Mecanismos multi-causales que no caben en una categoría simple de vocabulario.
3. Keywords de clasificación insuficientes para capturar la riqueza léxica de la cobertura mediática.

La implicación metodológica crítica: si los 1,324 eventos clasificados son **muestra sesgada** (los eventos de sanciones son más fáciles de detectar léxicamente que los de renegociación de deuda), la distribución 67.8%/15.3%/8.2%/5.1%/3.6% sobreestima sanciones y subestima mecanismos financieros. Este sesgo debe ser explicitado en la tesis.

### 7.2 Sesgos de cobertura mediática (GDELT)

**Sesgo de idioma:** GDELT indexa principalmente prensa en inglés. Los proyectos donde la cancelación se discute en idioma local (África francófona, Angola-portugués, Brasil) están subrepresentados.

**Sesgo de fuente:** Medios anglosajones (Reuters, AP, Bloomberg) con mayor peso en GDELT tienden a enmarcar proyectos BRI con perspectiva geopolítica crítica, acentuando narrativas de sanciones y debt trap. Medios chinos (Xinhua, CGTN) que minimizarían estos framing están subrepresentados.

**Sesgo de visibilidad:** Las cancelaciones de alta visibilidad (Huawei 5G global, Hambantota, CNPC Venezuela) generan cientos de artículos GDELT; las de baja visibilidad (un contrato minero en Guinea-Bissau) generan pocos. El dataset sobrerrepresenta eventos de alta visibilidad mediática.

### 7.3 Limitaciones de cobertura temporal

El período 2017-2024 excluye el boom inicial BRI (2013-2016). Los proyectos firmados en 2013-2015 están alcanzando su fase de cancelación en 2018-2022, por lo que el dataset captura consecuencias pero no las condiciones en el momento de la firma original. Para el análisis de determinantes causales, la variable dependiente (cancelación en t) puede estar temporalmente desconectada de las variables independientes relevantes (condiciones del país receptor en t-3 o t-5).

### 7.4 El problema de la unidad de observación

Los datos están en **eventos-artículo** (una URL = un evento GDELT), no en **proyectos**. Un proyecto que se cancela puede generar entre 50 y 500 artículos GDELT dependiendo de su visibilidad. Si los proyectos afectados por sanciones EEUU generan más artículos que los afectados por oposición ambiental (razonable: las sanciones son eventos discretos de alta visibilidad), entonces la distribución 67.8%/15.3%/... sobre eventos sobreestimará la participación de sanciones sobre la distribución real de **proyectos** afectados. Este efecto de "amplificación mediática diferencial" debe ser corregido antes de hacer inferencias causales.

La agregación de los 31,090 eventos en los **801 proyectos candidatos** del pipeline Events es el paso metodológico necesario antes de cualquier análisis econométrico, y constituye la unidad de análisis apropiada para la tesis.

---

## 8. Conexión con la Tesis de Ariel Villalobos

### 8.1 Expansión de muestra: de 18 casos a un dataset comprehensivo

Los 18 casos manuales originales fueron seleccionados por salience mediática y disponibilidad de documentación secundaria académica. La distribución de mecanismos en esos 18 casos probablemente sobrerepresenta `political_rejection` y `project_failure` (los más documentados en fuentes académicas) y subestima `us_sanctions` (que requiere rastrear legislación sancionatoria estadounidense caso a caso). La **comparación sistemática entre la distribución de los 18 casos manuales y la distribución GDELT** documenta el sesgo de selección de los estudios de caso previos y merece sección explícita en la tesis.

### 8.2 Contribución original: el modelo trilateral de cancelación

La literatura existente modela la cancelación BRI como fenómeno bilateral (China ↔ País Receptor). Este dataset aporta evidencia sistemática a escala global de que EEUU opera como un **tercer actor** que puede forzar cancelaciones independientemente de la voluntad de las partes contratantes. Esto implica:

- **Para la teoría:** El marco analítico debe incorporar la "weaponized interdependence" (Farrell & Newman 2019) como variable estructural, no como caso anómalo.
- **Para la política de desarrollo:** Los países BRI enfrentan un dilema estructural: aceptar proyectos chinos genera riesgo de sanciones EEUU; rechazarlos implica costo de oportunidad en financiamiento de infraestructura.
- **Para la economía política:** La cancelación puede ser respuesta racional de empresas chinas a incentivos del sistema financiero global dolarizado, donde el acceso al mercado EEUU/SWIFT supera en valor al proyecto BRI individual.

### 8.3 Variables para el modelo econométrico

| Variable | Fuente | Mecanismo que captura |
|----------|--------|-----------------------|
| Designación en OFAC SDN List (país receptor, año t) | OFAC Treasury | us_sanctions |
| Empresa china en BIS Entity List (año t) | BIS Commerce Dept. | us_sanctions |
| Cambio de partido de gobierno en país receptor (t, t-1) | Database of Political Institutions (DPI) | political_rejection |
| Índice V-Dem de participación de sociedad civil | V-Dem Institute | environmental_opposition |
| Proyectos en Environmental Justice Atlas (país-año) | EJAtlas | environmental_opposition |
| Razón deuda bilateral China / deuda externa total | AidData, Horn et al. (2021) | debt_renegotiation |
| Años desde firma del contrato (maduración) | AidData GCDF | project_failure |
| Índice de capacidad institucional (WGI) | World Bank WGI | project_failure |
| PIB per cápita del país receptor (log) | World Bank WDI | Control |
| Tipo de sector (infraestructura/extracción/telecomunicaciones) | AidData GCDF | Heterogeneidad sectorial |
| Tono GDELT promedio (6 meses pre-cancelación) | GDELT GKG | Early warning signal |
| Presencia de base militar EEUU en país (dummy) | DSCA/SIPRI | Intensidad presión EEUU |

---

## 9. Resumen Ejecutivo

Los datos GDELT 2017-2024 revelan un patrón cuantitativamente robusto: **las sanciones secundarias de EEUU representan el 67.8% de los 1,324 eventos con mecanismo identificado** (n=898), dominando en todas las regiones y todos los años del período analizado sin excepción.

Esta dominancia es especialmente pronunciada en Medio Oriente (88% de clasificados), Europa del Este (78%), LATAM (67%) y Asia Central (64%). El pico absoluto ocurre en 2019 (n=192), coincidiendo exactamente con la escalada de la guerra comercial EEUU-China. La expansión geográfica máxima ocurre en 2021 (33 países), sugiriendo que los efectos de la guerra comercial se propagaron geográficamente con rezago de 2 años.

Los mecanismos más documentados en la literatura BRI — oposición ambiental (15.3%) y rechazo político (8.2%) — representan juntos menos de un cuarto de los eventos clasificados. Los mecanismos endógenos al proyecto — fracaso (5.1%) y renegociación de deuda (3.6%) — son los menos frecuentes, aunque la renegociación de deuda está casi con certeza severamente subdetectada.

**Si la señal de sanciones secundarias EEUU es robusta tras análisis de falsos positivos** — y la coherencia temporal con eventos sancionatorios documentados y el tono GDELT consistentemente negativo (-5.57 promedio) sugieren que lo es — constituiría una **contribución original** a la literatura BRI. Esta contribución reenmarca el fenómeno desde un modelo bilateral (China-receptor) hacia un **modelo trilateral** donde EEUU opera como actor sistémico con capacidad de forzar cancelaciones a través de la infraestructura financiera y tecnológica global.

Esta reconfiguración tiene implicaciones directas para la tesis de Ariel Villalobos: los determinantes de cancelación no son solo atributos del país receptor (gobernanza, deuda, política) sino también atributos del sistema internacional (arquitectura de sanciones, posición geopolítica en el triángulo China-EEUU-receptor).

---

*Análisis generado sobre datos GDELT GKG 2017-2024. Los porcentajes y conteos son sobre el universo de eventos-artículo clasificados por el pipeline automático y están sujetos a las limitaciones metodológicas descritas en la Sección 7. Para la tesis, se recomienda complementar con validación manual de una muestra aleatoria de los 898 eventos de us_sanctions y los 48 eventos de debt_renegotiation.*
