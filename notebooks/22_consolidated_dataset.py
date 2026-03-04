"""
Script 22: Dataset Consolidado de Cancelaciones/Fricciones BRI
==============================================================
Combina:
1. Señales LATAM verificadas manualmente (Scripts 18-20)
2. Señales globales del pipeline GDELT (Script 21)
3. Casos conocidos de la literatura que el pipeline NO capturó

Output: data/samples/final/bri_cancellations_consolidated.csv
        data/samples/final/bri_cancellations_consolidated.md
"""

import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT_DIR = BASE / "data/samples/final"

# ══════════════════════════════════════════════════════════════════
# CASOS VERIFICADOS — Compilación exhaustiva
# ══════════════════════════════════════════════════════════════════

cases = []

def add(country, year, project, status, mechanism, value_usd, actors, source,
        pipeline_detected, description):
    cases.append({
        'country': country,
        'region': '',  # filled later
        'year': year,
        'project': project,
        'status': status,
        'mechanism': mechanism,
        'value_usd_millions': value_usd,
        'chinese_actors': actors,
        'source': source,
        'pipeline_detected': pipeline_detected,
        'description': description,
    })

# ── LATAM (9 verificados + 5 nuevos de la literatura) ──

add('Chile', 2018, 'SQM Lithium Acquisition', 'blocked',
    'political_rejection', 4000, 'Tianqi Lithium',
    'nasdaq.com', 'yes',
    'Chilean government blocks sale of SQM shares to Chinese lithium company Tianqi')

add('Chile', 2020, 'Commodity Contracts (Force Majeure)', 'suspended',
    'force_majeure', 0, 'Sinopec, CNOOC',
    'economia.uol.com.br (Bloomberg)', 'yes',
    'Chinese SOEs invoke force majeure on copper/LNG contracts during early COVID')

add('Ecuador', 2019, 'Shrimp Export Approval', 'suspended',
    'market_access_restriction', 0, 'Chinese customs authority',
    'undercurrentnews.com', 'yes',
    'China suspends shrimp export approval for Santa Priscila and Omarsa')

add('Venezuela', 2018, 'ZTE Surveillance Infrastructure', 'sanctioned',
    'us_secondary_sanctions', 0, 'ZTE',
    'telecomstechnews.com', 'yes',
    'US sanctions ZTE for installing surveillance infrastructure in Venezuela')

add('Venezuela', 2019, 'CNPC Oil Operations', 'suspended',
    'us_secondary_sanctions', 0, 'CNPC/PetroChina',
    'bloombergquint.com', 'yes',
    'CNPC suspends Venezuelan oil operations to avoid US sanctions')

add('Venezuela', 2020, 'Internet Censorship Infrastructure', 'sanctioned',
    'us_secondary_sanctions', 0, 'Unknown Chinese firm',
    'republicworld.com', 'yes',
    'US sanctions Chinese firm for role in Venezuela internet crackdown')

add('Brasil', 2017, 'Tamoios Highway Concession', 'withdrawn',
    'investor_withdrawal', 0, 'Chinese consortium (unnamed)',
    'bnamericas.com', 'yes',
    'Chinese investors may not pursue São Paulo Tamoios highway concession')

add('Argentina', 2020, 'Pork Production Deal', 'delayed',
    'environmental_opposition', 0, 'Chinese importers',
    'msn.com (Reuters)', 'yes',
    'Argentina delays China pork export MoU amid 200+ NGO environmental protests')

add('Perú', 2024, 'Chancay Port', 'disputed',
    'investor_state_arbitration', 3600, 'COSCO/Chinese consortium',
    'globalarbitrationreview.com', 'yes',
    'Chinese consortium threatens arbitration over exclusive operating rights')

# New LATAM from literature (not in pipeline)
add('Mexico', 2014, 'Mexico City-Queretaro HSR', 'cancelled',
    'corruption_scandal', 3750, 'China Railway Construction Corp',
    'fortune.com', 'no',
    'Mexico revokes $3.75B bullet train contract to Chinese-led consortium after corruption allegations')

