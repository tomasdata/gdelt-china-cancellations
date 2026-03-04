"""
Script 21: Global BRI Signals Analysis
=======================================
Expande el análisis más allá de LATAM para identificar señales de
cancelación/fricción de proyectos BRI a nivel global.

Input: data/samples/clusters/events_url_filtered.csv (8,912 eventos)
Output: data/samples/final/global_bri_verified_signals.csv
        data/samples/final/global_bri_verified_signals.md
"""

import csv
import re
from collections import defaultdict
from pathlib import Path

# ── Paths ──
BASE = Path(__file__).resolve().parent.parent
EVENTS_FILE = BASE / "data/samples/clusters/events_url_filtered.csv"
OUT_DIR = BASE / "data/samples/final"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Skip codes (LATAM already analyzed + noise countries) ──
LATAM_CODES = {
    'MX','BR','VE','CO','EC','CU','AR','PE','CI','BL','PM','GT',
    'NU','PA','UY','HO','ES','HA','JM','GY','CS','DR','NS','BH'
}
SKIP_CODES = LATAM_CODES | {'CH', 'US', 'HK', 'TW'}

# ── Known BRI project names ──
PROJECT_NAMES = {
    # Asia Central / Sur
    'cpec': 'CPEC (Pakistan)',
    'gwadar': 'Gwadar Port (Pakistan)',
    'diamer-bhasha': 'Diamer-Bhasha Dam (Pakistan)',
    'port-qasim': 'Port Qasim (Pakistan)',
    'sahiwal': 'Sahiwal Coal Plant (Pakistan)',
    'karot': 'Karot Hydropower (Pakistan)',
    'thar-coal': 'Thar Coal (Pakistan)',
    'hambantota': 'Hambantota Port (Sri Lanka)',
    'colombo-port': 'Colombo Port City (Sri Lanka)',
    'myitsone': 'Myitsone Dam (Myanmar)',
    'budhi-gandaki': 'Budhi Gandaki Dam (Nepal)',
    'pokhara': 'Pokhara Airport (Nepal)',
    'payra': 'Payra Power Plant (Bangladesh)',
    # Southeast Asia
    'east-coast-rail': 'ECRL (Malaysia)',
    'ecrl': 'ECRL (Malaysia)',
    'jakarta-bandung': 'Jakarta-Bandung HSR (Indonesia)',
    'kereta-cepat': 'HSR (Indonesia)',
    # Africa
    'mombasa': 'Mombasa-Nairobi SGR (Kenya)',
    'bagamoyo': 'Bagamoyo Port (Tanzania)',
    'lamu-coal': 'Lamu Coal Plant (Kenya)',
    # Europe
    'cernavoda': 'Cernavoda Nuclear (Romania)',
    'belene': 'Belene Nuclear (Bulgaria)',
    'tuzla': 'Tuzla Coal Plant (Bosnia)',
    'bar-boljare': 'Bar-Boljare Highway (Montenegro)',
    'peljesac': 'Peljesac Bridge (Croatia)',
    # Middle East
    'haifa': 'Haifa Port (Israel)',
}

# ── BRI-specific URL terms ──
BRI_TERMS = [
    'belt-and-road', 'belt-road', 'bri-project', 'bri-initiative',
    'debt-trap', 'chinese-loan', 'chinese-debt', 'china-loan',
    'chinese-investment', 'china-investment',
]

# ── Friction indicators ──
FRICTION_TERMS = [
    'cancel', 'suspend', 'halt', 'block', 'reject', 'scrap', 'abandon',
    'withdraw', 'pull-out', 'pullout', 'pull-back', 'revoke', 'terminate',
    'shelve', 'derail', 'axe', 'nix', 'dump', 'stall',
    'oppose', 'protest', 'backlash', 'controversy',
    'renegotiat', 'default', 'collapse', 'fail',
    'concern', 'security-risk', 'review', 'scrutin',
    'arbitrat', 'dispute', 'lawsuit',
    'attack', 'bomb', 'kill', 'militant', 'terrorist',
]

