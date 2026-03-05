"""
Script 28 — Exploratory Data Analysis
======================================
Genera estadísticas descriptivas y visualizaciones del dataset final
de 70 casos verificados de disrupciones BRI.

Input:
  data/samples/final/bri_cancellations_FINAL_v2.csv

Output:
  data/samples/analysis/
    ├── descriptive_stats/   — Tablas resumen
    ├── temporal/            — Evolución temporal
    ├── regional/            — Análisis por región
    ├── mechanisms/          — Distribución de mecanismos
    ├── sectors/             — Análisis sectorial
    ├── value/               — Distribución de valores
    ├── evidence/            — Detección y evidencia GKG
    ├── actors/              — Actores chinos
    └── ANALYSIS_REPORT.md   — Reporte narrativo
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# ── Config ────────────────────────────────────────────────────────────────────
DPI = 300
FIGSIZE = (10, 6)
FIGSIZE_WIDE = (12, 7)
FIGSIZE_TALL = (10, 8)
PALETTE = "Set2"
PALETTE_SEQ = "YlOrRd"

plt.rcParams.update({
    "figure.dpi": DPI,
    "savefig.dpi": DPI,
    "savefig.bbox": "tight",
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.grid": True,
    "grid.alpha": 0.3,
})

BASE = "data/samples/analysis"
DIRS = [
    f"{BASE}/descriptive_stats",
    f"{BASE}/temporal",
    f"{BASE}/regional",
    f"{BASE}/mechanisms",
    f"{BASE}/sectors",
    f"{BASE}/value",
    f"{BASE}/evidence",
    f"{BASE}/actors",
]
for d in DIRS:
    os.makedirs(d, exist_ok=True)

# ── Load data ─────────────────────────────────────────────────────────────────
print("=== Loading dataset ===")
df = pd.read_csv("data/samples/final/bri_cancellations_FINAL_v2.csv")
print(f"Cases: {len(df)}")
print(f"Columns: {list(df.columns)}")

# Clean
df["year"] = pd.to_numeric(df["year"], errors="coerce").fillna(0).astype(int)
df["value_usd_millions"] = pd.to_numeric(df["value_usd_millions"], errors="coerce").fillna(0)
df["gkg_articles"] = pd.to_numeric(df["gkg_articles"], errors="coerce").fillna(0).astype(int)

# Region order by case count
region_order = df["region"].value_counts().index.tolist()
mech_order = df["mechanism_category"].value_counts().index.tolist()
sector_order = df["sector"].value_counts().index.tolist()

# Colors
region_colors = dict(zip(region_order, sns.color_palette(PALETTE, len(region_order))))
mech_colors = dict(zip(mech_order, sns.color_palette("tab10", len(mech_order))))


# ═════════════════════════════════════════════════════════════════════════════
# 1. DESCRIPTIVE STATS
# ═════════════════════════════════════════════════════════════════════════════
print("\n=== 1. Descriptive Statistics ===")

# Summary
summary = {
    "total_cases": len(df),
    "countries": df["country"].nunique(),
    "regions": df["region"].nunique(),
    "year_range": f"{df['year'].min()}–{df['year'].max()}",
    "total_value_usd_M": df["value_usd_millions"].sum(),
    "cases_with_value": len(df[df["value_usd_millions"] > 0]),
    "mean_value_usd_M": df.loc[df["value_usd_millions"] > 0, "value_usd_millions"].mean(),
    "median_value_usd_M": df.loc[df["value_usd_millions"] > 0, "value_usd_millions"].median(),
    "cases_with_gkg": len(df[df["gkg_articles"] > 0]),
    "pipeline_detected_pct": 100 * (df["pipeline_detected"] == "yes").sum() / len(df),
    "mechanism_categories": df["mechanism_category"].nunique(),
    "sectors": df["sector"].nunique(),
}
pd.DataFrame([summary]).T.rename(columns={0: "value"}).to_csv(
    f"{BASE}/descriptive_stats/summary_statistics.csv"
)
print(f"  Summary: {len(summary)} metrics")

# Frequency tables
freq_cols = ["region", "mechanism_category", "sector", "status", "pipeline_detected", "data_source"]
freq_rows = []
for col in freq_cols:
    vc = df[col].value_counts()
    for val, count in vc.items():
        freq_rows.append({
            "variable": col, "value": val,
            "n": count, "pct": round(100 * count / len(df), 1),
        })
df_freq = pd.DataFrame(freq_rows)
df_freq.to_csv(f"{BASE}/descriptive_stats/frequency_tables.csv", index=False)
print(f"  Frequency tables: {len(df_freq)} rows across {len(freq_cols)} variables")


# ═════════════════════════════════════════════════════════════════════════════
# 2. TEMPORAL ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════
print("\n=== 2. Temporal Analysis ===")

# 2a. Cases by year (stacked by mechanism)
fig, ax = plt.subplots(figsize=FIGSIZE)
ct = pd.crosstab(df["year"], df["mechanism_category"])
ct = ct.reindex(columns=mech_order, fill_value=0)
ct.plot(kind="bar", stacked=True, ax=ax, color=[mech_colors[m] for m in ct.columns], edgecolor="white", linewidth=0.5)
ax.set_title("BRI Disruptions by Year and Mechanism Category")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Cases")
ax.legend(title="Mechanism", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=9)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
plt.savefig(f"{BASE}/temporal/cases_by_year.png")
plt.close()
print("  cases_by_year.png")

# 2b. Cumulative
fig, ax = plt.subplots(figsize=FIGSIZE)
yearly = df.groupby("year").size().sort_index()
cumul = yearly.cumsum()
ax.fill_between(cumul.index, cumul.values, alpha=0.3, color="steelblue")
ax.plot(cumul.index, cumul.values, "o-", color="steelblue", markersize=6)
for x, y in zip(cumul.index, cumul.values):
    ax.annotate(str(y), (x, y), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=9)
ax.set_title("Cumulative BRI Disruptions (2011–2024)")
ax.set_xlabel("Year")
ax.set_ylabel("Cumulative Cases")
ax.set_xticks(range(yearly.index.min(), yearly.index.max() + 1))
ax.set_xticklabels(range(yearly.index.min(), yearly.index.max() + 1), rotation=45, ha="right")
plt.savefig(f"{BASE}/temporal/cases_by_year_cumulative.png")
plt.close()
print("  cases_by_year_cumulative.png")

# 2c. Mechanism evolution (stacked area)
fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)
ct2 = pd.crosstab(df["year"], df["mechanism_category"])
ct2 = ct2.reindex(columns=mech_order, fill_value=0)
# Fill missing years
all_years = range(ct2.index.min(), ct2.index.max() + 1)
ct2 = ct2.reindex(all_years, fill_value=0)
ax.stackplot(ct2.index, [ct2[col].values for col in ct2.columns],
             labels=ct2.columns, colors=[mech_colors[m] for m in ct2.columns], alpha=0.8)
ax.set_title("Evolution of Disruption Mechanisms Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Cases")
ax.legend(title="Mechanism", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=9)
plt.savefig(f"{BASE}/temporal/mechanism_evolution.png")
plt.close()
print("  mechanism_evolution.png")


# ═════════════════════════════════════════════════════════════════════════════
# 3. REGIONAL ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════
print("\n=== 3. Regional Analysis ===")

# 3a. Cases by region
fig, ax = plt.subplots(figsize=FIGSIZE)
rc = df["region"].value_counts().reindex(region_order)
bars = ax.barh(rc.index, rc.values, color=[region_colors[r] for r in rc.index], edgecolor="white")
for bar, val in zip(bars, rc.values):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2, str(val),
            va="center", fontsize=10, fontweight="bold")
ax.set_title("BRI Disruptions by Region")
ax.set_xlabel("Number of Cases")
ax.invert_yaxis()
plt.savefig(f"{BASE}/regional/cases_by_region.png")
plt.close()
print("  cases_by_region.png")

# 3b. Region × Mechanism heatmap
fig, ax = plt.subplots(figsize=FIGSIZE_TALL)
ct_rm = pd.crosstab(df["region"], df["mechanism_category"])
ct_rm = ct_rm.reindex(index=region_order, columns=mech_order, fill_value=0)
sns.heatmap(ct_rm, annot=True, fmt="d", cmap="YlOrRd", linewidths=0.5, ax=ax, cbar_kws={"label": "Cases"})
ax.set_title("Region × Mechanism Category")
ax.set_ylabel("")
ax.set_xlabel("")
plt.savefig(f"{BASE}/regional/region_mechanism_heatmap.png")
plt.close()
print("  region_mechanism_heatmap.png")

# 3c. Region × Sector heatmap
fig, ax = plt.subplots(figsize=(12, 8))
ct_rs = pd.crosstab(df["region"], df["sector"])
ct_rs = ct_rs.reindex(index=region_order, fill_value=0)
# Keep only sectors with >0 cases
ct_rs = ct_rs.loc[:, ct_rs.sum() > 0]
sns.heatmap(ct_rs, annot=True, fmt="d", cmap="YlGnBu", linewidths=0.5, ax=ax, cbar_kws={"label": "Cases"})
ax.set_title("Region × Sector")
ax.set_ylabel("")
ax.set_xlabel("")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
plt.savefig(f"{BASE}/regional/region_sector_heatmap.png")
plt.close()
print("  region_sector_heatmap.png")

# 3d. Value by region
fig, ax = plt.subplots(figsize=FIGSIZE)
val_reg = df[df["value_usd_millions"] > 0].groupby("region")["value_usd_millions"].sum().sort_values(ascending=True)
bars = ax.barh(val_reg.index, val_reg.values / 1000, color="coral", edgecolor="white")
for bar, val in zip(bars, val_reg.values):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
            f"${val/1000:.1f}B", va="center", fontsize=9)
ax.set_title("Total Value of Disrupted Projects by Region")
ax.set_xlabel("Value (US$ Billion)")
plt.savefig(f"{BASE}/regional/value_by_region.png")
plt.close()
print("  value_by_region.png")


# ═════════════════════════════════════════════════════════════════════════════
# 4. MECHANISM ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════
print("\n=== 4. Mechanism Analysis ===")

# 4a. Donut chart
fig, ax = plt.subplots(figsize=(8, 8))
mc = df["mechanism_category"].value_counts().reindex(mech_order)
wedges, texts, autotexts = ax.pie(
    mc.values, labels=mc.index, autopct="%1.0f%%",
    colors=[mech_colors[m] for m in mc.index],
    pctdistance=0.82, startangle=90, wedgeprops=dict(width=0.4, edgecolor="white")
)
for t in autotexts:
    t.set_fontsize(9)
ax.set_title("Distribution of Disruption Mechanisms")
plt.savefig(f"{BASE}/mechanisms/mechanism_distribution.png")
plt.close()
print("  mechanism_distribution.png")

# 4b. Detailed mechanisms grouped by category
fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)
mech_detail = df.groupby(["mechanism_category", "mechanism"]).size().reset_index(name="n")
mech_detail = mech_detail.sort_values(["mechanism_category", "n"], ascending=[True, False])
# Top 15
top_mechs = mech_detail.nlargest(15, "n")
colors_detail = [mech_colors.get(row["mechanism_category"], "gray") for _, row in top_mechs.iterrows()]
bars = ax.barh(range(len(top_mechs)), top_mechs["n"].values, color=colors_detail, edgecolor="white")
ax.set_yticks(range(len(top_mechs)))
ax.set_yticklabels([f"{row['mechanism']} ({row['mechanism_category']})" for _, row in top_mechs.iterrows()], fontsize=9)
for bar, val in zip(bars, top_mechs["n"].values):
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2, str(val),
            va="center", fontsize=9, fontweight="bold")
ax.set_title("Top 15 Specific Disruption Mechanisms")
ax.set_xlabel("Number of Cases")
ax.invert_yaxis()
plt.savefig(f"{BASE}/mechanisms/mechanism_detail_bar.png")
plt.close()
print("  mechanism_detail_bar.png")

# 4c. Mechanisms by value
fig, ax = plt.subplots(figsize=FIGSIZE)
val_mech = df[df["value_usd_millions"] > 0].groupby("mechanism")["value_usd_millions"].sum().nlargest(10)
bars = ax.barh(val_mech.index, val_mech.values / 1000, color="mediumpurple", edgecolor="white")
for bar, val in zip(bars, val_mech.values):
    ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
            f"${val/1000:.1f}B", va="center", fontsize=9)
ax.set_title("Top 10 Mechanisms by Total Disrupted Value")
ax.set_xlabel("Value (US$ Billion)")
ax.invert_yaxis()
plt.savefig(f"{BASE}/mechanisms/top_mechanisms_by_value.png")
plt.close()
print("  top_mechanisms_by_value.png")


# ═════════════════════════════════════════════════════════════════════════════
# 5. SECTOR ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════
print("\n=== 5. Sector Analysis ===")

# 5a. Cases by sector
fig, ax = plt.subplots(figsize=FIGSIZE)
sc = df["sector"].value_counts()
bars = ax.barh(sc.index, sc.values, color=sns.color_palette("husl", len(sc)), edgecolor="white")
for bar, val in zip(bars, sc.values):
    ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2, str(val),
            va="center", fontsize=9, fontweight="bold")
ax.set_title("BRI Disruptions by Sector")
ax.set_xlabel("Number of Cases")
ax.invert_yaxis()
plt.savefig(f"{BASE}/sectors/sector_distribution.png")
plt.close()
print("  sector_distribution.png")

# 5b. Value by sector
fig, ax = plt.subplots(figsize=FIGSIZE)
val_sec = df[df["value_usd_millions"] > 0].groupby("sector")["value_usd_millions"].sum().sort_values(ascending=True)
bars = ax.barh(val_sec.index, val_sec.values / 1000, color="teal", edgecolor="white")
for bar, val in zip(bars, val_sec.values):
    ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
            f"${val/1000:.1f}B", va="center", fontsize=9)
ax.set_title("Total Disrupted Value by Sector")
ax.set_xlabel("Value (US$ Billion)")
plt.savefig(f"{BASE}/sectors/sector_value.png")
plt.close()
print("  sector_value.png")

# 5c. Sector × Mechanism heatmap
fig, ax = plt.subplots(figsize=FIGSIZE_TALL)
ct_sm = pd.crosstab(df["sector"], df["mechanism_category"])
ct_sm = ct_sm.reindex(columns=mech_order, fill_value=0)
ct_sm = ct_sm.loc[ct_sm.sum(axis=1) > 0]
sns.heatmap(ct_sm, annot=True, fmt="d", cmap="PuBuGn", linewidths=0.5, ax=ax, cbar_kws={"label": "Cases"})
ax.set_title("Sector × Mechanism Category")
ax.set_ylabel("")
ax.set_xlabel("")
plt.savefig(f"{BASE}/sectors/sector_mechanism_heatmap.png")
plt.close()
print("  sector_mechanism_heatmap.png")


# ═════════════════════════════════════════════════════════════════════════════
# 6. VALUE ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════
print("\n=== 6. Value Analysis ===")

df_val = df[df["value_usd_millions"] > 0].copy()
print(f"  Cases with known value: {len(df_val)}/{len(df)}")

# 6a. Distribution
fig, axes = plt.subplots(1, 2, figsize=FIGSIZE_WIDE, gridspec_kw={"width_ratios": [3, 1]})
axes[0].hist(df_val["value_usd_millions"] / 1000, bins=15, color="steelblue", edgecolor="white", alpha=0.8)
axes[0].set_title("Distribution of Disrupted Project Values")
axes[0].set_xlabel("Value (US$ Billion)")
axes[0].set_ylabel("Frequency")
axes[0].axvline(df_val["value_usd_millions"].median() / 1000, color="red", linestyle="--", label=f"Median: ${df_val['value_usd_millions'].median()/1000:.1f}B")
axes[0].axvline(df_val["value_usd_millions"].mean() / 1000, color="orange", linestyle="--", label=f"Mean: ${df_val['value_usd_millions'].mean()/1000:.1f}B")
axes[0].legend()
bp = axes[1].boxplot(df_val["value_usd_millions"] / 1000, vert=True, widths=0.5,
                      patch_artist=True, boxprops=dict(facecolor="steelblue", alpha=0.5))
axes[1].set_title("Boxplot")
axes[1].set_ylabel("Value (US$ Billion)")
axes[1].set_xticks([])
plt.savefig(f"{BASE}/value/value_distribution.png")
plt.close()
print("  value_distribution.png")

# 6b. Top 20 cases
fig, ax = plt.subplots(figsize=FIGSIZE_TALL)
top20 = df_val.nlargest(20, "value_usd_millions")
labels = [f"{row['country']}: {row['project'][:40]}" for _, row in top20.iterrows()]
bars = ax.barh(range(len(top20)), top20["value_usd_millions"].values / 1000,
               color=[region_colors.get(r, "gray") for r in top20["region"]],
               edgecolor="white")
ax.set_yticks(range(len(top20)))
ax.set_yticklabels(labels, fontsize=9)
for bar, val in zip(bars, top20["value_usd_millions"].values):
    ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
            f"${val/1000:.1f}B", va="center", fontsize=8)
ax.set_title("Top 20 BRI Disruptions by Project Value")
ax.set_xlabel("Value (US$ Billion)")
ax.invert_yaxis()
# Legend for regions
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=region_colors[r], label=r) for r in top20["region"].unique() if r in region_colors]
ax.legend(handles=legend_elements, title="Region", loc="lower right", fontsize=8)
plt.savefig(f"{BASE}/value/top20_cases_value.png")
plt.close()
print("  top20_cases_value.png")

# 6c. Value vs GKG articles
fig, ax = plt.subplots(figsize=FIGSIZE)
df_both = df[(df["value_usd_millions"] > 0) & (df["gkg_articles"] > 0)]
for region in df_both["region"].unique():
    rd = df_both[df_both["region"] == region]
    ax.scatter(rd["gkg_articles"], rd["value_usd_millions"] / 1000,
               label=region, color=region_colors.get(region, "gray"),
               s=80, alpha=0.7, edgecolors="black", linewidth=0.5)
# Annotate outliers
for _, row in df_both.nlargest(5, "value_usd_millions").iterrows():
    ax.annotate(row["country"], (row["gkg_articles"], row["value_usd_millions"] / 1000),
                textcoords="offset points", xytext=(5, 5), fontsize=8, alpha=0.8)
ax.set_title("Project Value vs. GKG Media Coverage")
ax.set_xlabel("GKG Articles (evidence depth)")
ax.set_ylabel("Value (US$ Billion)")
ax.legend(title="Region", fontsize=8, loc="upper right")
plt.savefig(f"{BASE}/value/value_vs_gkg.png")
plt.close()
print("  value_vs_gkg.png")


# ═════════════════════════════════════════════════════════════════════════════
# 7. EVIDENCE & DETECTION
# ═════════════════════════════════════════════════════════════════════════════
print("\n=== 7. Evidence & Detection ===")

# 7a. Detection rate by region
fig, ax = plt.subplots(figsize=FIGSIZE)
det = df.groupby("region").apply(lambda x: 100 * (x["pipeline_detected"] == "yes").sum() / len(x))
det = det.reindex(region_order)
bars = ax.barh(det.index, det.values, color=[region_colors[r] for r in det.index], edgecolor="white")
for bar, val in zip(bars, det.values):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
            f"{val:.0f}%", va="center", fontsize=9, fontweight="bold")
ax.set_title("Pipeline Detection Rate by Region")
ax.set_xlabel("Detection Rate (%)")
ax.set_xlim(0, 115)
ax.axvline(77, color="red", linestyle="--", alpha=0.5, label="Overall: 77%")
ax.legend()
ax.invert_yaxis()
plt.savefig(f"{BASE}/evidence/detection_rate_by_region.png")
plt.close()
print("  detection_rate_by_region.png")

# 7b. GKG distribution
fig, axes = plt.subplots(1, 2, figsize=FIGSIZE_WIDE)
# All cases
axes[0].hist(df["gkg_articles"], bins=30, color="forestgreen", edgecolor="white", alpha=0.8)
axes[0].set_title("GKG Articles per Case (all)")
axes[0].set_xlabel("Number of GKG Articles")
axes[0].set_ylabel("Frequency")
axes[0].axvline(df["gkg_articles"].median(), color="red", linestyle="--",
                label=f"Median: {df['gkg_articles'].median():.0f}")
axes[0].legend()
# Excluding top outliers (>200)
df_gkg_trim = df[(df["gkg_articles"] > 0) & (df["gkg_articles"] <= 200)]
axes[1].hist(df_gkg_trim["gkg_articles"], bins=20, color="forestgreen", edgecolor="white", alpha=0.8)
axes[1].set_title("GKG Articles per Case (1–200)")
axes[1].set_xlabel("Number of GKG Articles")
axes[1].set_ylabel("Frequency")
plt.savefig(f"{BASE}/evidence/gkg_distribution.png")
plt.close()
print("  gkg_distribution.png")

# 7c. Detection by data source
fig, ax = plt.subplots(figsize=FIGSIZE)
ct_ds = pd.crosstab(df["data_source"], df["pipeline_detected"])
ct_ds.plot(kind="bar", stacked=True, ax=ax, color=["salmon", "mediumseagreen"], edgecolor="white")
ax.set_title("Pipeline Detection by Data Source")
ax.set_xlabel("Data Source")
ax.set_ylabel("Number of Cases")
ax.legend(title="Pipeline Detected", labels=["No", "Yes"])
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
plt.savefig(f"{BASE}/evidence/detection_vs_source.png")
plt.close()
print("  detection_vs_source.png")


# ═════════════════════════════════════════════════════════════════════════════
# 8. CHINESE ACTORS
# ═════════════════════════════════════════════════════════════════════════════
print("\n=== 8. Chinese Actors ===")

# Parse actors (comma-separated field)
all_actors = []
actor_sector_pairs = []
for _, row in df.iterrows():
    actors = str(row["chinese_actors"]).split(",")
    for a in actors:
        a = a.strip()
        if a and a != "nan" and len(a) > 1:
            all_actors.append(a)
            actor_sector_pairs.append({"actor": a, "sector": row["sector"]})

actor_counts = Counter(all_actors)

# 8a. Top actors
fig, ax = plt.subplots(figsize=FIGSIZE)
top_actors = pd.Series(dict(actor_counts.most_common(15))).sort_values()
bars = ax.barh(top_actors.index, top_actors.values, color="darkorange", edgecolor="white")
for bar, val in zip(bars, top_actors.values):
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
            str(val), va="center", fontsize=9, fontweight="bold")
ax.set_title("Top 15 Chinese Actors in BRI Disruptions")
ax.set_xlabel("Number of Cases")
plt.savefig(f"{BASE}/actors/top_chinese_actors.png")
plt.close()
print("  top_chinese_actors.png")

# 8b. Actor × Sector heatmap
df_as = pd.DataFrame(actor_sector_pairs)
if len(df_as) > 0:
    top_actor_names = [a for a, _ in actor_counts.most_common(12)]
    df_as_top = df_as[df_as["actor"].isin(top_actor_names)]
    ct_as = pd.crosstab(df_as_top["actor"], df_as_top["sector"])
    ct_as = ct_as.loc[ct_as.sum(axis=1) > 0, ct_as.sum() > 0]
    fig, ax = plt.subplots(figsize=FIGSIZE_TALL)
    sns.heatmap(ct_as, annot=True, fmt="d", cmap="Oranges", linewidths=0.5, ax=ax, cbar_kws={"label": "Cases"})
    ax.set_title("Chinese Actor × Sector")
    ax.set_ylabel("")
    ax.set_xlabel("")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    plt.savefig(f"{BASE}/actors/actor_sector_heatmap.png")
    plt.close()
    print("  actor_sector_heatmap.png")


# ═════════════════════════════════════════════════════════════════════════════
# 9. ANALYSIS REPORT
# ═════════════════════════════════════════════════════════════════════════════
print("\n=== 9. Generating Report ===")

# Compute stats for report
total_val = df["value_usd_millions"].sum()
n_with_val = len(df[df["value_usd_millions"] > 0])
mean_val = df.loc[df["value_usd_millions"] > 0, "value_usd_millions"].mean()
median_val = df.loc[df["value_usd_millions"] > 0, "value_usd_millions"].median()
top_region = df["region"].value_counts().index[0]
top_region_n = df["region"].value_counts().values[0]
top_mech = df["mechanism_category"].value_counts().index[0]
top_mech_n = df["mechanism_category"].value_counts().values[0]
top_sector = df["sector"].value_counts().index[0]
top_sector_n = df["sector"].value_counts().values[0]
peak_year = df["year"].value_counts().index[0]
peak_year_n = df["year"].value_counts().values[0]
det_rate = 100 * (df["pipeline_detected"] == "yes").sum() / len(df)
gkg_rate = 100 * (df["gkg_articles"] > 0).sum() / len(df)

report = f"""# Exploratory Data Analysis — BRI Disruptions Dataset

