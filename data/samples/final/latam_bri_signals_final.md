# Señales BRI LATAM — Dataset Final Curado (GDELT 2017-2024)

## Metodología
- Fuente Events: eventos con actor CHN + mecanismo identificado (no-unknown) + URL relevante
- Fuente GKG: clusters de artículos (SOE sectorial × país × año) con ≥5 artículos, excluyendo SOE_TELECOM (noise Huawei)
- Relevancia = |tono| × log(n_artículos) × url_score

## Resumen por país

| País | N señales | Tono mín | Mecanismos |
|------|-----------|----------|------------|
| Brasil | 41 | -8.67 | confirmed_presence,environmental_opposition,political_rejection,us_sanctions |
| México | 37 | -8.87 | confirmed_presence,debt_renegotiation,environmental_opposition,political_rejection,us_sanctions |
| Venezuela | 33 | -10.81 | confirmed_presence,debt_renegotiation,political_rejection,us_sanctions |
| Chile | 28 | -9.14 | confirmed_presence,environmental_opposition,project_failure |
| Argentina | 25 | -9.49 | confirmed_presence,environmental_opposition,project_failure |
| Perú | 24 | -10.00 | confirmed_presence,project_failure |
| Cuba | 16 | -10.08 | confirmed_presence,political_rejection,us_sanctions |
| Ecuador | 14 | -9.74 | confirmed_presence |
| Panamá | 10 | -9.36 | confirmed_presence,political_rejection,us_sanctions |
| Jamaica | 8 | -5.83 | confirmed_presence,us_sanctions |
| Bolivia | 6 | -10.47 | confirmed_presence |
| Colombia | 6 | -6.11 | confirmed_presence,political_rejection |
| Haití | 4 | -10.47 | confirmed_presence,environmental_opposition,us_sanctions |
| Honduras | 4 | -10.47 | confirmed_presence |
| Guyana | 4 | -3.95 | confirmed_presence |
| Costa Rica | 3 | -10.47 | confirmed_presence |
| Uruguay | 3 | -4.07 | confirmed_presence |
| Guatemala | 2 | -10.47 | confirmed_presence |
| Nicaragua | 1 | -10.47 | confirmed_presence |

## Señales individuales (top 30 por relevancia)

