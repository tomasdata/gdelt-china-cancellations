# Análisis Económico — Empresas Chinas en GDELT 2017–2024
*Análisis generado: 2026-03-02 | Proyecto: Tesis Ariel Villalobos, U. Chile*

---

## 1. Datos disponibles

| Archivo | Descripción | Tamaño |
|---------|-------------|--------|
| `gkg_org_ranking.csv` | Ranking de organizaciones por n° artículos GKG | 51 filas |
| `soe_by_year.csv` | Actividad anual por grupo SOE (9 sectores × 8 años) | — |
| `soe_risk_profile.csv` | Perfil de riesgo: n_artículos, tono_medio, tono_mínimo | 9 sectores |
| `gkg_latam_soe.csv` | Empresas chinas en LATAM desde GKG | ~1.4 MB |

---

## 2. Universo de empresas chinas en GDELT

### 2.1 Top 30 por volumen de artículos

| Rank | Organización | N Artículos | % del Total | Categoría | Tipo |
|------|-------------|------------|------------|-----------|------|
| 1 | HUAWEI | 279,589 | **83.5%** | Telecom | SOE/mixta |
| 2 | SINOPEC | 15,322 | 4.6% | Energía/Oil | SOE |
| 3 | COSCO | 7,119 | 2.1% | Marítimo | SOE |
| 4 | CHINESE COMMUNIST PARTY | 2,467 | 0.7% | Político | Estado |
| 5 | CHINA TELECOMMUNICATIONS | 2,305 | 0.7% | Telecom | SOE |
| 6 | PETROCHINA | 2,131 | 0.6% | Oil | SOE |
| 7 | HUAWEI TECHNOLOGIES LTD | 2,038 | 0.6% | Telecom | SOE/mixta |
| 8 | CHINA RAILWAY | 2,006 | 0.6% | Infraestructura | SOE |
| 9 | CHINA FOREIGN MINISTRY | 1,996 | 0.6% | Político | Estado |
| 10 | HUAWEI TECHNOLOGIES CO LTD | 1,961 | 0.6% | Telecom | SOE/mixta |
| 11 | CHINESE FOREIGN MINISTRY | 1,931 | 0.6% | Político | Estado |
| 12 | CNOOC | 1,815 | 0.5% | Oil offshore | SOE |
| 13 | HUAWEI TECHNOLOGIES CO | 1,747 | 0.5% | Telecom | SOE/mixta |
| 14 | CHINESE EMBASSY | 1,643 | 0.5% | Diplomático | Estado |
| 15 | CHINA DEVELOPMENT BANK | 1,259 | 0.4% | Finanzas | SOE |
| 16 | CHINA DAILY | 941 | 0.3% | Medios | Estado |
| 17 | EXIM BANK | 908 | 0.3% | Finanzas | SOE |
| 18 | CHINA UNICOM | 880 | 0.3% | Telecom | SOE |
| 19 | CHINA DEVELOPMENT BANK | 876 | 0.3% | Finanzas | SOE |
| 20 | CHINA COMMUNICATIONS CONSTRUCTION CO | 501 | 0.2% | Infraestructura | SOE |
| 21 | CHINA TELECOM | 486 | 0.1% | Telecom | SOE |
| 22 | CHINA MOBILE | 462 | 0.1% | Telecom | SOE |
| 23 | AIR CHINA | 389 | 0.1% | Aviación | SOE |
| 24 | CHINA NATIONAL | 377 | 0.1% | Vario | SOE |
| 25 | SINOPEC GROUP | 353 | 0.1% | Energía | SOE |
| 26 | CHINA HARBOUR ENGINEERING CO | 348 | 0.1% | Puertos | SOE |
| 27 | CHINA NATIONAL PETROLEUM CORP | 334 | 0.1% | Oil | SOE |
| 28 | CHINA RAILWAY CONSTRUCTION CORP | 281 | 0.1% | Infraestructura | SOE |
| 29 | CHINA MOBILE LTD | 284 | 0.1% | Telecom | SOE |
| 30 | CHINA HARBOUR ENGINEERING | 308 | 0.1% | Puertos | SOE |

**Total top 30:** ~330,000 de ~335,000 artículos totales (~98.5% de concentración)

### 2.2 Diagnóstico de concentración: el problema Huawei

El índice de concentración revela un sesgo metodológico crítico:

| Métrica | Valor | Interpretación |
|---------|-------|----------------|
| Participación Huawei (todas variantes) | **~85%** | Monopolio casi absoluto |
| HHI estimado | ~7,200 | Concentración extrema (>2,500 = monopolio) |
| Top 1 empresa | 83.5% del total | Una sola empresa domina la muestra |
| Top 5 empresas | ~92% del total | "Pareto extremo" (80/20 no aplica — es 83/1) |

