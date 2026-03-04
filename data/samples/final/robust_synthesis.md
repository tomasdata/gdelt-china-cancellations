# Síntesis Robusta — Análisis BRI LATAM 2017–2024
## Script 20: Auditoría de calidad + re-scoring

## Resumen ejecutivo

| Métrica | Valor |
|---------|-------|
| Señales originales (Script 18) | 269 |
| URLs contaminadas (≥3 países comparten URL) | 52 |
| Señales con domain_score = 0 (fuentes chinas) | 79 |
| Señales de alta confianza (robust_score_final ≥ 6.0) | 12 |
| Reducción total de ruido | 96% |
| Recall casos manuales conocidos | 4/10 (40%) |

## Hallazgo crítico: Falsos positivos del Script 19

El análisis de robustez identificó **3 patrones de falsos positivos sistemáticos**:

### 1. URL qz.com (Villavicencio)
- 5 señales (Ecuador, Colombia, Brasil, México, Venezuela × 2023) usaban
  el artículo `ecuador-fernando-villavicencio-corruption-assassination`
- El artículo menciona PetroChina y BRI como contenido lateral, no como tema
- **Resultado con robust_score_final:** 0.00 (threshold 6.0) → eliminadas
- Señales eliminadas: 5

### 2. hinews.cn (cluster masivo)
- 13 señales (13 países distintos × 2021) compartían la misma URL de
  noticias chinas (inaccesible, domain_score = 0)
- **Resultado:** todas eliminadas por domain_score=0 + contaminación

### 3. Fuentes chinas inaccesibles (60%+ del ruido original)
- 79 señales apuntan a dominios chinos: sina.com.cn, eastmoney.com, sohu.com, xinhuanet.com, qianlong.com, etc.
- Ninguna supera el threshold de alta confianza

## Mecanismos identificados (alta confianza)

| Mecanismo | N señales | Países | Período | Score medio |
|-----------|-----------|--------|---------|-------------|
| us_sanctions | 11 | Cuba, Jamaica, México, Panamá, Venezuela | 2017–2024 | 6.4 |
| confirmed_presence | 1 | Chile | 2020–2020 | 6.0 |

## Recuperación de casos manuales conocidos