# ── Project type indicators ──
PROJECT_TYPES = [
    'dam', 'port', 'railway', 'railroad', 'highway', 'road-project',
    'bridge', 'airport', 'power-plant', 'nuclear', 'coal',
    'pipeline', 'mine', 'mining', 'refinery', 'steel',
    'factory', 'huawei', '5g', 'zte', 'telecom',
    'cosco', 'concession', 'acquisition', 'takeover',
    'infrastructure', 'hydro', 'wind-farm', 'solar',
    'fiber-optic', 'submarine-cable',
]

# ── Country name map ──
COUNTRY_NAMES = {
    'PK': 'Pakistán', 'IN': 'India', 'CE': 'Sri Lanka', 'BM': 'Myanmar',
    'BG': 'Bangladesh', 'NP': 'Nepal', 'AF': 'Afganistán',
    'MY': 'Malasia', 'ID': 'Indonesia', 'TH': 'Tailandia', 'KH': 'Camboya',
    'VM': 'Vietnam', 'RP': 'Filipinas', 'LA': 'Laos',
    'KE': 'Kenia', 'TZ': 'Tanzania', 'NI': 'Nigeria', 'ZA': 'Sudáfrica',
    'ZM': 'Zambia', 'GH': 'Ghana', 'ET': 'Etiopía', 'DJ': 'Djibouti',
    'MZ': 'Mozambique', 'UG': 'Uganda', 'ZI': 'Zimbabwe', 'SL': 'Sierra Leona',
    'AS': 'Australia', 'NZ': 'Nueva Zelanda',
    'UK': 'R.Unido', 'GM': 'Alemania', 'FR': 'Francia', 'IT': 'Italia',
    'SP': 'España', 'SW': 'Suecia', 'NO': 'Noruega', 'PO': 'Polonia',
    'RO': 'Rumania', 'BU': 'Bulgaria', 'BA': 'Bosnia', 'HR': 'Croacia',
    'MK': 'Macedonia', 'SR': 'Serbia', 'MJ': 'Montenegro',
    'UA': 'Ucrania', 'BO': 'Bielorrusia', 'HU': 'Hungría',
    'IR': 'Irán', 'IS': 'Israel', 'SA': 'Arabia Saudí', 'AE': 'EAU',
    'RS': 'Rusia', 'JA': 'Japón', 'KS': 'Corea del Sur', 'CA': 'Canadá',
    'MD': 'Mongolia',
}

# ── Region map ──
REGION_MAP = {
    'PK': 'Asia_Sur', 'IN': 'Asia_Sur', 'CE': 'Asia_Sur', 'BM': 'Asia_Sur',
    'BG': 'Asia_Sur', 'NP': 'Asia_Sur', 'AF': 'Asia_Sur',
    'MY': 'Asia_SE', 'ID': 'Asia_SE', 'TH': 'Asia_SE', 'KH': 'Asia_SE',
    'VM': 'Asia_SE', 'RP': 'Asia_SE', 'LA': 'Asia_SE',
    'KE': 'Africa', 'TZ': 'Africa', 'NI': 'Africa', 'ZA': 'Africa',
    'ZM': 'Africa', 'GH': 'Africa', 'ET': 'Africa', 'DJ': 'Africa',
    'MZ': 'Africa', 'UG': 'Africa', 'ZI': 'Africa', 'SL': 'Africa',
    'AS': 'Oceania', 'NZ': 'Oceania',
    'UK': 'Europa_W', 'GM': 'Europa_W', 'FR': 'Europa_W', 'IT': 'Europa_W',
    'SP': 'Europa_W', 'SW': 'Europa_W', 'NO': 'Europa_W',
    'RO': 'Europa_E', 'BU': 'Europa_E', 'BA': 'Europa_E', 'HR': 'Europa_E',
    'MK': 'Europa_E', 'SR': 'Europa_E', 'MJ': 'Europa_E',
    'UA': 'Europa_E', 'BO': 'Europa_E', 'HU': 'Europa_E', 'PO': 'Europa_E',
    'IR': 'MedioOriente', 'IS': 'MedioOriente', 'SA': 'MedioOriente', 'AE': 'MedioOriente',
    'RS': 'Eurasia', 'JA': 'Asia_E', 'KS': 'Asia_E', 'CA': 'NorteAmerica',
    'MD': 'Asia_C',
}