add('Costa Rica', 2016, 'SORESCO Oil Refinery', 'cancelled',
    'corruption_scandal', 1200, 'CNPC, Huanqiu Contracting, China Development Bank',
    'ticotimes.net', 'no',
    'Costa Rica terminates $1.2B Chinese refinery after corruption scandals. $61M lost.')

add('Bolivia', 2024, 'Salar de Uyuni Lithium', 'judicially_suspended',
    'indigenous_opposition', 2000, 'CBC consortium (CATL affiliate)',
    'mining.com', 'no',
    'Bolivian court suspends Chinese and Russian lithium deals after indigenous community complaints')

add('Ecuador', 2018, 'Coca Codo Sinclair Dam', 'disputed',
    'quality_defects', 2250, 'Sinohydro/PowerChina',
    'dialogue.earth', 'no',
    '$2.25B dam with 7,648 cracks, San Rafael Falls collapse. PowerChina pays $400M compensation.')

add('Venezuela', 2018, 'Unipec Oil Tankers', 'withdrawn',
    'us_secondary_sanctions', 0, 'Unipec (CNPC trading arm)',
    'reuters.com', 'yes',
    'Unipec bans use of oil tankers linked to Venezuela to avoid US sanctions')

# ── ASIA SUR (Pakistan CPEC + others) ──

add('Pakistán', '2017-2024', 'Gwadar Port Complex', 'under_attack',
    'terrorism', 0, 'China Overseas Port Holding',
    'apnews.com, timesofindia.com', 'yes',
    'Multiple BLA attacks on Gwadar port (2017, 2021, 2022, 2024). Airport delayed 3 times.')

add('Pakistán', 2021, 'Dasu Hydropower Dam', 'suspended',
    'terrorism', 0, 'China Gezhouba Group',
    'etemaaddaily.com', 'yes',
    'Suicide bombing kills 5 Chinese engineers. Construction paused on Dasu + Diamer-Bhasha dams.')

add('Pakistán', 2021, 'Gwadar Anti-CPEC Protests', 'protested',
    'community_opposition', 0, 'CPEC projects broadly',
    'timesofindia.com', 'yes',
    'Gwadar Haq Do Tehreek: local fishing communities protest Chinese trawlers and CPEC impact')

add('Pakistán', 2020, 'CPEC Corruption Row', 'delayed',
    'corruption_scandal', 0, 'Various CPEC contractors',
    'timesofindia.com', 'yes',
    'Xi Jinping postpones Pakistan visit amid CPEC corruption allegations at Sahiwal/Port Qasim plants')

add('Pakistán', 2024, 'Tarbela Dam Extension', 'suspended',
    'terrorism', 0, 'Chinese contractor',
    'dawn.com', 'yes',
    'Chinese company suspends work on Tarbela extension project due to terror threats')

add('Sri Lanka', 2017, 'Hambantota Port', 'coerced_lease',
    'debt_distress', 1120, 'China Merchants Port Holdings',
    'bdnews24.com, customstoday.com.pk', 'yes',
    'Sri Lanka leases Hambantota port to China for 99 years after defaulting on loans. Violent protests.')

add('Sri Lanka', 2020, 'Colombo Port City', 'sanctioned',
    'us_secondary_sanctions', 1400, 'CCCC subsidiaries',
    'sundaytimes.lk', 'yes',
    'US sanctions CCCC (Colombo Port City builder) over South China Sea island construction')

add('Myanmar', 2011, 'Myitsone Dam', 'suspended',
    'political_rejection', 3600, 'China Power Investment Corp',
    'thediplomat.com', 'no',
    'President Thein Sein suspends $3.6B dam citing "will of the people." 90% electricity was for China.')