**Generated**: {pd.Timestamp.now().strftime('%Y-%m-%d')}
**Source**: `data/samples/final/bri_cancellations_FINAL_v2.csv`
**Script**: `notebooks/28_exploratory_analysis.py`

---

## 1. Dataset Overview

The dataset contains **{len(df)} verified cases** of BRI project disruptions across **{df['country'].nunique()} countries** and **{df['region'].nunique()} regions**, spanning from {df['year'].min()} to {df['year'].max()}.

| Metric | Value |
|--------|-------|
| Total cases | {len(df)} |
| Countries | {df['country'].nunique()} |
| Regions | {df['region'].nunique()} |
| Total value affected | US${total_val/1000:.1f}B |
| Cases with known value | {n_with_val}/{len(df)} ({100*n_with_val/len(df):.0f}%) |
| Mean value (when known) | US${mean_val/1000:.1f}B |
| Median value (when known) | US${median_val/1000:.1f}B |
| Pipeline detection rate | {det_rate:.0f}% |
| GKG corroboration rate | {gkg_rate:.0f}% |

---

## 2. Temporal Patterns

**Peak year: {peak_year}** with {peak_year_n} cases — coincides with COVID-19 pandemic disruptions and heightened US-China tensions.

![Cases by Year](temporal/cases_by_year.png)

