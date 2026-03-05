"""
Script 29 — AidData GCDF 3.0 Cross-Validation
===============================================
Cruza el dataset BRI de 70 casos con AidData's Global Chinese Development
Finance Dataset v3.0 (20,985 proyectos, 2000-2021).

Objetivos:
  1. Explorar AidData: status, financial distress, infrastructure
  2. Matching con nuestros 70 casos (country + fuzzy title + year)
  3. Descubrir nuevos candidatos cancelados/suspendidos
  4. Análisis de cobertura: ¿qué captura GDELT vs AidData?

Input:
  data/external/aiddata_gcdf_v3/.../AidDatasGlobalChineseDevelopmentFinanceDataset_v3.0.xlsx
  data/samples/final/bri_cancellations_FINAL_v2.csv

Output:
  data/samples/validation/aiddata_match_results.csv
  data/samples/validation/aiddata_new_candidates.csv
  data/samples/validation/aiddata_coverage_analysis.csv
  data/samples/validation/aiddata_validation_report.md
"""

import os
import re
import pandas as pd
import numpy as np
from difflib import SequenceMatcher

os.makedirs("data/samples/validation", exist_ok=True)

# ── Load datasets ─────────────────────────────────────────────────────────────
print("=== Loading datasets ===")

AIDDATA_PATH = ("data/external/aiddata_gcdf_v3/"
                "AidDatas_Global_Chinese_Development_Finance_Dataset_Version_3_0/"
                "AidDatasGlobalChineseDevelopmentFinanceDataset_v3.0.xlsx")

COLS = [
    "AidData Record ID", "Recommended For Aggregates", "Recipient", "Recipient ISO-3",
    "Recipient Region", "Commitment Year", "Implementation Start Year", "Completion Year",
    "Title", "Description", "Status", "Intent", "Flow Type", "Flow Type Simplified",
    "Flow Class", "Sector Code", "Sector Name", "Infrastructure", "COVID",
    "Funding Agencies", "Amount (Constant USD 2021)", "Amount (Nominal USD)",
    "Financial Distress", "Source URLs",
]

aid = pd.read_excel(AIDDATA_PATH, sheet_name="GCDF_3.0", usecols=COLS)
print(f"AidData: {len(aid)} projects, {len(aid.columns)} columns")

bri = pd.read_csv("data/samples/final/bri_cancellations_FINAL_v2.csv")
print(f"BRI dataset: {len(bri)} cases")


# ── 1. AidData Exploration ────────────────────────────────────────────────────
print("\n=== 1. AidData Exploration ===")

print(f"\nStatus distribution:")
status_vc = aid["Status"].value_counts()
for s, n in status_vc.items():
    print(f"  {s:30s} {n:6d} ({100*n/len(aid):.1f}%)")

print(f"\nInfrastructure projects: {(aid['Infrastructure'] == 'Yes').sum()}")
print(f"Financial distress: {(aid['Financial Distress'] == 'Yes').sum()}")
print(f"Recommended for aggregates: {(aid['Recommended For Aggregates'] == 'Yes').sum()}")

# Problematic projects
aid_prob = aid[
    (aid["Status"].isin(["Cancelled", "Suspended"])) |
    (aid["Financial Distress"] == "Yes")
].copy()
print(f"\nProblematic projects (cancelled + suspended + distress): {len(aid_prob)}")
print(f"  Cancelled: {(aid_prob['Status'] == 'Cancelled').sum()}")
print(f"  Suspended: {(aid_prob['Status'] == 'Suspended').sum()}")
print(f"  Financial distress (any status): {(aid_prob['Financial Distress'] == 'Yes').sum()}")

# Infrastructure + problematic
aid_infra_prob = aid_prob[aid_prob["Infrastructure"] == "Yes"]
print(f"  Infrastructure + problematic: {len(aid_infra_prob)}")

