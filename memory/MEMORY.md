# GDELT Research Memory — Proyectos BRI Cancelados (Tesis Villalobos)

## Objetivo
Detectar proyectos de inversión china cancelados/disrumpidos (BRI) 2017-2024 usando GDELT.
Tesis de Ariel Villalobos (Economía, U. Chile) sobre determinantes de cancelaciones.

## Stack técnico
- Python 3.14 + `gdelt_env/` (activar con `source gdelt_env/bin/activate`)
- BigQuery: proyecto `tomasdata-gdelt-research` (cuenta `salareuniones113@gmail.com`)
- Scripts en `notebooks/`, datos en `data/samples/`
- `python3 notebooks/XX_script.py` (no `python`)

## Archivos de datos clave

| Archivo | Filas | Descripción |
|---------|-------|-------------|
| `data/samples/bri_investment_events_all.csv` | 31,090 | BRI v2 (script 09 mejorado) |
| `data/samples/events_conflict_classified.csv` | 248k | Conflicto clasificado con mecanismo |
| `data/samples/events_economic_classified.csv` | 45k | Económico clasificado con mecanismo |
| `data/samples/geo/bri_events_geo.csv` | 31,090 | BRI con región/país |
| `data/samples/clusters/project_candidates_events_v2.csv` | 309 | Clusters v2 (actor-aware) |
| `data/samples/clusters/project_candidates_latam_v2.csv` | 28 | Candidatos LATAM |
| `data/samples/gkg_por_año/raw/gkg_china_2017_2024.parquet` | 92,990 | GKG artículos SOE chinas |
| `data/samples/companies/soe_risk_profile.csv` | - | Perfil riesgo por SOE |
| `data/samples/validation/cross_validated_candidates.csv` | 309 | Con confidence score |
| `data/samples/validation/high_confidence_candidates.csv` | 1 | Alta confianza geo+SOE |

## Pipeline ejecutado (v2)

```
Script 07 → Script 09 → Script 10 → Script 12 → Script 14 → Script 15 → Script 16
  (GKG)    (clasif.)  (geo/LATAM) (cluster)  (empresa)  (causal)  (validación)
```

Todos ejecutados exitosamente. Ver `docs/ANALYSIS_FINDINGS.md` para hallazgos.

## Resultados globales del pipeline

### Events pipeline
- **31,090 eventos BRI v2** (bajó de 52,439 v1, -41% falsos positivos)
- **309 clusters** proyectos candidatos (bajó de 801 v1)
- **28 candidatos LATAM**
- Mecanismos: us_sanctions=898 (2.9%), environmental=203 (0.7%), political=108 (0.3%)

### GKG pipeline (script 07)
- **92,990 artículos** con SOE china 2017-2024
- SOE_TELECOM domina: 64,808 artículos (Huawei pico 2019: 25,575 artículos = arresto Meng Wanzhou)
- SOE_OIL: 9,142 | SOE_MINING: 5,726 | SOE_RAILWAY: 4,037 | SOE_MARITIME: 2,860

### Validación cruzada (script 16)
- **Recall 88%** (7/8 casos conocidos LATAM recuperados)
- Jamaica CHEC attack 2022 detectado en GKG pero no en Events (gap inter-tabla)
- 1 cluster con high confidence (geo+SOE match en GKG): Irán SOE_TELECOM 2017 (Huawei)

## Señales reales LATAM identificadas

| País | Año | Caso | Mecanismo | GKG artículos |
|------|-----|------|-----------|---------------|
| Chile (CI) | 2018-19 | SQM → Tianqi Lithium (litio) | regulatorio | 460 geo |
| Ecuador (EC) | 2017-19 | Camarón/pesca suspensión China | sanitario | 442 geo |
| Venezuela (VE) | 2018 | Unipec ban tanqueros venezolanos | us_sanctions | 1464 geo |
| Venezuela (VE) | 2018 | ZTE — contrato vigilancia (OFAC) | us_sanctions | 1464 geo |
| Venezuela (VE) | 2019 | CNPC — suspensión operaciones | us_sanctions | 1448 geo |
| Venezuela (VE) | 2020 | Empresa china internet crackdown | us_sanctions | 1209 geo |
| Brasil (BR) | 2017-19 | Tamoios highway (concesión china) | project_failure | 727 geo |
| Jamaica (JM) | 2022 | CHEC complex — ataque mortal | violencia | solo GKG |
| Perú (PE) | 2024 | Puerto — reclamo arbitraje | project_failure | detectado |

