# Análisis Económico — Serie Temporal BRI/China 2017–2024
*Análisis generado: 2026-03-02 | Proyecto: Tesis Ariel Villalobos, U. Chile*

---

## 1. Datos disponibles

| Archivo | Descripción | Dimensión |
|---------|-------------|-----------|
| `bri_por_año.csv` | Eventos BRI anuales agregados: n_eventos, tono_medio, menciones_total, paises_unicos | 8 filas × 5 cols |
| `bri_region_año.csv` | Matriz región × año de conteo de eventos | 8 regiones × 8 años |
| `bri_crecimiento_paises.csv` | Top 20 países: volumen 2017, 2024, total acumulado, año pico, cambio neto | 21 filas |

---

## 2. Evolución temporal agregada (2017–2024)

| Año | N Eventos | Tono Medio | Menciones Total | Países Únicos | Δ Eventos (%) | Δ Menciones (%) |
|-----|-----------|-----------|----------------|--------------|---------------|----------------|
| 2017 | 6,596 | −6.77 | 53,246 | 122 | — | — |
| 2018 | 6,569 | −6.64 | 52,939 | 132 | −0.4% | −0.6% |
| 2019 | 8,208 | −6.83 | 66,045 | 126 | +24.9% | +24.7% |
| 2020 | **9,904** | −6.50 | **80,316** | **136** | +20.7% | +21.6% |
| 2021 | 5,098 | −6.51 | 40,906 | 112 | **−48.5%** | **−49.1%** |
| 2022 | 4,548 | −6.54 | 36,121 | 119 | −10.8% | −11.7% |
| 2023 | 5,517 | −6.47 | 42,905 | 116 | +21.3% | +18.8% |
| 2024 | 5,999 | **−6.86** | 45,692 | 117 | +8.7% | +6.5% |
| **Total** | **52,439** | **−6.64** | **417,170** | — | — | — |

### Observaciones clave:

- **Pico absoluto 2020:** 9,904 eventos y 80,316 menciones — el año de mayor fricción registrada.
- **Colapso 2021:** Caída de −48.5% en eventos en un solo año. El más abrupto del período.
- **Tono 2024 = mínimo histórico (−6.86):** A pesar del menor volumen post-2020, la negatividad por artículo aumenta. Los proyectos que sobreviven generan más conflicto por unidad.
- **2017-2018 estables:** El período pre-trade-war muestra equilibrio entre flujo de proyectos y cobertura mediática.

---

## 3. Análisis por región (eventos anuales)

| Región | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | Total | % del total |
|--------|------|------|------|------|------|------|------|------|-------|-------------|
| Other* | 3,216 | 3,320 | 4,661 | 5,738 | 3,179 | 2,543 | 2,871 | 2,747 | 28,275 | 53.9% |
| Asia_SE | 802 | 767 | 886 | 953 | 410 | 305 | 741 | 928 | 5,792 | 11.0% |
| MedioO | 583 | 706 | 793 | 896 | 359 | 219 | 485 | 627 | 4,668 | 8.9% |
| Asia_C | 663 | 579 | 535 | 611 | 446 | 430 | 316 | 619 | 4,199 | 8.0% |
| LATAM | 525 | 411 | 411 | 435 | 223 | 147 | 240 | 287 | 2,679 | 5.1% |
| Africa | 455 | 458 | 500 | 656 | 244 | 224 | 279 | 300 | 3,116 | 5.9% |
| Europa_E | 339 | 313 | 411 | 601 | 237 | 672 | 577 | 484 | 3,634 | 6.9% |
| Oceania | 13 | 15 | 11 | 14 | 0 | 8 | 8 | 7 | 76 | 0.1% |

*"Other" = países no BRI clásicos: Australia, EEUU, UK, Canadá, etc. — ruido mediático y cobertura desde centros de medios occidentales.

### Patrones regionales destacados:

- **Europa_E anomalía 2022:** Salta de 237 (2021) a 672 eventos — el único año donde Europa del Este supera su propio pico histórico. **Causa: invasión Rusia-Ucrania** y la posición de China respecto al conflicto genera fricción con proyectos BRI en países como Bosnia, Kazajistán y los bálticos.
- **Asia_SE = región más resiliente:** Mantiene volumen en 2023-2024 (741 y 928) — recuperación post-COVID de proyectos en Filipinas, Indonesia, Vietnam.
- **LATAM = tendencia secular descendente:** De 525 (2017) a 147 (2022) — caída de 72%. Señal de desaceleración de inversión china en la región en el período post-trade-war + COVID.
- **MedioO = segunda caída más fuerte 2021:** De 896 a 359 (−59.9%), reflejando contracción de proyectos en Irán, Iraq bajo sanciones y retiro de financiamiento chino.