add('Nepal', 2024, 'Pokhara International Airport', 'white_elephant',
    'community_opposition', 216, 'China Exim Bank (funder)',
    'newsx.com', 'yes',
    'Chinese-funded airport opens 2023 but almost no international flights. Protests against Chinese influence.')

add('Bangladesh', 2016, 'Banshkhali Coal Power Plant', 'protested',
    'community_opposition', 0, 'SEPCO (Shandong Electric Power)',
    'dnaindia.com', 'yes',
    'Police kill 4-5 protesters opposing Chinese-backed 1,320MW coal plant. Forced land acquisition.')

add('Maldives', 2018, 'Sinamale Bridge + Others', 'debt_crisis',
    'debt_distress', 0, 'CCCC (bridge builder)',
    'dailymail.co.uk (AFP)', 'yes',
    'Chinese bridge pushes Maldives deeper in debt. Opposition warns of debt trap.')

# ── ASIA SE ──

add('Malasia', 2018, 'ECRL + Two Pipelines', 'cancelled_then_renegotiated',
    'new_government_reversal', 22000, 'CCCC, China Petroleum Pipeline Bureau',
    'straitstimes.com', 'yes',
    'PM Mahathir cancels ECRL and two pipelines ($22B). ECRL later renegotiated at lower cost.')

add('Philippines', 2023, 'Three Railway Projects', 'cancelled',
    'geopolitical_tension', 4900, 'China Exim Bank',
    'thediplomat.com', 'no',
    'Marcos drops Chinese funding for 3 railways ($4.9B) amid SCS tensions. China demanded 3% vs Japan 0.01%.')

add('Indonesia', 2020, 'Jakarta-Bandung HSR Debt Concerns', 'debt_anxiety',
    'debt_distress', 7300, 'China Railway, KCIC consortium',
    'thejakartapost.com, devdiscourse.com', 'yes',
    'Indonesia worries about Sri Lanka-like debt trap. HSR requests 30-year concession extension.')

add('Thailand', 2020, 'Kra Canal', 'cancelled',
    'political_rejection', 0, 'Chinese proponents',
    'msn.com', 'yes',
    'Thailand scraps Kra Canal project backed by China')

# ── ASIA CENTRAL ──

add('Kazajistán', 2019, '55 Joint Industrial Projects', 'stalled',
    'community_opposition', 0, 'Various Chinese companies',
    'carnegieendowment.org', 'no',
    'Anti-China protests in 6 cities over fears of Chinese workers and economic dependence')

add('Kirguistán', 2020, 'At-Bashi Free Trade Zone', 'cancelled',
    'community_opposition', 275, 'Chinese government',
    'thediplomat.com', 'no',
    '$275M logistics center cancelled after anti-China protests')

# ── AFRICA ──

add('Sierra Leona', 2018, 'Mamamah International Airport', 'cancelled',
    'new_government_reversal', 318, 'China Railway Seventh Group, China Exim Bank',
    'cnn.com', 'no',
    'New president Bio cancels $318M airport as "uneconomical." IMF raised debt concerns.')

add('Kenia', 2020, 'Lamu Coal Power Plant', 'cancelled',
    'environmental_opposition', 2000, 'Amu Power, ICBC (withdrew)',
    'business-humanrights.org', 'no',
    'Courts cancel environmental license. ICBC withdraws financing. Near UNESCO World Heritage Site.')

add('Tanzania', 2019, 'Bagamoyo Mega-Port', 'suspended',
    'predatory_terms_rejected', 10000, 'China Merchants Holdings',
    'orfonline.org', 'no',
    'President Magufuli suspends $10B port. China demanded 99-year lease and no competing ports.')

add('Zimbabwe', 2021, 'Sengwa Coal Power Station', 'financing_withdrawn',
    'climate_policy', 3000, 'ICBC (withdrew), RioZim',
    'business-humanrights.org', 'no',
    'ICBC withdraws after China 2021 pledge to end overseas coal financing')