def classify_signal(url_lower, country_code):
    """Classify a URL into signal categories and assign a quality score."""

    # 1. Check for known project names
    project_match = None
    for name, desc in PROJECT_NAMES.items():
        if name in url_lower:
            project_match = desc
            break

    # 2. Check for BRI-specific terms
    bri_hits = [t for t in BRI_TERMS if t in url_lower]

    # 3. Check for friction indicators
    friction_hits = [t for t in FRICTION_TERMS if t in url_lower]

    # 4. Check for project type
    project_hits = [t for t in PROJECT_TYPES if t in url_lower]

    # ── Scoring ──
    score = 0
    category = 'unknown'

    # Known project name = high value
    if project_match:
        score += 4
        category = 'named_project'

    # BRI-specific term
    if bri_hits:
        score += 3
        category = 'bri_explicit' if not project_match else category

    # Friction + project type combo
    if friction_hits and project_hits:
        score += 2
        if category == 'unknown':
            category = 'project_friction'
    elif friction_hits:
        score += 1
    elif project_hits:
        score += 0.5

    # Bonus for specific cancellation verbs (not generic "ban" or "kill")
    strong_friction = ['cancel', 'suspend', 'halt', 'scrap', 'abandon', 'withdraw',
                       'shelve', 'derail', 'renegotiat', 'arbitrat', 'pullout', 'pull-out']
    if any(sf in url_lower for sf in strong_friction):
        score += 1

    return {
        'score': score,
        'category': category,
        'project_match': project_match or '',
        'bri_terms': ', '.join(bri_hits),
        'friction_terms': ', '.join(friction_hits[:3]),
        'project_terms': ', '.join(project_hits[:3]),
    }