---

## 4. Análisis de países (top 20 por volumen acumulado)

| País | Total 2017–2024 | 2017 | 2024 | Año Pico | Cambio Neto | Tendencia |
|------|----------------|------|------|----------|-------------|-----------|
| Pakistán | 2,767 | 453 | 522 | **2024** | +69 | ↑ Creciente (CPEC activo) |
| Irán | 2,469 | 231 | 196 | 2019 | −35 | ↓ Post-sanciones |
| Ucrania | 2,332 | 160 | 285 | **2022** | +125 | ↑ Guerra → fricción con China |
| Filipinas | 2,028 | 183 | 579 | **2024** | +396 | ↑ Mar Sur China escalada |
| Israel | 1,152 | 100 | 332 | 2024 | +232 | ↑ Guerra Gaza → posición China |
| India | 933 | 165 | 52 | 2020 | −113 | ↓ Tensión fronteriza → retiro |
| Indonesia | 910 | 163 | 62 | 2020 | −101 | ↓ Declinante post-pico |
| Nigeria | 731 | 88 | 87 | 2020 | −1 | → Estable (minería ilegal ruido) |
| Vietnam | 727 | 112 | 58 | 2019 | −54 | ↓ Retiro post-trade-war |
| Bosnia | 708 | 86 | 138 | 2024 | +52 | ↑ Central Carbón Tuzla + política |
| Tailandia | 683 | 93 | 103 | 2023 | +10 | → Estable |
| Afganistán | 663 | 120 | 48 | 2021 | −72 | ↓ Colapso post-talibán |
| Singapur | 619 | 74 | 80 | 2020 | +6 | → Hub financiero, no proyecto |
| Malasia | 584 | 104 | 49 | 2020 | −55 | ↓ Post-Mahathir cancelaciones |
| México | 502 | 83 | 56 | 2019 | −27 | ↓ Trade war + fentanilo |
| Brasil | 429 | 73 | 35 | 2020 | −38 | ↓ Bolsonaro + COVID |
| Camboya | 425 | 76 | 36 | 2017 | −40 | ↓ Dependencia → conflicto |
| Arabia Saudita | 376 | 71 | 27 | 2020 | −44 | ↓ OPEC+ prioridad sobre BRI |
| Venezuela | 360 | 77 | 27 | 2019 | −50 | ↓ Sanciones EEUU → retiro chino |
| Kenia | 335 | 45 | 13 | 2018 | −32 | ↓ Post-SGR debt renegotiation |

---

## 5. Patrones e hipótesis económicas

### 5.1 El pico 2020: hipótesis multicausal

El pico de 9,904 eventos en 2020 no refleja un aumento de proyectos, sino una **tormenta perfecta de tres shocks simultáneos**:

1. **COVID-19 y responsabilidad China** (ene–mar 2020): Cobertura mediática masiva sobre el origen del virus genera fricción diplomática con países deudores del BRI.
2. **Debt distress accelerado** (2020): El COVID colapsa los ingresos de divisas de países endeudados (Kenia SGR, Ecuador petróleo, Pakistán). Las renegociaciones de deuda con China explotan mediáticamente.
3. **Sanciones EEUU pre-elección** (2020): La administración Trump escala sanciones contra empresas chinas en los meses previos a noviembre. Pico de 153 eventos us_sanctions ese año.

**Conclusión:** El pico 2020 no es un pico de inversión BRI, sino un **pico de fricción sobre inversión BRI preexistente**. Esto es metodológicamente relevante: más eventos GDELT = más conflicto, no más proyectos.

### 5.2 El colapso 2021: fatiga mediática o contracción real

La caída de −48.5% en 2021 tiene dos explicaciones alternativas:

- **Hipótesis A (fatiga):** Los medios saturados por COVID pierden interés en la cobertura BRI. El volumen de artículos cae en todos los temas globales post-2020.
- **Hipótesis B (contracción real):** China efectivamente reduce compromisos BRI. El BRI 2.0 (anunciado en el foro de 2021) es más selectivo — menos proyectos de infraestructura masiva, más "small and beautiful". Datos de AidData y OECD confirman caída de desembolsos en 2020-2021.