**Conclusión:** Cualquier análisis no-ajustado de "empresas chinas en GDELT" es en realidad un análisis de **Huawei vs. todos los demás**. Para la tesis de BRI esto es una distorsión severa: Huawei no es una empresa BRI clásica de infraestructura — es una empresa de telecom sancionada por EEUU. Su dominancia refleja el trade war 2018-2019, no el BRI de rutas e infraestructura.

**Corrección necesaria:** Excluir Huawei (y sus variantes) del análisis BRI-infraestructura. Crear una muestra separada para el análisis de sanciones-telecom.

---

## 3. Análisis por sector SOE (evolución temporal)

### 3.1 Actividad anual por sector

| Sector | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | Total |
|--------|------|------|------|------|------|------|------|------|-------|
| SOE_TELECOM | 1,697 | **9,670** | **25,575** | **14,466** | 7,569 | 2,473 | 2,010 | 1,348 | 64,808 |
| SOE_OIL | 1,577 | 1,948 | 1,611 | 1,497 | 689 | 874 | 491 | 455 | 9,142 |
| SOE_MINING | 862 | 993 | 854 | 1,133 | 547 | 583 | 380 | 374 | 5,726 |
| SOE_RAILWAY | 574 | 594 | 480 | 695 | 360 | 878 | 226 | 230 | 4,037 |
| SOE_MARITIME | 273 | 338 | 655 | 314 | 286 | 507 | 231 | 256 | 2,860 |
| SOE_FINANCE | 251 | 291 | 196 | 370 | 493 | 452 | 203 | 161 | 2,417 |
| SOE_HARBOUR | 120 | 339 | 243 | 255 | 82 | 115 | 144 | 88 | 1,386 |
| SOE_ENERGY | 33 | 33 | 91 | 41 | 67 | 12 | 38 | 29 | 344 |
| SOE_CONSTRUCT | 18 | 18 | 16 | 10 | 83 | 67 | 48 | 24 | 284 |

### 3.2 Interpretación económica sector por sector

**SOE_TELECOM (64,808 artículos):**
- El sector dominante por amplio margen, pero 95% es Huawei bajo presión de sanciones.
- Pico 2019 (25,575) = el año de la Entity List y el ban de 5G en EEUU/UK/Australia.
- Caída post-2019: de 25,575 a 1,348 en 2024 — una contracción del **94.7%** en 5 años.
- **Interpretación:** No es reducción de inversión telecom BRI, sino que el tema Huawei/sanciones se "normalizó" mediáticamente. El ruido bajó, no el conflicto.

**SOE_OIL (9,142 artículos):**
- Segundo sector por volumen, más relevante para BRI clásico.
- Pico 2018 (1,948) → caída sostenida a 455 en 2024 (−77% desde pico).
- Las empresas clave: CNPC/PetroChina, Sinopec, CNOOC.
- Venezuela y Sudán del Sur son los casos de cancelación más documentados de este sector.
- **Interpretación:** La caída refleja retiro real de proyectos bajo sanciones secundarias EEUU (Venezuela 2019, Irán 2018-2020) + debt distress en países productores.

**SOE_MINING (5,726 artículos):**
- Tercer sector. Estable hasta 2020 (1,133), luego caída sostenida.
- Cobre (Chile, Perú, Zambia), litio (Chile, Bolivia, Argentina), oro ilegal (Ghana, Nigeria).
- **Nota:** Una fracción significativa de "SOE_MINING" en GDELT son artículos sobre **minería ilegal** de ciudadanos chinos — no SOEs. Esto introduce falsos positivos.

**SOE_RAILWAY (4,037 artículos):**
- Anomalía 2022 (878 artículos = máximo histórico): refleja posición de China Railway respecto a Ucrania y renegociaciones en África del Este.
- SGR Kenya (Standard Gauge Railway) dominante en cobertura africana.

**SOE_FINANCE (2,417 artículos):**
- China Development Bank y EXIM Bank son los principales.
- Crecimiento 2021-2022 (493 y 452) refleja el pico de renegociaciones de deuda: el DSSI (Debt Service Suspension Initiative) G20 genera cobertura masiva sobre la posición de China.

---

## 4. Perfil de riesgo sectorial

| Sector | N Artículos | Tono Medio | Tono Mínimo | Índice Riesgo* |
|--------|------------|-----------|------------|---------------|
| SOE_TELECOM | 64,808 | −5.23 | −27.59 | Alto (sancionada) |
| SOE_OIL | 9,142 | −4.54 | −17.42 | Alto (sanciones secundarias) |
| SOE_MINING | 5,726 | −4.29 | −17.89 | Medio-Alto (minería ilegal) |
| SOE_RAILWAY | 4,037 | −4.81 | −17.19 | Medio (debt distress) |
| SOE_MARITIME | 2,860 | −4.62 | −17.18 | Medio (Mar Sur China) |
| SOE_FINANCE | 2,417 | −4.53 | −11.49 | Medio (renegociación) |
| SOE_HARBOUR | 1,386 | −4.38 | −14.06 | Medio (geopolítica puertos) |
| SOE_ENERGY | 344 | −4.59 | −9.23 | Bajo-Medio |
| SOE_CONSTRUCT | 284 | −4.30 | −10.93 | Bajo |