def main():
    # ── Load events ──
    with open(EVENTS_FILE) as f:
        events = list(csv.DictReader(f))
    print(f"Total eventos URL-filtered: {len(events)}")

    # ── Filter non-LATAM ──
    global_events = [e for e in events if e['ActionGeo_CountryCode'] not in SKIP_CODES]
    print(f"Eventos globales (excl. LATAM/CH/US): {len(global_events)}")

    # ── Classify each event ──
    scored_events = []
    for e in global_events:
        url = e.get('SOURCEURL', '')
        url_lower = url.lower().replace(' ', '-')
        cc = e['ActionGeo_CountryCode']

        classification = classify_signal(url_lower, cc)

        if classification['score'] >= 2:  # Minimum threshold
            scored_events.append({
                'url': url,
                'country_code': cc,
                'country_name': COUNTRY_NAMES.get(cc, e.get('pais', cc)),
                'region': REGION_MAP.get(cc, 'Other'),
                'year': e['year'],
                'tone': float(e['AvgTone']),
                'actor1': e.get('Actor1Name', ''),
                'actor2': e.get('Actor2Name', ''),
                'geo': e.get('ActionGeo_FullName', ''),
                'mentions': int(e.get('NumMentions', 0)),
                **classification,
            })

    # ── Deduplicate by URL ──
    seen_urls = set()
    unique = []
    for s in scored_events:
        if s['url'] not in seen_urls:
            seen_urls.add(s['url'])
            unique.append(s)

    unique.sort(key=lambda x: (-x['score'], x['tone']))

    print(f"\nSeñales con score >= 2: {len(unique)} URLs únicas")

    # ── Stats by category ──
    from collections import Counter
    cats = Counter(s['category'] for s in unique)
    print(f"\nPor categoría:")
    for cat, n in cats.most_common():
        print(f"  {cat:20s}: {n}")

    # ── Stats by region ──
    regions = Counter(s['region'] for s in unique)
    print(f"\nPor región:")
    for reg, n in regions.most_common():
        print(f"  {reg:20s}: {n}")

    # ── Group by country and aggregate ──
    by_country = defaultdict(list)
    for s in unique:
        by_country[s['country_name']].append(s)

    # ── Build country-level summary ──
    country_summaries = []
    for country, signals in sorted(by_country.items(), key=lambda x: -len(x[1])):
        best = max(signals, key=lambda x: x['score'])
        named = [s for s in signals if s['project_match']]
        bri_explicit = [s for s in signals if s['bri_terms']]
        country_summaries.append({
            'country': country,
            'region': signals[0]['region'],
            'n_signals': len(signals),
            'max_score': best['score'],
            'avg_tone': sum(s['tone'] for s in signals) / len(signals),
            'years': sorted(set(s['year'] for s in signals)),
            'named_projects': list(set(s['project_match'] for s in named if s['project_match'])),
            'top_url': best['url'],
            'has_bri_explicit': len(bri_explicit) > 0,
        })

    # ── Print top countries ──
    print(f"\n{'='*80}")
    print(f"TOP PAÍSES CON SEÑALES BRI (por cantidad de señales)")
    print(f"{'='*80}")

    for cs in sorted(country_summaries, key=lambda x: (-x['max_score'], -x['n_signals']))[:30]:
        projects_str = ', '.join(cs['named_projects'][:3]) if cs['named_projects'] else '-'
        years_str = f"{cs['years'][0]}-{cs['years'][-1]}" if len(cs['years']) > 1 else cs['years'][0]
        print(f"\n  {cs['country']:20s} | {cs['region']:12s} | {cs['n_signals']:3d} señales | "
              f"score_max={cs['max_score']:.0f} | tone={cs['avg_tone']:.1f} | {years_str}")
        if cs['named_projects']:
            print(f"    Proyectos: {projects_str}")
        if cs['has_bri_explicit']:
            print(f"    [BRI explícito en URLs]")

    # ── Write CSV ──
    out_csv = OUT_DIR / "global_bri_verified_signals.csv"
    fieldnames = ['country_name', 'country_code', 'region', 'year', 'score', 'category',
                  'project_match', 'bri_terms', 'friction_terms', 'project_terms',
                  'tone', 'mentions', 'actor1', 'actor2', 'geo', 'url']

    with open(out_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(unique)

    print(f"\n✓ CSV guardado: {out_csv} ({len(unique)} señales)")

    # ── Write narrative MD ──
    out_md = OUT_DIR / "global_bri_verified_signals.md"

    # Separate into tiers
    tier1 = [s for s in unique if s['score'] >= 5]  # Named project + friction
    tier2 = [s for s in unique if 3 <= s['score'] < 5]  # BRI explicit or strong signal
    tier3 = [s for s in unique if 2 <= s['score'] < 3]  # Moderate signal

    with open(out_md, 'w') as f:
        f.write("# Señales Globales BRI — Proyectos con Fricción/Cancelación\n")
        f.write(f"## Script 21: Análisis global de {len(unique)} señales\n\n")

        f.write("## Resumen\n\n")
        f.write(f"| Métrica | Valor |\n|---------|-------|\n")
        f.write(f"| Eventos URL-filtered analizados | {len(global_events)} |\n")
        f.write(f"| Señales con score ≥ 2 | {len(unique)} |\n")
        f.write(f"| Tier 1 (score ≥ 5) | {len(tier1)} |\n")
        f.write(f"| Tier 2 (score 3-4.9) | {len(tier2)} |\n")
        f.write(f"| Tier 3 (score 2-2.9) | {len(tier3)} |\n")
        f.write(f"| Países representados | {len(by_country)} |\n")
        f.write(f"| Regiones | {len(regions)} |\n\n")

        f.write("## Tier 1 — Señales de alta confianza (score ≥ 5)\n\n")
        f.write("Estas señales tienen nombre de proyecto conocido + fricción explícita, o BRI explícito + múltiples indicadores.\n\n")

        for s in tier1:
            f.write(f"### {s['country_name']} ({s['year']}) — score {s['score']:.0f}\n")
            if s['project_match']:
                f.write(f"- **Proyecto**: {s['project_match']}\n")
            if s['bri_terms']:
                f.write(f"- **BRI terms**: {s['bri_terms']}\n")
            if s['friction_terms']:
                f.write(f"- **Fricción**: {s['friction_terms']}\n")
            f.write(f"- **Tono**: {s['tone']:.1f}\n")
            f.write(f"- **URL**: [{s['url'][:80]}...]({s['url']})\n\n")

        f.write("\n## Tier 2 — Señales de confianza media (score 3-4.9)\n\n")

        # Group tier2 by country
        tier2_by_country = defaultdict(list)
        for s in tier2:
            tier2_by_country[s['country_name']].append(s)

        for country in sorted(tier2_by_country, key=lambda c: -len(tier2_by_country[c])):
            signals = tier2_by_country[country]
            f.write(f"### {country} ({len(signals)} señales)\n")
            for s in sorted(signals, key=lambda x: -x['score'])[:5]:
                proj = f" — {s['project_match']}" if s['project_match'] else ""
                f.write(f"- [{s['year']}] score={s['score']:.0f} | tone={s['tone']:.1f}{proj} | "
                        f"[link]({s['url']})\n")
            if len(signals) > 5:
                f.write(f"- ... y {len(signals)-5} más\n")
            f.write("\n")

        # Summary by region
        f.write("\n## Distribución por región\n\n")
        f.write("| Región | Señales | Tier 1 | Tier 2 | Tier 3 |\n")
        f.write("|--------|---------|--------|--------|--------|\n")
        for reg in sorted(regions, key=lambda r: -regions[r]):
            reg_signals = [s for s in unique if s['region'] == reg]
            t1 = len([s for s in reg_signals if s['score'] >= 5])
            t2 = len([s for s in reg_signals if 3 <= s['score'] < 5])
            t3 = len([s for s in reg_signals if 2 <= s['score'] < 3])
            f.write(f"| {reg} | {len(reg_signals)} | {t1} | {t2} | {t3} |\n")

        # Named projects summary
        f.write("\n## Proyectos BRI nombrados detectados\n\n")
        named_all = [s for s in unique if s['project_match']]
        by_project = defaultdict(list)
        for s in named_all:
            by_project[s['project_match']].append(s)

        f.write("| Proyecto | Señales | Años | Tono medio | Score max |\n")
        f.write("|----------|---------|------|-----------|----------|\n")
        for proj in sorted(by_project, key=lambda p: -len(by_project[p])):
            sigs = by_project[proj]
            years = sorted(set(s['year'] for s in sigs))
            avg_tone = sum(s['tone'] for s in sigs) / len(sigs)
            max_score = max(s['score'] for s in sigs)
            f.write(f"| {proj} | {len(sigs)} | {years[0]}-{years[-1]} | {avg_tone:.1f} | {max_score:.0f} |\n")

    print(f"✓ Markdown guardado: {out_md}")

    # ── Final summary ──
    print(f"\n{'='*80}")
    print(f"RESUMEN FINAL")
    print(f"{'='*80}")
    print(f"Total señales globales: {len(unique)}")
    print(f"  Tier 1 (alta confianza): {len(tier1)}")
    print(f"  Tier 2 (media):          {len(tier2)}")
    print(f"  Tier 3 (baja):           {len(tier3)}")
    print(f"Proyectos BRI nombrados:   {len(set(s['project_match'] for s in unique if s['project_match']))}")
    print(f"Países:                    {len(by_country)}")


if __name__ == "__main__":
    main()