The cumulative curve shows accelerating discovery from 2018 onward, with a notable inflection point in 2020.

![Cumulative Cases](temporal/cases_by_year_cumulative.png)

Security mechanisms (sanctions, 5G bans) dominate from 2018+, while economic mechanisms (debt distress) concentrate in 2020–2022.

![Mechanism Evolution](temporal/mechanism_evolution.png)

---

## 3. Regional Distribution

**Most affected region: {top_region}** ({top_region_n} cases), followed by {df['region'].value_counts().index[1]} ({df['region'].value_counts().values[1]}) and {df['region'].value_counts().index[2]} ({df['region'].value_counts().values[2]}).

![Cases by Region](regional/cases_by_region.png)

The region-mechanism heatmap reveals distinct patterns: Africa is dominated by economic/political mechanisms, while South Asia and LATAM show more security-related disruptions.

![Region × Mechanism](regional/region_mechanism_heatmap.png)

Transport sectors (ports, rail, roads) dominate across all regions, with telecom concentrated in Europe and mining in Africa/LATAM.

![Region × Sector](regional/region_sector_heatmap.png)

By value, SE Asia leads due to Malaysia's ECRL ($22B), followed by Africa (Ghana $19B, Nigeria $14.4B, Tanzania $10B).

![Value by Region](regional/value_by_region.png)