add('Uganda', 2023, 'Kampala-Malaba SGR Railway', 'cancelled',
    'financing_failure', 2300, 'CHEC, China Exim Bank',
    'aljazeera.com', 'no',
    'Uganda fires CHEC after 8 years of Chinese financing delays. Replaced with Turkish contractor.')

add('Nigeria', 2021, 'Railway Financing', 'abandoned',
    'debt_concerns', 14400, 'Standard Chartered (replacement)',
    'breitbart.com', 'yes',
    'Nigeria abandons Chinese financing for $14.4B railroad projects due to debt concerns')

add('Ghana', 2017, '$19B China Loan Package', 'opposed',
    'political_opposition', 19000, 'Sinohydro (bauxite deal)',
    'businessghana.com', 'yes',
    'Parliamentary opposition attacks $19B Chinese loan package including $2B Sinohydro bauxite deal')

add('Kenia', 2022, 'SGR Loan Default', 'defaulted',
    'debt_distress', 1300, 'China Exim Bank',
    'nation.africa', 'yes',
    'China fines Kenya $1.3B for defaulting on SGR railway loans')

add('Zambia', 2020, 'Chinese Loans Default', 'defaulted',
    'debt_distress', 6000, 'Various Chinese creditors',
    'lusakatimes.com', 'yes',
    'Zambia defaults on sovereign debt. Calls to renegotiate ~$6B Chinese loans.')

add('DRC', 2021, 'Sicomines Mining Contracts', 'renegotiated',
    'new_government_reversal', 6000, 'Sicomines (Chinese consortium)',
    'business-standard.com', 'no',
    'President Tshisekedi calls for review of 2008 mining contracts, arguing DRC was shortchanged')

# ── EUROPA ──

add('Australia', 2021, 'Victoria BRI Agreement', 'cancelled',
    'geopolitical_tension', 0, 'Chinese government',
    'aninews.in, sbs.com.au', 'yes',
    'Federal government cancels Victoria state BRI deal. China retaliates suspending economic dialogue.')

add('Australia', 2018, 'Huawei/ZTE 5G Network', 'banned',
    'security_concern', 0, 'Huawei, ZTE',
    'obiaks.com', 'yes',
    'Australia bans Huawei and ZTE from 5G network rollout citing national security')

add('Italia', 2023, 'Belt and Road Initiative MoU', 'withdrawn',
    'geopolitical_realignment', 0, 'Chinese government',
    'afr.com, voanews.com', 'yes',
    'Italy formally exits BRI. First G7 country to withdraw after joining in 2019.')

add('Rumania', 2020, 'Cernavoda Nuclear Units 3 & 4', 'cancelled',
    'us_geopolitical_pressure', 0, 'China General Nuclear Power Corp (CGN)',
    'balkaninsight.com', 'no',
    'Romania terminates agreement with CGN under US pressure. US replaces China as nuclear partner.')

add('Montenegro', 2014, 'Bar-Boljare Highway', 'debt_trap',
    'debt_distress', 944, 'China Road and Bridge Corp, China Exim Bank',
    'npr.org', 'no',
    '$944M loan (~25% GDP) for 41km highway. Montenegro seeks EU/US refinancing.')

add('Alemania', 2024, 'Huawei/ZTE 5G Network', 'banned',
    'security_concern', 0, 'Huawei, ZTE',
    'scmp.com, poandpo.com', 'yes',
    'Germany restricts Huawei/ZTE from core 5G networks')

add('Bielorrusia', 2020, 'BRI Projects (Great Stone Industrial Park)', 'uncertain',
    'political_instability', 0, 'Various Chinese companies',
    'scmp.com', 'yes',
    '2020 Belarus protests create uncertainty for Chinese BRI projects including Great Stone park')

add('R.Unido', 2020, 'Huawei 5G Network', 'banned',
    'security_concern', 0, 'Huawei',
    'telecompaper.com', 'yes',
    'UK reverses Huawei decision, bans from 5G after US pressure and security review')

