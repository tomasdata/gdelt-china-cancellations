# BRI Cancellations & Disruptions Dataset v2

**Generated**: 2026-03-04
**Pipeline**: Scripts 01-27 (GDELT v2 + GKG + web verification)

## Summary

- **70 verified cases** of BRI project disruptions across **51 countries** and **9 regions**
- Total value affected: **$123,353M**
- Cases with known value: 28/70
- Pipeline detection rate: 54/70 (77%)

## Dataset by Region

| Region | Cases | Value ($M) | Top mechanisms |
|--------|-------|-----------|----------------|
| Africa | 16 | 64,318 | economic, political |
| LATAM | 14 | 16,800 | security, economic |
| South_Asia | 13 | 6,516 | security, social |
| Europe | 8 | 1,244 | security, economic |
| Middle_East | 7 | 0 | security, political |
| Central_Asia | 4 | 275 | social, security |
| SE_Asia | 4 | 34,200 | political, economic |
| Oceania | 3 | 0 | political, security |
| Eurasia | 1 | 0 | unknown |

## Mechanism Analysis

| Category | N | % | Regions |
|----------|---|---|--------|
| security | 23 | 33% | Africa, Central_Asia, Europe, LATAM |
| economic | 15 | 21% | Africa, Central_Asia, Europe, LATAM |
| political | 12 | 17% | Africa, Europe, LATAM, Middle_East |
| social | 9 | 13% | Africa, Central_Asia, LATAM, Middle_East |
| legal | 5 | 7% | Europe, LATAM, South_Asia |
| unknown | 4 | 6% | Africa, Eurasia, Europe, Middle_East |
| quality | 1 | 1% | LATAM |
| climate | 1 | 1% | Africa |

## Sector Distribution

| Sector | N | Value ($M) |
|--------|---|------------|
| Transport_Port | 17 | 38,816 |
| Transport_Rail | 11 | 34,268 |
| Other | 10 | 0 |
| Telecom | 7 | 0 |
| Energy_OilGas | 5 | 1,200 |
| Transport_Road | 5 | 944 |
| Energy_Hydro | 5 | 24,850 |
| Mining | 3 | 12,000 |
| Energy_Coal | 3 | 5,000 |
| Manufacturing | 2 | 275 |
| Finance | 1 | 6,000 |
| Energy_Nuclear | 1 | 0 |

## Temporal Evolution

| Year | Cases |
|------|-------|
| 2011 | 1 |
| 2014 | 2 |
| 2016 | 2 |
| 2017 | 4 |
| 2018 | 11 |
| 2019 | 7 |
| 2020 | 16 |
| 2021 | 9 |
| 2022 | 5 |
| 2023 | 5 |
| 2024 | 8 |

## Top 20 Cases by Value

| Country | Project | Value ($M) | Mechanism | Year |
|---------|---------|-----------|-----------|------|
| Malasia | ECRL + Two Pipelines | 22,000 | new_government_reversal | 2018 |
| Ghana | $19B China Loan Package | 19,000 | political_opposition | 2017 |
| Nigeria | Railway Financing | 14,400 | debt_concerns | 2021 |
| Tanzania | Bagamoyo Mega-Port | 10,000 | predatory_terms_rejected | 2019 |
| Indonesia | Jakarta-Bandung HSR Debt Concerns | 7,300 | debt_distress | 2020 |
| Zambia | Chinese Loans Default | 6,000 | debt_distress | 2020 |
| DRC | Sicomines Mining Contracts | 6,000 | new_government_reversal | 2021 |
| Philippines | Three Railway Projects | 4,900 | geopolitical_tension | 2023 |
| Chile | SQM Lithium Acquisition | 4,000 | political_rejection | 2018 |
| Mexico | Mexico City-Queretaro HSR | 3,750 | corruption_scandal | 2014 |
| Perú | Chancay Port | 3,600 | investor_state_arbitration | 2024 |
| Myanmar | Myitsone Dam | 3,600 | political_rejection | 2011 |
| Zimbabwe | Sengwa Coal Power Station | 3,000 | climate_policy | 2021 |
| Uganda | Kampala-Malaba SGR Railway | 2,300 | financing_failure | 2023 |
| Ecuador | Coca Codo Sinclair Dam | 2,250 | quality_defects | 2018 |
| Bolivia | Salar de Uyuni Lithium | 2,000 | indigenous_opposition | 2024 |
| Kenia | Lamu Coal Power Plant | 2,000 | environmental_opposition | 2020 |
| Sri Lanka | Colombo Port City | 1,400 | us_secondary_sanctions | 2020 |
| Kenia | SGR Loan Default | 1,300 | debt_distress | 2022 |
| Costa Rica | SORESCO Oil Refinery | 1,200 | corruption_scandal | 2016 |

## Data Sources

| Source | N cases |
|--------|--------|
| existing_consolidated | 52 |
| regional_deep_dive | 13 |
| tier2_confirmed | 5 |

## Methodology

This dataset was constructed through a 27-script pipeline:

1. **GDELT Events** (Scripts 01-12): 663,825 events → 52,439 BRI-related → 801 candidates
2. **GKG Text Mining** (Scripts 07, 17, 23a/b): 626,775 articles → SOE timelines, debt/environmental signals, project name extraction
3. **Web Verification** (Scripts 19-20, 24, 26): URL scraping + evidence extraction
4. **Manual Curation** (Script 22): Literature cross-reference, 52 base cases
5. **Enrichment** (Script 25): Mechanism taxonomy, sector classification, value estimation
6. **Consolidation** (Script 27): Merge, dedup, quality control, thesis tables

### Limitations

- GDELT v2 begins 2015-02-19; pre-2015 cases from literature only
- English-language bias: francophone Africa, Central Asia (Russian), Pacific Islands underrepresented
- Huawei/5G bans dominate telecom sector; may inflate security mechanism counts
- Value estimates from news sources; may not match final project costs
- Some cases classified as 'disrupted' may have been subsequently resumed