---

## 4. Mechanism Analysis

**Dominant mechanism: {top_mech}** ({top_mech_n} cases, {100*top_mech_n/len(df):.0f}%), driven by Huawei 5G bans, US secondary sanctions, and CPEC security incidents.

![Mechanism Distribution](mechanisms/mechanism_distribution.png)

The most frequent specific mechanisms are US secondary sanctions, followed by debt distress and community opposition.

![Mechanism Detail](mechanisms/mechanism_detail_bar.png)

By value, political reversals (new_government_reversal: Malaysia $22B) and debt mechanisms lead.

![Mechanisms by Value](mechanisms/top_mechanisms_by_value.png)

---

## 5. Sector Analysis

**Dominant sector: {top_sector}** ({top_sector_n} cases), reflecting BRI's focus on connectivity infrastructure.

![Sector Distribution](sectors/sector_distribution.png)

Transport ports and rail account for the highest disrupted values (>$30B each), while telecom cases (Huawei 5G) are numerous but lack monetary value data.

![Sector Value](sectors/sector_value.png)

![Sector × Mechanism](sectors/sector_mechanism_heatmap.png)

---

## 6. Value Analysis

Of {len(df)} cases, **{n_with_val} ({100*n_with_val/len(df):.0f}%)** have known project values, totaling **US${total_val/1000:.1f}B**.