## Hallazgos causales clave (script 15)

- **US sanctions**: único mecanismo que crece post-2018 (2.1% → 3.0-4.2%)
  - Pico 2021: 4.2% de eventos BRI tienen mecanismo "us_sanctions"
  - Medio Oriente lidera: 6.2% (vs LATAM 2.2%, África 1.0%)
- **Environmental opposition**: estable 0.5-0.9%, no crece post-ESG 2019
- **Debt renegotiation**: muy baja frecuencia (0.2%), no pico COVID esperado
- **Project failure**: concentrado en "Other" (países fuera de muestra) y Asia Central

## FIPS importantes (GDELT ≠ ISO)
- CH=China, CI=Chile, BL=Bolivia, PM=Panamá, PA=Paraguay, VM=Vietnam
- SN=Senegal (NO Singapore — Singapore removido de Asia_SE)
- GY=Guyana, NS=Suriname, CS=Costa Rica, JM=Jamaica, HA=Haití

## SOE normalization (script 12)
```python
SOE_GROUPS = {
    "RAILWAY":  ["CHINA RAILWAY","CRRC","CR GROUP"],
    "MARITIME": ["COSCO","CHINA OCEAN SHIPPING"],
    "HARBOUR":  ["CHINA HARBOUR","CHINA COMMUNICATIONS","CCCC"],
    "ENERGY":   ["SINOHYDRO","POWERCHINA","THREE GORGES","GEZHOUBA"],
    "OIL":      ["CNPC","PETROCHINA","SINOPEC","CNOOC"],
    "TELECOM":  ["HUAWEI","ZTE","CHINA TELECOM","CHINA MOBILE"],
    "FINANCE":  ["CHINA DEVELOPMENT BANK","EXIM BANK","CDB"],
    "CONSTRUCT":["CHINA STATE CONSTRUCTION","CHINA ROAD AND BRIDGE"],
    "MINING":   ["CHINALCO","CHINA MINMETALS","CITIC"],
}
```

## Limitaciones del pipeline actual

1. **actor_norm en Events**: Actor1/2 son actores del PAÍS HOST, no de China → SOE en Events casi siempre NAN/UNKNOWN
2. **High confidence solo 1 cluster**: La validación SOE cruzada requiere que el cluster de Events tenga `actor_norm=SOE_XXX` → raramente se da porque Actor1 es gobierno/host
3. **95.7% mecanismo "unknown"**: Los clasificadores de mecanismo son conservadores, requieren keywords en URL
4. **Jamaica CHEC**: gap inter-tabla — GKG captura el artículo pero Events no genera evento JM con esa URL

## Script 17 — GKG-LATAM Deep (completado)
- 11,058 artículos GKG con SOE china + país LATAM + tono < -2
- 791 clusters (país × SOE × año), 452 con ≥3 artículos, señales fuertes ≥5 artículos
- **Perú × SOE_MARITIME 2023**: 49 artículos, tono min -17.18 → posible caso Chancay COSCO
- **Venezuela × SOE_OIL 2019**: 230 artículos, Yahoo Finance confirma "PetroChina pull Venezuela amid US sanctions"
- **Chile × SOE_MINING 2019**: 99 artículos → caso Tianqi/SQM litio

## Script 18 — Dataset final curado (completado)
- 269 señales LATAM curadas: 44 Events + 225 GKG
- Archivo principal: `data/samples/final/latam_bri_signals_final.csv`
- Narrativa tesis: `data/samples/final/latam_bri_signals_final.md`
- Top señal: Perú × SOE_MARITIME 2023 (tono -7.22, 49 artículos) → COSCO Chancay
- Venezuela domina en us_sanctions (33 señales), Brasil en volumen (41 señales)

## Próximos posibles pasos
- Investigar Perú × COSCO 2023 (Chancay megaport — ¿oposición, accidente o arbitraje?)
- Comparación con base datos manual (18 casos Villalobos) cuando esté disponible
- Pipeline histórico 2015-2016 (datos ya descargados, pendiente ejecutar scripts 08-12 sobre ellos)
- Ampliar narrativa de casos Venezuela (ZTE + Unipec + CNPC + empresa internet) para la tesis
