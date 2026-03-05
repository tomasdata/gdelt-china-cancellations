# AidData GCDF 3.0 Cross-Validation Report

**Generated**: 2026-03-05
**Script**: `notebooks/29_aiddata_cross_validation.py`

---

## 1. AidData Universe

AidData's Global Chinese Development Finance Dataset v3.0 tracks **20,985 projects**
across 165 countries, totaling US$1.34T (2000-2021).

### Project Status Distribution

| Status | Projects | % |
|--------|----------|---|
| Completion | 14,375 | 68.5% |
| Pipeline: Commitment | 2,854 | 13.6% |
| Implementation | 2,263 | 10.8% |
| Pipeline: Pledge | 1,356 | 6.5% |
| **Cancelled** | **92** | 0.4% |
| **Suspended** | **45** | 0.2% |

### Key Flags

- **Financial distress**: 493 projects (2.3%)
- **Infrastructure**: 5743 projects (27.4%)
- **Cancelled + Suspended + Distress (union)**: 627 projects
- **Infrastructure + problematic**: 511 projects
- **Cancelled value**: US$42.0B
- **Suspended value**: US$39.2B

---

## 2. Matching Results

Of our **70 BRI disruption cases**, matching against AidData's 20,985 projects:

| Match Quality | Cases |
|---------------|-------|
| Strong (score >= 0.35) | 42 |
| Partial (score >= 0.2) | 13 |
| No match | 15 |

**AidData-confirmed disruptions**: 5 of our cases are also marked as
cancelled/suspended/distressed in AidData.

### Strong Matches

