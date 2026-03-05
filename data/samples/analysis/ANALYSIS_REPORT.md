# Exploratory Data Analysis — BRI Disruptions Dataset

**Generated**: 2026-03-05
**Source**: `data/samples/final/bri_cancellations_FINAL_v2.csv`
**Script**: `notebooks/28_exploratory_analysis.py`

---

## 1. Dataset Overview

The dataset contains **70 verified cases** of BRI project disruptions across **51 countries** and **9 regions**, spanning from 2011 to 2024.

| Metric | Value |
|--------|-------|
| Total cases | 70 |
| Countries | 51 |
| Regions | 9 |
| Total value affected | US$123.4B |
| Cases with known value | 28/70 (40%) |
| Mean value (when known) | US$4.4B |
| Median value (when known) | US$2.3B |
| Pipeline detection rate | 77% |
| GKG corroboration rate | 41% |

---

## 2. Temporal Patterns

**Peak year: 2020** with 16 cases — coincides with COVID-19 pandemic disruptions and heightened US-China tensions.

![Cases by Year](temporal/cases_by_year.png)

The cumulative curve shows accelerating discovery from 2018 onward, with a notable inflection point in 2020.

![Cumulative Cases](temporal/cases_by_year_cumulative.png)

Security mechanisms (sanctions, 5G bans) dominate from 2018+, while economic mechanisms (debt distress) concentrate in 2020–2022.

![Mechanism Evolution](temporal/mechanism_evolution.png)

---

## 3. Regional Distribution

**Most affected region: Africa** (16 cases), followed by LATAM (14) and South_Asia (13).

![Cases by Region](regional/cases_by_region.png)

The region-mechanism heatmap reveals distinct patterns: Africa is dominated by economic/political mechanisms, while South Asia and LATAM show more security-related disruptions.

![Region × Mechanism](regional/region_mechanism_heatmap.png)

Transport sectors (ports, rail, roads) dominate across all regions, with telecom concentrated in Europe and mining in Africa/LATAM.

![Region × Sector](regional/region_sector_heatmap.png)

By value, SE Asia leads due to Malaysia's ECRL ($22B), followed by Africa (Ghana $19B, Nigeria $14.4B, Tanzania $10B).

![Value by Region](regional/value_by_region.png)

---

## 4. Mechanism Analysis

**Dominant mechanism: security** (23 cases, 33%), driven by Huawei 5G bans, US secondary sanctions, and CPEC security incidents.

![Mechanism Distribution](mechanisms/mechanism_distribution.png)

The most frequent specific mechanisms are US secondary sanctions, followed by debt distress and community opposition.

![Mechanism Detail](mechanisms/mechanism_detail_bar.png)

By value, political reversals (new_government_reversal: Malaysia $22B) and debt mechanisms lead.

![Mechanisms by Value](mechanisms/top_mechanisms_by_value.png)

---

## 5. Sector Analysis

**Dominant sector: Transport_Port** (17 cases), reflecting BRI's focus on connectivity infrastructure.

![Sector Distribution](sectors/sector_distribution.png)

Transport ports and rail account for the highest disrupted values (>$30B each), while telecom cases (Huawei 5G) are numerous but lack monetary value data.

![Sector Value](sectors/sector_value.png)

![Sector × Mechanism](sectors/sector_mechanism_heatmap.png)

---

## 6. Value Analysis

Of 70 cases, **28 (40%)** have known project values, totaling **US$123.4B**.

The distribution is right-skewed with a median of US$2.3B and mean of US$4.4B, indicating a few mega-projects driving the total.

![Value Distribution](value/value_distribution.png)

The top 20 cases by value span from US$1.2B to US$22.0B.

![Top 20 Cases](value/top20_cases_value.png)

There is a weak positive relationship between project value and media coverage (GKG articles), though some high-value cases have minimal coverage and vice versa.

![Value vs GKG](value/value_vs_gkg.png)

---

## 7. Evidence & Detection

The automated GDELT pipeline detected **77%** of all cases (54/70). Detection rates vary by region:

![Detection Rate](evidence/detection_rate_by_region.png)

GKG article counts follow a power-law distribution: most cases have few articles, while a handful (Australia BRI: 1,575 articles) have extensive coverage.

![GKG Distribution](evidence/gkg_distribution.png)

Cases from the original consolidated dataset have higher detection rates than those added via regional deep dives.

![Detection by Source](evidence/detection_vs_source.png)

---

## 8. Chinese Actors

The most frequently involved Chinese actors reflect the sectoral distribution: Huawei and ZTE dominate telecom, CCCC and China Railway lead in transport, and CNPC/Sinopec in energy.

![Top Actors](actors/top_chinese_actors.png)

![Actor × Sector](actors/actor_sector_heatmap.png)

---

## 9. Key Findings for Thesis

1. **Security dominates**: 33% of disruptions are security-related (sanctions, 5G bans, attacks on workers), challenging the narrative that BRI failures are primarily economic.

2. **2020 inflection**: The pandemic year saw the most disruptions (16 cases), combining health-related delays with accelerated geopolitical realignment.

3. **Value concentration**: The top 5 cases account for 59% of total disrupted value, suggesting that BRI risk is concentrated in mega-projects.

4. **Detection gap**: The pipeline misses ~23% of cases, particularly in Central Asia (Russian-language media) and cases pre-dating GDELT v2 (pre-2015).

5. **Transport vulnerability**: Transport infrastructure (ports + rail + roads) accounts for 47% of all disruptions and the highest values.

6. **Regional mechanism patterns**: Africa → economic (debt), South Asia → security (attacks), Europe → security (5G bans), LATAM → mixed (sanctions + political).