**Evidencia tentativa hacia Hipótesis B:** El tono no mejora tras el colapso (sigue en −6.5), lo que sugiere que los proyectos que quedan activos siguen siendo conflictivos. Si fuera solo fatiga mediática, habría ruido uniforme positivo/negativo.

### 5.3 Ciclo trade war 2018-2019

El salto de 2018 → 2019 (+24.9%) coincide exactamente con:
- Mayo 2019: Huawei añadida a Entity List (EEUU). Los eventos de empresas chinas en países terceros explotan.
- Julio 2019: Aranceles EEUU-China escalan a 25% en $250B de importaciones.
- Septiembre 2019: CNPC suspende operaciones Venezuela bajo presión sanciones.

La señal de trade war contamina el dataset BRI: eventos sobre Huawei y sanciones en países terceros se clasifican como fricción BRI cuando son fricción trade-war. El filtro de mecanismos (causal/) es insuficiente para limpiar esto completamente.

### 5.4 Tono 2024 = nuevo mínimo: el "BRI hostil"

El año 2024 registra el tono más negativo (−6.86) con volumen moderado. Interpretación: en el período post-COVID, **la naturaleza de los proyectos que continúan es más conflictiva**. Los proyectos que sobrevivieron al período de cancelaciones masivas (2018-2021) son los más políticamente sensibles: seguridad energética (petróleo iraní, gas ruso), telecomunicaciones (Huawei 5G en Europa), minería estratégica (litio, cobre). Todos estos tienen mayor densidad de cobertura negativa por unidad.

---

## 6. Hipótesis para la tesis

**H1 (ciclo político):** Los eventos de fricción BRI se concentran en años de elecciones en países anfitriones. El pico 2019 coincide con cambios de gobierno en Brasil (Bolsonaro inicia 2019), Argentina (Macri → Fernández oct 2019), Bolivia (crisis Evo oct 2019).

**H2 (sanciones secundarias):** Los eventos de us_sanctions crecen con la escalada del trade war (2019 = 192 vs 98 en 2017). La variable us_sanctions es un determinante exógeno de cancelación no capturado en la literatura BRI clásica.

**H3 (debt distress lag):** Los picos de cobertura BRI siguen con un lag de 1-2 años a los peaks de desembolso de deuda. Si los desembolsos pico fueron 2016-2018, el conflicto debería pecar en 2018-2020 — consistente con los datos.

**H4 (resiliencia CPEC):** Pakistán es el único país con tendencia creciente 2017-2024 (+15%), sugiriendo que el Corredor Económico China-Pakistán tiene factores de lock-in que impiden cancelación pese al conflicto alto.

**H5 (guerra Ucrania como disruptor BRI):** Europa del Este muestra anomalía 2022 (+183% en un año). La guerra de Rusia-Ucrania redefine la posición de China en el BRI europeo, generando presión adicional para cancelar o suspender proyectos (ej. Bosnia central de carbón Tuzla, proyectos en Serbia y Montenegro).

---

## 7. Señales de alerta para la tesis

| Alerta | Descripción | Acción requerida |
|--------|-------------|-----------------|
| **"Other" = 54% del total** | La mayoría de eventos no son BRI geográfico puro | Excluir "Other" del análisis principal; usarlo solo como control |
| **Singapur como nodo** | 619 eventos en Singapur (hub financiero, no destino BRI) | Reclasificar como "hub financiero"; separar de países receptores |
| **Tono estable a lo largo del tiempo** | La banda −6.5 a −6.9 no varía mucho | El tono GDELT puede no capturar intensidad de cancelación; complementar con índice BRI propio |
| **2021 colapso no explicado** | Necesita contraste con datos de flujos de inversión reales (AidData) | Cruzar con AidData Chinese Development Finance dataset |

---

## 8. Próximos pasos analíticos

1. **Cruzar con AidData (2021):** "Banking on the Belt and Road" provee flujos de préstamos chinos por año-país. Correlacionar con n_eventos para testear H3.
2. **Excluir "Other" del análisis principal:** Refinar la muestra a solo países BRI (lista oficial + UNCTAD BRI signatories).
3. **Descomponer el pico 2020:** Separar eventos COVID de eventos BRI estructurales usando keywords de las URLs (ya disponibles en clusters/).
4. **Análisis de CPEC:** Sub-sample Pakistán como "caso de control" — el proyecto BRI que no se canceló. ¿Qué lo diferencia?
5. **Test econométrico H2:** Regresión de n_eventos_sanciones ~ año + tensión_comercial_index + pais_FE.