- **Chile** (2018): SQM Lithium Acquisition → AidData: China CITIC Bank provides $1.3 billion loan for Tianqi Lithi [Completion] **[CONFIRMED]**
- **Chile** (2020): Commodity Contracts (Force Majeure) → AidData: China Co-Financing Fund for Latin America and the Caribbean  [Completion]
- **Ecuador** (2019): Shrimp Export Approval → AidData: [China Co-financing Fund] IDB administers $50 million CHC lo [Completion]
- **Venezuela** (2018): ZTE Surveillance Infrastructure → AidData: CDB offers $5 billion line of credit for oil sector developm [Pipeline: Pledge]
- **Venezuela** (2019): CNPC Oil Operations → AidData: CDB reschedules $19 billion of outstanding debt via grace pe [Implementation]
- **Venezuela** (2020): Internet Censorship Infrastructure → AidData: China donates 5 ambulances to Venezuela to aid in the pandem [Completion]
- **Brasil** (2017): Tamoios Highway Concession → AidData: Chinese consortium finances Fiol railway in Brazil (linked t [Pipeline: Pledge]
- **Argentina** (2020): Pork Production Deal → AidData: Beijing's Fengtai District provides a grant of 10,000 masks  [Completion]
- **Mexico** (2014): Mexico City-Queretaro HSR → AidData: China Eximbank offers $3.23 billion loan for Mexico City–Que [Pipeline: Pledge]
- **Costa Rica** (2016): SORESCO Oil Refinery → AidData: China Development Bank provides $900 million USD loan for oi [Suspended] **[CONFIRMED]**
- **Ecuador** (2018): Coca Codo Sinclair Dam → AidData: Chinese Academy of Governance provides training to Ecuadoria [Completion]
- **Venezuela** (2018): Unipec Oil Tankers → AidData: CDB offers $5 billion line of credit for oil sector developm [Pipeline: Pledge]
- **Pakistán** (2017): Gwadar Port Complex → AidData: Chinese Government provides RMB 657 million grant for New Gw [Implementation]
- **Pakistán** (2021): Dasu Hydropower Dam → AidData: [IPP] China Eximbank asked to provide overseas investment lo [Pipeline: Pledge]
- **Pakistán** (2021): Gwadar Anti-CPEC Protests → AidData: [CPEC, IPP] CDB contributes to $1.54 billion syndicated loan [Implementation]
- **Pakistán** (2020): CPEC Corruption Row → AidData: [CPEC, IPP] CDB contributes to $1.43 billion syndicated loan [Implementation]
- **Sri Lanka** (2017): Hambantota Port → AidData: CDB provides $500 million loan to CMPort Holdings to facilit [Completion]
- **Sri Lanka** (2020): Colombo Port City → AidData: China Development Bank provides $100 million interest-free l [Pipeline: Commitment]
- **Myanmar** (2011): Myitsone Dam → AidData: [Suspended] China Development Bank contributes to loan syndi [Suspended] **[CONFIRMED]**
- **Nepal** (2024): Pokhara International Airport → AidData: MOFCOM provides RMB 355.9 million interest-free loan — via E [Completion]
- **Bangladesh** (2016): Banshkhali Coal Power Plant → AidData: China Power Construction Corporation to construct Daudkandi  [Pipeline: Pledge]
- **Maldives** (2018): Sinamale Bridge + Others → AidData: Dongfang Electric Corporation provides $38.9 million supplie [Completion]
- **Malasia** (2018): ECRL + Two Pipelines → AidData: [Disbursed Portion] China Eximbank provides RM 39.1 billion  [Implementation]
- **Indonesia** (2020): Jakarta-Bandung HSR Debt Concerns → AidData: CDB provides $2.3805 billion loan tranche for the Jakarta-Ba [Implementation] **[CONFIRMED]**
- **Thailand** (2020): Kra Canal → AidData: Chinese government donates first batch of anti-epidemic mate [Completion]
- **Kenia** (2020): Lamu Coal Power Plant → AidData: China EXIM Bank loans 16 million USD to Kenya for Uplands (L [Pipeline: Pledge]
- **Tanzania** (2019): Bagamoyo Mega-Port → AidData: The Chinese Government Grants $20,000 for the Construction o [Completion]
- **Zimbabwe** (2021): Sengwa Coal Power Station → AidData: Chinese Government provides loan for Kunzvi Dam Project [Implementation]
- **Nigeria** (2021): Railway Financing → AidData: China Railway Construction Corporation provides medical expe [Completion]
- **Ghana** (2017): $19B China Loan Package → AidData: China Eximbank reschedules preferential buyer’s credit for B [Completion]
- **Kenia** (2022): SGR Loan Default → AidData: China Eximbank provides KES 2 billion loan for Eastern Bypas [Implementation]
- **Zambia** (2020): Chinese Loans Default → AidData: Chinese Government cancels RMB 170 million of the Government [Pipeline: Commitment]
- **Montenegro** (2014): Bar-Boljare Highway → AidData: China Eximbank provides $943.9 million preferential buyer's  [Completion] **[CONFIRMED]**
- **EU** (2021): Comprehensive Agreement on Investment → AidData: China Eximbank provides $50 million loan to Black Sea Trade  [Pipeline: Commitment]
- **Israel** (2019): Haifa Port Terminal → AidData: Bank of China contributes $340 million loan for the Bayport  [Completion]
- **Sri Lanka** (2020): port Administration Regulations  → AidData: China Merchants Port Group donates 1,000 protective suits to [Completion]
- **Iran** (2019): Feds Accuse Huawei of Stealing T-Mobile Robot Secr → AidData: Chinese Government provides RMB 1.7 billion loan for Phase I [Pipeline: Pledge]
- **Fiji** (2018): Fiji court hands out light fine for Chinese constr → AidData: Chinese Grant Trust Fund pays retention fee for Valelvu mult [Completion]
- **Senegal** (2018): Hong Kong Businessman Convicted in UN Bribery Sche → AidData: China awards 75 Chinese Government scholarships to students  [Completion]
- **Djibouti** (2020): Djibouti dismisses ruling on Doraleh, says ‘not su → AidData: China sends epidemic expert team to Djibouti in April 2020 [Completion]
- **Djibouti** (2018): ERC Grilled Over Capricious, Delayed Compensation  → AidData: Chinese Government provides a grant for the Djibouti Luban W [Completion]
- **Algeria** (2021): Take Abuja-Kaduna Rail Attacks Seriously - Daily T → AidData: Chinese Government donates 3.2 million Sinovac Covid-19 vacc [Completion]


---

## 3. New Candidates from AidData

AidData identifies **627 problematic projects** (cancelled/suspended/distress)
that could be new cases for our dataset.

### High Priority (infrastructure + cancelled/suspended + high value)

- **Malaysia** (2018): [Cancelled Portion] China Eximbank provides RM 39.1 billion preferential buyer's [Cancelled] US$10567M
- **Kenya** (2015): [Cancelled] ICBC provides $900 million export credit for 981.5 MW Lamu Coal-Fire [Cancelled] US$1010M
- **Ukraine** (2011): [Cancelled] China Eximbank provides $320.1 million for Tranche 2 of buyer’s cred [Cancelled] US$394M
- **Niger** (2013): China Eximbank provides $1 billion master facility agreement for various infrast [Cancelled] US$1128M
- **Ukraine** (2012): [Cancelled] CDB provides $3.656 billion loan to help Ukraine transition its powe [Cancelled] US$4293M
- **Kazakhstan** (2011): Cancelled: China Eximbank $1.4 billion USD loan for Atyrau Petrochemical Complex [Cancelled] US$1722M
- **Thailand** (2020): China Eximbank pledges 38.2 billion baht loan for Phase 1 of the Nong Khai High- [Cancelled] US$5937M
- **Malaysia** (2017): [Cancelled Portion] China Eximbank provides RMB 12.87 billion loan for Trans-Sab [Cancelled] US$2196M
- **Sri Lanka** (2012): [Cancelled] China Eximbank provides $51 million buyer’s credit loan for Phase II [Cancelled] US$60M
- **Belarus** (2010): [Cancelled] China Eximbank provides $600 million loan for Minsk National Airport [Cancelled] US$836M
- **Pakistan** (2009): China Eximbank agrees to a $67.35 million preferential buyer’s credit (PBC) loan [Cancelled] US$101M
- **Pakistan** (2009): China Eximbank provides a USD 144.18 million preferential buyer's credit loan fo [Cancelled] US$217M
- **Sri Lanka** (2009): China Eximbank offers $245 million loan for the construction of a 56 km railway  [Cancelled] US$368M
- **Argentina** (2014): Chinese loan syndicate supports Atucha 3 and Atucha 4 Nuclear Plant Project [Sus [Suspended] US$7434M
- **Belarus** (2010): [Cancelled] China Eximbank provides $186.4 million buyer’s credit loan for Soda  [Cancelled] US$260M
- **South Sudan** (2016): [Cancelled] China Eximbank provides $169 million loan for 130 km Juba-Torit Sect [Cancelled] US$200M
- **Trinidad and Tobago** (2019): Shanghai Construction Group receives a TT$1.1 Billion contract to design build a [Cancelled] US$183M
- **Zimbabwe** (2012): China Exim Bank loans Zimbabwe $864 million for Matabeleland Zambezi Water Pipel [Suspended] US$1014M
- **Colombia** (2015): [Cancelled] ICBC provides $198 million export buyer’s credit for Caribbean Float [Cancelled] US$222M
- **Zambia** (2018): [Suspended] China Eximbank provides loan for 321 km Lusaka-Ndola Dual Carriagewa [Suspended] US$1154M


### Coverage Gaps by Country

Top countries where AidData has more problematic projects than we have cases:

| Country | AidData Problematic | Our Cases | Gap |
|---------|--------------------:|----------:|----:|
| Pakistan | 60 | 5 | +55 |
| Sri Lanka | 55 | 3 | +52 |
| Myanmar | 35 | 1 | +34 |
| Ethiopia | 29 | 0 | +29 |
| Cameroon | 27 | 0 | +27 |
| Ghana | 22 | 1 | +21 |
| Russia | 20 | 0 | +20 |
| Sudan | 18 | 0 | +18 |
| Zimbabwe | 16 | 1 | +15 |
| Brazil | 16 | 1 | +15 |
| Mozambique | 14 | 2 | +12 |
| Ecuador | 14 | 2 | +12 |
| Marshall Islands | 11 | 0 | +11 |
| Kenya | 13 | 2 | +11 |
| Venezuela | 15 | 4 | +11 |


---

## 4. Implications for Thesis

### What AidData tells us

1. **Scale**: Of 20,985 Chinese development projects, only 137 (0.7%) are formally cancelled/suspended — our 70 cases represent a significant portion of documented disruptions.

2. **Financial distress is widespread**: 493 projects (2.3%) are flagged for financial distress, far more than the 137 formally cancelled — suggesting many "troubled" projects continue despite problems.

3. **Infrastructure focus validated**: 511 of 627 problematic projects are infrastructure, confirming that BRI infrastructure is disproportionately affected.

4. **Our pipeline captures events AidData doesn't track**: Many of our cases (Huawei 5G bans, CPEC security incidents, political opposition) aren't in AidData because they aren't "development finance" — they're commercial investments or geopolitical events.

### Recommended next steps

- Verify top 20 high-priority AidData candidates for potential addition to dataset
- Use AidData project IDs to enrich existing cases with financing details
- The low formal cancellation rate (0.7%) vs. high distress rate (2.3%) is itself a thesis finding