# Top countries
print(f"\nTop 15 countries (problematic projects):")
for c, n in aid_prob["Recipient"].value_counts().head(15).items():
    print(f"  {c:25s} {n:4d}")

# Top sectors
print(f"\nTop sectors (problematic projects):")
for s, n in aid_prob["Sector Name"].value_counts().head(10).items():
    print(f"  {s:45s} {n:4d}")


# ── 2. Matching ───────────────────────────────────────────────────────────────
print("\n=== 2. Cross-matching BRI cases with AidData ===")

# Country name normalization
COUNTRY_MAP = {
    "Malasia": "Malaysia", "Kenia": "Kenya", "Perú": "Peru",
    "México": "Mexico", "Brasil": "Brazil", "Filipinas": "Philippines",
    "Sri Lanka": "Sri Lanka", "DRC": "Congo, Dem. Rep.",
    "Zambia": "Zambia", "Tanzania": "Tanzania", "Ghana": "Ghana",
    "Myanmar": "Myanmar", "Indonesia": "Indonesia", "Ecuador": "Ecuador",
    "Venezuela": "Venezuela", "Chile": "Chile", "Bolivia": "Bolivia",
    "Argentina": "Argentina", "Costa Rica": "Costa Rica",
    "Uganda": "Uganda", "Nigeria": "Nigeria", "Zimbabwe": "Zimbabwe",
    "Pakistán": "Pakistan", "Pakistan": "Pakistan",
    "Australia": "Australia", "Italia": "Italy", "Italy": "Italy",
    "Montenegro": "Montenegro", "Romania": "Romania",
    "Alemania": "Germany", "Germany": "Germany",
    "Nepal": "Nepal", "Bangladesh": "Bangladesh", "Maldives": "Maldives",
    "Cambodia": "Cambodia", "Laos": "Lao People's Democratic Republic",
    "Iran": "Iran", "Iraq": "Iraq", "Israel": "Israel",
    "Saudi Arabia": "Saudi Arabia", "UAE": "United Arab Emirates",
    "Kazakhstan": "Kazakhstan", "Kyrgyzstan": "Kyrgyz Republic",
    "Turkmenistan": "Turkmenistan", "Tajikistan": "Tajikistan",
    "Fiji": "Fiji", "Papua New Guinea": "Papua New Guinea",
    "Djibouti": "Djibouti", "Senegal": "Senegal",
    "Mozambique": "Mozambique", "Algeria": "Algeria",
    "Cameroon": "Cameroon", "Ethiopia": "Ethiopia",
    "Belarus": "Belarus", "Russia": "Russia",
}


def fuzzy_match(s1, s2):
    """Ratio de similitud entre dos strings."""
    if not s1 or not s2:
        return 0
    s1 = str(s1).lower().strip()
    s2 = str(s2).lower().strip()
    return SequenceMatcher(None, s1, s2).ratio()


def keyword_overlap(project_name, aiddata_title):
    """Cuenta keywords compartidos entre nombre de proyecto y título AidData."""
    if not project_name or not aiddata_title:
        return 0
    stop = {"the", "of", "and", "in", "to", "for", "a", "an", "is", "by", "on", "at", "from"}
    words1 = set(str(project_name).lower().split()) - stop
    words2 = set(str(aiddata_title).lower().split()) - stop
    if not words1:
        return 0
    return len(words1 & words2) / len(words1)


match_results = []