| País | Año | Mecanismo | SOE | Tono | Fuente | URL |
|------|-----|-----------|-----|------|--------|-----|
| Guatemala | 2021 | confirmed_presence | SOE_OIL | -10.47 | GKG | [http://www.hinews.cn/news/system/2021/04/09/032536464.shtml...](http://www.hinews.cn/news/system/2021/04/09/032536464.shtml) |
| Bolivia | 2021 | confirmed_presence | SOE_OIL | -10.47 | GKG | [http://www.hinews.cn/news/system/2021/04/09/032536464.shtml...](http://www.hinews.cn/news/system/2021/04/09/032536464.shtml) |
| Haití | 2021 | confirmed_presence | SOE_OIL | -10.47 | GKG | [http://www.hinews.cn/news/system/2021/04/09/032536464.shtml...](http://www.hinews.cn/news/system/2021/04/09/032536464.shtml) |
| Honduras | 2021 | confirmed_presence | SOE_OIL | -10.47 | GKG | [http://www.hinews.cn/news/system/2021/04/09/032536464.shtml...](http://www.hinews.cn/news/system/2021/04/09/032536464.shtml) |
| Costa Rica | 2021 | confirmed_presence | SOE_OIL | -10.47 | GKG | [http://www.hinews.cn/news/system/2021/04/09/032536464.shtml...](http://www.hinews.cn/news/system/2021/04/09/032536464.shtml) |
| Nicaragua | 2021 | confirmed_presence | SOE_OIL | -10.47 | GKG | [http://www.hinews.cn/news/system/2021/04/09/032536464.shtml...](http://www.hinews.cn/news/system/2021/04/09/032536464.shtml) |
| Cuba | 2021 | confirmed_presence | SOE_OIL | -10.08 | GKG | [http://www.hinews.cn/news/system/2021/04/09/032536464.shtml...](http://www.hinews.cn/news/system/2021/04/09/032536464.shtml) |
| Ecuador | 2021 | confirmed_presence | SOE_OIL | -9.74 | GKG | [http://www.hinews.cn/news/system/2021/04/09/032536464.shtml...](http://www.hinews.cn/news/system/2021/04/09/032536464.shtml) |
| Argentina | 2021 | confirmed_presence | SOE_OIL | -9.49 | GKG | [http://www.hinews.cn/news/system/2021/04/09/032536464.shtml...](http://www.hinews.cn/news/system/2021/04/09/032536464.shtml) |
| Panamá | 2021 | confirmed_presence | SOE_OIL | -9.36 | GKG | [http://www.hinews.cn/news/system/2021/04/09/032536464.shtml...](http://www.hinews.cn/news/system/2021/04/09/032536464.shtml) |
| Venezuela | 2021 | confirmed_presence | SOE_OIL | -9.15 | GKG | [http://www.hinews.cn/news/system/2021/04/09/032536464.shtml...](http://www.hinews.cn/news/system/2021/04/09/032536464.shtml) |
| Chile | 2021 | confirmed_presence | SOE_OIL | -8.67 | GKG | [http://www.hinews.cn/news/system/2021/04/09/032536464.shtml...](http://www.hinews.cn/news/system/2021/04/09/032536464.shtml) |
| Brasil | 2021 | confirmed_presence | SOE_OIL | -8.67 | GKG | [http://www.hinews.cn/news/system/2021/04/09/032536464.shtml...](http://www.hinews.cn/news/system/2021/04/09/032536464.shtml) |
| Perú | 2023 | confirmed_presence | SOE_MARITIME | -7.22 | GKG | [https://www.albawabhnews.com/4737953...](https://www.albawabhnews.com/4737953) |
| Chile | 2022 | confirmed_presence | SOE_RAILWAY | -9.14 | GKG | [http://sc.sina.com.cn/news/b/2022-01-31/detail-ikyakumy35292...](http://sc.sina.com.cn/news/b/2022-01-31/detail-ikyakumy3529227.shtml) |
| Venezuela | 2018 | confirmed_presence | SOE_OIL | -4.27 | GKG | [http://news.cnfol.com/chanyejingji/20180810/26744959.shtml...](http://news.cnfol.com/chanyejingji/20180810/26744959.shtml) |
| Venezuela | 2019 | confirmed_presence | SOE_OIL | -4.04 | GKG | [https://finance.yahoo.com/news/petrochina-pull-venezuela-ami...](https://finance.yahoo.com/news/petrochina-pull-venezuela-amid-us-125012728.html) |
| Ecuador | 2021 | confirmed_presence | SOE_FINANCE | -4.03 | GKG | [https://www.westport-news.com/news/article/Great-Wall-of-Lig...](https://www.westport-news.com/news/article/Great-Wall-of-Lights-China-s-sea-power-on-16483687.php) |
| Perú | 2024 | project_failure | unknown | -10.00 | Events | [https://globalarbitrationreview.com/article/peru-risks-claim...](https://globalarbitrationreview.com/article/peru-risks-claim-over-port-project) |
| Venezuela | 2019 | confirmed_presence | SOE_MARITIME | -4.71 | GKG | [http://newsabah.com/newspaper/196066...](http://newsabah.com/newspaper/196066) |
| Chile | 2019 | confirmed_presence | SOE_MINING | -4.40 | GKG | [http://hk.eastmoney.com/a/201901231032796874.html...](http://hk.eastmoney.com/a/201901231032796874.html) |
| Brasil | 2017 | confirmed_presence | SOE_OIL | -4.24 | GKG | [http://world.qianlong.com/2017/1127/2203949.shtml...](http://world.qianlong.com/2017/1127/2203949.shtml) |
| México | 2017 | confirmed_presence | SOE_OIL | -4.46 | GKG | [http://china.qianlong.com/2017/0606/1744069.shtml...](http://china.qianlong.com/2017/0606/1744069.shtml) |
| Brasil | 2020 | confirmed_presence | SOE_RAILWAY | -5.39 | GKG | [http://origin-businesstoday.intoday.in/current/economy-polit...](http://origin-businesstoday.intoday.in/current/economy-politics/notorious-chinese-hackers-attack-indian-entities-defence-ministry-jio-airtel-cipla-lt-top-targets/story/407737.html) |
| Argentina | 2021 | confirmed_presence | SOE_FINANCE | -4.30 | GKG | [https://www.westport-news.com/news/article/Great-Wall-of-Lig...](https://www.westport-news.com/news/article/Great-Wall-of-Lights-China-s-sea-power-on-16483687.php) |
| México | 2021 | confirmed_presence | SOE_FINANCE | -4.25 | GKG | [https://www.westport-news.com/news/article/Great-Wall-of-Lig...](https://www.westport-news.com/news/article/Great-Wall-of-Lights-China-s-sea-power-on-16483687.php) |
| Perú | 2021 | confirmed_presence | SOE_FINANCE | -4.20 | GKG | [https://www.washingtonpost.com/business/great-wall-of-lights...](https://www.washingtonpost.com/business/great-wall-of-lights-chinas-sea-power-on-darwins-doorstep/2021/09/24/aaeab9f0-1cec-11ec-bea8-308ea134594f_story.html) |
| Chile | 2021 | confirmed_presence | SOE_FINANCE | -4.29 | GKG | [https://www.washingtonpost.com/business/great-wall-of-lights...](https://www.washingtonpost.com/business/great-wall-of-lights-chinas-sea-power-on-darwins-doorstep/2021/09/24/aaeab9f0-1cec-11ec-bea8-308ea134594f_story.html) |
| Venezuela | 2017 | confirmed_presence | SOE_MINING | -4.81 | GKG | [http://dailytimes.com.pk/business/23-Jul-17/us-weighs-financ...](http://dailytimes.com.pk/business/23-Jul-17/us-weighs-financial-sanctions-to-hit-venezuelas-oil-revenue-sources) |
| Brasil | 2019 | confirmed_presence | SOE_MARITIME | -4.48 | GKG | [http://www.sohu.com/a/342100104_260616...](http://www.sohu.com/a/342100104_260616) |

## Casos conocidos validados

- **Venezuela CNPC/Unipec/ZTE — sanciones secundarias EEUU**: ✓ ENCONTRADO (6 señales)
- **Chile — restricción flota pesca china**: ✓ ENCONTRADO (2 señales)
- **Perú — reclamo arbitraje puerto COSCO Chancay**: ✓ ENCONTRADO (1 señales)
- **Argentina — demora acuerdo cerdo China por protestas ambientales**: ✓ ENCONTRADO (1 señales)
- **Venezuela — reestructuración deuda China/Rusia**: ✓ ENCONTRADO (1 señales)
- **Brasil — JBS escándalo carne afecta exportaciones China**: ✓ ENCONTRADO (1 señales)