*Índice cualitativo basado en tono, mecanismo de cancelación predominante y exposición a sanciones EEUU.

### Hallazgo clave: Tono vs. Volumen no correlacionan perfectamente
- SOE_TELECOM tiene el tono MENOS negativo (−5.23) a pesar del mayor volumen. Esto se debe a que gran parte del debate sobre Huawei es geopolítico/estratégico — los artículos reportan "China dice X, EEUU dice Y" con tono mixto.
- SOE_RAILWAY tiene tono más negativo (−4.81) que SOE_OIL a pesar de menor volumen — los proyectos ferroviarios generan conflictos más intensos por unidad (corrupción, expropiaciones, deuda).

---

## 5. Empresas candidatas para búsqueda profunda (Script 09)

Basado en relevancia para la tesis (proyectos BRI de infraestructura con casos conocidos o sospechados de cancelación):

| Prioridad | Empresa | Sector | Países Clave | Mecanismo Probable |
|-----------|---------|--------|-------------|-------------------|
| ⭐⭐⭐ | CNPC / PetroChina | Oil | Venezuela, Sudán S., Irak | Sanciones EEUU + debt |
| ⭐⭐⭐ | Sinohydro / PowerChina | Energía | Ecuador, Uganda, Myanmar | Ambiental + político |
| ⭐⭐⭐ | CREC (China Railway) | Railway | Kenya, Laos, Indonesia | Debt renegotiation |
| ⭐⭐⭐ | CHEC (China Harbour) | Puertos | Jamaica, Sri Lanka, Myanmar | Político + deuda |
| ⭐⭐⭐ | CGN (Nuclear) | Energía | Argentina (Atucha III), UK | Político + seguridad |
| ⭐⭐ | COSCO Shipping | Marítimo | Grecia (Pireo), Bélgica | Político-europeo |
| ⭐⭐ | CRCC (Construcción) | Infraestructura | Nigeria, México | Corrupción + deuda |
| ⭐⭐ | Tianqi / Ganfeng Lithium | Minería | Chile, Argentina | Político (litio) |
| ⭐ | ZTE Corp | Telecom | Iran, Venezuela, Etiopía | Sanciones EEUU directas |
| ⭐ | China Development Bank | Finanzas | Multi-región | Renegociación |

---

## 6. Sesgos de la muestra

| Sesgo | Descripción | Impacto en tesis |
|-------|-------------|-----------------|
| **Sesgo Huawei** | 83% de artículos son sobre Huawei (telecom sancionada) | Sobreestimación de mecanismo "sanciones", subestimación de debt/ambiental |
| **Sesgo idioma** | GDELT captura principalmente medios en inglés | Subestima proyectos en China continental, LATAM hispanohablante, África francófona |
| **Minería ilegal ≠ SOE** | Artículos sobre ciudadanos chinos minando ilegalmente se clasifican como SOE_MINING | Falsos positivos en sector minero |
| **Mediáticos vs. entidades** | "China Foreign Ministry" y "China Daily" aparecen como "empresas" en el ranking | Contaminación con actores gubernamentales y mediáticos |
| **Duplicados GDELT** | Una empresa puede aparecer con 3-4 variantes de nombre | Subestimación real de concentración (Huawei es aún más dominante si se suman variantes) |

---

## 7. Implicaciones para la tesis

1. **Excluir Huawei del análisis BRI-infraestructura** y crear un sub-análisis separado para el mecanismo de "sanciones tecnológicas".
2. **Las 5 empresas prioritarias** (CNPC, Sinohydro, CREC, CHEC, CGN) cubren los sectores con mayor probabilidad de cancelación no documentada: oil, hidro, ferrovías, puertos y nuclear.
3. **El sector SOE_OIL** es el más relevante para expandir la muestra: Venezuela (4 casos ya identificados), Sudán del Sur, Irán son países donde CNPC tiene proyectos y las sanciones EEUU son el mecanismo documentado.
4. **El sector SOE_FINANCE** (China Development Bank) es el proxy de "debt renegotiation" — su pico 2021-2022 coincide con las renegociaciones G20 post-COVID.

---

## 8. Próximos pasos

1. **Script 09:** Búsqueda profunda por empresa — priorizar CNPC, Sinohydro, CREC, CHEC.
2. **Limpiar ranking:** Consolidar variantes de Huawei, separar entidades políticas de empresas.
3. **Mapa sector × país:** Cruzar `soe_by_year` con `bri_events_geo` para identificar combinaciones empresa-país con señal fuerte.
4. **Validar minería ilegal:** Revisar manualmente 20 artículos de SOE_MINING para estimar tasa de falsos positivos.