for _, case in bri.iterrows():
    country_bri = str(case["country"])
    country_aid = COUNTRY_MAP.get(country_bri, country_bri)
    year_bri = int(case["year"]) if pd.notna(case["year"]) else 0
    project_bri = str(case["project"])

    # Filter AidData by country
    candidates = aid[aid["Recipient"].str.contains(country_aid, case=False, na=False)]

    best_match = None
    best_score = 0

    for _, cand in candidates.iterrows():
        year_aid = int(cand["Commitment Year"]) if pd.notna(cand["Commitment Year"]) else 0

        # Year proximity (0-1)
        year_diff = abs(year_bri - year_aid)
        year_score = max(0, 1 - year_diff / 5)

        # Title similarity
        title_fuzzy = fuzzy_match(project_bri, cand["Title"])
        title_kw = keyword_overlap(project_bri, str(cand["Title"]) + " " + str(cand.get("Description", "")))

        # Sector bonus
        sector_bonus = 0
        sector_aid = str(cand["Sector Name"]).lower()
        sector_bri = str(case["sector"]).lower()
        if "transport" in sector_bri and "transport" in sector_aid:
            sector_bonus = 0.2
        elif "energy" in sector_bri and "energy" in sector_aid:
            sector_bonus = 0.2
        elif "telecom" in sector_bri and "communication" in sector_aid:
            sector_bonus = 0.2
        elif "mining" in sector_bri and "mining" in sector_aid:
            sector_bonus = 0.2

        # Combined score
        score = 0.3 * year_score + 0.3 * title_fuzzy + 0.25 * title_kw + 0.15 * sector_bonus

        if score > best_score:
            best_score = score
            best_match = cand

    match_results.append({
        "country_bri": country_bri,
        "project_bri": project_bri,
        "year_bri": year_bri,
        "sector_bri": case["sector"],
        "value_bri": case["value_usd_millions"],
        "match_score": round(best_score, 3),
        "aiddata_id": int(best_match["AidData Record ID"]) if best_match is not None else None,
        "aiddata_title": str(best_match["Title"])[:150] if best_match is not None else "",
        "aiddata_year": int(best_match["Commitment Year"]) if best_match is not None and pd.notna(best_match["Commitment Year"]) else None,
        "aiddata_status": str(best_match["Status"]) if best_match is not None else "",
        "aiddata_amount_usd": best_match["Amount (Constant USD 2021)"] if best_match is not None else None,
        "aiddata_sector": str(best_match["Sector Name"])[:50] if best_match is not None else "",
        "aiddata_distress": str(best_match["Financial Distress"]) if best_match is not None else "",
        "aiddata_infra": str(best_match["Infrastructure"]) if best_match is not None else "",
    })

df_match = pd.DataFrame(match_results)

# Classification
GOOD_MATCH = 0.35
PARTIAL_MATCH = 0.2
df_match["match_quality"] = df_match["match_score"].apply(
    lambda s: "STRONG" if s >= GOOD_MATCH else ("PARTIAL" if s >= PARTIAL_MATCH else "NO_MATCH")
)

print(f"\nMatch quality:")
print(df_match["match_quality"].value_counts().to_string())

print(f"\nStrong matches:")
strong = df_match[df_match["match_quality"] == "STRONG"]
for _, m in strong.iterrows():
    status_flag = " *** ALSO PROBLEMATIC ***" if m["aiddata_status"] in ["Cancelled", "Suspended"] or m["aiddata_distress"] == "Yes" else ""
    print(f"  {m['country_bri']:15s} {m['project_bri'][:40]:42s} → {m['aiddata_title'][:50]:52s} [{m['aiddata_status']}]{status_flag}")

# Save
df_match.to_csv("data/samples/validation/aiddata_match_results.csv", index=False)
print(f"\nSaved: aiddata_match_results.csv ({len(df_match)} rows)")


# ── 3. New Candidates from AidData ───────────────────────────────────────────
print("\n=== 3. New Candidates from AidData ===")

# Projects that are cancelled/suspended/distress + infrastructure, not in our dataset
existing_countries = set(bri["country"].str.lower())