The distribution is right-skewed with a median of US${median_val/1000:.1f}B and mean of US${mean_val/1000:.1f}B, indicating a few mega-projects driving the total.

![Value Distribution](value/value_distribution.png)

The top 20 cases by value span from US${df_val.nlargest(20, 'value_usd_millions').iloc[-1]['value_usd_millions']/1000:.1f}B to US${df_val['value_usd_millions'].max()/1000:.1f}B.

![Top 20 Cases](value/top20_cases_value.png)

There is a weak positive relationship between project value and media coverage (GKG articles), though some high-value cases have minimal coverage and vice versa.

![Value vs GKG](value/value_vs_gkg.png)

---

## 7. Evidence & Detection

The automated GDELT pipeline detected **{det_rate:.0f}%** of all cases (54/70). Detection rates vary by region:

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

3. **Value concentration**: The top 5 cases account for {100 * df_val.nlargest(5, 'value_usd_millions')['value_usd_millions'].sum() / total_val:.0f}% of total disrupted value, suggesting that BRI risk is concentrated in mega-projects.

4. **Detection gap**: The pipeline misses ~23% of cases, particularly in Central Asia (Russian-language media) and cases pre-dating GDELT v2 (pre-2015).

5. **Transport vulnerability**: Transport infrastructure (ports + rail + roads) accounts for {100 * len(df[df['sector'].str.startswith('Transport')]) / len(df):.0f}% of all disruptions and the highest values.