add('EU', 2021, 'Comprehensive Agreement on Investment', 'frozen',
    'human_rights_sanctions', 0, 'Chinese government',
    'aninews.in', 'yes',
    'European Parliament freezes CAI ratification 599-30 after China counter-sanctions MEPs over Xinjiang')

# ── MEDIO ORIENTE ──

add('Israel', 2019, 'Haifa Port Terminal', 'scrutinized',
    'us_geopolitical_pressure', 0, 'Shanghai International Port Group',
    'thestar.com.my', 'yes',
    'US officials warn Israel about security risks of Chinese 25-year lease near naval base')

add('Rusia', 2022, 'BRI Northern Corridor', 'disrupted',
    'geopolitical_conflict', 0, 'BRI logistics broadly',
    'oilprice.com', 'yes',
    'Russia Ukraine invasion disrupts BRI northern transit corridor through Central Asia to Europe')

# ── Region mapping ──
REGION_MAP = {
    'Chile': 'LATAM', 'Ecuador': 'LATAM', 'Venezuela': 'LATAM', 'Brasil': 'LATAM',
    'Argentina': 'LATAM', 'Perú': 'LATAM', 'Mexico': 'LATAM', 'Costa Rica': 'LATAM',
    'Bolivia': 'LATAM', 'Pakistán': 'Asia Sur', 'Sri Lanka': 'Asia Sur',
    'Myanmar': 'Asia Sur', 'Nepal': 'Asia Sur', 'Bangladesh': 'Asia Sur',
    'Maldives': 'Asia Sur', 'Malasia': 'Asia SE', 'Philippines': 'Asia SE',
    'Indonesia': 'Asia SE', 'Thailand': 'Asia SE', 'Kazajistán': 'Asia Central',
    'Kirguistán': 'Asia Central', 'Sierra Leona': 'Africa', 'Kenia': 'Africa',
    'Tanzania': 'Africa', 'Zimbabwe': 'Africa', 'Uganda': 'Africa',
    'Nigeria': 'Africa', 'Ghana': 'Africa', 'Zambia': 'Africa', 'DRC': 'Africa',
    'Australia': 'Oceania', 'Italia': 'Europa W', 'Rumania': 'Europa E',
    'Montenegro': 'Europa E', 'Alemania': 'Europa W', 'Bielorrusia': 'Europa E',
    'R.Unido': 'Europa W', 'EU': 'Europa W', 'Israel': 'Medio Oriente',
    'Rusia': 'Eurasia',
}

for c in cases:
    c['region'] = REGION_MAP.get(c['country'], 'Other')

# ══════════════════════════════════════════════════════════════════
# OUTPUT
# ══════════════════════════════════════════════════════════════════

# CSV
fieldnames = ['country', 'region', 'year', 'project', 'status', 'mechanism',
              'value_usd_millions', 'chinese_actors', 'source',
              'pipeline_detected', 'description']