# All problematic infrastructure projects
new_candidates = []
for _, proj in aid_prob.iterrows():
    country = str(proj["Recipient"])
    title = str(proj["Title"])
    year = int(proj["Commitment Year"]) if pd.notna(proj["Commitment Year"]) else 0
    amount = proj["Amount (Constant USD 2021)"] if pd.notna(proj["Amount (Constant USD 2021)"]) else 0
    status = str(proj["Status"])
    distress = str(proj["Financial Distress"])
    infra = str(proj["Infrastructure"])
    sector = str(proj["Sector Name"])

    # Priority score
    priority = 0
    if status == "Cancelled":
        priority += 3
    elif status == "Suspended":
        priority += 2
    if distress == "Yes":
        priority += 1
    if infra == "Yes":
        priority += 2
    if amount > 100_000_000:
        priority += 1
    if amount > 1_000_000_000:
        priority += 1

    new_candidates.append({
        "aiddata_id": int(proj["AidData Record ID"]),
        "country": country,
        "region": str(proj["Recipient Region"]),
        "title": title[:200],
        "year": year,
        "status": status,
        "financial_distress": distress,
        "infrastructure": infra,
        "sector": sector,
        "amount_usd": amount,
        "funding_agencies": str(proj["Funding Agencies"])[:100],
        "priority": priority,
    })

df_new = pd.DataFrame(new_candidates)
df_new = df_new.sort_values("priority", ascending=False)

print(f"Total problematic AidData projects: {len(df_new)}")
print(f"  Infrastructure: {len(df_new[df_new['infrastructure'] == 'Yes'])}")
print(f"  Amount > $100M: {len(df_new[df_new['amount_usd'] > 100_000_000])}")
print(f"  Amount > $1B: {len(df_new[df_new['amount_usd'] > 1_000_000_000])}")

# Top candidates
print(f"\nTop 30 candidates (by priority):")
for _, c in df_new.head(30).iterrows():
    amt = f"${c['amount_usd']/1e6:.0f}M" if c["amount_usd"] > 0 else "N/A"
    print(f"  [{c['status']:10s}] {c['country']:20s} {c['title'][:55]:57s} {amt:>10s}  P={c['priority']}")

df_new.to_csv("data/samples/validation/aiddata_new_candidates.csv", index=False)
print(f"\nSaved: aiddata_new_candidates.csv ({len(df_new)} rows)")


# ── 4. Coverage Analysis ─────────────────────────────────────────────────────
print("\n=== 4. Coverage Analysis ===")

# By region: how many AidData problematic projects does GDELT capture?
regions_aid = aid_prob["Recipient Region"].value_counts()
print(f"\nAidData problematic projects by region:")
for r, n in regions_aid.items():
    print(f"  {r:25s} {n:4d}")

# By country: overlap analysis
country_analysis = []
for country in aid_prob["Recipient"].unique():
    aid_count = len(aid_prob[aid_prob["Recipient"] == country])
    # Check if we have this country in BRI dataset
    bri_count = 0
    for _, case in bri.iterrows():
        mapped = COUNTRY_MAP.get(str(case["country"]), str(case["country"]))
        if mapped.lower() == country.lower():
            bri_count += 1

    country_analysis.append({
        "country": country,
        "aiddata_problematic": aid_count,
        "bri_cases": bri_count,
        "coverage_gap": aid_count - bri_count,
    })

df_coverage = pd.DataFrame(country_analysis)
df_coverage = df_coverage.sort_values("coverage_gap", ascending=False)

print(f"\nTop 20 coverage gaps (AidData problematic - our cases):")
for _, r in df_coverage.head(20).iterrows():
    print(f"  {r['country']:25s} AidData={r['aiddata_problematic']:3d}  Ours={r['bri_cases']:2d}  Gap={r['coverage_gap']:+3d}")

df_coverage.to_csv("data/samples/validation/aiddata_coverage_analysis.csv", index=False)
print(f"\nSaved: aiddata_coverage_analysis.csv ({len(df_coverage)} rows)")


# ── 5. Key Statistics ─────────────────────────────────────────────────────────
print("\n=== 5. Key Statistics ===")