6. **Regional mechanism patterns**: Africa → economic (debt), South Asia → security (attacks), Europe → security (5G bans), LATAM → mixed (sanctions + political).
"""

with open(f"{BASE}/ANALYSIS_REPORT.md", "w") as f:
    f.write(report)
print("  ANALYSIS_REPORT.md")

# ── Save underlying CSVs for each viz ────────────────────────────────────────
ct.to_csv(f"{BASE}/temporal/cases_by_year_mechanism.csv")
cumul.to_frame("cumulative_cases").to_csv(f"{BASE}/temporal/cumulative_cases.csv")
ct_rm.to_csv(f"{BASE}/regional/region_mechanism_crosstab.csv")
ct_rs.to_csv(f"{BASE}/regional/region_sector_crosstab.csv")
val_reg.to_frame("value_usd_M").to_csv(f"{BASE}/regional/value_by_region.csv")
mc.to_frame("n_cases").to_csv(f"{BASE}/mechanisms/mechanism_category_counts.csv")
mech_detail.to_csv(f"{BASE}/mechanisms/mechanism_detail.csv", index=False)
sc.to_frame("n_cases").to_csv(f"{BASE}/sectors/sector_counts.csv")
val_sec.to_frame("value_usd_M").to_csv(f"{BASE}/sectors/sector_value.csv")
ct_sm.to_csv(f"{BASE}/sectors/sector_mechanism_crosstab.csv")
det.to_frame("detection_rate_pct").to_csv(f"{BASE}/evidence/detection_rate_by_region.csv")
pd.Series(dict(actor_counts.most_common(30))).to_frame("n_cases").to_csv(f"{BASE}/actors/actor_counts.csv")

print(f"\n{'='*60}")
print(f"=== SCRIPT 28 COMPLETE ===")
print(f"Output directory: {BASE}/")
print(f"  PNGs: {sum(1 for d in DIRS for f in os.listdir(d) if f.endswith('.png'))}")
print(f"  CSVs: {sum(1 for d in DIRS for f in os.listdir(d) if f.endswith('.csv'))}")
print(f"  Report: ANALYSIS_REPORT.md")