out_csv = OUT_DIR / "bri_cancellations_consolidated.csv"
with open(out_csv, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(cases)

print(f"✓ CSV: {out_csv} ({len(cases)} casos)")

# ── Stats ──
from collections import Counter

print(f"\n{'='*70}")
print(f"DATASET CONSOLIDADO: {len(cases)} casos de fricción BRI")
print(f"{'='*70}")

regions = Counter(c['region'] for c in cases)
print(f"\nPor región:")
for r, n in regions.most_common():
    print(f"  {r:15s}: {n}")

mechanisms = Counter(c['mechanism'] for c in cases)
print(f"\nPor mecanismo:")
for m, n in mechanisms.most_common():
    print(f"  {m:30s}: {n}")

statuses = Counter(c['status'] for c in cases)
print(f"\nPor status:")
for s, n in statuses.most_common():
    print(f"  {s:30s}: {n}")

detected = Counter(c['pipeline_detected'] for c in cases)
print(f"\nDetectado por pipeline GDELT:")
for d, n in detected.most_common():
    print(f"  {d:5s}: {n}")

values = [c['value_usd_millions'] for c in cases if c['value_usd_millions'] > 0]
print(f"\nValor total afectado: ${sum(values):,.0f}M ({len(values)} proyectos con valor conocido)")

# ── Markdown ──
out_md = OUT_DIR / "bri_cancellations_consolidated.md"
with open(out_md, 'w') as f:
    f.write(f"# Dataset Consolidado: Cancelaciones y Fricciones BRI 2011-2024\n\n")
    f.write(f"**Total: {len(cases)} casos** en {len(set(c['country'] for c in cases))} países\n\n")

    f.write("## Resumen\n\n")
    f.write(f"| Métrica | Valor |\n|---------|-------|\n")
    f.write(f"| Total casos | {len(cases)} |\n")
    f.write(f"| Países | {len(set(c['country'] for c in cases))} |\n")
    f.write(f"| Detectados por GDELT pipeline | {detected.get('yes', 0)} ({detected.get('yes', 0)/len(cases)*100:.0f}%) |\n")
    f.write(f"| Agregados de literatura | {detected.get('no', 0)} ({detected.get('no', 0)/len(cases)*100:.0f}%) |\n")
    f.write(f"| Valor total afectado | ${sum(values):,.0f}M |\n")
    f.write(f"| Período | 2011-2024 |\n\n")

    f.write("## Por región\n\n")
    for region in ['LATAM', 'Asia Sur', 'Asia SE', 'Asia Central', 'Africa', 'Europa W', 'Europa E', 'Oceania', 'Medio Oriente', 'Eurasia']:
        region_cases = [c for c in cases if c['region'] == region]
        if not region_cases:
            continue
        f.write(f"\n### {region} ({len(region_cases)} casos)\n\n")
        f.write("| País | Año | Proyecto | Status | Mecanismo | Valor $M |\n")
        f.write("|------|-----|----------|--------|-----------|----------|\n")
        for c in sorted(region_cases, key=lambda x: (x['country'], str(x['year']))):
            val = f"${c['value_usd_millions']:,.0f}" if c['value_usd_millions'] > 0 else '-'
            f.write(f"| {c['country']} | {c['year']} | {c['project']} | {c['status']} | {c['mechanism']} | {val} |\n")

    f.write("\n## Por mecanismo\n\n")
    f.write("| Mecanismo | N casos | Ejemplos |\n")
    f.write("|-----------|---------|----------|\n")
    for mech, n in mechanisms.most_common():
        examples = [c['project'] for c in cases if c['mechanism'] == mech][:3]
        f.write(f"| {mech} | {n} | {', '.join(examples)} |\n")

    f.write("\n## Metodología\n\n")
    f.write("Este dataset combina tres fuentes:\n\n")
    f.write("1. **Pipeline GDELT automatizado** (Scripts 01-21): ~450k eventos procesados → 8,912 URL-filtered → ")
    f.write(f"{detected.get('yes', 0)} casos verificados\n")
    f.write("2. **Verificación manual de URLs**: Web scraping y revisión artículo por artículo\n")
    f.write(f"3. **Literatura académica y periodística**: {detected.get('no', 0)} casos conocidos que el pipeline no capturó\n\n")
    f.write("### Limitaciones\n\n")
    f.write("- GDELT v2 solo cubre desde 2015-02-19 (casos pre-2015 como Myanmar Myitsone 2011 no detectables)\n")
    f.write("- El pipeline sobrepondera sanciones EEUU (mejor cobertura mediática anglófona)\n")
    f.write("- Proyectos en países con poca prensa en inglés (Central Asia, Africa francófona) subrepresentados\n")
    f.write("- Algunos casos conocidos (Tanzania Bagamoyo, Sierra Leone airport) no aparecen en GDELT con las keywords usadas\n")

print(f"✓ Markdown: {out_md}")

if __name__ == "__main__":
    pass