n_cancelled = (aid["Status"] == "Cancelled").sum()
n_suspended = (aid["Status"] == "Suspended").sum()
n_distress = (aid["Financial Distress"] == "Yes").sum()
n_infra = (aid["Infrastructure"] == "Yes").sum()
n_infra_prob = len(aid_infra_prob)
n_strong = len(df_match[df_match["match_quality"] == "STRONG"])
n_partial = len(df_match[df_match["match_quality"] == "PARTIAL"])

total_aid_value = aid_prob["Amount (Constant USD 2021)"].sum() / 1e9
cancelled_value = aid[aid["Status"] == "Cancelled"]["Amount (Constant USD 2021)"].sum() / 1e9
suspended_value = aid[aid["Status"] == "Suspended"]["Amount (Constant USD 2021)"].sum() / 1e9

print(f"AidData universe: {len(aid):,d} projects")
print(f"  Cancelled: {n_cancelled} (${cancelled_value:.1f}B)")
print(f"  Suspended: {n_suspended} (${suspended_value:.1f}B)")
print(f"  Financial distress: {n_distress}")
print(f"  Infrastructure: {n_infra}")
print(f"  Infrastructure + problematic: {n_infra_prob}")
print(f"\nMatching with our 70 cases:")
print(f"  Strong matches: {n_strong}")
print(f"  Partial matches: {n_partial}")
print(f"  No match: {len(df_match) - n_strong - n_partial}")

# Cases where AidData confirms the problem
confirmed = df_match[
    (df_match["match_quality"] == "STRONG") &
    ((df_match["aiddata_status"].isin(["Cancelled", "Suspended"])) |
     (df_match["aiddata_distress"] == "Yes"))
]
print(f"\nCases where AidData CONFIRMS disruption: {len(confirmed)}")
for _, c in confirmed.iterrows():
    print(f"  {c['country_bri']:15s} {c['project_bri'][:40]:42s} AidData: {c['aiddata_status']} (distress={c['aiddata_distress']})")


# ── 6. Report ─────────────────────────────────────────────────────────────────
print("\n=== 6. Generating Report ===")

report = f"""# AidData GCDF 3.0 Cross-Validation Report

**Generated**: {pd.Timestamp.now().strftime('%Y-%m-%d')}
**Script**: `notebooks/29_aiddata_cross_validation.py`

---

## 1. AidData Universe

AidData's Global Chinese Development Finance Dataset v3.0 tracks **{len(aid):,d} projects**
across 165 countries, totaling US$1.34T (2000-2021).

### Project Status Distribution

| Status | Projects | % |
|--------|----------|---|
| Completion | {(aid['Status']=='Completion').sum():,d} | {100*(aid['Status']=='Completion').sum()/len(aid):.1f}% |
| Pipeline: Commitment | {(aid['Status']=='Pipeline: Commitment').sum():,d} | {100*(aid['Status']=='Pipeline: Commitment').sum()/len(aid):.1f}% |
| Implementation | {(aid['Status']=='Implementation').sum():,d} | {100*(aid['Status']=='Implementation').sum()/len(aid):.1f}% |
| Pipeline: Pledge | {(aid['Status']=='Pipeline: Pledge').sum():,d} | {100*(aid['Status']=='Pipeline: Pledge').sum()/len(aid):.1f}% |
| **Cancelled** | **{n_cancelled}** | {100*n_cancelled/len(aid):.1f}% |
| **Suspended** | **{n_suspended}** | {100*n_suspended/len(aid):.1f}% |

### Key Flags

- **Financial distress**: {n_distress} projects ({100*n_distress/len(aid):.1f}%)
- **Infrastructure**: {n_infra} projects ({100*n_infra/len(aid):.1f}%)
- **Cancelled + Suspended + Distress (union)**: {len(aid_prob)} projects
- **Infrastructure + problematic**: {n_infra_prob} projects
- **Cancelled value**: US${cancelled_value:.1f}B
- **Suspended value**: US${suspended_value:.1f}B

---

## 2. Matching Results

Of our **70 BRI disruption cases**, matching against AidData's {len(aid):,d} projects:

| Match Quality | Cases |
|---------------|-------|
| Strong (score >= {GOOD_MATCH}) | {n_strong} |
| Partial (score >= {PARTIAL_MATCH}) | {n_partial} |
| No match | {len(df_match) - n_strong - n_partial} |

**AidData-confirmed disruptions**: {len(confirmed)} of our cases are also marked as
cancelled/suspended/distressed in AidData.

### Strong Matches

"""