| País | Año | Caso | Señales totales | Alta confianza | Score máximo |
|------|-----|------|----------------|---------------|--------------|
| Chile | 2018 | SQM/Tianqi — bloqueo adquisición litio | 4 | 0 | 4.0 |
| Ecuador | 2019 | Camarón — China suspende exportaciones | 3 | 0 | 1.5 |
| Ecuador | 2024 | Yasuní — moratoria ambiental | 0 | 0 | 0.0 |
| Brasil | 2017 | Autopista Tamoios — inversores chinos se retiran | 7 | 0 | 4.0 |
| Venezuela | 2018 | Unipec — prohíbe tanqueros Venezuela (EEUU sancion | 5 | 1 | 6.5 |
| Venezuela | 2018 | ZTE — sancionada por vigilancia Venezuela | 5 | 1 | 6.5 |
| Venezuela | 2019 | CNPC — suspende operaciones Venezuela | 5 | 1 | 6.0 |
| Venezuela | 2020 | EEUU sanciona empresa china por censura internet | 5 | 1 | 6.5 |
| Jamaica | 2021 | CHEC attack | 1 | 0 | 2.0 |
| Perú | 2021 | COSCO Chancay — proyecto portuario | 2 | 0 | 3.0 |

**Recall total: 4/10 (40%)**

## Top 30 señales de alta confianza para la tesis

| # | País | Año | Mecanismo | SOE | Tono | N arts | Score | URL |
|---|------|-----|-----------|-----|------|--------|-------|-----|
| 1 | Cuba | 2017 | us_sanctions | unknown | -8.5 | 1 | 7.0 | [link](http://www.domain-b.com/industry/telecom/20170308_sanctions.html) |
| 2 | Venezuela | 2018 | us_sanctions | unknown | -5.9 | 1 | 6.5 | [link](https://www.telecomstechnews.com/news/2018/dec/03/zte-us-sanctions-venezuelan-surveillance/) |
| 3 | Panamá | 2017 | us_sanctions | unknown | -5.7 | 1 | 6.5 | [link](http://www.africanewsanalysis.com/european-union-considers-including-bahamas-on-another-blacklist-by-xian-persaud-nassau-guardian-business-reporter/) |
| 4 | Venezuela | 2020 | us_sanctions | unknown | -6.9 | 1 | 6.5 | [link](https://www.republicworld.com/world-news/south-america/us-imposes-sanctions-on-chinese-firm-over-alleged-role-in-venezuela-internet-crackdown.html) |
| 5 | México | 2024 | us_sanctions | unknown | -5.9 | 1 | 6.5 | [link](https://timesofindia.indiatimes.com/world/china/china-opposes-us-sanctions-on-chinese-companies-for-supporting-russia/articleshow/108005860.cms) |
| 6 | Jamaica | 2020 | us_sanctions | unknown | -5.8 | 1 | 6.5 | [link](https://www.reuters.com/article/usa-rights-pompeo/u-s-sanctions-people-in-china-jamaica-el-salvador-over-alleged-human-rights-violations-idUSKBN28K29N) |
| 7 | Venezuela | 2017 | us_sanctions | unknown | -5.6 | 1 | 6.5 | [link](http://www.4-traders.com/news/Bill-Cassidy-Cassidy-Sends-Letter-to-White-House-on-Potential-Venezuelan-Energy-Sanctions--24928841/) |
| 8 | Venezuela | 2019 | us_sanctions | unknown | -10.8 | 1 | 6.0 | [link](https://www.bloombergquint.com/global-economics/major-china-buyer-shuns-venezuela-oil-loadings-on-u-s-sanctions) |
| 9 | México | 2023 | us_sanctions | unknown | -3.6 | 1 | 6.0 | [link](https://go955.com/2023/04/17/in-the-wake-of-drug-related-deaths-and-overdoses-huizinga-calls-for-more-sanctions-on-companies-he-says-are-supporting-drug-trade/) |
| 10 | Cuba | 2020 | us_sanctions | unknown | -9.4 | 1 | 6.0 | [link](https://www.strategic-culture.org/news/2020/04/10/trump-self-isolates-with-barbaric-sanctions/) |
| 11 | México | 2019 | us_sanctions | unknown | -1.8 | 1 | 6.0 | [link](https://www.timesonline.com/news/20190412/us-sen-pat-toomey-pushing-bills-on-chinese-fentanyl-sanctions-small-business-investment) |
| 12 | Chile | 2018 | political_rejection | Events_raw | -2.6 | 1 | 5.5 | [link](https://www.nasdaq.com/article/chile-files-complaint-to-block-sale-of-sqm-shares-to-chinese-companies-20180309-00699) |
| 13 | Ecuador | 2019 | political_rejection | Events_raw | -2.6 | 1 | 4.0 | [link](https://www.undercurrentnews.com/2019/09/09/china-appears-to-have-suspended-shrimp-export-approval-for-santa-priscila-omarsa/) |
| 14 | Brasil | 2017 | project_failure | Events_raw | -3.4 | 1 | 3.5 | [link](https://www.bnamericas.com/en/news/infrastructure/chinese-investors-may-not-pursue-sao-paulos-tamoios-highway-concession1/) |
| 15 | Chile | 2020 | confirmed_presence | SOE_OIL | -4.4 | 37 | 6.0 | [link](https://economia.uol.com.br/noticias/bloomberg/2020/02/07/china-agrava-caos-com-forca-maior-em-contratos-de-commodities.htm) |

## Distribución temporal de mecanismos (alta confianza)

| mecanismo | 2017 | 2018 | 2019 | 2020 | 2023 | 2024 |
|---|---|---|---|---|---|---|
| confirmed_presence | 0 | 0 | 0 | 1 | 0 | 0 |
| us_sanctions | 3 | 1 | 2 | 3 | 1 | 1 |

## Metodología del re-scoring

```
robust_score (escala 0-10) = mech_score + dom_bonus + vol_bonus + tone_bonus
                           + review_bonus + ev_url_bonus + ev_mech_bonus

mech_score   : us_sanctions=4, environ/political/debt=3, failure=2, presence=0
dom_bonus    : domain_score=3→2, =2→1, =1→0.5, =0→0 (hard disqualify)
vol_bonus    : n_articles≥30→2, ≥10→1, ≥5→0.5, <5→0
tone_bonus   : tone<-7→1, <-5→0.5, else→0
review_bonus : Script19 CONFIRMED(URL)→3, LIKELY(URL)→1.5, else→0
ev_url_bonus : URL exacta en Events dataset→1
ev_mech_bonus: mecanismo causal corroborado en Events→0.5

HARD DISQUALIFIERS (robust_score_final = 0):
  - url_contaminated=True (URL compartida por ≥3 país-año distintos)
  - domain_score=0 (fuente china inaccesible)

Threshold alta confianza: ≥ 6.0
```

## Implicaciones para la tesis

1. **Las 269 señales del Script 18 no deben citarse directamente** — el ~96% son ruido confirmado.
2. **12 señales de alta confianza** constituyen el corpus validado.
3. **El mecanismo `confirmed_presence`** solo tiene valor cuando:
   - La URL es de fuente anglófona de calidad (domain_score ≥ 2)
   - No está contaminada (URL única para ese país-año)
   - Es corroborada por el dataset Events
4. **Sanciones secundarias EEUU** (Venezuela 2018-2020) sigue siendo el
   mecanismo mejor documentado y con mayor originalidad teórica.
5. **Próximo paso:** Cruzar contra AidData TUFF 3.0 para validación externa.