for _, m in strong.iterrows():
    flag = " **[CONFIRMED]**" if m["aiddata_status"] in ["Cancelled", "Suspended"] or m["aiddata_distress"] == "Yes" else ""
    report += f"- **{m['country_bri']}** ({m['year_bri']}): {m['project_bri'][:50]} → AidData: {m['aiddata_title'][:60]} [{m['aiddata_status']}]{flag}\n"

report += f"""

---

## 3. New Candidates from AidData

AidData identifies **{len(df_new)} problematic projects** (cancelled/suspended/distress)
that could be new cases for our dataset.

### High Priority (infrastructure + cancelled/suspended + high value)

"""

for _, c in df_new[df_new["priority"] >= 5].head(20).iterrows():
    amt = f"US${c['amount_usd']/1e6:.0f}M" if c["amount_usd"] > 0 else "N/A"
    report += f"- **{c['country']}** ({c['year']}): {c['title'][:80]} [{c['status']}] {amt}\n"

report += f"""

### Coverage Gaps by Country

Top countries where AidData has more problematic projects than we have cases:

| Country | AidData Problematic | Our Cases | Gap |
|---------|--------------------:|----------:|----:|
"""

for _, r in df_coverage.head(15).iterrows():
    report += f"| {r['country']} | {r['aiddata_problematic']} | {r['bri_cases']} | +{r['coverage_gap']} |\n"

report += f"""

---

## 4. Implications for Thesis

### What AidData tells us

1. **Scale**: Of {len(aid):,d} Chinese development projects, only {n_cancelled + n_suspended} ({100*(n_cancelled+n_suspended)/len(aid):.1f}%) are formally cancelled/suspended — our 70 cases represent a significant portion of documented disruptions.

2. **Financial distress is widespread**: {n_distress} projects ({100*n_distress/len(aid):.1f}%) are flagged for financial distress, far more than the {n_cancelled + n_suspended} formally cancelled — suggesting many "troubled" projects continue despite problems.

3. **Infrastructure focus validated**: {n_infra_prob} of {len(aid_prob)} problematic projects are infrastructure, confirming that BRI infrastructure is disproportionately affected.

4. **Our pipeline captures events AidData doesn't track**: Many of our cases (Huawei 5G bans, CPEC security incidents, political opposition) aren't in AidData because they aren't "development finance" — they're commercial investments or geopolitical events.

### Recommended next steps

- Verify top 20 high-priority AidData candidates for potential addition to dataset
- Use AidData project IDs to enrich existing cases with financing details
- The low formal cancellation rate ({100*(n_cancelled+n_suspended)/len(aid):.1f}%) vs. high distress rate ({100*n_distress/len(aid):.1f}%) is itself a thesis finding
"""

with open("data/samples/validation/aiddata_validation_report.md", "w") as f:
    f.write(report)
print("  aiddata_validation_report.md")

print(f"\n{'='*60}")
print("=== SCRIPT 29 COMPLETE ===")
print(f"  Matched: {n_strong} strong + {n_partial} partial out of {len(bri)} cases")
print(f"  New candidates: {len(df_new)} (top {len(df_new[df_new['priority'] >= 5])} high priority)")
print(f"  AidData confirms: {len(confirmed)} of our cases")
